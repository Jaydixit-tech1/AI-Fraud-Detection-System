# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Web Server
```bash
# Windows
python app.py
# OR double-click: start_server.bat

# Linux/Mac  
python3 app.py
# OR run: ./start_server.sh
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

⚠️ **CRITICAL:** Do NOT open the HTML file directly (file://). You MUST access it through the Flask server at http://localhost:5000

That's it! You're ready to analyze transactions.

---

## 🎯 First Transaction Analysis

1. Click **"Load Sample"** button to fill in a sample transaction
2. Click **"Analyze Transaction"** to see the fraud detection in action
3. Review the risk score, factors, and recommended action

---

## 📊 Understanding the Results

- **Risk Score (0-100)**: Higher scores indicate higher fraud risk
  - 0-39: Low risk → Allow transaction
  - 40-69: Medium risk → Flag for review
  - 70-100: High risk → Block transaction

- **Risk Factors**: Specific indicators that contributed to the score
- **Reasoning**: Detailed explanation of the analysis
- **Recommended Action**: What action to take based on the risk assessment

---

## 🔧 Alternative Usage Methods

### Python Script
```python
from transaction_processor import TransactionProcessor

processor = TransactionProcessor()
result = processor.process_transaction(transaction_data)
```

### Command Line
```bash
python fraud_detection_api.py sample_transactions.json results.json
```

### REST API
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "TXN001", ...}'
```

---

## 💡 Tips

- Fill in optional history fields for more accurate detection
- Use "Load Sample" to see example high-risk transactions
- The system learns from user patterns - more history = better accuracy

---

Need help? Check the full [README.md](README.md) for detailed documentation.
