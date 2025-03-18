from fastapi import HTTPException
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict

# Domain model with encapsulated logic
# Note: The Account class is used to encapsulate account-related business logic (e.g., transfers, deletion)
# and ensure operations are performed safely and consistently. This improves maintainability by
# keeping rules like balance checks in one place, rather than scattered across API endpoints.
class Account:
    def __init__(self, account_id: str, customer_id: int, initial_deposit: float) -> None:
        self._account_id = account_id
        self._customer_id = customer_id
        self._balance = initial_deposit

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def balance(self) -> float:
        return self._balance

    def transfer_to(self, target: 'Account', amount: float) -> Dict[str, str | float]:
        """Transfer money to another account and log the transaction."""
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Transfer amount must be positive")
        if self._balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        self._balance -= amount
        target._balance += amount
        from src.data import transactions  # Import here to avoid circular import
        transaction: Dict[str, str | float] = {  # Explicitly type the dict
            "from_account_id": self.account_id,
            "to_account_id": target.account_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }
        transactions.append(transaction)
        return transaction

# Pydantic model for creating an account
class AccountCreate(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer from data.py")
    initial_deposit: float = Field(..., ge=0, description="Initial deposit amount, must be non-negative")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"customer_id": 1, "initial_deposit": 100.0}
        }
    )

# Pydantic model for transfer requests
class TransferRequest(BaseModel):
    from_account_id: str = Field(..., description="The source account ID")
    to_account_id: str = Field(..., description="The destination account ID")
    amount: float = Field(..., gt=0, description="Amount to transfer, must be positive")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"from_account_id": "customer_1_account_1", "to_account_id": "customer_2_account_1", "amount": 50.0}
        }
    )