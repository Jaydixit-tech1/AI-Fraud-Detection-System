# AI Fraud Detection System

A comprehensive fraud detection engine for fintech companies that analyzes financial transactions and identifies potentially fraudulent activities.

## Features

- **Intelligent Risk Scoring**: Calculates fraud risk scores (0-100) based on multiple factors
- **Pattern Detection**: Identifies unusual patterns including:
  - Amount spikes compared to user average
  - Location mismatches and international transactions
  - Abnormal transaction frequency
  - Device and IP address changes
  - Time-based anomalies
- **Actionable Recommendations**: Provides clear action recommendations:
  - Allow transaction
  - Flag for review
  - Block transaction immediately
- **Detailed Reasoning**: Explains why transactions are flagged with specific risk factors

## Transaction Data Requirements

Each transaction must include:

- **transaction_id**: Unique transaction identifier
- **user_id**: User identifier
- **amount**: Transaction amount (float)
- **currency**: Currency code (e.g., "USD")
- **transaction_time**: ISO format datetime string
- **merchant_name**: Name of the merchant
- **merchant_category**: Category of merchant
- **payment_method**: Payment method (UPI, Card, Net Banking, Wallet)
- **user_location**: User's location (e.g., "City, Country")
- **merchant_location**: Merchant's location
- **device_type**: Device type (mobile/web)
- **ip_address**: IP address of the transaction
- **transaction_frequency_24h**: Number of transactions in last 24 hours
- **avg_user_transaction_amount**: User's average transaction amount

Optional fields for enhanced detection:
- **user_device_history**: List of previously used device types
- **user_location_history**: List of previously used locations
- **user_ip_history**: List of previously used IP addresses
- **user_international_history**: Boolean indicating if user has international transaction history

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For web frontend, Flask and Flask-CORS are required (included in requirements.txt)

## Usage

### 🌐 Web Frontend (Recommended)

The easiest way to use the system is through the modern web interface:

1. **Install dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server:**
   ```bash
   # Windows
   python app.py
   # OR double-click: start_server.bat
   
   # Linux/Mac
   python3 app.py
   # OR run: ./start_server.sh
   ```

3. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - ⚠️ **IMPORTANT:** Do NOT open the HTML file directly (file://)
   - You MUST access it through the Flask server at http://localhost:5000

4. **Use the interface:**
   - Fill in the transaction form
   - Click "Analyze Transaction" to get real-time fraud detection
   - View detailed risk analysis and recommendations
   - Use "Load Sample" to try example transactions

**Troubleshooting:**
- If you see CORS errors, make sure you're accessing via `http://localhost:5000`, not opening the HTML file directly
- Check that the server is running (you should see "Server connected" in the header)
- Make sure port 5000 is not already in use

The web interface provides:
- ✅ Beautiful, modern UI with real-time analysis
- ✅ Interactive forms with validation
- ✅ Visual risk score indicators
- ✅ Detailed risk factor explanations
- ✅ Color-coded fraud status badges

### 💻 Python API Usage

#### Basic Usage

```python
from transaction_processor import TransactionProcessor

# Initialize processor
processor = TransactionProcessor()

# Prepare transaction data
transaction = {
    "transaction_id": "TXN001",
    "user_id": "USER123",
    "amount": 5000.00,
    "currency": "USD",
    "transaction_time": "2024-01-15T14:30:00Z",
    "merchant_name": "Online Store",
    "merchant_category": "Electronics",
    "payment_method": "Card",
    "user_location": "New York, USA",
    "merchant_location": "Moscow, Russia",
    "device_type": "mobile",
    "ip_address": "192.168.1.100",
    "transaction_frequency_24h": 12,
    "avg_user_transaction_amount": 150.00,
    "user_device_history": ["web"],
    "user_location_history": ["New York, USA"],
    "user_ip_history": ["192.168.1.50"],
    "user_international_history": False
}

# Process transaction
result = processor.process_transaction(transaction)

# Print result
print(processor.format_output(result))
```

#### Batch Processing

```python
# Process multiple transactions
transactions = [transaction1, transaction2, transaction3]
results = processor.process_transactions_batch(transactions)

# Save results to file
processor.save_results(results, "fraud_detection_results.json")
```

#### REST API Endpoints

When the web server is running, you can also use the REST API:

- **POST `/api/analyze`** - Analyze a single transaction
- **POST `/api/analyze-batch`** - Analyze multiple transactions
- **GET `/api/health`** - Health check

Example API call:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d @sample_transactions.json
```

### 📝 Running Examples

```bash
# Python examples
python example_usage.py

# Command-line API
python fraud_detection_api.py sample_transactions.json results.json
```

## Output Format

The system returns results in the following JSON format:

```json
{
  "transaction_id": "TXN001",
  "fraud_status": "Fraudulent",
  "risk_score": 85,
  "risk_factors": [
    "Amount spike: 33.33x user average ($5000.00 vs $150.00)",
    "Abnormal frequency: 12 transactions in last 24 hours",
    "International transaction without history: USA → Russia",
    "New device type detected: mobile"
  ],
  "reasoning": "Risk assessment for transaction TXN001:\nHIGH RISK - Multiple suspicious indicators detected:\n1. Amount spike: 33.33x user average...",
  "recommended_action": "Block transaction immediately"
}
```

## Risk Scoring Logic

The system evaluates transactions based on:

1. **Amount Analysis** (0-25 points)
   - High amount compared to user average
   - Unusually small amounts (test transactions)

2. **Frequency Analysis** (0-20 points)
   - Multiple transactions in short time period
   - Abnormal transaction patterns

3. **Location Analysis** (0-30 points)
   - International transactions without history
   - New location detection
   - Location mismatches

4. **Device Analysis** (0-12 points)
   - New device type detection
   - Device switching patterns

5. **IP Address Analysis** (0-15 points)
   - New IP address detection
   - Suspicious IP patterns

6. **Payment Method Analysis** (0-5 points)
   - Unusual payment method patterns

7. **Merchant Analysis** (-5 to 10 points)
   - High-risk merchant categories
   - Known safe merchant categories

8. **Time Pattern Analysis** (0-5 points)
   - Off-peak hour transactions

## Risk Thresholds

- **Risk Score ≥ 70**: Fraudulent → Block transaction immediately
- **Risk Score ≥ 40**: Flag for review
- **Risk Score < 40**: Allow transaction

## Customization

You can customize risk thresholds and multipliers in `fraud_detection_engine.py`:

```python
self.HIGH_AMOUNT_MULTIPLIER = 3.0
self.MEDIUM_AMOUNT_MULTIPLIER = 2.0
self.HIGH_FREQUENCY_THRESHOLD = 10
self.MEDIUM_FREQUENCY_THRESHOLD = 5
self.FRAUD_THRESHOLD = 70
self.REVIEW_THRESHOLD = 40
```

## Production Considerations

For production deployment, consider:

1. **IP Reputation Services**: Integrate with services like MaxMind, AbuseIPDB
2. **Machine Learning**: Add ML models for pattern recognition
3. **Real-time Processing**: Implement async processing for high-volume scenarios
4. **Database Integration**: Connect to transaction databases
5. **API Endpoints**: Create REST API for integration
6. **Monitoring**: Add logging and alerting systems
7. **Performance**: Optimize for high-throughput scenarios

## File Structure

```
AI Fraud Detection System/
├── fraud_detection_engine.py    # Core fraud detection logic
├── transaction_processor.py      # Transaction processing and I/O
├── app.py                        # Flask web server and API
├── fraud_detection_api.py        # Command-line API interface
├── example_usage.py              # Example usage demonstrations
├── sample_transactions.json      # Sample transaction data
├── requirements.txt              # Python dependencies
├── static/                       # Web frontend files
│   ├── index.html               # Main web interface
│   ├── styles.css               # Modern CSS styling
│   └── app.js                   # Frontend JavaScript
└── README.md                     # This file
```

## License

This is a proprietary fraud detection system for fintech use.

## Support

For questions or issues, please contact the development team.
