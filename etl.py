import pandas as pd
from sqlalchemy import create_engine

# Создадим подключение к моему локальному серверу PostgreSQL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

# Загружаем таблицу supermarket_sales с сервера в pandas для дальнейшей работы с ней
df = pd.read_sql("SELECT * FROM nds.supermarket_sales", con=engine).convert_dtypes()

# Заполним таблицу branch
branch_df = df[['Branch', 'City']].rename(columns={'Branch': 'branch_code', 'City': 'city'}).drop_duplicates(subset=['branch_code', 'city'])
branch_df['branch_id'] = range(1, len(branch_df) + 1)
branch_df.to_sql('branch', engine, schema='nds', if_exists='append', index=False)

# Заполним таблицу customer
customer_df = df[['Customer type', 'Gender']].drop_duplicates().reset_index(drop=True)
customer_df['customer_id'] = customer_df.index + 1
customer_df.rename(columns={'Customer type': 'customer_type', 'Gender': 'customer_gender'}, inplace=True)
customer_df.to_sql('customer', engine, schema='nds', if_exists='append', index=False)

# Заполним таблицу payment
payment_df = df[['Payment']].drop_duplicates().rename(columns={'Payment': 'payment_method'})
payment_df['payment_id'] = range(1, len(payment_df) + 1)
payment_df.to_sql('payment', engine, schema='nds', if_exists='append', index=False)

# Заполним таблицу product
product_df = df[['Product line', 'Unit price']].rename(columns={'Product line': 'product_line', 'Unit price': 'unit_price'}).drop_duplicates(subset=['product_line'])
product_df['product_id'] = range(1, len(product_df) + 1)
product_df.to_sql('product', engine, schema='nds', if_exists='append', index=False, method='multi')

# Заполним таблицу invoice, для этого нам понадобится немного преобразовать customer_df
customer_df['customer_key'] = customer_df['customer_type'] + "_" + customer_df['customer_gender']

invoice_df = df[['Invoice ID', 'Date', 'Time', 'Branch', 'Customer type', 'Payment', 'Gender']]
invoice_df['customer_key'] = invoice_df['Customer type'] + "_" + invoice_df['Gender']
invoice_df = invoice_df.merge(branch_df[['branch_code', 'branch_id']], left_on='Branch', right_on='branch_code', how='left') \
                       .merge(customer_df, on=['customer_key'], how='left').drop_duplicates() \
                       .merge(payment_df[['payment_method', 'payment_id']], left_on='Payment', right_on='payment_method', how='left').drop_duplicates()
invoice_df = invoice_df[['Invoice ID', 'Date', 'Time', 'branch_id', 'customer_id', 'payment_id']]
invoice_df['Date'] = pd.to_datetime(invoice_df['Date'], format='%m/%d/%Y')
invoice_df.rename(columns={'Invoice ID': 'invoice_id', 'Date': 'date', 'Time': 'time'}, inplace=True)
invoice_df.to_sql('invoice', engine, schema='nds', if_exists='append', index=False, method='multi')

# Заполним таблицу sale
sale_df = df[['Invoice ID', 'Product line', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'gross margin percentage']]
sale_df = sale_df.merge(product_df, left_on='Product line', right_on='product_line')
sale_df = sale_df[['Invoice ID', 'product_id', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'gross margin percentage']]
sale_df.rename(columns={'Invoice ID': 'invoice_id', 'Quantity': 'quantity', 'Tax 5%': 'tax',
                        'Total': 'total', 'gross income': 'gross_income', 'gross margin percentage': 'gross_margin_percentage'}, inplace=True)
sale_df.to_sql('sale', engine, schema='nds', if_exists='append', index=False)