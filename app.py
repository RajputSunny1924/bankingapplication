from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import (
    create_account, 
    deposit_money,
    withdraw_money,
    check_balance,
    fund_transfer,
    apply_loan,
    mini_statement,
    calculate_interest,
)

app = Flask(__name__)
CORS(app)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_account", methods=["POST"])
def create():

    data = request.get_json()

    create_account(
        data["account_no"],
        data["customer_name"],
        data["mobile"],
        data["address"],
        data["account_type"],
        data["balance"]
    )

    return jsonify({"message": "Account Created Successfully"})

@app.route("/deposit", methods=["POST"])
def deposit():

    data = request.get_json()

    deposit_money(
        data["account_no"],
        data["amount"]
    )

    return jsonify({"message": "Money Deposited Successfully"})

@app.route("/withdraw", methods=["POST"])
def withdraw():

    data = request.get_json()

    withdraw_money(
        data["account_no"],
        data["amount"]
    )

    return jsonify({"message": "Money Withdrawn Successfully"})

@app.route("/balance", methods=["POST"])
def balance():

    data = request.get_json()

    balance = check_balance(data["account_no"])

    return jsonify({
        "balance": balance[0]
    })

@app.route("/transfer", methods=["POST"])
def transfer():

    data = request.get_json()

    fund_transfer(
        data["from_account"],
        data["to_account"],
        data["amount"]
    )

    return jsonify({"message": "Money Transferred Successfully"})

@app.route("/loan", methods=["POST"])
def loan():

    data = request.get_json()

    apply_loan(
        data["account_no"],
        data["loan_amount"]
    )

    return jsonify({"message": "Loan Applied Successfully"})

@app.route("/statement", methods=["POST"])
def statement():

    data = request.get_json()

    records = mini_statement(data["account_no"])

    return jsonify(records)

@app.route("/interest", methods=["POST"])
def interest():
    data = request.get_json()

    result = calculate_interest(data["account_no"])

    if result is None:
        return jsonify({"message": "Account Not Found"}), 404

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

