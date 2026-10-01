from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))

db = client["banking_management"]

accounts_collection = db["accounts"]
transactions_collection = db["transactions"]
loans_collection = db["loans"]


# -----------------------------
# CREATE ACCOUNT
# -----------------------------

def create_account(
    account_no,
    customer_name,
    mobile,
    address,
    account_type,
    balance
):
    # Check if account already exists
    existing_account = accounts_collection.find_one({
        "account_no": account_no
    })

    if existing_account:
        raise ValueError("Account Already Exists")

    account = {
        "account_no": account_no,
        "customer_name": customer_name,
        "mobile": mobile,
        "address": address,
        "account_type": account_type,
        "balance": float(balance)
    }

    accounts_collection.insert_one(account)

    return True


# -----------------------------
# DEPOSIT MONEY
# -----------------------------

def deposit_money(account_no, amount):

    if amount <= 0:
        raise ValueError("Invalid Amount")

    account = accounts_collection.find_one({
        "account_no": account_no
    })

    if account is None:
        raise ValueError("Account Not Found")

    # Add money to account
    accounts_collection.update_one(
        {"account_no": account_no},
        {"$inc": {"balance": float(amount)}}
    )

    # Save transaction
    transactions_collection.insert_one({
        "account_no": account_no,
        "transaction_type": "Deposit",
        "amount": float(amount),
        "transaction_date": datetime.now()
    })


# -----------------------------
# WITHDRAW MONEY
# -----------------------------

def withdraw_money(account_no, amount):

    if amount <= 0:
        raise ValueError("Invalid Amount")

    account = accounts_collection.find_one({
        "account_no": account_no
    })

    if account is None:
        raise ValueError("Account Not Found")

    balance = float(account["balance"])

    if balance < amount:
        raise ValueError("Insufficient Balance")

    # Remove money
    accounts_collection.update_one(
        {"account_no": account_no},
        {"$inc": {"balance": -float(amount)}}
    )

    # Save transaction
    transactions_collection.insert_one({
        "account_no": account_no,
        "transaction_type": "Withdrawal",
        "amount": float(amount),
        "transaction_date": datetime.now()
    })


# -----------------------------
# CHECK BALANCE
# -----------------------------

def check_balance(account_no):

    account = accounts_collection.find_one({
        "account_no": account_no
    })

    if account is None:
        return None

    # Return tuple like the old MySQL version
    return (account["balance"],)


# -----------------------------
# FUND TRANSFER
# -----------------------------

def fund_transfer(from_account, to_account, amount):

    if from_account == to_account:
        raise ValueError("Cannot transfer to same account")

    if amount <= 0:
        raise ValueError("Invalid Amount")

    # Check sender
    sender = accounts_collection.find_one({
        "account_no": from_account
    })

    if sender is None:
        raise ValueError("Sender Account Not Found")

    # Check receiver
    receiver = accounts_collection.find_one({
        "account_no": to_account
    })

    if receiver is None:
        raise ValueError("Receiver Account Not Found")

    sender_balance = float(sender["balance"])

    if sender_balance < amount:
        raise ValueError("Insufficient Balance")

    # Remove money from sender
    accounts_collection.update_one(
        {"account_no": from_account},
        {"$inc": {"balance": -float(amount)}}
    )

    # Add money to receiver
    accounts_collection.update_one(
        {"account_no": to_account},
        {"$inc": {"balance": float(amount)}}
    )

    # Sender transaction
    transactions_collection.insert_one({
        "account_no": from_account,
        "transaction_type": "Transfer Sent",
        "amount": float(amount),
        "transaction_date": datetime.now()
    })

    # Receiver transaction
    transactions_collection.insert_one({
        "account_no": to_account,
        "transaction_type": "Transfer Received",
        "amount": float(amount),
        "transaction_date": datetime.now()
    })


# -----------------------------
# APPLY LOAN
# -----------------------------

def apply_loan(account_no, loan_amount):

    account = accounts_collection.find_one({
        "account_no": account_no
    })

    if account is None:
        raise ValueError("Account Not Found")

    if loan_amount <= 0:
        raise ValueError("Invalid Loan Amount")

    loan = {
        "account_no": account_no,
        "loan_amount": float(loan_amount),
        "interest_rate": 8.5,
        "loan_status": "Pending",
        "loan_date": datetime.now()
    }

    loans_collection.insert_one(loan)


# -----------------------------
# MINI STATEMENT
# -----------------------------

def mini_statement(account_no):

    transactions = transactions_collection.find(
        {
            "account_no": account_no
        },
        {
            "_id": 0,
            "transaction_type": 1,
            "amount": 1,
            "transaction_date": 1
        }
    ).sort("transaction_date", -1)

    data = []

    for transaction in transactions:
        data.append((
            transaction.get("transaction_type"),
            transaction.get("amount"),
            transaction.get("transaction_date")
        ))

    return data


# -----------------------------
# CALCULATE INTEREST
# -----------------------------

def calculate_interest(account_no):

    account = accounts_collection.find_one({
        "account_no": account_no
    })

    if account is None:
        return None

    balance = float(account["balance"])

    interest = balance * 0.04

    total_balance = balance + interest

    return {
        "balance": balance,
        "interest": interest,
        "total_balance": total_balance
    }