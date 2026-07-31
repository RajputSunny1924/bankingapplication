import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )

    print("✅ Oracle Connected Successfully")

except Exception as e:
    print("Connection Error:", e)


def create_account(account_no, customer_name, mobile, address, account_type, balance):

    cursor = connection.cursor()

    sql = """
    INSERT INTO ACCOUNT
    (ACCOUNT_NO, CUSTOMER_NAME, MOBILE, ADDRESS, ACCOUNT_TYPE, BALANCE)
    VALUES (:1, :2, :3, :4, :5, :6)
    """

    cursor.execute(sql, (
        account_no,
        customer_name,
        mobile,
        address,
        account_type,
        balance
    ))

    connection.commit()

    cursor.close()

    return True
def deposit_money(account_no, amount):
    cursor = connection.cursor()

    sql = """
    UPDATE ACCOUNT
    SET BALANCE = BALANCE + :1
    WHERE ACCOUNT_NO = :2
    """

    cursor.execute(sql, (amount, account_no))

    cursor.execute("SELECT NVL(MAX(TRANSACTION_ID),0)+1 FROM TRANSACTIONS")
    transaction_id = cursor.fetchone()[0]

    cursor.execute("""
    INSERT INTO TRANSACTIONS
    (TRANSACTION_ID, ACCOUNT_NO, TRANSACTION_TYPE, AMOUNT, TRANSACTION_DATE)
    VALUES (:1, :2, :3, :4, SYSDATE)
    """, (
        transaction_id,
        account_no,
        "Deposit",
        amount
    ))

    connection.commit()
    cursor.close()
def withdraw_money(account_no, amount):
    cursor = connection.cursor()

    sql = """
    UPDATE ACCOUNT
    SET BALANCE = BALANCE - :1
    WHERE ACCOUNT_NO = :2
    """

    cursor.execute(sql, (amount, account_no))

    cursor.execute("SELECT NVL(MAX(TRANSACTION_ID),0)+1 FROM TRANSACTIONS")
    transaction_id = cursor.fetchone()[0]

    cursor.execute("""
    INSERT INTO TRANSACTIONS
    (TRANSACTION_ID, ACCOUNT_NO, TRANSACTION_TYPE, AMOUNT, TRANSACTION_DATE)
    VALUES (:1, :2, :3, :4, SYSDATE)
    """, (
        transaction_id,
        account_no,
        "Withdrawal",
        amount
    ))

    connection.commit()
    cursor.close()

def check_balance(account_no):

    cursor = connection.cursor()

    sql = """
    SELECT BALANCE
    FROM ACCOUNT
    WHERE ACCOUNT_NO = :1
    """

    cursor.execute(sql, (account_no,))

    balance = cursor.fetchone()

    cursor.close()

    return balance


def fund_transfer(from_account, to_account, amount):

    cursor = connection.cursor()

    # Sender ke account se paise minus
    cursor.execute("""
    UPDATE ACCOUNT
    SET BALANCE = BALANCE - :1
    WHERE ACCOUNT_NO = :2
    """, (amount, from_account))

    # Receiver ke account me paise add
    cursor.execute("""
    UPDATE ACCOUNT
    SET BALANCE = BALANCE + :1
    WHERE ACCOUNT_NO = :2
    """, (amount, to_account))

    connection.commit()

    cursor.close()

def apply_loan(account_no, loan_amount):

    cursor = connection.cursor()

    # Generate next loan id
    cursor.execute("SELECT NVL(MAX(LOAN_ID),0)+1 FROM LOAN")
    loan_id = cursor.fetchone()[0]

    sql = """
    INSERT INTO LOAN
    (LOAN_ID, ACCOUNT_NO, LOAN_AMOUNT, INTEREST_RATE, LOAN_STATUS)
    VALUES (:1, :2, :3, :4, :5)
    """

    cursor.execute(sql, (
        loan_id,
        account_no,
        loan_amount,
        8.5,
        "Pending"
    ))

    connection.commit()

    cursor.close()


def mini_statement(account_no):

    cursor = connection.cursor()

    sql = """
    SELECT TRANSACTION_TYPE, AMOUNT, TRANSACTION_DATE
    FROM TRANSACTIONS
    WHERE ACCOUNT_NO = :1
    ORDER BY TRANSACTION_DATE DESC
    """

    cursor.execute(sql, (account_no,))

    data = cursor.fetchall()

    cursor.close()

    return data

def calculate_interest(account_no):
    cursor = connection.cursor()

    sql = """
    SELECT BALANCE
    FROM ACCOUNT
    WHERE ACCOUNT_NO = :1
    """

    cursor.execute(sql, (account_no,))
    balance = cursor.fetchone()

    if balance is None:
        cursor.close()
        return None

    interest = balance[0] * 0.04   # 4% Annual Interest

    cursor.close()

    return {
        "balance": balance[0],
        "interest": interest,
        "total_balance": balance[0] + interest
    }