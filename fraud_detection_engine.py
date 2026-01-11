"""
AI Fraud Detection Engine for Fintech Company
Analyzes financial transactions and identifies potentially fraudulent activities
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class Transaction:
    """Transaction data model"""
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    transaction_time: str  # ISO format datetime string
    merchant_name: str
    merchant_category: str
    payment_method: str  # UPI, Card, Net Banking, Wallet
    user_location: str
    merchant_location: str
    device_type: str  # mobile/web
    ip_address: str
    transaction_frequency_24h: int
    avg_user_transaction_amount: float
    # Optional fields for context
    user_device_history: Optional[List[str]] = None
    user_location_history: Optional[List[str]] = None
    user_ip_history: Optional[List[str]] = None
    user_international_history: Optional[bool] = None


class FraudDetectionEngine:
    """Main fraud detection engine with risk scoring and pattern analysis"""
    
    def __init__(self):
        # Risk thresholds
        self.HIGH_AMOUNT_MULTIPLIER = 3.0  # 3x average = high risk
        self.MEDIUM_AMOUNT_MULTIPLIER = 2.0  # 2x average = medium risk
        self.HIGH_FREQUENCY_THRESHOLD = 10  # 10+ transactions in 24h = high risk
        self.MEDIUM_FREQUENCY_THRESHOLD = 5  # 5+ transactions in 24h = medium risk
        self.FRAUD_THRESHOLD = 70  # Risk score >= 70 = Fraudulent
        self.REVIEW_THRESHOLD = 40  # Risk score >= 40 = Flag for review
        
    def analyze_transaction(self, transaction: Transaction) -> Dict:
        """
        Main analysis function that processes a transaction and returns fraud assessment
        
        Args:
            transaction: Transaction object with all relevant data
            
        Returns:
            Dictionary with fraud_status, risk_score, risk_factors, reasoning, and recommended_action
        """
        risk_factors = []
        risk_score = 0
        
        # 1. Amount Analysis
        amount_risk, amount_factors = self._analyze_amount(transaction)
        risk_score += amount_risk
        risk_factors.extend(amount_factors)
        
        # 2. Frequency Analysis
        frequency_risk, frequency_factors = self._analyze_frequency(transaction)
        risk_score += frequency_risk
        risk_factors.extend(frequency_factors)
        
        # 3. Location Analysis
        location_risk, location_factors = self._analyze_location(transaction)
        risk_score += location_risk
        risk_factors.extend(location_factors)
        
        # 4. Device Analysis
        device_risk, device_factors = self._analyze_device(transaction)
        risk_score += device_risk
        risk_factors.extend(device_factors)
        
        # 5. IP Address Analysis
        ip_risk, ip_factors = self._analyze_ip(transaction)
        risk_score += ip_risk
        risk_factors.extend(ip_factors)
        
        # 6. Payment Method Analysis
        payment_risk, payment_factors = self._analyze_payment_method(transaction)
        risk_score += payment_risk
        risk_factors.extend(payment_factors)
        
        # 7. Merchant Analysis
        merchant_risk, merchant_factors = self._analyze_merchant(transaction)
        risk_score += merchant_risk
        risk_factors.extend(merchant_factors)
        
        # 8. Time Pattern Analysis
        time_risk, time_factors = self._analyze_time_pattern(transaction)
        risk_score += time_risk
        risk_factors.extend(time_factors)
        
        # Cap risk score at 100
        risk_score = min(100, risk_score)
        
        # Determine fraud status
        fraud_status = "Fraudulent" if risk_score >= self.FRAUD_THRESHOLD else "Legitimate"
        
        # Generate reasoning
        reasoning = self._generate_reasoning(risk_factors, risk_score, transaction)
        
        # Recommend action
        recommended_action = self._recommend_action(risk_score)
        
        return {
            "transaction_id": transaction.transaction_id,
            "fraud_status": fraud_status,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "reasoning": reasoning,
            "recommended_action": recommended_action
        }
    
    def _analyze_amount(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze transaction amount against user's average"""
        risk_score = 0
        factors = []
        
        if transaction.avg_user_transaction_amount > 0:
            ratio = transaction.amount / transaction.avg_user_transaction_amount
            
            if ratio >= self.HIGH_AMOUNT_MULTIPLIER:
                risk_score += 25
                factors.append(f"Amount spike: {ratio:.2f}x user average (${transaction.amount:.2f} vs ${transaction.avg_user_transaction_amount:.2f})")
            elif ratio >= self.MEDIUM_AMOUNT_MULTIPLIER:
                risk_score += 15
                factors.append(f"Above-average amount: {ratio:.2f}x user average")
            elif ratio < 0.1:
                risk_score += 5
                factors.append(f"Unusually small amount: {ratio:.2f}x user average (possible test transaction)")
        else:
            # First transaction or no history
            if transaction.amount > 1000:
                risk_score += 10
                factors.append("High-value first transaction without user history")
        
        return risk_score, factors
    
    def _analyze_frequency(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze transaction frequency in last 24 hours"""
        risk_score = 0
        factors = []
        
        if transaction.transaction_frequency_24h >= self.HIGH_FREQUENCY_THRESHOLD:
            risk_score += 20
            factors.append(f"Abnormal frequency: {transaction.transaction_frequency_24h} transactions in last 24 hours")
        elif transaction.transaction_frequency_24h >= self.MEDIUM_FREQUENCY_THRESHOLD:
            risk_score += 10
            factors.append(f"Elevated frequency: {transaction.transaction_frequency_24h} transactions in last 24 hours")
        elif transaction.transaction_frequency_24h == 0:
            # First transaction in 24h - could be normal or suspicious if combined with other factors
            pass
        
        return risk_score, factors
    
    def _analyze_location(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze location patterns and mismatches"""
        risk_score = 0
        factors = []
        
        # Check if user and merchant locations match
        user_country = self._extract_country(transaction.user_location)
        merchant_country = self._extract_country(transaction.merchant_location)
        
        if user_country and merchant_country:
            if user_country != merchant_country:
                # International transaction
                if transaction.user_international_history is False:
                    risk_score += 30
                    factors.append(f"International transaction without history: {user_country} → {merchant_country}")
                elif transaction.user_international_history is None:
                    risk_score += 20
                    factors.append(f"International transaction: {user_country} → {merchant_country} (no history available)")
                else:
                    risk_score += 5
                    factors.append(f"International transaction: {user_country} → {merchant_country}")
        
        # Check location history
        if transaction.user_location_history:
            if transaction.user_location not in transaction.user_location_history:
                risk_score += 15
                factors.append(f"New location detected: {transaction.user_location}")
        
        return risk_score, factors
    
    def _analyze_device(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze device type and device history"""
        risk_score = 0
        factors = []
        
        if transaction.user_device_history:
            # Check if device is new
            if transaction.device_type not in transaction.user_device_history:
                risk_score += 12
                factors.append(f"New device type detected: {transaction.device_type}")
        else:
            # No device history - first transaction or new user
            risk_score += 3
            factors.append("No device history available")
        
        return risk_score, factors
    
    def _analyze_ip(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze IP address patterns"""
        risk_score = 0
        factors = []
        
        if transaction.user_ip_history:
            if transaction.ip_address not in transaction.user_ip_history:
                risk_score += 10
                factors.append(f"New IP address detected: {transaction.ip_address}")
        else:
            # No IP history
            risk_score += 2
        
        # Check for suspicious IP patterns (simplified - in production, use IP reputation services)
        if self._is_suspicious_ip(transaction.ip_address):
            risk_score += 15
            factors.append(f"Suspicious IP address pattern detected: {transaction.ip_address}")
        
        return risk_score, factors
    
    def _analyze_payment_method(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze payment method for risk patterns"""
        risk_score = 0
        factors = []
        
        # Wallet and UPI are generally lower risk for small amounts
        # Card and Net Banking might have different risk profiles
        payment_method = transaction.payment_method.lower()
        
        if payment_method == "wallet" and transaction.amount > 5000:
            risk_score += 5
            factors.append("High-value wallet transaction")
        elif payment_method == "net banking" and transaction.amount < 100:
            risk_score += 3
            factors.append("Unusually small net banking transaction")
        
        return risk_score, factors
    
    def _analyze_merchant(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze merchant information"""
        risk_score = 0
        factors = []
        
        # Known merchant categories with higher risk
        high_risk_categories = ["gambling", "cryptocurrency", "adult", "cash advance"]
        merchant_category_lower = transaction.merchant_category.lower()
        
        if any(category in merchant_category_lower for category in high_risk_categories):
            risk_score += 10
            factors.append(f"High-risk merchant category: {transaction.merchant_category}")
        
        # If merchant is known and category is normal, reduce risk slightly
        if merchant_category_lower in ["retail", "groceries", "restaurant", "utilities"]:
            risk_score -= 5
            factors.append(f"Known low-risk merchant category: {transaction.merchant_category}")
        
        return max(0, risk_score), factors  # Don't allow negative risk
    
    def _analyze_time_pattern(self, transaction: Transaction) -> Tuple[int, List[str]]:
        """Analyze transaction time patterns"""
        risk_score = 0
        factors = []
        
        try:
            trans_time = datetime.fromisoformat(transaction.transaction_time.replace('Z', '+00:00'))
            hour = trans_time.hour
            
            # Transactions between 2 AM and 5 AM are slightly more suspicious
            if 2 <= hour <= 5:
                risk_score += 5
                factors.append(f"Unusual transaction time: {hour:02d}:00 (off-peak hours)")
        except:
            pass  # If time parsing fails, skip this analysis
        
        return risk_score, factors
    
    def _extract_country(self, location: str) -> Optional[str]:
        """Extract country from location string (simplified)"""
        if not location:
            return None
        
        # Simple extraction - in production, use proper geocoding
        parts = location.split(',')
        if len(parts) > 0:
            return parts[-1].strip()
        return location.strip()
    
    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP address is suspicious (simplified check)"""
        # In production, integrate with IP reputation services
        # For now, check for common patterns
        if not ip_address:
            return False
        
        # Check for private/local IPs used in suspicious contexts
        if ip_address.startswith('192.168.') or ip_address.startswith('10.'):
            return False  # These are usually legitimate
        
        # You could add more sophisticated checks here
        return False
    
    def _generate_reasoning(self, risk_factors: List[str], risk_score: int, transaction: Transaction) -> str:
        """Generate human-readable reasoning for the fraud assessment"""
        if not risk_factors:
            return f"Transaction appears legitimate. Normal transaction pattern for user {transaction.user_id} with amount ${transaction.amount:.2f} via {transaction.payment_method}."
        
        reasoning_parts = [f"Risk assessment for transaction {transaction.transaction_id}:"]
        
        if risk_score >= self.FRAUD_THRESHOLD:
            reasoning_parts.append("HIGH RISK - Multiple suspicious indicators detected:")
        elif risk_score >= self.REVIEW_THRESHOLD:
            reasoning_parts.append("MEDIUM RISK - Some unusual patterns detected:")
        else:
            reasoning_parts.append("LOW RISK - Minor anomalies detected:")
        
        for i, factor in enumerate(risk_factors, 1):
            reasoning_parts.append(f"{i}. {factor}")
        
        reasoning_parts.append(f"\nOverall risk score: {risk_score}/100")
        
        return "\n".join(reasoning_parts)
    
    def _recommend_action(self, risk_score: int) -> str:
        """Recommend action based on risk score"""
        if risk_score >= self.FRAUD_THRESHOLD:
            return "Block transaction immediately"
        elif risk_score >= self.REVIEW_THRESHOLD:
            return "Flag for review"
        else:
            return "Allow transaction"
