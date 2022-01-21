from re import L
import os
from flask import Flask,render_template,request,redirect
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager,login_user,logout_user,login_required
from werkzeug.security import generate_password_hash ,check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search.db'
app.config['SECRET_KEY']= os.urandom(24)
db = SQLAlchemy(app)
Login_manager=LoginManager()
Login_manager.init_app(app)
#データベース機能ログインサインアップ機能完成2021/12/29
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
def __init__(self,user_name=None, password=None): 
     self.user_name =user_name
     self.password=password

@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#homepage route
@app.route('/',methods=["GET", "POST"])
def index():
    return render_template('index.html')
@app.route('/searched',methods=["GET", "POST"])
def searched():
    if request.method=='GET':
     return render_template('searched.html')
@app.route("/howto",methods=["GET"])
def howto():
     return render_template("howto.html")



#user機能
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        user_name= request.form.get('user_name')
        password= request.form.get('password')
        user= User(user_name=user_name, password=generate_password_hash(password, method='sHa256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
      return render_template("signup.html")


@app.route("/login",methods=["GET","POSt"])
def login():
    if request.method == 'POST':
        user_name= request.form.get('user_name')
        password= request.form.get('password')
        user=User.query.filter_by(user_name=user_name).first()
        if check_password_hash(user.password,password):
            login_user(user) #間違っていた時の処理は課題
        return redirect('/')
    else:
      return render_template("login.html")
@app.route('/logout')
@login_required #ログインしてないとアクセスできません文
def logout():
    logout_user()
    return redirect('/login')



#財務表　分析関数　route
@app.route("/roughprofit",methods=["POST"])
def sales_rough_profit():
    if request.method == 'POST':
        sales= int(request.form.get('sales'))
        roughprofit = int(request.form.get('roughprofit'))
        a=roughprofit/sales
        aa='{:.1%}'.format(a)
        return render_template("index.html",result=aa,originaldata1=roughprofit,originaldata2=sales)




if __name__ == "__main__": #最後に記述する
    app.run(debug=True)
