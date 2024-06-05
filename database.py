import psycopg2

 
# connecting to the postgreSQL database
conn=psycopg2.connect(
host= 'localhost',
database='myduka',
user= 'postgres',
password= '12345',
port= 5432
)
# open a cursor to perform database operation

cur = conn.cursor()

# to get products
def get_data(table_name):
    cur.execute(f'select * from {table_name}')
    data = cur.fetchall()
    return data


# to get profit per day
def perday_profit():
   dd_profit="select date(created_at) as day, sum((selling_price-buying_price)*quantity) \
      as profit from products as p join sales as s on s.pid=p.id group by date(created_at)  order by date(created_at) ;"
   cur.execute(dd_profit)
   data=cur.fetchall()
   return data


# to get profit per product
def allprofit():
   tt_profit="select p.name, sum(((selling_price-buying_price)*quantity)) as profit from products as p join sales as s on s.pid=p.id group by p.name;"
   cur.execute(tt_profit)
   data=cur.fetchall()
   return data
   


# to get sales per product
def all_sales():
  tt_sales="select p.name, sum(selling_price*quantity) as total_sales from products as p join sales as s on s.pid=p.id group by p.name;"
  cur.execute(tt_sales)
  data=cur.fetchall()
  return data

# to get sales per day
def perday_sales():
   dd_sales="select date(created_at), sum(selling_price*quantity) as profit from products as p join sales as s on s.pid=p.id group by date(created_at);"
   cur.execute(dd_sales)
   data=cur.fetchall()
   return data

# to insert sales
def insert_sales(values):
   cur.execute("insert into sales(pid,quantity,created_at)values(%s,%s,now())",values)
   conn.commit

# to insert products
def insert_products(values):
   cur.execute("insert into products(name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)",values)
   conn.commit()

#INSERT USER
def insert_user(values):
   query="insert into user2(full_name,password,email)values(%s,%s,%s);"
   cur.execute(values,query)
   conn.commit()

# check email
def confirm_email(email):
   query="select from user2 where email=%s "
   cur.execute(query,(email))
   data=cur.fetchone()
   return data


#check if email and password exists
def check_email_pass(email,password):
    query='select * from user2 where email=%s and password=%s'
    cur.execute(query,(email,password,))
    data=cur.fetchall()
    return data