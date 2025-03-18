from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import AccountCreate, TransferRequest, Account
from .data import customers, accounts, get_all_accounts, get_account_transactions  # Add new import

app = FastAPI(
    title="Banking API",
    description="An in-memory API with encapsulated account management.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def customer_exists(customer_id: int) -> bool:
    return any(c["id"] == customer_id for c in customers)

def get_account(account_id: str) -> Account:
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]

@app.post("/accounts/", response_model=dict)
def create_account(account: AccountCreate):
    """Create a new bank account for a customer."""
    if not customer_exists(account.customer_id):
        raise HTTPException(status_code=400, detail="Customer not found")
    if account.initial_deposit < 0:
        raise HTTPException(status_code=400, detail="Initial deposit cannot be negative")
    
    existing_accounts = sum(1 for a in accounts.values() if a.customer_id == account.customer_id)
    sequence_number = existing_accounts + 1
    account_id = f"customer_{account.customer_id}_account_{sequence_number}"
    
    new_account = Account(account_id, account.customer_id, account.initial_deposit)
    accounts[account_id] = new_account
    return {"account_id": account_id, "customer_id": account.customer_id, "balance": account.initial_deposit}

@app.get("/accounts/", response_model=List[dict])
def list_all_accounts():
    """Retrieve information for all accounts."""
    accounts_list = get_all_accounts()  # Calls the function from data.py
    return [
        {
            "account_id": account.account_id,
            "customer_id": account.customer_id,
            "balance": account.balance
        }
        for account in accounts_list
    ]

@app.post("/transfers/", response_model=dict)
def transfer_amount(transfer: TransferRequest):
    """Transfer money between two accounts."""
    source = get_account(transfer.from_account_id)
    target = get_account(transfer.to_account_id)
    return source.transfer_to(target, transfer.amount)

@app.get("/accounts/{account_id}/balance", response_model=dict)
def get_balance(account_id: str):
    """Retrieve the current balance of an account."""
    account = get_account(account_id)
    return {"account_id": account_id, "balance": account.balance}

@app.get("/accounts/{account_id}/transfers", response_model=List[dict])
def get_transfer_history(account_id: str):
    """Retrieve the transfer history for an account."""
    get_account(account_id)  # Verify account exists
    return get_account_transactions(account_id)  # Use the new function
