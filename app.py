from flask import Flask,render_template,request,make_response,jsonify,session,redirect
app = Flask(__name__)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




#-----------------------------------------------DATABASE-------------------------------------------------------------------
import sqlite3
conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS register
             (username text,email text,password text)''')			
conn.commit()
conn.close()


#----------------------------------------------------------------------------------------------------------------------------




@app.route('/',methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        data=request.get_json()
        if data['which_condiction']=="signup":
            print("signup")
            conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM register")
            for query_result in c.fetchall():
                if data['username'] in query_result:
                    return "exists"
                else:  
                    pass   
            password = bytes(data['password'], 'utf-8')
            password = hashing(password)
            data['password']=password
            c.execute("""INSERT INTO register (username,email,password) values (?,?,?)""",(data['username'],data['email'],data['password']))
            conn.commit()
            return "success"
        elif data['which_condiction']=="login":
            print("login")
            conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM register WHERE username=?", ( data['username'],))
            result = c.fetchall()
            if len(result)==0:     
                return "no"
            for i in result:
                if verify_pass(i[2],data['password']):
                    return "success"
                else:
                    return "error"

    return render_template("login.html")


@app.route('/user/<username>',methods=['GET','POST'])
def Home(username):
    return render_template("home.html")





def hashing(password):
    pw_hash = bcrypt.generate_password_hash(password)
    return pw_hash
def verify_pass(password,password1):
    return bcrypt.check_password_hash(password,password1)


if __name__=="__main__":
    app.run()
    app.run(debug=True)