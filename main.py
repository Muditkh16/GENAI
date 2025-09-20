
"""main.py

Example run script that exercises services and models to produce a clear runtime call sequence.
Run this to simulate a user login, list accounts, and perform a fund transfer.
"""

from models import User, Account
from services import Database, AuthService, NotificationService, BankingService

def seed_data(db: Database):
    """Seed sample users and accounts into the in-memory DB."""
    alice = User(1, 'Alice')
    bob = User(2, 'Bob')

    a1 = Account(101, alice, balance=500.0)
    a2 = Account(102, alice, balance=150.0)
    b1 = Account(201, bob, balance=300.0)

    db.save_user(alice)
    db.save_user(bob)
    db.save_account(a1)
    db.save_account(a2)
    db.save_account(b1)

    return alice, bob, a1, a2, b1

def main():
    db = Database()
    alice, bob, a1, a2, b1 = seed_data(db)

    auth = AuthService(db)
    notifier = NotificationService()
    bank = BankingService(db, notifier)

    # Simulate user flow:
    # 1) Alice logs in
    user = auth.login(1)
    print('User logged in ->', user)

    # 2) List accounts (service call)
    accounts = bank.list_accounts(user)
    print('Accounts for', user.name, '->', accounts)

    # 3) Alice transfers from a1 -> b1
    tx = bank.transfer(101, 201, 120.0)
    print('Transaction result ->', tx)

    # 4) Another transfer that will fail due to insufficient funds
    tx2 = bank.transfer(102, 201, 500.0)
    print('Transaction result ->', tx2)

if __name__ == '__main__':
    main()
