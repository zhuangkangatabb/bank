import pytest
from fastapi.testclient import TestClient
from src.banking_api import app
from src.data import accounts, transactions


@pytest.fixture
def pytest_client():
    # Clear in-memory storage before each test
    accounts.clear()
    transactions.clear()
    return TestClient(app)


def test_customer_exists():
    from src.banking_api import customer_exists

    assert customer_exists(1) is True
    assert customer_exists(5) is False


def test_create_account_success(pytest_client):
    response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 100.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 1
    assert data["balance"] == 100.0
    assert data["account_id"] == "customer_1_account_1"


def test_create_account_invalid_customer(pytest_client):
    response = pytest_client.post(
        "/accounts/", json={"customer_id": 5, "initial_deposit": 100.0}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Customer not found"


def test_create_account_negative_deposit(pytest_client):
    response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": -50.0}
    )
    assert response.status_code == 422
    assert "initial_deposit" in response.json()["detail"][0]["loc"]


def test_create_multiple_accounts_same_customer(pytest_client):
    response1 = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 100.0}
    )
    response2 = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 200.0}
    )
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["account_id"] == "customer_1_account_1"
    assert response2.json()["account_id"] == "customer_1_account_2"

def test_transfer_amount_success(pytest_client):
    acc1_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 200.0}
    )
    acc2_response = pytest_client.post(
        "/accounts/", json={"customer_id": 2, "initial_deposit": 50.0}
    )
    acc1 = acc1_response.json()
    acc2 = acc2_response.json()

    response = pytest_client.post(
        "/transfers/",
        json={
            "from_account_id": acc1["account_id"],
            "to_account_id": acc2["account_id"],
            "amount": 100.0,
        },
    )
    assert response.status_code == 200
    assert accounts[acc1["account_id"]].balance == 100.0
    assert accounts[acc2["account_id"]].balance == 150.0
    assert len(transactions) == 1


def test_transfer_amount_insufficient_funds(pytest_client):
    acc1_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 50.0}
    )
    acc2_response = pytest_client.post(
        "/accounts/", json={"customer_id": 2, "initial_deposit": 50.0}
    )
    acc1 = acc1_response.json()
    acc2 = acc2_response.json()

    response = pytest_client.post(
        "/transfers/",
        json={
            "from_account_id": acc1["account_id"],
            "to_account_id": acc2["account_id"],
            "amount": 100.0,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"


def test_transfer_amount_invalid_account(pytest_client):
    acc1_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 200.0}
    )
    acc1 = acc1_response.json()

    response = pytest_client.post(
        "/transfers/",
        json={
            "from_account_id": acc1["account_id"],
            "to_account_id": "customer_999_account_1",
            "amount": 50.0,
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"


def test_get_balance_success(pytest_client):
    acc_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 300.0}
    )
    acc = acc_response.json()

    response = pytest_client.get(f"/accounts/{acc['account_id']}/balance")
    assert response.status_code == 200
    assert response.json()["balance"] == 300.0


def test_get_balance_invalid_account(pytest_client):
    response = pytest_client.get("/accounts/customer_999_account_1/balance")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"


def test_get_transfer_history_success(pytest_client):
    acc1_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 200.0}
    )
    acc2_response = pytest_client.post(
        "/accounts/", json={"customer_id": 2, "initial_deposit": 50.0}
    )
    acc1 = acc1_response.json()
    acc2 = acc2_response.json()

    pytest_client.post(
        "/transfers/",
        json={
            "from_account_id": acc1["account_id"],
            "to_account_id": acc2["account_id"],
            "amount": 100.0,
        },
    )

    response = pytest_client.get(f"/accounts/{acc1['account_id']}/transfers")
    assert response.status_code == 200
    transfers = response.json()
    assert len(transfers) == 1
    assert transfers[0]["amount"] == 100.0


def test_get_transfer_history_no_transfers(pytest_client):
    acc_response = pytest_client.post(
        "/accounts/", json={"customer_id": 1, "initial_deposit": 100.0}
    )
    acc = acc_response.json()

    response = pytest_client.get(f"/accounts/{acc['account_id']}/transfers")
    assert response.status_code == 200
    assert len(response.json()) == 0
