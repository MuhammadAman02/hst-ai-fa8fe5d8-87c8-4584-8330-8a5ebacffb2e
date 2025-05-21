import re
from app.models.transaction import Transaction

class FraudDetectionService:
    def __init__(self):
        self.irish_mobile_pattern = re.compile(r'^(\+353|0)8[35679]\d{7}$')
        self.suspicious_keywords = ['quick transfer', 'urgent payment', 'gift card', 'lottery winnings']

    def detect_fraud(self, transaction: Transaction) -> dict:
        risk_score = 0
        risk_factors = []

        # Check for high-value transactions
        if transaction.amount > 10000:
            risk_score += 20
            risk_factors.append("High-value transaction")

        # Check for transactions outside normal hours (assuming Irish business hours)
        if transaction.timestamp.hour < 9 or transaction.timestamp.hour > 18:
            risk_score += 10
            risk_factors.append("Transaction outside normal business hours")

        # Check for suspicious keywords in the description
        if transaction.description:
            if any(keyword in transaction.description.lower() for keyword in self.suspicious_keywords):
                risk_score += 15
                risk_factors.append("Suspicious keywords in description")

        # Check for non-Irish IP addresses (simplified check, assumes Irish IPs start with 87.)
        if transaction.ip_address and not transaction.ip_address.startswith('87.'):
            risk_score += 10
            risk_factors.append("Non-Irish IP address")

        # Check for potential money mule activity (multiple small transactions to different accounts)
        # This would require tracking previous transactions, which is beyond the scope of this example
        # But we'll add a placeholder check
        if transaction.amount < 1000 and len(set(transaction.recipient)) > 5:
            risk_score += 25
            risk_factors.append("Potential money mule activity")

        # Classify the risk level
        risk_level = "Low" if risk_score < 20 else "Medium" if risk_score < 50 else "High"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors
        }