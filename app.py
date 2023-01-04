from flask import Flask, redirect, url_for, render_template, flash
import pymysql
from tables import Results
from db_config import MySQL
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pijarcamp'
@app.route('/')
def index():
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM tbl_user")
    rows = cursor.fetchall()
    table = Results(rows)
    table.border = True    
    cursor.close() 
    conn.close()
    return render_template('index.html', table=table)


@app.route('/create', methods=["POST","GET"])
def create():
    if request.method == "POST":
        name = request.form['name']
        keterangan = request.form['keterangan']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        conn = None
        cursor = None
        sql = "INSERT INTO produk(id_produk, nama, keterangan, harga, jumlah) VALUES(%s, %s, %d, %d)"
        data = (name, keterangan, harga, jumlah)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close() 
        conn.close()
        flash('Produk added successfully!')
        return redirect('/')
    else: 
        return render_template('create.html')

@app.route('/edit/<int:id>', methods=["POST","GET"] )
def edit(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update.html', row=row)
   

@app.route('/update', methods=["POST","GET"] )
def update():
     if request.method == "POST":
        name = request.form['name']
        keterangan = request.form['keterangan']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        id = request.form['id']
        sql = "UPDATE produk SET nama=%s, keterangan=%s, harga=%d, jumlah=%d WHERE id_produk=%d"
        data = (name, keterangan, harga, jumlah, id,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash('Produk updated successfully!')
        return redirect('/')
     else:
         return render_template('update.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id_produk=%d", (id,))
    conn.commit()
    flash('Produk deleted successfully!')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
