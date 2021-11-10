# this is a dummy file usd as an intro to pytest

from app.calculation import InsufficientFunds, add, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account_with_balance():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, value", [
    (3, 5, 8),
    (5, 5, 10),
    (20, 25, 45),
    (20, 20, 40),
    (17, 15, 32),
    (52, -17, 35)
])
def test_add(num1, num2, value):
    assert add(num1, num2) == value

class TestBankAccount():
    def test_create_account_with_default_balance(self, zero_bank_account):
        assert zero_bank_account.balance == 0

    def test_create_account(self, bank_account_with_balance):
        assert bank_account_with_balance.balance == 50

    @pytest.mark.parametrize('deposit, expected', [(50, 100), (100, 150), (200, 250)])
    def test_deposit(self, bank_account_with_balance, deposit, expected):
        bank_account_with_balance.deposit(deposit)
        assert bank_account_with_balance.balance == expected

    def test_withdraw(self, bank_account_with_balance):
        bank_account_with_balance.withdraw(40)
        assert bank_account_with_balance.balance == 10

    def test_invalid_withdraw(self, zero_bank_account):
        with pytest.raises(InsufficientFunds):
            zero_bank_account.withdraw(200)
        

    def collect_interest(self, bank_account_with_balance):
        bank_account_with_balance.collect_interest()
        assert bank_account_with_balance.balance == 55