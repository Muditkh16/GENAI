
"""services.py

Services that orchestrate workflows and interactions between models and external concerns.
These trigger runtime call sequences suitable for sequence diagrams.
"""

from models import User, Account, Transaction
from typing import Optional, List

class Database:
    """A trivial persistence abstraction (in-memory)"""
    def __init__(self):
        self._store = {'users': {}, 'accounts': {}, 'transactions': {}}

    def save_user(self, user: User) -> None:
        self._store['users'][user.user_id] = user

    def save_account(self, account: Account) -> None:
        self._store['accounts'][account.account_id] = account

    def save_transaction(self, tx: Transaction) -> None:
        self._store['transactions'][tx.tx_id] = tx

    def get_user(self, user_id: int) -> Optional[User]:
        return self._store['users'].get(user_id)

    def __repr__(self):
        return f"Database(users={len(self._store['users'])}, accounts={len(self._store['accounts'])}, transactions={len(self._store['transactions'])})"


class AuthService:
    """Simulated authentication service."""
    def __init__(self, db: Database):
        self.db = db

    def login(self, user_id: int) -> Optional[User]:
        """Return user object if exists (simulates authentication)."""
        user = self.db.get_user(user_id)
        return user


class NotificationService:
    """Simple notification (prints)."""
    def notify(self, user: User, message: str) -> None:
        print(f'[notify] To {user.name}: {message}')


class BankingService:
    """High-level orchestrator that uses models and other services."""
    def __init__(self, db: Database, notifier: NotificationService):
        self.db = db
        self.notifier = notifier
        self._next_tx_id = 1

    def list_accounts(self, user: User) -> List[Account]:
        return user.accounts

    def transfer(self, source_account_id: int, dest_account_id: int, amount: float) -> Transaction:
        """Create and process a transaction between two accounts."""
        source = self.db._store['accounts'].get(source_account_id)
        dest = self.db._store['accounts'].get(dest_account_id)
        tx = Transaction(self._next_tx_id, source, dest, amount)
        self._next_tx_id += 1
        success = tx.process()
        self.db.save_transaction(tx)
        if success:
            self.notifier.notify(source.owner, f'Transfer of {amount} to account {dest.account_id} succeeded.')
            self.notifier.notify(dest.owner, f'Received {amount} from account {source.account_id}.')
        else:
            self.notifier.notify(source.owner, f'Transfer of {amount} failed.')
        return tx

