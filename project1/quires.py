fact_order_table_drop = "DROP TABLE IF EXISTS fact_order"
dim_customers_table_drop = "DROP TABLE IF EXISTS dim_customer"
dim_date_table_drop = "DROP TABLE IF EXISTS dim_date"
dim_payment_table_drop = "DROP TABLE IF EXISTS dim_payment"
dim_feedback_table_drop = "DROP TABLE IF EXISTS dim_feedback"

dim_customer_table = """
CREATE TABLE IF NOT EXISTS dim_customer(
    id SERIAL PRIMARY KEY,
    user_name VARCHAR UNIQUE NOT NULL,
    customer_zip_code VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR)
    """

dim_date_table = """
CREATE TABLE IF NOT EXISTS dim_date(
    id SERIAL PRIMARY KEY,
    date TIMESTAMP UNIQUE NOT NULL,
    year INT NOT NULL CHECK (year > 0),
    quarter INT NOT NULL CHECK (quarter > 0),
    season VARCHAR NOT NULL,
    month INT NOT NULL CHECK (month > 0),
    month_name VARCHAR NOT NULL,
    day INT NOT NULL CHECK (day > 0),
    day_name  VARCHAR NOT NULL,
    hour INT NOT NULL CHECK (hour >= 0),
    am_or_pm VARCHAR
)
"""
dim_payment_table = """
CREATE TABLE IF NOT EXISTS dim_payment(
    id SERIAL PRIMARY KEY,
    payment_id VARCHAR UNIQUE NOT NULL,
    payment_sequential INT,
    payment_type VARCHAR,
    payment_installments INT NOT NULL CHECK (payment_installments > 0),
    payment_value FLOAT NOT NULL CHECK (payment_value > 0)
)
"""

dim_feedback_table = """
CREATE TABLE IF NOT EXISTS dim_feedback(
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR NOT NULL,
    order_id VARCHAR NOT NULL,
    feedback_score FLOAT,
    feedback_form_sent_date TIMESTAMP,
    feedback_answer_date TIMESTAMP,
    UNIQUE(feedback_id, order_id)
)
"""
fact_order_table = """
CREATE TABLE IF NOT EXISTS fact_order(
    id SERIAL PRIMARY KEY,
    order_id VARCHAR UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    order_status VARCHAR NOT NULL,
    payment_id INTEGER NOT NULL,
    feedback_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL,
    order_approved_date TIMESTAMP NOT NULL,
    pickup_date TIMESTAMP NOT NULL,
    delivered_date TIMESTAMP NOT NULL,
    estimated_time_delivery TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(id),
    FOREIGN KEY (order_date) REFERENCES dim_date(date),
    FOREIGN KEY (order_approved_date) REFERENCES dim_date(date),
    FOREIGN KEY (pickup_date) REFERENCES dim_date(date),
    FOREIGN KEY (delivered_date) REFERENCES dim_date(date),
    FOREIGN KEY (estimated_time_delivery) REFERENCES dim_date(date),
    FOREIGN KEY (payment_id) REFERENCES dim_payment(id),
    FOREIGN KEY (feedback_id) REFERENCES dim_feedback(id)
)
"""

fact_order_table_insert = """
INSERT INTO fact_order(
    order_id,
    customer_id,
    order_status,
    payment_id,
    feedback_id,
    order_date,
    order_approved_date,
    pickup_date,
    delivered_date,
    estimated_time_delivery
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
dim_customer_table_insert = """
INSERT INTO dim_customer(
    user_name,
    customer_zip_code,
    customer_city,
    customer_state
) VALUES (%s, %s, %s, %s)
ON CONFLICT (user_name) DO UPDATE SET 
customer_zip_code = EXCLUDED.customer_zip_code, 
customer_city = EXCLUDED.customer_city, 
customer_state = EXCLUDED.customer_state
"""
dim_date_table_insert = """
INSERT INTO dim_date(
    date,
    year,
    quarter,
    season,
    month,
    month_name,
    day,
    day_name,
    hour,
    am_or_pm
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (date) DO NOTHING
"""

dim_payment_table_insert = """
INSERT INTO dim_payment(
    payment_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (payment_id) DO NOTHING
"""

dim_feedback_table_insert = """
INSERT INTO dim_feedback(
    feedback_id,
    feedback_score,
    feedback_form_sent_date,
    feedback_answer_date
) VALUES (%s, %s, %s, %s)
ON CONFLICT (feedback_id) DO NOTHING
"""

select_payment_by_id = "SELECT id FROM dim_payment WHERE payment_id = %s"
select_feedback_by_id = "SELECT id FROM dim_feedback WHERE feedback_id = %s"
select_customer_by_id = "SELECT id FROM dim_customer WHERE user_name = %s"
drop_table_queries = [
    fact_order_table_drop,
    dim_customers_table_drop,
    dim_date_table_drop,
    dim_payment_table_drop,
    dim_feedback_table_drop,
]
create_table_queries = [
    dim_customer_table,
    dim_date_table,
    dim_payment_table,
    dim_feedback_table,
    fact_order_table,
]
