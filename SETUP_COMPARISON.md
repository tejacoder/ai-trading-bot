# 🤖 Setup Agent: Manual vs Auto

## 📋 Dua Cara Setup Agent

### Option 1: Semi-Auto (setup_new_agent.py)
```bash
python3 setup_new_agent.py
```
- ✅ Auto create wallet
- ❌ Manual input builder code
- ❌ Manual fund wallet

### Option 2: Full Auto (setup_auto.py) ← BARU!
```bash
python3 setup_auto.py
```
- ✅ Auto create wallet
- ✅ Auto request builder code
- ❌ Manual fund wallet (tidak bisa auto)

---

## 🎯 Untuk 5 Agents

### Cara 1: Semi-Auto (Recommended)

**Lebih reliable karena kamu control builder code request**

```bash
# Agent 1
git clone https://github.com/YOUR_USERNAME/ai-trading-bot.git agent1
cd agent1

# Request builder code manual
curl -X POST https://api.base.dev/v1/agents/builder-codes \
  -H "Content-Type: application/json" \
  -d '{"email": "agent1@example.com"}'
# Copy builder code: bc_agent1_xyz

# Setup
python3 setup_new_agent.py
# Paste: bc_agent1_xyz

# Fund wallet
# Transfer ETH + USDC

# Repeat untuk agent 2, 3, 4, 5...
```

**Pros:**
- ✅ Kamu control setiap step
- ✅ Bisa verify builder code
- ✅ Lebih reliable

**Cons:**
- ❌ Perlu manual request builder code
- ❌ Perlu copy-paste

---

### Cara 2: Full Auto (Faster)

**Lebih cepat tapi depend on API**

```bash
# Agent 1
git clone https://github.com/YOUR_USERNAME/ai-trading-bot.git agent1
cd agent1
python3 setup_auto.py
# Enter email: agent1@example.com
# ✅ Done! (wallet + builder code auto)

# Agent 2
git clone https://github.com/YOUR_USERNAME/ai-trading-bot.git agent2
cd agent2
python3 setup_auto.py
# Enter email: agent2@example.com
# ✅ Done!

# Agent 3, 4, 5...
# Repeat!
```

**Pros:**
- ✅ Super cepat
- ✅ One command
- ✅ Less manual work

**Cons:**
- ❌ Depend on Base API
- ❌ Kalau API down, gagal
- ❌ Less control

---

## 📊 Comparison

| Feature | Semi-Auto | Full Auto |
|---------|-----------|-----------|
| Create wallet | ✅ Auto | ✅ Auto |
| Request builder code | ❌ Manual | ✅ Auto |
| Input builder code | ❌ Manual | ✅ Auto |
| Update config | ✅ Auto | ✅ Auto |
| Fund wallet | ❌ Manual | ❌ Manual |
| Reliability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Control | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 Recommendation

### Untuk 5 Agents:

**Use Full Auto (setup_auto.py)** kalau:
- ✅ Mau cepat
- ✅ Base API reliable
- ✅ Trust automation

**Use Semi-Auto (setup_new_agent.py)** kalau:
- ✅ Mau control penuh
- ✅ Verify setiap step
- ✅ Production deployment

---

## 💡 Best Practice: Hybrid Approach

```bash
# 1. Request semua builder codes dulu (batch)
for i in {1..5}; do
  curl -X POST https://api.base.dev/v1/agents/builder-codes \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"agent${i}@example.com\"}" \
    >> builder_codes.txt
  echo "" >> builder_codes.txt
done

# 2. Setup agents dengan codes yang sudah ada
# Agent 1
git clone https://github.com/YOUR_USERNAME/ai-trading-bot.git agent1
cd agent1
python3 setup_new_agent.py
# Paste builder code dari builder_codes.txt

# Agent 2
cd ..
git clone https://github.com/YOUR_USERNAME/ai-trading-bot.git agent2
cd agent2
python3 setup_new_agent.py
# Paste builder code dari builder_codes.txt

# Repeat...
```

**Pros:**
- ✅ Batch request (efficient)
- ✅ Verify codes before use
- ✅ Reliable setup
- ✅ Fast deployment

---

## 🚀 Quick Setup Script (All 5 Agents)

```bash
#!/bin/bash
# setup_all_agents.sh

REPO="https://github.com/YOUR_USERNAME/ai-trading-bot.git"

for i in {1..5}; do
  echo "Setting up Agent $i..."
  
  # Clone
  git clone $REPO agent$i
  cd agent$i
  
  # Auto setup
  echo "agent${i}@example.com" | python3 setup_auto.py
  
  # Back to parent
  cd ..
  
  echo "✅ Agent $i done!"
  echo ""
done

echo "🎉 All 5 agents setup complete!"
echo ""
echo "Next steps:"
echo "1. Fund each wallet"
echo "2. Test: cd agent1 && python3 trading_bot.py backtest 7"
echo "3. Run: python3 trading_bot.py 300"
```

**Usage:**
```bash
chmod +x setup_all_agents.sh
./setup_all_agents.sh
```

---

## 📋 Summary

### Yang OTOMATIS:
- ✅ Create wallet (kedua script)
- ✅ Request builder code (setup_auto.py only)
- ✅ Update config (kedua script)

### Yang MANUAL:
- ❌ Request builder code (setup_new_agent.py)
- ❌ Fund wallet (semua script)
- ❌ Test & deploy (semua script)

### Untuk 5 Agents:

**Fastest:**
```bash
# Use setup_auto.py
for i in {1..5}; do
  git clone REPO agent$i
  cd agent$i
  python3 setup_auto.py  # Enter email
  cd ..
done
```

**Most Reliable:**
```bash
# Request codes first
curl ... # Get 5 builder codes

# Then setup
for i in {1..5}; do
  git clone REPO agent$i
  cd agent$i
  python3 setup_new_agent.py  # Paste code
  cd ..
done
```

---

## ✅ Recommendation

**Untuk 5 agents, pakai Full Auto (setup_auto.py):**

```bash
# Agent 1
git clone REPO agent1 && cd agent1
python3 setup_auto.py  # Email: agent1@example.com

# Agent 2
cd .. && git clone REPO agent2 && cd agent2
python3 setup_auto.py  # Email: agent2@example.com

# Agent 3, 4, 5...
# Repeat!
```

**Total time: ~5 minutes untuk 5 agents!** ⚡

---

**File baru:** `setup_auto.py` - Full automation!
**Pilih yang sesuai kebutuhan kamu!** 🚀
