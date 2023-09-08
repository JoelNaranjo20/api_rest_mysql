from distutils.util import execute
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

app.secret_key= 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute ('SELECT * FROM contactos ')
    data =  cur.fetchall()
   

    return render_template('index.html', contactos = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos ( fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname, phone, email) ) 
        mysql.connection.commit()
        flash('Contact add successfully')

        return redirect(url_for('Index'))

@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s'%(id))
    data = cur.fetchall()
    return render_template('edit_contact.html',contact =data[0] )

@app.route('/update/<id>', methods = ['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('''
        UPDATE contactos 
        SET fullname =%s, 
            phone = %s, 
            email = %s 
        WHERE id = %s''',(fullname, phone, email, id))
        mysql.connection.commit()
        flash ('Contacto actualizado')
        return redirect(url_for('Index'))


@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact remove')
    
    return redirect(url_for('Index'))
    

if __name__=='__main__':
    app.run(port =3000, debug=True)
