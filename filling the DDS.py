import pandas as pd
from sqlalchemy import create_engine


# Подключение к базе данных
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

# # Копируем измерения без изменений
for table in ["branch", "customer", "payment", "product"]:
    df = pd.read_sql(f"SELECT * FROM nds.{table}", con=engine).convert_dtypes()
    df.to_sql(f"dim_{table}", engine, schema="dds", if_exists="append", index=False, method='multi')

# Создаем таблицу dim_time
invoice_df = pd.read_sql("SELECT DISTINCT date FROM nds.invoice", con=engine)
invoice_df["date"] = pd.to_datetime(invoice_df["date"])
invoice_df["year"] = invoice_df["date"].dt.year
invoice_df["month"] = invoice_df["date"].dt.month
invoice_df["day"] = invoice_df["date"].dt.day
invoice_df["day_of_week"] = invoice_df["date"].dt.day_name()
invoice_df["time_id"] = range(1, len(invoice_df) + 1)
invoice_df.to_sql("dim_time", engine, schema="dds", if_exists="append", index=False, method='multi')

# Создаем таблицу fact_sales
fact_sales_df = pd.read_sql("""
    SELECT 
        s.sale_id, 
        t.time_id,
        i.branch_id, 
        i.customer_id, 
        s.product_id, 
        i.payment_id, 
        s.quantity, 
        s.tax, 
        s.total, 
        s.cogs, 
        s.gross_income, 
        s.gross_margin_percentage
    FROM nds.sale s
    JOIN nds.invoice i ON s.invoice_id = i.invoice_id
    JOIN dds.dim_time t ON i.date = t.date
""", con=engine)

fact_sales_df.to_sql("fact_sales", engine, schema="dds", if_exists="append", index=False, method='multi')

