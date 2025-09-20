
"""models.py

Example domain model classes that show relationships suitable for class diagrams:
  - User has Accounts (association)
  - Account uses Transactions (composition)
  - Transaction refers to two Accounts (association)
"""

from typing import List, Dict

class User:
    """Represents a user in the system."""
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.accounts: List['Account'] = []

    def add_account(self, account: 'Account') -> None:
        """Associate an Account with this User."""
        self.accounts.append(account)

    def get_profile(self) -> Dict[str, str]:
        """Return a simple profile summary."""
        return {'user_id': str(self.user_id), 'name': self.name, 'accounts': str(len(self.accounts))}

    def __repr__(self):
        return f"User(id={self.user_id}, name='{self.name}')"


class Account:
    """Bank account with basic operations."""
    def __init__(self, account_id: int, owner: User, balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = float(balance)
        self.owner.add_account(self)
        self._transactions: List['Transaction'] = []

    def deposit(self, amount: float) -> None:
        """Deposit amount to the account."""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw amount from the account."""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.balance -= amount

    def add_transaction(self, tx: 'Transaction') -> None:
        self._transactions.append(tx)

    def get_balance(self) -> float:
        return self.balance

    def __repr__(self):
        return f"Account(id={self.account_id}, owner={self.owner.name}, balance={self.balance})"


class Transaction:
    """Represents a transfer between two accounts."""
    STATUS_PENDING = 'PENDING'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_FAILED = 'FAILED'

    def __init__(self, tx_id: int, source: Account, destination: Account, amount: float):
        self.tx_id = tx_id
        self.source = source
        self.destination = destination
        self.amount = float(amount)
        self.status = self.STATUS_PENDING

    def validate(self) -> bool:
        """Basic validation: amount >0 and source has funds."""
        return self.amount > 0 and self.source.get_balance() >= self.amount

    def process(self) -> bool:
        """Process the transaction: withdraw from source and deposit to destination."""
        if not self.validate():
            self.status = self.STATUS_FAILED
            return False
        try:
            self.source.withdraw(self.amount)
            self.destination.deposit(self.amount)
            self.source.add_transaction(self)
            self.destination.add_transaction(self)
            self.status = self.STATUS_COMPLETED
            return True
        except Exception as exc:
            self.status = self.STATUS_FAILED
            return False

    def __repr__(self):
        return f"Transaction(id={self.tx_id}, from={self.source.account_id}, to={self.destination.account_id}, amount={self.amount}, status={self.status})"

