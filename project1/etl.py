import logging

import pandas as pd
import psycopg2

from quires import *
from settings import *

logger = logging.getLogger(__name__)


def extract_info_from_date(date):
    year = date.year
    quarter = date.quarter
    season = ""
    month = date.month
    month_name = date.month_name()
    day = date.day
    day_name = date.day_name()
    hour = date.hour
    am_or_pm = "AM" if hour < 12 else "PM"
    if (month == 12 and day >= 21) or (month <= 3 and day < 21):
        season = "Winter"
    elif (month == 3 and day >= 21) or (month <= 6 and day < 21):
        season = "Spring"
    elif (month == 6 and day >= 21) or (month <= 9 and day < 21):
        season = "Summer"
    elif (month == 9 and day >= 21) or (month <= 12 and day < 21):
        season = "Fall"
    return (
        date,
        year,
        quarter,
        season,
        month,
        month_name,
        day,
        day_name,
        hour,
        am_or_pm,
    )


def main():
    conn = psycopg2.connect(
        f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    logger.info("Start ETL process")

    # ETL user
    user_df = pd.read_csv("ecommerce_dataset/user_dataset.csv")
    user_df.dropna(subset=["user_name"], inplace=True)
    user_df["customer_zip_code"] = user_df["customer_zip_code"].astype(str)

    data_to_insert = [
        (
            row["user_name"],
            row["customer_zip_code"],
            row["customer_city"],
            row["customer_state"],
        )
        for index, row in user_df.iterrows()
    ]

    cur.executemany(
        dim_customer_table_insert,
        data_to_insert,
    )

    # ETL date
    order_df = pd.read_csv("ecommerce_dataset/order_dataset.csv")
    dates_df = order_df[
        [
            "order_date",
            "order_approved_date",
            "pickup_date",
            "delivered_date",
            "estimated_time_delivery",
        ]
    ]
    for col in dates_df.columns:
        dates_df[col] = pd.to_datetime(dates_df[col])

    date_data_to_insert = []
    for index, row in dates_df.iterrows():
        for col in dates_df.columns:
            date_data_to_insert.append((row[col], *extract_info_from_date(row[col])))

    cur.executemany(
        dim_date_table_insert,
        date_data_to_insert,
    )

    # ETL payment
    payment_df = pd.read_csv("ecommerce_dataset/payment_dataset.csv")
    payment_df.dropna(subset=["order_id"], inplace=True)
    payment_df["payment_type"] = payment_df["payment_type"].astype(str)
    payment_df["payment_sequential"] = payment_df["payment_sequential"].astype(int)
    payment_df["payment_installments"] = payment_df["payment_installments"].astype(int)
    payment_df["payment_value"] = payment_df["payment_value"].astype(float)

    payment_data_to_insert = [
        (
            row["order_id"],
            row["payment_sequential"],
            row["payment_type"],
            row["payment_installments"],
            row["payment_value"],
        )
        for index, row in payment_df.iterrows()
    ]

    cur.executemany(
        dim_payment_table_insert,
        payment_data_to_insert,
    )

    # ETL feedback
    feedback_df = pd.read_csv("ecommerce_dataset/feedback_dataset.csv")
    feedback_df.dropna(subset=["order_id"], inplace=True)
    feedback_df["feedback_score"] = feedback_df["feedback_score"].astype(int)
    feedback_df["feedback_answer_date"] = pd.to_datetime(
        feedback_df["feedback_answer_date"]
    )
    feedback_df["feedback_form_sent_date"] = pd.to_datetime(
        feedback_df["feedback_form_sent_date"]
    )
    # Drop duplicated feedback and keep only the latest feedback
    feedback_df.sort_values(by="feedback_answer_date", inplace=True)
    feedback_df.drop_duplicates(subset=["feedback_id"], keep="last", inplace=True)

    feedback_data_to_insert = [
        (
            row["feedback_id"],
            row["feedback_score"],
            row["feedback_form_sent_date"],
            row["feedback_answer_date"],
        )
        for index, row in feedback_df.iterrows()
    ]

    cur.executemany(
        dim_feedback_table_insert,
        feedback_data_to_insert,
    )

    # ETL order
    order_df.dropna(subset=["order_id"], inplace=True)
    order_df["order_status"] = order_df["order_status"].astype(str)

    order_data_to_insert = []
    for index, row in order_df.iterrows():
        cur.execute(select_feedback_by_id, (row["feedback_id"],))
        feedback_id = cur.fetchone()[0]
        cur.execute(select_customer_by_id, (row["customer_id"],))
        customer_id = cur.fetchone()[0]
        cur.execute(select_payment_by_id, (row["order_id"],))
        payment_id = cur.fetchone()[0]
        order_data_to_insert.append(
            (
                row["order_id"],
                customer_id,
                row["order_status"],
                payment_id,
                feedback_id,
                row["order_date"],
                row["order_approved_date"],
                row["pickup_date"],
                row["delivered_date"],
                row["estimated_time_delivery"],
            )
        )

    cur.executemany(
        fact_order_table_insert,
        order_data_to_insert,
    )

    conn.commit()
    conn.close()
    logger.info("Finished ETL process successfully")


if __name__ == "__main__":
    main()
