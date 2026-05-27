import pytest
import asyncio
from decimal import Decimal
from uuid import uuid4


async def test_create_wallet(ac):
    response = await ac.post("/api/v1/wallets", json={})
    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert Decimal(data["balance"]) == Decimal(0)


async def test_get_wallet_balance(ac, wallet_uuid):
    response = await ac.get(f"/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 200
    assert Decimal(response.json()["balance"]) == Decimal(0)

    response = await ac.get(f"/api/v1/wallets/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "amount, balance, operation_type, status_code",
    [
        (1000, 1000, "DEPOSIT", 200),
        (500, 1500, "DEPOSIT", 200),
        (250, 1250, "WITHDRAW", 200),
        (1250, 0, "WITHDRAW", 200),
        (2000, 1500, "WITHDRAW", 409),
        (9999999999999999999999999, 1500, "DEPOSIT", 422),
        (-5, 1500, "DEPOSIT", 422),
        (250, 1500, "fakeOper", 422),
    ],
)
async def test_operation_wallet(
    amount, balance, operation_type, status_code, ac, wallet_uuid
):
    response = await ac.put(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": operation_type,
            "amount": amount,
        },
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    data = response.json()
    assert Decimal(data["balance"]) == Decimal(balance)


async def test_operation_wallet_not_found_wallet(ac):
    fake_uuid = uuid4()
    response = await ac.put(
        f"/api/v1/wallets/{fake_uuid}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 100,
        },
    )
    assert response.status_code == 404


async def _make_withdraw(ac, wallet_uuid):
    return await ac.put(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": 100,
        },
    )


async def test_concurrent_withdraw(ac, wallet_uuid):
    await ac.put(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 1000,
        },
    )
    responses = await asyncio.gather(
        *[_make_withdraw(ac, wallet_uuid) for _ in range(10)]
    )
    success_count = sum(response.status_code == 200 for response in responses)

    assert success_count == 10
    balance_response = await ac.get(f"/api/v1/wallets/{wallet_uuid}")

    assert balance_response.status_code == 200
    assert Decimal(balance_response.json()["balance"]) == Decimal(0)


async def test_concurrent_overwithdraw(ac, wallet_uuid):
    await ac.put(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 1000,
        },
    )
    responses = await asyncio.gather(
        *[_make_withdraw(ac, wallet_uuid) for _ in range(20)]
    )
    success_count = sum(response.status_code == 200 for response in responses)
    failed_count = sum(response.status_code == 409 for response in responses)

    assert success_count == 10
    assert failed_count == 10

    balance_response = await ac.get(f"/api/v1/wallets/{wallet_uuid}")
    assert balance_response.status_code == 200
    assert Decimal(balance_response.json()["balance"]) == Decimal(0)
