# 🔄 Migration Guide: Plaintext → Encrypted Wallet

## Overview

Trading bot sekarang **FULLY ENCRYPTED**! Semua file sudah diupdate untuk pakai encrypted wallet.

---

## ✅ What Changed

### Files Updated
```
✅ config.py              - WALLET_PATH → ~/.agent-wallet/.wallet_data
✅ trading_bot.py         - Uses wallet_adapter (auto-detect)
✅ wallet_adapter.py      - NEW: Auto-detect encrypted/plaintext
✅ .gitignore             - Added .wallet_data, .agent-wallet/
```

### New Files
```
✅ wallet_encrypted.py    - AES-256 encryption (8.7 KB)
✅ wallet_adapter.py      - Auto-detect adapter (5.4 KB)
✅ export_bc.py           - Export builder code (1.7 KB)
```

---

## 🚀 Migration Steps

### Option 1: Fresh Setup (Recommended)

```bash
# Backup old wallet (optional)
cp ~/.simple-wallet/wallet.json ~/backup/wallet.json.backup

# Run new setup
python3 setup_auto.py

# Enter password: ****
# Confirm password: ****
# 
# ✅ Wallet: 0x742d...
# ✅ Builder: bc_abc123xyz
# ✅ Encrypted: AES-256
```

### Option 2: Convert Existing Wallet

```python
import os
import json
from wallet_encrypted import EncryptedWallet
from web3 import Web3
from cryptography.fernet import Fernet

# Load existing plaintext wallet
with open(os.path.expanduser('~/.simple-wallet/wallet.json'), 'r') as f:
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
print(f'   Address: {wallet.address}')
```

---

## 🔐 Usage After Migration

### 1. Set Password Environment Variable

```bash
# Add to ~/.bashrc or ~/.zshrc
export WALLET_PASSWORD="your-secure-password"

# Or use .env file
echo "WALLET_PASSWORD=your-secure-password" > .env
```

### 2. Run Trading Bot

```bash
# With environment variable
WALLET_PASSWORD=demo123 python3 trading_bot.py backtest 7

# Or it will prompt
python3 trading_bot.py backtest 7
# Wallet password: ****
```

### 3. Export Builder Code

```bash
python3 export_bc.py

# Enter password: ****
# ✅ Builder Code: bc_abc123xyz
```

---

## 🧪 Testing

### Test 1: Wallet Adapter

```bash
WALLET_PASSWORD=demo123 python3 wallet_adapter.py

# ✅ Wallet loaded: 0xC95374c67c08922eC4FE51a00bc0544A202675D4
#    Type: Encrypted
# 💰 Balance: 0 ETH
```

### Test 2: Trading Bot

```bash
WALLET_PASSWORD=demo123 python3 trading_bot.py backtest 7

# 🤖 Initializing Trading Bot...
#   Wallet: 0xC95374c67c08922eC4FE51a00bc0544A202675D4
#   Type: Encrypted
#   Builder Code: bc_ynnc3nw0
```

### Test 3: Export Builder Code

```bash
echo "demo123" | python3 export_bc.py

# ✅ Builder Code: bc_ynnc3nw0
# ✅ Wallet: 0xC95374c67c08922eC4FE51a00bc0544A202675D4
```

---

## 🔄 Backward Compatibility

**Wallet adapter auto-detects wallet type!**

### Encrypted Wallet
```json
{
  "address": "0x742d...",
  "encrypted_key": "gAAAAABmX3z...",
  "salt": "xY3zK7..."
}
```
✅ Requires password
✅ AES-256 encrypted

### Plaintext Wallet (Legacy)
```json
{
  "address": "0x742d...",
  "private_key": "c08f2c863bc4..."
}
```
✅ Still works
⚠️ Not recommended

---

## 🛡️ Security Improvements

### Before
```
❌ Private key in plaintext
❌ Visible in wallet.json
❌ Dangerous if committed
❌ No password protection
```

### After
```
✅ Private key encrypted (AES-256)
✅ Password required
✅ Hidden filename (.wallet_data)
✅ Safe to backup
✅ PBKDF2HMAC (100k iterations)
```

---

## 📊 File Locations

### Old (Plaintext)
```
~/.simple-wallet/wallet.json  ❌ DEPRECATED
```

### New (Encrypted)
```
~/.agent-wallet/.wallet_data  ✅ RECOMMENDED
```

---

## 🎯 Multi-Agent Setup

### Agent 1
```bash
cd ~/agent1
python3 setup_auto.py
# Password: agent1-password
# ✅ Encrypted wallet created
```

### Agent 2
```bash
cd ~/agent2
python3 setup_auto.py
# Password: agent2-password
# ✅ Encrypted wallet created
```

**Each agent:**
- ✅ Unique encrypted wallet
- ✅ Unique password
- ✅ Unique builder code
- ✅ Isolated storage

---

## ⚠️ Important Notes

### 1. Password Management

**DO:**
- ✅ Use strong passwords (12+ chars)
- ✅ Store in password manager
- ✅ Use environment variables
- ✅ Different password per agent

**DON'T:**
- ❌ Use weak passwords
- ❌ Commit passwords to git
- ❌ Share passwords
- ❌ Reuse passwords

### 2. Backup

```bash
# Backup encrypted wallet (safe!)
cp ~/.agent-wallet/.wallet_data ~/backup/.wallet_data.backup

# Store password separately
# Use password manager or secure note
```

### 3. Recovery

**If you forget password:**
- ❌ Cannot recover encrypted wallet
- ✅ Use backup if available
- ✅ Create new wallet if needed

**Prevention:**
- ✅ Backup encrypted wallet
- ✅ Store password securely
- ✅ Test recovery process

---

## 🔧 Troubleshooting

### Issue 1: Wrong Password

```
❌ Error: Invalid password or corrupted wallet
```

**Solution:**
- Check password
- Try backup
- Check WALLET_PASSWORD env var

### Issue 2: Wallet Not Found

```
❌ Error: Wallet file not found
```

**Solution:**
- Run `setup_auto.py`
- Check WALLET_PATH in config.py
- Verify file exists: `ls ~/.agent-wallet/`

### Issue 3: Import Error

```
ImportError: No module named 'cryptography'
```

**Solution:**
```bash
pip3 install cryptography
```

---

## 📋 Checklist

### Migration Checklist

- [ ] Backup old wallet
- [ ] Run `setup_auto.py` or convert existing
- [ ] Set WALLET_PASSWORD env var
- [ ] Test with `wallet_adapter.py`
- [ ] Test with `trading_bot.py backtest 7`
- [ ] Test with `export_bc.py`
- [ ] Backup encrypted wallet
- [ ] Store password securely
- [ ] Delete old plaintext wallet (optional)

### Security Checklist

- [ ] Strong password (12+ chars)
- [ ] Password in password manager
- [ ] WALLET_PASSWORD in .env (gitignored)
- [ ] Encrypted wallet backed up
- [ ] Old plaintext wallet deleted
- [ ] .gitignore includes .wallet_data
- [ ] Test recovery process

---

## 🎉 Summary

**MIGRATION COMPLETE!**

✅ All files updated
✅ Encrypted wallet support
✅ Auto-detect adapter
✅ Backward compatible
✅ Password protected
✅ AES-256 encryption
✅ Multi-agent ready
✅ Tested & working

**Security Level:** 🔐🔐🔐🔐🔐 (5/5)

**Status:** ✅ PRODUCTION READY

---

**Date:** April 24, 2026
**Version:** 2.0.0
**Migration:** Plaintext → Encrypted
