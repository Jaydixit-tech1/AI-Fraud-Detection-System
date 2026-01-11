"""
Flask API Server for Fraud Detection System
Provides REST API endpoints and serves the web frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transaction_processor import TransactionProcessor
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
# Enable CORS for all routes and origins (for development)
CORS(app, resources={r"/api/*": {"origins": "*"}})

processor = TransactionProcessor()


@app.route('/')
def index():
    """Serve the main frontend page"""
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        return f"Error loading page: {str(e)}", 500


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)


@app.route('/api/analyze', methods=['POST'])
def analyze_transaction():
    """
    Analyze a single transaction
    POST /api/analyze
    Body: JSON transaction data
    """
    try:
        transaction_data = request.get_json()
        
        if not transaction_data:
            return jsonify({
                "error": "No transaction data provided"
            }), 400
        
        # Process transaction
        result = processor.process_transaction(transaction_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Processing error",
            "details": str(e)
        }), 500


@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """
    Analyze multiple transactions
    POST /api/analyze-batch
    Body: JSON array of transaction data
    """
    try:
        transactions = request.get_json()
        
        if not transactions:
            return jsonify({
                "error": "No transaction data provided"
            }), 400
        
        if not isinstance(transactions, list):
            return jsonify({
                "error": "Expected array of transactions"
            }), 400
        
        # Process batch
        results = processor.process_transactions_batch(transactions)
        
        return jsonify({
            "results": results,
            "total": len(results),
            "fraudulent": sum(1 for r in results if r["fraud_status"] == "Fraudulent"),
            "legitimate": sum(1 for r in results if r["fraud_status"] == "Legitimate"),
            "average_risk_score": sum(r["risk_score"] for r in results) / len(results) if results else 0
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Processing error",
            "details": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Fraud Detection Engine"
    }), 200


if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    print("=" * 80)
    print("Fraud Detection System - Web Server")
    print("=" * 80)
    print("Server starting...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("=" * 80)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port 5000 is already in use.")
            print("Please stop the other application using port 5000 or change the port in app.py")
        else:
            print(f"\n❌ Error starting server: {e}")
