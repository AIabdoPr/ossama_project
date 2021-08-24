from flask import Flask, render_template, request, redirect
import MySQLdb
import yaml

app = Flask(__name__)

db = yaml.load(open('static/data/db.yaml'))
try:
  db_connection = MySQLdb.connect(db['mysql_host'], db['mysql_user'], db['mysql_password'])
  cursor = db_connection.cursor()
  cursor.execute(
      open("static/data/db_install.sql", "r").read().replace("--DB_NAME--", db["mysql_db"]))
  mysql = MySQLdb.connect(
      db['mysql_host'], db['mysql_user'], db['mysql_password'], db['mysql_db'])
except Exception as e:
  print("Eror:"+str(e))

@app.route('/', methods = ['GET', 'POST'])
def index():
  print(request.method)
  if request.method == 'POST':
    userDetails = request.form
    email = userDetails['email']

    cursor = mysql.cursor()
    cursor.execute('INSERT INTO emails (email) VALUES("%s")' % (email))
    mysql.commit()

    return redirect('portfol.html')
  return render_template('index.html')

@app.route('/portfol.html')
def portfol():
  return render_template('portfol.html')

@app.route('/porjikt_cv.html')
def porjikt_cv():
  return render_template('porjikt_cv.html')

if __name__ == "__main__":
  app.run(port = 80, debug = True)
