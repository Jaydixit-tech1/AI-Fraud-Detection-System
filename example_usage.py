"""
Example usage of the Fraud Detection Engine
Demonstrates how to analyze transactions
"""

from transaction_processor import TransactionProcessor
import json


def main():
    """Example usage with sample transactions"""
    processor = TransactionProcessor()
    
    # Example 1: High-risk transaction (amount spike + new location)
    print("=" * 80)
    print("EXAMPLE 1: High-Risk Transaction")
    print("=" * 80)
    
    transaction1 = {
        "transaction_id": "TXN001",
        "user_id": "USER123",
        "amount": 5000.00,
        "currency": "USD",
        "transaction_time": "2024-01-15T14:30:00Z",
        "merchant_name": "Online Store XYZ",
        "merchant_category": "Electronics",
        "payment_method": "Card",
        "user_location": "New York, USA",
        "merchant_location": "Moscow, Russia",
        "device_type": "mobile",
        "ip_address": "192.168.1.100",
        "transaction_frequency_24h": 12,
        "avg_user_transaction_amount": 150.00,
        "user_device_history": ["web"],
        "user_location_history": ["New York, USA", "Boston, USA"],
        "user_ip_history": ["192.168.1.50"],
        "user_international_history": False
    }
    
    result1 = processor.process_transaction(transaction1)
    print(processor.format_output(result1))
    print("\n")
    
    # Example 2: Legitimate transaction (normal pattern)
    print("=" * 80)
    print("EXAMPLE 2: Legitimate Transaction")
    print("=" * 80)
    
    transaction2 = {
        "transaction_id": "TXN002",
        "user_id": "USER456",
        "amount": 45.50,
        "currency": "USD",
        "transaction_time": "2024-01-15T12:15:00Z",
        "merchant_name": "Local Grocery Store",
        "merchant_category": "Groceries",
        "payment_method": "UPI",
        "user_location": "San Francisco, USA",
        "merchant_location": "San Francisco, USA",
        "device_type": "mobile",
        "ip_address": "192.168.1.200",
        "transaction_frequency_24h": 2,
        "avg_user_transaction_amount": 50.00,
        "user_device_history": ["mobile", "web"],
        "user_location_history": ["San Francisco, USA"],
        "user_ip_history": ["192.168.1.200", "192.168.1.201"],
        "user_international_history": False
    }
    
    result2 = processor.process_transaction(transaction2)
    print(processor.format_output(result2))
    print("\n")
    
    # Example 3: Medium-risk transaction (flagged for review)
    print("=" * 80)
    print("EXAMPLE 3: Medium-Risk Transaction (Review Required)")
    print("=" * 80)
    
    transaction3 = {
        "transaction_id": "TXN003",
        "user_id": "USER789",
        "amount": 1200.00,
        "currency": "USD",
        "transaction_time": "2024-01-15T03:45:00Z",
        "merchant_name": "Online Casino",
        "merchant_category": "Gambling",
        "payment_method": "Net Banking",
        "user_location": "Los Angeles, USA",
        "merchant_location": "Las Vegas, USA",
        "device_type": "web",
        "ip_address": "192.168.1.300",
        "transaction_frequency_24h": 6,
        "avg_user_transaction_amount": 200.00,
        "user_device_history": ["mobile"],
        "user_location_history": ["Los Angeles, USA"],
        "user_ip_history": ["192.168.1.250"],
        "user_international_history": False
    }
    
    result3 = processor.process_transaction(transaction3)
    print(processor.format_output(result3))
    print("\n")
    
    # Example 4: Batch processing
    print("=" * 80)
    print("EXAMPLE 4: Batch Processing")
    print("=" * 80)
    
    transactions_batch = [transaction1, transaction2, transaction3]
    batch_results = processor.process_transactions_batch(transactions_batch)
    
    # Save results
    processor.save_results(batch_results, "example_results.json")
    
    # Print summary
    print("\nBatch Processing Summary:")
    print(f"Total transactions processed: {len(batch_results)}")
    fraudulent = sum(1 for r in batch_results if r["fraud_status"] == "Fraudulent")
    legitimate = sum(1 for r in batch_results if r["fraud_status"] == "Legitimate")
    print(f"Fraudulent: {fraudulent}")
    print(f"Legitimate: {legitimate}")
    print(f"Average risk score: {sum(r['risk_score'] for r in batch_results) / len(batch_results):.2f}")


if __name__ == "__main__":
    main()
