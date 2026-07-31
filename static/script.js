// =========================
// BANK ACCOUNT OBJECT
// =========================

let account = null;

// =========================
// OPEN ACCOUNT
// =========================
document
  .getElementById("accountForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const account = {
      account_no: Math.floor(Math.random() * 9000) + 1000,
      customer_name: document.getElementById("customerName").value,
      mobile: document.getElementById("mobile").value,
      address: document.getElementById("address").value,
      account_type: document.getElementById("accountType").value,
      balance: Number(document.getElementById("openingBalance").value),
    };

    const response = await fetch("http://127.0.0.1:5000/create_account", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(account),
    });

    const result = await response.json();

    alert(result.message);
  });
// =========================
// DEPOSIT
// =========================

async function deposit() {
  const account = document.getElementById("depositAccount").value;
  const amount = document.getElementById("depositAmount").value;

  const response = await fetch("/deposit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      account_no: Number(account),
      amount: Number(amount),
    }),
  });

  const result = await response.json();

  alert(result.message);
}

// =========================
// WITHDRAW
// =========================

async function withdraw() {
  const account = document.getElementById("withdrawAccount").value;
  const amount = document.getElementById("withdrawAmount").value;

  const response = await fetch("/withdraw", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      account_no: Number(account),
      amount: Number(amount),
    }),
  });

  const result = await response.json();

  alert(result.message);
}

// =========================
// BALANCE
// =========================
async function checkBalance() {
  const account = document.getElementById("balanceAccount").value;

  const response = await fetch("/balance", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      account_no: Number(account),
    }),
  });

  const result = await response.json();

  alert("Current Balance : ₹" + result.balance);
}
// =========================
// transfer money
// =========================
async function transferMoney() {
  const from = document.getElementById("fromAccount").value;
  const to = document.getElementById("toAccount").value;
  const amount = document.getElementById("transferAmount").value;

  const response = await fetch("/transfer", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      from_account: Number(from),
      to_account: Number(to),
      amount: Number(amount),
    }),
  });

  const result = await response.json();

  alert(result.message);
}

// =========================
// loan
// =========================

async function applyLoan() {
  const account = document.getElementById("loanAccount").value;

  const amount = document.getElementById("loanAmount").value;

  const response = await fetch("/loan", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      account_no: Number(account),
      loan_amount: Number(amount),
    }),
  });

  const result = await response.json();

  alert(result.message);
}
// =========================
// MINI STATEMENT
// =========================
async function showStatement() {
  const account = document.getElementById("statementAccount").value;

  const response = await fetch("/statement", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      account_no: Number(account),
    }),
  });

  const data = await response.json();

  let output = "";

  if (data.length === 0) {
    output = "<p>No transactions found.</p>";
  } else {
    data.forEach((item) => {
      output += `
                <p>
                    <strong>${item[0]}</strong> |
                    ₹${item[1]} |
                    ${item[2]}
                </p>
            `;
    });
  }

  document.getElementById("statement").innerHTML = output;
}

// =========================
// calculate interest
// =========================

async function calculateInterest() {
  const account = document.getElementById("interestAccount").value;

  const response = await fetch("/interest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      account_no: Number(account),
    }),
  });

  const data = await response.json();

  if (data.message) {
    alert(data.message);
    return;
  }

  document.getElementById("interestResult").innerHTML = `
    <p><b>Current Balance:</b> ₹${data.balance}</p>
    <p><b>Interest (4%):</b> ₹${data.interest}</p>
    <p><b>Total Balance:</b> ₹${data.total_balance}</p>
  `;
}
