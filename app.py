from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import DB_CONFIG
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "warranty123"

# ---------------- Database Connection ---------------- #

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- Home ---------------- #

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- User Registration ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users(name,email,phone,password) VALUES(%s,%s,%s,%s)",
            (name, email, phone, password)
        )

        con.commit()

        cur.close()
        con.close()

        return redirect('/login')

    return render_template('register.html')

# ---------------- Login ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

# ---------------- Dashboard ---------------- #

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template('dashboard.html', name=session['name'])

# ---------------- Add Product ---------------- #

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        product_name = request.form['product_name']
        brand = request.form['brand']
        model = request.form['model']
        serial_number = request.form['serial_number']
        purchase_date = request.form['purchase_date']
        warranty_months = request.form['warranty_months']

        con = get_db()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO products
            (user_id, product_name, brand, model, serial_number, purchase_date, warranty_months)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session['user_id'],
            product_name,
            brand,
            model,
            serial_number,
            purchase_date,
            warranty_months
        ))

        con.commit()

        cur.close()
        con.close()

        return redirect('/view_products')

    return render_template('add_product.html')

# ---------------- View Products ---------------- #

@app.route('/view_products')
def view_products():

    if 'user_id' not in session:
        return redirect('/login')

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT product_name,
               brand,
               model,
               serial_number,
               purchase_date,
               warranty_months
        FROM products
        WHERE user_id=%s
    """, (session['user_id'],))

    products = cur.fetchall()

    cur.close()
    con.close()

    return render_template("view_products.html", products=products)

# ---------------- Warranty Status ---------------- #

@app.route('/warranty_status')
def warranty_status():

    if 'user_id' not in session:
        return redirect('/login')

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT product_name,
               purchase_date,
               warranty_months
        FROM products
        WHERE user_id=%s
    """, (session['user_id'],))

    rows = cur.fetchall()

    products = []

    today = datetime.today().date()

    for row in rows:

        product_name = row[0]
        purchase_date = row[1]
        warranty_months = row[2]

        expiry_date = purchase_date + timedelta(days=int(warranty_months) * 30)

        if today <= expiry_date:
            status = "🟢 Active"
        else:
            status = "🔴 Expired"

        products.append((
            product_name,
            purchase_date,
            warranty_months,
            status
        ))

    cur.close()
    con.close()

    return render_template(
        "warranty_status.html",
        products=products
    )

# ---------------- Warranty Claim ---------------- #

@app.route('/claim', methods=['GET', 'POST'])
def claim():

    if 'user_id' not in session:
        return redirect('/login')

    con = get_db()
    cur = con.cursor()

    # Read all registered products of the logged-in user
    cur.execute("""
        SELECT product_id, product_name
        FROM products
        WHERE user_id=%s
    """, (session['user_id'],))

    products = cur.fetchall()

    if request.method == 'POST':

        product_id = request.form['product_id']
        claim_reason = request.form['claim_reason']
        description = request.form['description']

        today = datetime.today().date()

        cur.execute("""
            INSERT INTO claims
            (user_id, product_id, claim_reason, description, claim_date)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            session['user_id'],
            product_id,
            claim_reason,
            description,
            today
        ))

        con.commit()

        cur.close()
        con.close()

        return redirect('/dashboard')

    cur.close()
    con.close()

    return render_template(
        "claim.html",
        products=products
    )
# ---------------- Admin Dashboard ---------------- #

@app.route('/admin_dashboard')
def admin_dashboard():

    if 'admin_id' not in session:
        return redirect('/admin_login')

    return render_template('admin_dashboard.html')
# ---------------- Admin Login ---------------- #

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cur.fetchone()

        cur.close()
        con.close()

        if admin:

            session['admin_id'] = admin[0]
            session['admin_name'] = admin[1]

            return redirect('/admin_dashboard')

        else:

            return "Invalid Admin Username or Password"

    return render_template('admin_login.html')
# ---------------- View All Claims ---------------- #

@app.route('/view_claims')
def view_claims():

    if 'admin_id' not in session:
        return redirect('/admin_login')

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            claims.claim_id,
            users.name,
            products.product_name,
            claims.claim_reason,
            claims.description,
            claims.claim_date,
            claims.status
        FROM claims
        JOIN users
            ON claims.user_id = users.user_id
        JOIN products
            ON claims.product_id = products.product_id
        ORDER BY claims.claim_id DESC
    """)

    claims = cur.fetchall()

    cur.close()
    con.close()

    return render_template(
        "view_claims.html",
        claims=claims
    )
# ---------------- Approve Claim ---------------- #

@app.route('/approve_claim/<int:claim_id>')
def approve_claim(claim_id):

    if 'admin_id' not in session:
        return redirect('/admin_login')

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "UPDATE claims SET status='Approved' WHERE claim_id=%s",
        (claim_id,)
    )

    con.commit()

    cur.close()
    con.close()

    return redirect('/view_claims')
# ---------------- Reject Claim ---------------- #

@app.route('/reject_claim/<int:claim_id>')
def reject_claim(claim_id):

    if 'admin_id' not in session:
        return redirect('/admin_login')

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "UPDATE claims SET status='Rejected' WHERE claim_id=%s",
        (claim_id,)
    )

    con.commit()

    cur.close()
    con.close()

    return redirect('/view_claims')
# ---------------- Logout ---------------- #

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# ---------------- Run Application ---------------- #

if __name__ == "__main__":
    app.run(debug=True)