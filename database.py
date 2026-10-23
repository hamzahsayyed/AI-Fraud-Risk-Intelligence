import sqlite3
import pandas as pd 


def create_table():
    conn = sqlite3.connect("fraud_history.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            amount REAL,
            hour INTEGER,
            card_type TEXT,
            payment_type TEXT,
            device TEXT,
            fraud_risk REAL,
            risk_level TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_transaction(data):
    conn = sqlite3.connect("fraud_history.db")

    conn.execute("""
        INSERT INTO transactions (
            timestamp,
            amount,
            hour,
            card_type,
            payment_type,
            device,
            fraud_risk,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["Timestamp"],
        data["Amount"],
        data["Hour"],
        data["Card Type"],
        data["Payment Type"],
        data["Device"],
        data["Fraud Risk (%)"],
        data["Risk Level"]
    ))

    conn.commit()
    conn.close()
def load_transactions():
    conn = sqlite3.connect("fraud_history.db")

    df = pd.read_sql_query(
        "SELECT timestamp AS Timestamp, amount AS Amount, "
        "hour AS Hour, card_type AS 'Card Type', "
        "payment_type AS 'Payment Type', device AS Device, "
        "fraud_risk AS 'Fraud Risk (%)', "
        "risk_level AS 'Risk Level' "
        "FROM transactions ORDER BY id DESC",
        conn
    )

    conn.close()
    return df