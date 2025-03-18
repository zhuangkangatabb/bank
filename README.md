### Objective

Your assignment is to build an internal API for a fake financial institution using Python and any framework except Django and Litestar.

### Brief

While modern banks have evolved to serve a plethora of functions, at their core, banks must provide certain basic features. Today, your task is to build the basic HTTP API for one of those banks! Imagine you are designing a backend API for bank employees. It could ultimately be consumed by multiple frontends (web, iOS, Android etc).

### Important
You may not have knowledge in all areas required to achieve this task. Feel free to make simplifications, but add your reasoning to your documentation. Describe which aspects you chose to focus on in your solution.

### Tasks

- Implement assignment using:
  - Language: **Python**
  - Framework: **any framework except Django and Litestar** 
- There should be API routes that allow them to:
  - Create a new bank account for a customer, with an initial deposit amount. A
    single customer may have multiple bank accounts.
  - Transfer amounts between any two accounts, including those owned by
    different customers.
  - Retrieve balances for a given account.
  - Retrieve transfer history for a given account.
- Write tests for your business logic

Feel free to pre-populate your customers with the following:

```json
[
  {
    "id": 1,
    "name": "Arisha Barron"
  },
  {
    "id": 2,
    "name": "Branden Gibson"
  },
  {
    "id": 3,
    "name": "Rhonda Church"
  },
  {
    "id": 4,
    "name": "Georgina Hazel"
  }
]
```

You are expected to design any other required models and routes for your API.

### Evaluation Criteria

- **Python** best practices
- Completeness: did you complete the features?
- Correctness: does the functionality act in sensible, thought-out ways?
- Maintainability: is it written in a clean, maintainable way?
- Testing: Is the system adequately tested?
- Documentation

### CodeSubmit

Please organize, design, test and document your code so that it could be easily reviewed by a colleague - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The Entrix Team


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