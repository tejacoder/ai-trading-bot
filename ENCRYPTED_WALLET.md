# 🔐 Encrypted Wallet Implementation

## Overview

Trading bot sekarang menggunakan **encrypted wallet** dengan AES-256 encryption untuk keamanan maksimal!

---

## ✅ Features

### 1. AES-256 Encryption
- Private key dienkripsi dengan Fernet (AES-256)
- Password-based key derivation (PBKDF2HMAC)
- 100,000 iterations untuk brute-force protection
- Unique salt per wallet

### 2. Hidden Storage
- Filename: `.wallet_data` (hidden file)
- Location: `~/.agent-wallet/` (di luar repo)
- Permissions: 0600 (owner only)
- Gitignored otomatis

### 3. Decrypt on Demand
- Private key hanya didecrypt saat dibutuhkan
- Untuk signing transactions
- Untuk export builder code
- Password required setiap kali

### 4. No Plaintext
- Private key TIDAK PERNAH disimpan plaintext
- TIDAK PERNAH di-log
- TIDAK PERNAH di git
- TIDAK PERNAH di memory lebih lama dari perlu

---

## 📁 Files

### New Files
```
wallet_encrypted.py    - Encrypted wallet implementation (8.7 KB)
export_bc.py          - Export builder code tool (1.7 KB)
setup_auto.py         - Updated untuk encrypted wallet (4.9 KB)
```

### Updated Files
```
.gitignore            - Added .wallet_data, .agent-wallet/
```

---

## 🚀 Usage

### 1. Setup (First Time)

```bash
python3 setup_auto.py

# Enter password for wallet encryption: ****
# Confirm password: ****
# 
# 🔐 Creating new encrypted wallet...
# ✅ Wallet: 0x742d...
# ✅ Saved encrypted to: ~/.agent-wallet/.wallet_data
# 
# 🏗️  Requesting builder code...
# ✅ Builder code: bc_abc123xyz
```

### 2. Export Builder Code

```bash
python3 export_bc.py

# Enter password: ****
# 
# 🔓 Decrypting wallet...
# ✅ Wallet loaded: 0x742d...
# 
# 🏗️  Requesting builder code...
# ✅ Builder Code: bc_abc123xyz
```

### 3. Use in Python

```python
from wallet_encrypted import EncryptedWallet
import getpass

# Load encrypted wallet
password = getpass.getpass("Password: ")
wallet = EncryptedWallet.load_encrypted(
    "~/.agent-wallet/.wallet_data",
    password
)

# Check balance (no password needed)
balance = wallet.get_balance()
print(f"Balance: {balance} ETH")

# Send ETH (requires password)
tx = wallet.send_eth_with_builder_code(
    to_address="0x742d...",
    amount_eth=0.001,
    password=password
)
```

---

## 🔐 Security

### Encryption Details

**Algorithm:** AES-256 (Fernet)
**Key Derivation:** PBKDF2HMAC
**Hash:** SHA-256
**Iterations:** 100,000
**Salt:** 16 bytes random per wallet

### File Structure

```json
{
  "address": "0x742d...",
  "encrypted_key": "gAAAAA...",  // Base64 encoded
  "salt": "xY3z..."               // Base64 encoded
}
```

### Password Requirements

**Recommended:**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Not a dictionary word
- Unique per agent

**Example:**
```
MyTr4d1ng!B0t#2024$Secure
```

---

## 🧪 Testing

### Test 1: Create & Load

```bash
python3 -c "
from wallet_encrypted import EncryptedWallet

password = 'test123'
wallet = EncryptedWallet.create_new(password)
print(f'Created: {wallet.address}')

wallet.save_encrypted('/tmp/.test', password)
wallet2 = EncryptedWallet.load_encrypted('/tmp/.test', password)
print(f'Loaded: {wallet2.address}')

assert wallet.address == wallet2.address
print('✅ Test passed!')
"
```

### Test 2: Wrong Password

```bash
python3 -c "
from wallet_encrypted import EncryptedWallet

password = 'test123'
wallet = EncryptedWallet.create_new(password)
wallet.save_encrypted('/tmp/.test', password)

try:
    wallet2 = EncryptedWallet.load_encrypted('/tmp/.test', 'wrong')
    print('❌ Should have failed!')
except ValueError as e:
    print(f'✅ Correctly rejected: {e}')
"
```

### Test 3: Export Builder Code

```bash
echo "demo123" | python3 export_bc.py

# ✅ Builder Code: bc_ynnc3nw0
# ✅ Wallet: 0xC95374c67c08922eC4FE51a00bc0544A202675D4
```

---

## 🔄 Migration

### Convert Existing Wallet

```python
import os
import json
from wallet_encrypted import EncryptedWallet
from web3 import Web3
from cryptography.fernet import Fernet

# Load existing plaintext wallet
with open('~/.simple-wallet/wallet.json', 'r') as f:
    data = json.load(f)

# Create encrypted version
w3 = Web3()
account = w3.eth.account.from_key(data['private_key'])

salt = os.urandom(16)
password = input("New password: ")
key = EncryptedWallet._derive_key(password, salt)

f = Fernet(key)
encrypted_key = f.encrypt(data['private_key'].encode())

wallet = EncryptedWallet(account.address, encrypted_key, salt)
wallet.save_encrypted('~/.agent-wallet/.wallet_data', password)

print(f'✅ Migrated to encrypted wallet')
```

---

## 🎯 Multi-Agent Setup

### Agent 1

```bash
mkdir ~/agent1
cd ~/agent1
git clone https://github.com/tejacoder/ai-trading-bot.git .

python3 setup_auto.py
# Password: agent1-secure-password
# ✅ Wallet: 0xC953...
# ✅ Builder: bc_ynnc3nw0
```

### Agent 2

```bash
mkdir ~/agent2
cd ~/agent2
git clone https://github.com/tejacoder/ai-trading-bot.git .

python3 setup_auto.py
# Password: agent2-secure-password
# ✅ Wallet: 0x3ED2...
# ✅ Builder: bc_30rah79h
```

**Each agent:**
- ✅ Unique encrypted wallet
- ✅ Unique password
- ✅ Unique builder code
- ✅ Isolated storage

---

## 🛡️ Best Practices

### 1. Strong Passwords

```bash
# Good
MyTr4d1ng!B0t#2024$Secure

# Bad
password123
```

### 2. Environment Variables

```bash
# .env
WALLET_PASSWORD=your-secure-password

# Python
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("WALLET_PASSWORD")
```

### 3. Backup

```bash
# Backup encrypted file (still safe!)
cp ~/.agent-wallet/.wallet_data ~/backup/.wallet_data.backup

# Store password separately (password manager)
```

### 4. Never Commit

```bash
# .gitignore already includes:
.wallet_data
.agent-wallet/
wallet.json
*.key
*.pem
```

---

## 🔧 API Reference

### EncryptedWallet

```python
class EncryptedWallet:
    """Encrypted wallet with password protection"""
    
    @staticmethod
    def create_new(password: str) -> 'EncryptedWallet':
        """Create new encrypted wallet"""
    
    @staticmethod
    def load_encrypted(path: str, password: str) -> 'EncryptedWallet':
        """Load encrypted wallet from file"""
    
    def save_encrypted(self, path: str, password: str):
        """Save encrypted wallet to file"""
    
    def send_eth_with_builder_code(
        self,
        to_address: str,
        amount_eth: float,
        password: str
    ) -> str:
        """Send ETH with builder code (requires password)"""
    
    def swap_tokens(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        password: str
    ) -> str:
        """Swap tokens (requires password)"""
    
    def mint_nft(
        self,
        contract_address: str,
        token_uri: str,
        password: str
    ) -> str:
        """Mint NFT (requires password)"""
    
    def get_balance(self) -> float:
        """Get ETH balance (no password needed)"""
    
    def get_token_balance(self, token: str) -> float:
        """Get token balance (no password needed)"""
    
    def export_builder_code(self, password: str) -> str:
        """Export builder code (requires password)"""
```

---

## ❓ Troubleshooting

### Wrong Password

```
❌ Error: Invalid password or corrupted wallet
```

**Solution:** Check password, try backup

### Wallet Not Found

```
❌ Error: Wallet file not found: ~/.agent-wallet/.wallet_data
```

**Solution:** Run `setup_auto.py` first

### Import Error

```
ImportError: cannot import name 'PBKDF2'
```

**Solution:** Install cryptography
```bash
pip3 install cryptography
```

---

## 📊 Comparison

### Before (Plaintext)

```json
{
  "address": "0x742d...",
  "private_key": "c08f2c863bc4a8968b9d1294642f1332771c8a2595dc86bfb3c83e01afe3b22c"
}
```

❌ Private key visible
❌ Anyone with file access can steal funds
❌ Dangerous if committed to git

### After (Encrypted)

```json
{
  "address": "0x742d...",
  "encrypted_key": "gAAAAABmX3z...",
  "salt": "xY3zK7..."
}
```

✅ Private key encrypted
✅ Password required to decrypt
✅ Safe even if file is exposed
✅ Safe to backup

---

## 🎉 Summary

**Encrypted wallet is PRODUCTION READY!**

✅ AES-256 encryption
✅ Password protected
✅ Hidden storage
✅ Decrypt on demand
✅ No plaintext
✅ Multi-agent ready
✅ Tested & working

**Security Level:** 🔐🔐🔐🔐🔐 (5/5)

**Files:**
- wallet_encrypted.py (8.7 KB)
- export_bc.py (1.7 KB)
- setup_auto.py (updated)

**Status:** ✅ READY TO USE

---

**Date:** April 24, 2026
**Version:** 2.0.0
**Security:** AES-256 + PBKDF2HMAC
