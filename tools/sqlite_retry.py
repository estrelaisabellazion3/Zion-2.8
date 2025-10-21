"""
SQLite Retry Wrapper for ZION Pool
Provides exponential backoff for database operations to handle "database is locked" errors.
"""

import sqlite3
import time
import random
import functools
import logging
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


def with_db_retry(
    max_retries: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 2.0,
    jitter: bool = True
):
    """
    Decorator to retry SQLite operations with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds (doubles each retry)
        max_delay: Maximum delay cap in seconds
        jitter: Add random jitter to prevent thundering herd
    
    Usage:
        @with_db_retry(max_retries=3)
        def my_db_operation(conn):
            conn.execute("INSERT ...")
            conn.commit()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e).lower():
                        last_exception = e
                        
                        if attempt < max_retries - 1:
                            # Calculate delay with exponential backoff
                            delay = min(base_delay * (2 ** attempt), max_delay)
                            
                            # Add jitter to prevent synchronized retries
                            if jitter:
                                delay = delay * (0.5 + random.random())
                            
                            logger.warning(
                                f"💾 Database locked, retry {attempt + 1}/{max_retries} "
                                f"after {delay:.3f}s: {func.__name__}"
                            )
                            time.sleep(delay)
                        else:
                            logger.error(
                                f"❌ Database locked after {max_retries} attempts: "
                                f"{func.__name__}"
                            )
                    else:
                        # Not a lock error, re-raise immediately
                        raise
                        
                except Exception as e:
                    # Non-SQLite errors, re-raise immediately
                    raise
            
            # All retries exhausted
            raise last_exception
        
        return wrapper
    return decorator


class RetryConnection:
    """
    SQLite connection wrapper that applies retry logic to all operations.
    
    Usage:
        conn = RetryConnection("pool.db", max_retries=5)
        cursor = conn.execute("SELECT * FROM shares")
        conn.commit()
        conn.close()
    """
    
    def __init__(
        self,
        database: str,
        max_retries: int = 5,
        base_delay: float = 0.05,
        max_delay: float = 2.0,
        timeout: float = 30.0,
        **kwargs
    ):
        self.database = database
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.kwargs = kwargs
        self.kwargs['timeout'] = timeout
        self._conn: Optional[sqlite3.Connection] = None
        self._connect()
    
    def _connect(self):
        """Establish connection with retry logic."""
        @with_db_retry(self.max_retries, self.base_delay, self.max_delay)
        def _do_connect():
            self._conn = sqlite3.connect(self.database, **self.kwargs)
            # Enable WAL mode for better concurrency
            self._conn.execute("PRAGMA journal_mode=WAL")
            return self._conn
        
        return _do_connect()
    
    def execute(self, sql: str, parameters=None):
        """Execute SQL with retry logic."""
        @with_db_retry(self.max_retries, self.base_delay, self.max_delay)
        def _do_execute():
            if parameters:
                return self._conn.execute(sql, parameters)
            return self._conn.execute(sql)
        
        return _do_execute()
    
    def executemany(self, sql: str, parameters):
        """Execute many with retry logic."""
        @with_db_retry(self.max_retries, self.base_delay, self.max_delay)
        def _do_executemany():
            return self._conn.executemany(sql, parameters)
        
        return _do_executemany()
    
    def commit(self):
        """Commit with retry logic."""
        @with_db_retry(self.max_retries, self.base_delay, self.max_delay)
        def _do_commit():
            self._conn.commit()
        
        _do_commit()
    
    def rollback(self):
        """Rollback (no retry needed)."""
        self._conn.rollback()
    
    def close(self):
        """Close connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()
        return False


# Example usage functions for common pool operations

@with_db_retry(max_retries=5)
def save_share_with_retry(conn, wallet, nonce, result, valid, timestamp):
    """Save a mining share with automatic retry."""
    conn.execute(
        """
        INSERT INTO shares (wallet, nonce, result, valid, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (wallet, nonce, result, valid, timestamp)
    )
    conn.commit()


@with_db_retry(max_retries=3)
def update_miner_stats_with_retry(conn, wallet, hashrate, shares_accepted, shares_rejected):
    """Update miner statistics with automatic retry."""
    conn.execute(
        """
        INSERT OR REPLACE INTO miner_stats 
        (wallet, hashrate, shares_accepted, shares_rejected, last_seen)
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (wallet, hashrate, shares_accepted, shares_rejected)
    )
    conn.commit()


@with_db_retry(max_retries=3)
def award_consciousness_xp_with_retry(conn, wallet, xp_gained, new_level):
    """Award consciousness XP with automatic retry."""
    conn.execute(
        """
        UPDATE consciousness_miners
        SET xp = xp + ?,
            level = ?,
            last_activity = datetime('now')
        WHERE wallet = ?
        """,
        (xp_gained, new_level, wallet)
    )
    conn.commit()


if __name__ == "__main__":
    # Test the retry mechanism
    logging.basicConfig(level=logging.INFO)
    
    # Example 1: Using decorator
    @with_db_retry(max_retries=3, base_delay=0.1)
    def test_insert():
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute("INSERT INTO test (value) VALUES (?)", ("test",))
        conn.commit()
        conn.close()
        print("✅ Decorator test passed")
    
    test_insert()
    
    # Example 2: Using wrapper class
    with RetryConnection(":memory:", max_retries=3) as conn:
        conn.execute("CREATE TABLE test2 (id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute("INSERT INTO test2 (value) VALUES (?)", ("test2",))
        print("✅ Wrapper class test passed")
    
    print("\n🎉 All tests passed! SQLite retry wrapper is ready.")
