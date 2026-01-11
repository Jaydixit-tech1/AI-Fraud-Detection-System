"""
Transaction Processor - Handles input/output and processes transactions
"""

import json
from typing import Dict, List, Optional
from fraud_detection_engine import FraudDetectionEngine, Transaction


class TransactionProcessor:
    """Processes transaction data and generates fraud detection results"""
    
    def __init__(self):
        self.engine = FraudDetectionEngine()
    
    def process_transaction(self, transaction_data: Dict) -> Dict:
        """
        Process a single transaction from dictionary input
        
        Args:
            transaction_data: Dictionary containing transaction fields
            
        Returns:
            Fraud detection result in specified format
        """
        # Convert dictionary to Transaction object
        transaction = self._dict_to_transaction(transaction_data)
        
        # Analyze transaction
        result = self.engine.analyze_transaction(transaction)
        
        return result
    
    def process_transactions_batch(self, transactions: List[Dict]) -> List[Dict]:
        """
        Process multiple transactions
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            List of fraud detection results
        """
        results = []
        for transaction_data in transactions:
            result = self.process_transaction(transaction_data)
            results.append(result)
        return results
    
    def _dict_to_transaction(self, data: Dict) -> Transaction:
        """Convert dictionary to Transaction object"""
        return Transaction(
            transaction_id=data.get("transaction_id", ""),
            user_id=data.get("user_id", ""),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", "USD"),
            transaction_time=data.get("transaction_time", ""),
            merchant_name=data.get("merchant_name", ""),
            merchant_category=data.get("merchant_category", ""),
            payment_method=data.get("payment_method", ""),
            user_location=data.get("user_location", ""),
            merchant_location=data.get("merchant_location", ""),
            device_type=data.get("device_type", ""),
            ip_address=data.get("ip_address", ""),
            transaction_frequency_24h=int(data.get("transaction_frequency_24h", 0)),
            avg_user_transaction_amount=float(data.get("avg_user_transaction_amount", 0)),
            user_device_history=data.get("user_device_history"),
            user_location_history=data.get("user_location_history"),
            user_ip_history=data.get("user_ip_history"),
            user_international_history=data.get("user_international_history")
        )
    
    def format_output(self, result: Dict) -> str:
        """Format result as JSON string"""
        return json.dumps(result, indent=2)
    
    def save_results(self, results: List[Dict], filename: str = "fraud_detection_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filename}")
