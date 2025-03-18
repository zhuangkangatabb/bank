# Banking API

An internal HTTP API for a fake financial institution, built with Python and FastAPI.

## Objective

This project implements a basic banking API for bank employees, supporting account creation, transfers, balance retrieval, and transfer history. It’s designed for consumption by multiple frontends (web, iOS, Android).

## Features

- **POST /accounts/**: Create a new account with an initial deposit. Supports multiple accounts per customer with readable IDs (e.g., `customer_1_account_1`).
- **POST /transfers/**: Transfer money between any two accounts, including across customers, with validation for funds and positive amounts.
- **GET /accounts/{account_id}/balance**: Retrieve an account’s balance.
- **GET /accounts/{account_id}/transfers**: Retrieve an account’s transfer history.
- **GET /accounts/**: List all accounts (extra feature).

## Design Choices

- **Framework**: Used FastAPI for its simplicity, async support, and built-in Swagger UI, avoiding Django and Litestar as per the task.
- **Storage**: Applied in-memory storage (dict/list in `data.py`) to simplify the demo. This sacrifices persistence across restarts but suits a fake institution’s needs.
- **Encapsulation**: Business logic (e.g., transfers, deletion) is encapsulated in the `Account` class for maintainability and safety.
- **Readable IDs**: Changed from UUIDs to `customer_x_account_y` format for better usability, as requested.
- **Testing**: Comprehensive tests cover all endpoints and edge cases using `pytest`.

## Running the API

1. Install dependencies:
   ```bash
   poetry install

2. Start the API:
   ```bash
   poetry run python -m uvicorn src.banking_api:app --reload

3. Test:
   ```bash
   poetry run pytest .\tests\test_overalll.py