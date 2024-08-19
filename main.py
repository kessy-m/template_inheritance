from flask import Flask,render_template,request,flash,redirect,url_for,session
from database import get_data,all_sales,perday_sales,insert_user,insert_products,insert_sales,allprofit,perday_profit,confirm_email,check_email_pass,allprofit

app=Flask(__name__)

app.config['SECRET_KEY']='dfjfgmgh,gfddf'

#confirm login
# def confirm_login():
#    if "email " not in session:
#       return redirect(url_for('login'))
   



@app.route('/')
def home():
       return render_template('index.html')


# create a login route
@app.route('/login',methods=['GET','POST'])
def login():
#get form data
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=check_email_pass(email,password)
        print(user)

        if user:
           session["email"]=email
           flash(f"You have been logged in! ")
           return redirect(url_for("dashboard"))
        elif confirm_email(email):
            flash('email does not exist')
            return redirect(url_for('register'))
        else:
           flash("Login Unsuccessful.")
    return render_template('login.html')
    
           
        

    #     #  check email exists
    #     ch_email=confirm_email(email)
    #     if len(ch_email)<1:
    #         flash('email does not exist')
    #         return redirect(url_for('register'))
    #     else:
    #         ch_pass=check_email_pass(email,password)
    #         if len(ch_pass)<1:
    #             flash('try again')
    #         else:
    #             session['email']=email
    #             flash('login succesfully')    
    #             return redirect(url_for('dashboard'))
    # return render_template('login.html')
   

@app.route('/register', methods=['GET','POST'])
def register():
   if request.method=="POST":
        ful_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
# insert users
        con_email=confirm_email(email)
        if con_email==None:
           new_users=(ful_name,email,password)
           insert_user(new_users)
           flash('please register','primary')
           return redirect(url_for('login'))
        else:
           flash('This email already exists') 

   return  render_template('register.html')


# create a products route
@app.route('/products')
def products():
    if "email" not in session:
       return redirect(url_for('login'))
    products=get_data('products')
    return render_template('products.html',products=products)


# create a sales route
@app.route('/sales')
def sales():
    if 'email' not in session:
        return redirect(url_for('login'))
    sales=get_data('sales')
    totalprods=get_data('products')
    return render_template('sales.html',sales=sales,prods=totalprods)



# create a dashboard route
@app.route('/dashboard')
def dashboard():
   total_profit=allprofit()
   profit=[]
   name_pr=[]
   for p in total_profit:
      profit.append(float(p[1]))
      name_pr.append(str(p[0]))

# create profit per day
   daysprofit=perday_profit()
   days=[]
   dy_profit=[]

   for d in daysprofit:
    days.append(str(d[0]))
    dy_profit.append(float(d[1]))
    print(dy_profit)

    # create sales per day
    daysales=perday_sales()
    days=[]
    dy_sales=[]
    for s in daysales:
        days.append(str(s[0]))
        dy_sales.append(float(s[1]))

# create sales  per product
    total_sales=all_sales()
    sales=[]
    sales_pr=[]
    for q in total_sales:
     sales.append(str(q[0]))
     sales_pr.append(float(q[1]))
    return render_template('dashboard.html',name=name_pr,profit=profit,pr_day=dy_profit,days=days,s_pr=sales_pr,s_day=dy_sales)
     


# create an adding product route
@app.route('/adding_products',methods=['GET','POST'])
def adding_prods():
   pr_name=request.form['product_name']
   b_price=request.form['buying_price']
   s_price=request.form['selling_price']
   stock=request.form['stock_quantity']
   added_products=(pr_name,b_price,s_price,stock)

# insert products
   insert_products(added_products)
   flash(f"{stock}  {pr_name} added succesfully")
   return redirect(url_for('products'))


@app.route('/adding_sales',methods=['GET','POST'])
def making_sales():
    pid=request.form['pid']
    quantity=request.form['stock-quantity']
    new_sales=(pid,quantity)

    # insert sales
    insert_sales(new_sales)
    return redirect(url_for('sales'))



#create a log out route
@app.route('/log_out')
def log_out():
    session.pop('email',None)
    flash('loging out successfully','')
    return redirect(url_for('login'))

app.run(debug=True)
