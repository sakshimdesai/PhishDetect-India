import os
import sqlite3
import json


# ---------------------------------------------------------
# Database path
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DATABASE_PATH = os.path.join(
    PROJECT_ROOT,
    "database",
    "phishdetect.db"
)


# ---------------------------------------------------------
# Initialize database
# ---------------------------------------------------------

def initialize_database():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            input_type TEXT NOT NULL,

            input TEXT NOT NULL,

            prediction TEXT NOT NULL,

            confidence REAL NOT NULL,

            reasons TEXT
        )
        """
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# Save prediction
# ---------------------------------------------------------

def save_prediction(
    input_type,
    input_text,
    prediction,
    confidence,
    reasons
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            input_type,
            input,
            prediction,
            confidence,
            reasons
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            input_type,
            input_text,
            prediction,
            confidence,
            reasons
        )
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# Get prediction history
# ---------------------------------------------------------

def get_prediction_history(limit=50):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            input_type,
            input,
            prediction,
            confidence,
            reasons
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "input_type": row["input_type"],
            "input": row["input"],
            "prediction": row["prediction"],
            "confidence": row["confidence"],
            "reasons": json.loads(row["reasons"])
            if row["reasons"]
            else []
        })

    return history