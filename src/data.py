# src/data.py
# Pre-populated customers and in-memory storage for accounts and transactions

from typing import List, Dict
from .models import Account  # Import Account explicitly

# Pre-populated list of customers
customers: List[Dict[str, int | str]] = [
    {"id": 1, "name": "Arisha Barron"},
    {"id": 2, "name": "Branden Gibson"},
    {"id": 3, "name": "Rhonda Church"},
    {"id": 4, "name": "Georgina Hazel"},
]

# In-memory storage for accounts
# Format: {account_id: Account instance}
# Note: Using a dict instead of a database since this is a fake bank for demo purpose.
# In a real-world case, accounts would be stored in a persistent database (e.g., PostgreSQL)
# with proper indexing and security measures.
accounts: Dict[str, Account] = {}

# In-memory storage for transactions
# Format: [{"from_account_id": str, "to_account_id": str, "amount": float, "timestamp": str}, ...]
# Note: Storing transactions in a list instead of a database for simplicity.
# In a real-world scenario, this would be a database table with foreign keys to accounts.
transactions: List[Dict[str, str | float]] = []

def get_all_accounts() -> List[Account]:
    """Retrieve all accounts from in-memory storage.
        
        Note: This function is not strictly necessary for the core banking API requirements.
        Added for convenience during development and testing to quickly inspect all accounts.
    """
    return list(accounts.values())

def get_account_transactions(account_id: str) -> List[Dict[str, str | float]]:
    """Retrieve transfer history for a given account."""
    return [
        t for t in transactions
        if t["from_account_id"] == account_id or t["to_account_id"] == account_id
    ]