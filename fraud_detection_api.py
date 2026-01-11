"""
Simple API interface for Fraud Detection Engine
Can be used as a standalone script or imported as a module
"""

import json
import sys
from transaction_processor import TransactionProcessor


def analyze_single_transaction(transaction_json: str) -> str:
    """
    Analyze a single transaction from JSON string
    
    Args:
        transaction_json: JSON string containing transaction data
        
    Returns:
        JSON string with fraud detection results
    """
    processor = TransactionProcessor()
    
    try:
        transaction_data = json.loads(transaction_json)
        result = processor.process_transaction(transaction_data)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({
            "error": "Invalid JSON format",
            "details": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Processing error",
            "details": str(e)
        }, indent=2)


def analyze_from_file(input_file: str, output_file: str = None):
    """
    Analyze transactions from a JSON file
    
    Args:
        input_file: Path to input JSON file (single transaction or array)
        output_file: Optional path to save results
    """
    processor = TransactionProcessor()
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Handle both single transaction and array of transactions
        if isinstance(data, list):
            results = processor.process_transactions_batch(data)
        else:
            results = [processor.process_transaction(data)]
        
        # Print results
        for result in results:
            print(processor.format_output(result))
            print("\n" + "="*80 + "\n")
        
        # Save to file if specified
        if output_file:
            processor.save_results(results, output_file)
        
        return results
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fraud_detection_api.py <input_file.json> [output_file.json]")
        print("\nExample:")
        print("  python fraud_detection_api.py transactions.json results.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyze_from_file(input_file, output_file)


if __name__ == "__main__":
    main()
