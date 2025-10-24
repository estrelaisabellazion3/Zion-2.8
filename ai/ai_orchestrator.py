#!/usr/bin/env python3
"""
ZION AI Orchestrator
Master Coordinator for AI-Powered ZION Nebula Mining

This module orchestrates all AI components:
- Consciousness Mining AI
- AI Pool Orchestrator
- AI Warp Engine
- Real-time optimization coordination
- Multi-agent decision making
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import redis
import json
import signal
import sys

# Import AI components
from consciousness_mining_ai import ConsciousnessMiningAI
from ai_pool_orchestrator import AIPoolOrchestrator
from ai_warp_engine import AIWarpEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIAgent:
    """Base class for AI agents"""

    def __init__(self, name: str, redis_client: redis.Redis):
        self.name = name
        self.redis_client = redis_client
        self.is_running = False
        self.last_update = datetime.now()

    async def start(self):
        """Start the AI agent"""
        self.is_running = True
        logger.info(f"Starting AI agent: {self.name}")

    async def stop(self):
        """Stop the AI agent"""
        self.is_running = False
        logger.info(f"Stopping AI agent: {self.name}")

    async def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'name': self.name,
            'running': self.is_running,
            'last_update': self.last_update.isoformat(),
            'health': 'healthy' if self.is_running else 'stopped'
        }

class ConsciousnessAgent(AIAgent):
    """AI Agent for consciousness mining optimization"""

    def __init__(self, redis_client: redis.Redis):
        super().__init__('consciousness_ai', redis_client)
        self.ai_optimizer = ConsciousnessMiningAI()

    async def start(self):
        await super().start()
        asyncio.create_task(self.ai_optimizer.run_optimization_loop())

    async def get_status(self) -> Dict[str, Any]:
        status = await super().get_status()
        status.update({
            'consciousness_level': self.ai_optimizer.current_consciousness.level,
            'optimization_cycles': len(self.ai_optimizer.metrics_history),
            'performance_score': self.ai_optimizer._calculate_performance_score(
                self.ai_optimizer.metrics_history[-1] if self.ai_optimizer.metrics_history else {}
            )
        })
        return status

class PoolAgent(AIAgent):
    """AI Agent for pool orchestration"""

    def __init__(self, redis_client: redis.Redis):
        super().__init__('pool_orchestrator', redis_client)
        self.pool_orchestrator = AIPoolOrchestrator()

    async def start(self):
        await super().start()
        asyncio.create_task(self.pool_orchestrator.run_orchestrator())

    async def get_status(self) -> Dict[str, Any]:
        status = await super().get_status()
        recommendation = await self.pool_orchestrator.get_optimal_pool_recommendation()
        status.update({
            'active_pools': len(self.pool_orchestrator.pool_metrics),
            'current_strategy': self.pool_orchestrator.current_strategy.primary_pool,
            'recommendation': recommendation.get('recommendation', 'none'),
            'recommendation_confidence': recommendation.get('confidence', 0.0)
        })
        return status

class WarpAgent(AIAgent):
    """AI Agent for warp engine optimization"""

    def __init__(self, redis_client: redis.Redis):
        super().__init__('warp_engine', redis_client)
        self.warp_engine = AIWarpEngine()

    async def start(self):
        await super().start()
        asyncio.create_task(self.warp_engine.run_warp_engine())

    async def get_status(self) -> Dict[str, Any]:
        status = await super().get_status()
        status.update({
            'consciousness_level': self.warp_engine.current_consciousness.level,
            'warp_intensity': self.warp_engine.warp_field.intensity,
            'quantum_coherence': self.warp_engine.current_consciousness.coherence,
            'adaptation_cycles': self.warp_engine.adaptation_cycles
        })
        return status

class ZIONAIOrchestrator:
    """Master orchestrator for all ZION AI components"""

    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        # Initialize AI agents
        self.agents = {
            'consciousness': ConsciousnessAgent(self.redis_client),
            'pool': PoolAgent(self.redis_client),
            'warp': WarpAgent(self.redis_client)
        }

        # Orchestrator state
        self.is_running = False
        self.coordination_interval = 30  # seconds
        self.last_coordination = datetime.now()

        # Multi-agent decision making
        self.agent_weights = {
            'consciousness': 0.4,
            'pool': 0.3,
            'warp': 0.3
        }

        self.conflict_resolution_strategy = 'weighted_voting'

        logger.info("ZION AI Orchestrator initialized")

    async def start_orchestrator(self):
        """Start the AI orchestrator and all agents"""
        logger.info("Starting ZION AI Orchestrator...")

        self.is_running = True

        # Start all AI agents
        start_tasks = []
        for agent in self.agents.values():
            start_tasks.append(agent.start())

        await asyncio.gather(*start_tasks)

        # Start coordination loop
        asyncio.create_task(self.coordination_loop())

        # Start health monitoring
        asyncio.create_task(self.health_monitoring_loop())

        logger.info("ZION AI Orchestrator started successfully")

    async def stop_orchestrator(self):
        """Stop the AI orchestrator and all agents"""
        logger.info("Stopping ZION AI Orchestrator...")

        self.is_running = False

        # Stop all agents
        stop_tasks = []
        for agent in self.agents.values():
            stop_tasks.append(agent.stop())

        await asyncio.gather(*stop_tasks)

        logger.info("ZION AI Orchestrator stopped")

    async def coordination_loop(self):
        """Main coordination loop for multi-agent decision making"""
        while self.is_running:
            try:
                # Collect decisions from all agents
                agent_decisions = await self.collect_agent_decisions()

                # Resolve conflicts and create unified strategy
                unified_strategy = self.resolve_agent_conflicts(agent_decisions)

                # Implement coordinated strategy
                await self.implement_coordinated_strategy(unified_strategy)

                # Update coordination timestamp
                self.last_coordination = datetime.now()

                # Store coordination results
                self.store_coordination_results(unified_strategy, agent_decisions)

                await asyncio.sleep(self.coordination_interval)

            except Exception as e:
                logger.error(f"Error in coordination loop: {e}")
                await asyncio.sleep(10)

    async def collect_agent_decisions(self) -> Dict[str, Any]:
        """Collect decisions and recommendations from all AI agents"""
        decisions = {}

        try:
            # Get consciousness AI optimization
            consciousness_key = 'ai:optimized_params'
            consciousness_data = self.redis_client.get(consciousness_key)
            if consciousness_data:
                decisions['consciousness'] = json.loads(consciousness_data)

            # Get pool orchestrator recommendation
            pool_key = 'ai:pool_recommendation'
            pool_data = self.redis_client.get(pool_key)
            if pool_data:
                decisions['pool'] = json.loads(pool_data)

            # Get warp engine optimization
            warp_key = 'ai:warp_optimization'
            warp_data = self.redis_client.get(warp_key)
            if warp_data:
                decisions['warp'] = json.loads(warp_data)

        except Exception as e:
            logger.error(f"Error collecting agent decisions: {e}")

        return decisions

    def resolve_agent_conflicts(self, agent_decisions: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts between different AI agent recommendations"""
        try:
            if not agent_decisions:
                return self.get_default_strategy()

            unified_strategy = {
                'mining_parameters': {},
                'pool_strategy': {},
                'warp_parameters': {},
                'confidence_scores': {},
                'coordination_timestamp': datetime.now().isoformat()
            }

            # Resolve mining parameters (consciousness vs warp engine)
            if 'consciousness' in agent_decisions and 'warp' in agent_decisions:
                consciousness_params = agent_decisions['consciousness']
                warp_params = agent_decisions['warp'].get('mining_optimization', {})

                # Weighted combination
                c_weight = self.agent_weights['consciousness']
                w_weight = self.agent_weights['warp']

                unified_mining = {}
                for param in set(consciousness_params.keys()) | set(warp_params.keys()):
                    c_val = consciousness_params.get(param, 0)
                    w_val = warp_params.get(param, 0)

                    if c_val != 0 and w_val != 0:
                        unified_mining[param] = (c_val * c_weight + w_val * w_weight) / (c_weight + w_weight)
                    elif c_val != 0:
                        unified_mining[param] = c_val
                    else:
                        unified_mining[param] = w_val

                unified_strategy['mining_parameters'] = unified_mining

            # Pool strategy (from pool orchestrator)
            if 'pool' in agent_decisions:
                pool_decision = agent_decisions['pool']
                unified_strategy['pool_strategy'] = {
                    'recommended_pool': pool_decision.get('recommendation', 'zion-official'),
                    'confidence': pool_decision.get('confidence', 0.0),
                    'strategy_weights': pool_decision.get('strategy_weights', {})
                }

            # Warp parameters (from warp engine)
            if 'warp' in agent_decisions:
                warp_decision = agent_decisions['warp']
                unified_strategy['warp_parameters'] = warp_decision.get('warp_field_optimization', {})

            # Calculate confidence scores
            unified_strategy['confidence_scores'] = {
                agent: len(decisions) for agent, decisions in agent_decisions.items()
            }

            return unified_strategy

        except Exception as e:
            logger.error(f"Error resolving agent conflicts: {e}")
            return self.get_default_strategy()

    def get_default_strategy(self) -> Dict[str, Any]:
        """Return default strategy when coordination fails"""
        return {
            'mining_parameters': {
                'target_hash_rate': 5000000,
                'difficulty_adjustment': 1.0,
                'power_target': 200,
                'temperature_target': 70,
                'efficiency_weight': 0.7
            },
            'pool_strategy': {
                'recommended_pool': 'zion-official',
                'confidence': 0.5,
                'strategy_weights': {'zion-official': 1.0}
            },
            'warp_parameters': {
                'field_intensity': 0.5,
                'field_frequency': 7.83,
                'field_coherence': 0.6
            },
            'confidence_scores': {'default': 1},
            'coordination_timestamp': datetime.now().isoformat()
        }

    async def implement_coordinated_strategy(self, strategy: Dict[str, Any]):
        """Implement the coordinated strategy across all mining components"""
        try:
            # Send mining parameters to mining processes
            mining_params = strategy.get('mining_parameters', {})
            self.redis_client.setex(
                'orchestrator:mining_params',
                300,  # 5 minutes
                json.dumps(mining_params)
            )

            # Send pool strategy to pool manager
            pool_strategy = strategy.get('pool_strategy', {})
            self.redis_client.setex(
                'orchestrator:pool_strategy',
                300,
                json.dumps(pool_strategy)
            )

            # Send warp parameters to warp engine
            warp_params = strategy.get('warp_parameters', {})
            self.redis_client.setex(
                'orchestrator:warp_params',
                300,
                json.dumps(warp_params)
            )

            # Publish coordination event
            coordination_event = {
                'type': 'strategy_update',
                'strategy': strategy,
                'timestamp': datetime.now().isoformat()
            }

            self.redis_client.publish('orchestrator:events', json.dumps(coordination_event))

            logger.info("Coordinated strategy implemented successfully")

        except Exception as e:
            logger.error(f"Error implementing coordinated strategy: {e}")

    def store_coordination_results(self, unified_strategy: Dict[str, Any],
                                 agent_decisions: Dict[str, Any]):
        """Store coordination results for analysis and learning"""
        try:
            coordination_record = {
                'timestamp': datetime.now().isoformat(),
                'unified_strategy': unified_strategy,
                'agent_decisions': agent_decisions,
                'agent_weights': self.agent_weights,
                'coordination_method': self.conflict_resolution_strategy
            }

            # Store in Redis (keep last 100 records)
            key = f"orchestrator:coordination:{int(datetime.now().timestamp())}"
            self.redis_client.setex(key, 86400, json.dumps(coordination_record))  # 24 hours

            # Maintain coordination history
            history_key = 'orchestrator:history'
            self.redis_client.lpush(history_key, json.dumps(coordination_record))
            self.redis_client.ltrim(history_key, 0, 99)  # Keep last 100

        except Exception as e:
            logger.error(f"Error storing coordination results: {e}")

    async def health_monitoring_loop(self):
        """Monitor health of all AI agents"""
        while self.is_running:
            try:
                # Check agent statuses
                agent_statuses = {}
                for agent_name, agent in self.agents.items():
                    status = await agent.get_status()
                    agent_statuses[agent_name] = status

                # Check for unhealthy agents
                unhealthy_agents = []
                for agent_name, status in agent_statuses.items():
                    if status.get('health') != 'healthy':
                        unhealthy_agents.append(agent_name)

                if unhealthy_agents:
                    logger.warning(f"Unhealthy agents detected: {unhealthy_agents}")
                    # Could implement auto-recovery here

                # Store health status
                self.redis_client.setex(
                    'orchestrator:health',
                    60,  # 1 minute
                    json.dumps({
                        'timestamp': datetime.now().isoformat(),
                        'agent_statuses': agent_statuses,
                        'overall_health': 'healthy' if not unhealthy_agents else 'degraded'
                    })
                )

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(10)

    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator status"""
        try:
            agent_statuses = {}
            for agent_name, agent in self.agents.items():
                agent_statuses[agent_name] = await agent.get_status()

            # Get latest coordination results
            latest_coordination = self.redis_client.get('orchestrator:history')
            if latest_coordination:
                latest_coordination = json.loads(latest_coordination)

            return {
                'orchestrator_running': self.is_running,
                'agent_statuses': agent_statuses,
                'last_coordination': self.last_coordination.isoformat(),
                'coordination_interval': self.coordination_interval,
                'agent_weights': self.agent_weights,
                'latest_coordination': latest_coordination,
                'overall_health': 'healthy' if all(
                    status.get('health') == 'healthy'
                    for status in agent_statuses.values()
                ) else 'degraded'
            }

        except Exception as e:
            logger.error(f"Error getting orchestrator status: {e}")
            return {'error': str(e)}

    async def update_agent_weights(self, new_weights: Dict[str, float]):
        """Update agent weights for decision making"""
        try:
            # Validate weights
            if not all(0 <= weight <= 1 for weight in new_weights.values()):
                raise ValueError("Weights must be between 0 and 1")

            if abs(sum(new_weights.values()) - 1.0) > 0.01:
                raise ValueError("Weights must sum to approximately 1.0")

            self.agent_weights = new_weights
            logger.info(f"Updated agent weights: {new_weights}")

        except Exception as e:
            logger.error(f"Error updating agent weights: {e}")
            raise

async def main():
    """Main function for ZION AI Orchestrator"""
    orchestrator = ZIONAIOrchestrator()

    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(orchestrator.stop_orchestrator())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Start orchestrator
        await orchestrator.start_orchestrator()

        # Keep running until stopped
        while orchestrator.is_running:
            await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Error in main orchestrator loop: {e}")
    finally:
        await orchestrator.stop_orchestrator()

if __name__ == "__main__":
    asyncio.run(main())