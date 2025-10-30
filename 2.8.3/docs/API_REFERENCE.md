# 📚 ZION Blockchain - Complete RPC API Reference

**Version:** 2.8.3 "Terra Nova"  
**Last Updated:** October 30, 2025  
**API Tested:** ✅ All methods validated in security audit

---

## 📋 Table of Contents

1. [API Overview](#api-overview)
2. [Blockchain RPCs](#blockchain-rpcs)
3. [Wallet RPCs](#wallet-rpcs)
4. [Mining RPCs](#mining-rpcs)
5. [Network RPCs](#network-rpcs)
6. [Error Codes](#error-codes)
7. [Rate Limiting](#rate-limiting)

---

## 🌐 API Overview

### Connection Details
- **Protocol:** JSON-RPC 2.0
- **Default Port:** 8332 (testnet/regtest)
- **Endpoint:** `http://127.0.0.1:8332`
- **Content-Type:** `application/json`

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "METHOD_NAME",
  "params": [PARAMETERS],
  "id": 1
}
```

### Response Format (Success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": RESULT_DATA
}
```

### Response Format (Error)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": ERROR_CODE,
    "message": "Error description"
  }
}
```

### Rate Limiting
- **Limit:** 10,000 requests per minute
- **Enforcement:** Automatic (429 status code when exceeded)
- **Burst Protection:** Yes

---

## 🔗 Blockchain RPCs

### getblockchaininfo

Get general blockchain information.

**Parameters:** None

**Returns:**
```json
{
  "chain": "regtest",
  "blocks": 150,
  "headers": 150,
  "bestblockhash": "0000abc123...",
  "difficulty": 1.0,
  "mediantime": 1730246400,
  "verificationprogress": 1.0,
  "chainwork": "00000000000000000000000000000000000000000000000000000000000000c8",
  "pruned": false
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

---

### getblockcount

Get the current block height.

**Parameters:** None

**Returns:** Integer (block height)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockcount","params":[],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": 150
}
```

---

### getblockhash

Get block hash by height.

**Parameters:**
- `height` (integer, required): Block height

**Returns:** String (64-character hex block hash)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockhash","params":[100],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0000abc123def456789abcdef0123456789abcdef0123456789abcdef0123456"
}
```

**Errors:**
- `-8`: Block height out of range

---

### getblock

Get detailed block information.

**Parameters:**
- `blockhash` (string, required): 64-character hex block hash
- `verbosity` (integer, optional): 0=raw hex, 1=json (default), 2=json with tx details

**Returns:** Object (block details)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"getblock",
    "params":["0000abc123def456789abcdef0123456789abcdef0123456789abcdef0123456"],
    "id":1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "hash": "0000abc123def456789abcdef0123456789abcdef0123456789abcdef0123456",
    "confirmations": 50,
    "height": 100,
    "version": 1,
    "merkleroot": "abc123...",
    "time": 1730246400,
    "mediantime": 1730246000,
    "nonce": 123456,
    "bits": "1d00ffff",
    "difficulty": 1.0,
    "chainwork": "0000000000000000000000000000000000000000000000000000000000000064",
    "previousblockhash": "0000def456...",
    "nextblockhash": "0000ghi789...",
    "tx": [
      "txid1...",
      "txid2..."
    ]
  }
}
```

**Errors:**
- `-5`: Block not found
- `-8`: Invalid block hash format

---

### getbestblockhash

Get the hash of the best (tip) block.

**Parameters:** None

**Returns:** String (64-character hex block hash)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getbestblockhash","params":[],"id":1}'
```

---

### getdifficulty

Get current mining difficulty.

**Parameters:** None

**Returns:** Float (difficulty value)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getdifficulty","params":[],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": 1.0
}
```

---

### gettransaction

Get detailed transaction information.

**Parameters:**
- `txid` (string, required): Transaction ID (64-character hex)

**Returns:** Object (transaction details)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"gettransaction",
    "params":["abc123def456..."],
    "id":1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "txid": "abc123def456...",
    "hash": "abc123def456...",
    "version": 1,
    "size": 250,
    "locktime": 0,
    "confirmations": 25,
    "blockhash": "0000abc123...",
    "blockindex": 1,
    "blocktime": 1730246400,
    "time": 1730246350,
    "vin": [
      {
        "txid": "prev_tx_id...",
        "vout": 0,
        "scriptSig": "...",
        "sequence": 4294967295
      }
    ],
    "vout": [
      {
        "value": 50.0,
        "n": 0,
        "scriptPubKey": {
          "addresses": ["ZION_abc123..."]
        }
      }
    ]
  }
}
```

**Errors:**
- `-5`: Transaction not found

---

## 💰 Wallet RPCs

### getnewaddress

Generate a new ZION wallet address.

**Parameters:**
- `label` (string, optional): Address label/account name

**Returns:** String (ZION address with "ZION_" prefix)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getnewaddress","params":["mining_wallet"],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "ZION_a3f5b8c9d2e1f4a7b6c5d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9"
}
```

**Address Format:**
- Prefix: `ZION_`
- Length: 45+ characters (ZION_ + 40 hex chars)
- Character set: Hexadecimal (0-9, a-f)

---

### validateaddress

Validate a ZION address.

**Parameters:**
- `address` (string, required): ZION address to validate

**Returns:** Object (validation result)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"validateaddress",
    "params":["ZION_a3f5b8c9d2e1f4a7b6c5d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9"],
    "id":1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "isvalid": true,
    "address": "ZION_a3f5b8c9d2e1f4a7b6c5d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9",
    "ismine": true,
    "iswatchonly": false
  }
}
```

**Accepted Formats:**
1. `ZION_` + 40+ hex characters
2. Plain 64/66 hex characters (legacy Bitcoin format)

---

### getbalance

Get wallet balance.

**Parameters:**
- `account` (string, optional): Account name or "*" for total balance
- `minconf` (integer, optional): Minimum confirmations (default: 1)

**Returns:** Float (balance in ZION)

**Example:**
```bash
# Get total balance
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getbalance","params":["*"],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": 250.0
}
```

**Special Parameters:**
- `"*"`: Returns total balance across all addresses
- Account name: Returns balance for specific account

---

### listunspent

List unspent transaction outputs (UTXOs).

**Parameters:**
- `minconf` (integer, optional): Minimum confirmations (default: 1)
- `maxconf` (integer, optional): Maximum confirmations (default: 9999999)
- `addresses` (array, optional): Filter by specific addresses

**Returns:** Array of unspent outputs

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listunspent","params":[1,9999999],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "txid": "abc123def456...",
      "vout": 0,
      "address": "ZION_abc123...",
      "account": "mining_wallet",
      "scriptPubKey": "76a914...88ac",
      "amount": 50.0,
      "confirmations": 100,
      "spendable": true,
      "solvable": true
    }
  ]
}
```

---

### listtransactions

List recent transactions.

**Parameters:**
- `account` (string, optional): Account name or "*" for all (default: "*")
- `count` (integer, optional): Number of transactions (default: 10)
- `skip` (integer, optional): Number to skip (default: 0)

**Returns:** Array of transactions

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listtransactions","params":["*",20,0],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "account": "mining_wallet",
      "address": "ZION_abc123...",
      "category": "receive",
      "amount": 50.0,
      "confirmations": 100,
      "blockhash": "0000abc123...",
      "blockindex": 1,
      "blocktime": 1730246400,
      "txid": "abc123def456...",
      "time": 1730246350,
      "timereceived": 1730246350
    }
  ]
}
```

---

### sendtoaddress

Send ZION to an address.

**Parameters:**
- `address` (string, required): Recipient ZION address
- `amount` (float, required): Amount to send
- `comment` (string, optional): Transaction comment
- `comment_to` (string, optional): Recipient comment

**Returns:** String (transaction ID)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"sendtoaddress",
    "params":["ZION_recipient_address...", 10.0, "Payment for services"],
    "id":1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "abc123def456789abcdef0123456789abcdef0123456789abcdef0123456789ab"
}
```

**Errors:**
- `-1`: Invalid address
- `-3`: Invalid amount (negative or zero)
- `-6`: Insufficient funds

**Validation:**
- Address must be valid ZION format
- Amount must be positive (> 0)
- Balance must be sufficient

---

### sendmany

Send ZION to multiple addresses.

**Parameters:**
- `fromaccount` (string, required): Source account (use "" for default)
- `amounts` (object, required): {address: amount} pairs
- `minconf` (integer, optional): Minimum confirmations (default: 1)
- `comment` (string, optional): Transaction comment

**Returns:** String (transaction ID)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"sendmany",
    "params":[
      "",
      {
        "ZION_address1...": 10.0,
        "ZION_address2...": 20.0,
        "ZION_address3...": 30.0
      },
      1,
      "Batch payment"
    ],
    "id":1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "def456abc123789def456abc123789def456abc123789def456abc123789def456"
}
```

**Errors:**
- `-1`: Invalid address in batch
- `-3`: Invalid amount (negative or zero)
- `-6`: Insufficient funds for total amount

---

### estimatefee

Estimate transaction fee.

**Parameters:**
- `nblocks` (integer, required): Confirmation target (blocks)

**Returns:** Float (estimated fee in ZION)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"estimatefee","params":[6],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": 0.0001
}
```

---

## ⛏️ Mining RPCs

### getmininginfo

Get current mining information.

**Parameters:** None

**Returns:** Object (mining stats)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getmininginfo","params":[],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "blocks": 150,
    "currentblocksize": 1000,
    "currentblocktx": 0,
    "difficulty": 1.0,
    "networkhashps": 1234567890,
    "pooledtx": 0,
    "chain": "regtest",
    "algorithm": "cosmic_harmony"
  }
}
```

---

### generate

Generate blocks immediately (regtest only).

**Parameters:**
- `nblocks` (integer, required): Number of blocks to generate

**Returns:** Array of block hashes

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"generate","params":[5],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    "0000abc123...",
    "0000def456...",
    "0000ghi789...",
    "0000jkl012...",
    "0000mno345..."
  ]
}
```

**Note:** Only works in regtest mode. For testnet/mainnet, use actual miners.

---

### getnetworkhashps

Get estimated network hash rate.

**Parameters:**
- `nblocks` (integer, optional): Number of blocks to average (default: 120)
- `height` (integer, optional): Block height to estimate from (default: -1 = current)

**Returns:** Float (hash rate in H/s)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getnetworkhashps","params":[120,-1],"id":1}'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": 1234567890.5
}
```

---

## 🌐 Network RPCs

### getpeerinfo

Get information about connected peers.

**Parameters:** None

**Returns:** Array of peer objects

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getpeerinfo","params":[],"id":1}'
```

---

### getnetworkinfo

Get network-related information.

**Parameters:** None

**Returns:** Object (network info)

**Example:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getnetworkinfo","params":[],"id":1}'
```

---

## ❌ Error Codes

### Standard JSON-RPC Errors
- `-32700`: Parse error (invalid JSON)
- `-32600`: Invalid request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

### ZION-Specific Errors
- `-1`: Invalid address format
- `-3`: Invalid amount (negative, zero, or too large)
- `-5`: Resource not found (block, transaction, etc.)
- `-6`: Insufficient funds
- `-8`: Invalid parameter (height, hash, etc.)
- `-32`: Rate limit exceeded

### Error Response Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -6,
    "message": "Insufficient funds"
  }
}
```

---

## 🚦 Rate Limiting

### Limits
- **Maximum Requests:** 10,000 per minute
- **Window:** Rolling 60-second window
- **Enforcement:** Automatic

### Rate Limit Headers
When rate limited, response includes:
- **Status Code:** 429 (Too Many Requests)
- **Retry-After:** Seconds until limit resets

### Best Practices
1. **Implement exponential backoff** for retries
2. **Cache blockchain info** when possible
3. **Batch requests** using sendmany instead of multiple sendtoaddress
4. **Monitor rate limits** in production environments

### Example Rate Limit Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32,
    "message": "Rate limit exceeded. Please retry after 30 seconds."
  }
}
```

---

## 🔐 Security Notes

### Input Validation
✅ All inputs are validated:
- **Addresses:** Must match ZION format
- **Amounts:** Must be positive floats
- **Block heights:** Must be valid integers
- **Hashes:** Must be 64-character hex strings

### Protection Against
- ✅ SQL Injection
- ✅ XSS Attacks
- ✅ Path Traversal
- ✅ Null Byte Injection
- ✅ Buffer Overflow
- ✅ Race Conditions

### Recommendations
1. **Use HTTPS** in production
2. **Implement authentication** (firewall rules)
3. **Monitor rate limits**
4. **Validate responses** in client applications
5. **Handle errors gracefully**

---

## 📖 Additional Resources

- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Mining Guide:** [MINING_GUIDE.md](MINING_GUIDE.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

**🙏 JAI RAM SITA HANUMAN - ON THE STAR! ⭐**

*Complete RPC API documentation for ZION 2.8.3 blockchain*
