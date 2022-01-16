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

@app.route("/SAG",methods=["POST"])
def SAG():
    if request.method == 'POST':
        SAG= int(request.form.get('SAG'))
        roughprofit= int(request.form.get('roughprofit'))
        b= SAG/roughprofit
        ab='{:.1%}'.format(b)
        return render_template("index.html",result1=ab,o1=SAG,o2=roughprofit)

@app.route("/research",methods=["POST"])
def research():
    if request.method == 'POST':
        research= int(request.form.get('research'))
        roughprofit= int(request.form.get('roughprofit'))
        c= research/roughprofit
        ac='{:.1%}'.format(c)
        return render_template("index.html",result2=ac,o3=research,o4=roughprofit)

@app.route("/DPC",methods=["POST"])
def DPC():
    if request.method == 'POST':
        DPC= int(request.form.get('DPC'))
        roughprofit= int(request.form.get('roughprofit'))
        d= DPC/roughprofit
        ad='{:.1%}'.format(d)
        return render_template("index.html",result3=ad,o5=DPC,o6=roughprofit)

@app.route("/pay_salep",methods=["POST"])
def pay_salep():
    if request.method == 'POST':
        payinterest= int(request.form.get('payinterest'))
        saleprofit= int(request.form.get('saleprofit'))
        e= payinterest/saleprofit
        ae='{:.1%}'.format(e)
        return render_template("index.html",result4=ae,o7=payinterest,o8=saleprofit)

@app.route("/Netincome_sales",methods=["POST"])
def Netincome_sales():
    if request.method == 'POST':
        Netincome= int(request.form.get('Netincome'))
        sales= int(request.form.get('sales'))
        f= Netincome/sales
        af='{:.1%}'.format(f)
        return render_template("index.html",result5=af,o9=Netincome,o10=sales)

#貸借対照表

@app.route("/Accounts_sales",methods=["POST"])
def Accounts_sales():
    if request.method == 'POST':
        AccountsReceivable= int(request.form.get('AccountsReceivable'))
        sales= int(request.form.get('sales'))
        g= AccountsReceivable/sales
        ag='{:.1%}'.format(g)
        return render_template("index.html",result6=ag,o11= AccountsReceivable,o12=sales)


@app.route("/Net_income_Asset",methods=["POST"])
def Net_income_Asset():
    if request.method == 'POST':
        Netincome= int(request.form.get('Netincome'))
        NetAssets= int(request.form.get('NetAssets'))
        h= Netincome/NetAssets
        ah='{:.1%}'.format(h)
        return render_template("index.html",result7=ah,o13=Netincome,o14=NetAssets)

#キャッシュフロー計算書

@app.route("/Netincome_CapitalE",methods=["POST"])
def Netincome_CapitalE():
    if request.method == 'POST':
        Netincome= int(request.form.get('Netincome'))
        CapitalExpenditure= int(request.form.get('CapitalExpenditure'))
        i= CapitalExpenditure/Netincome
        ai='{:.1%}'.format(i)
        return render_template("index.html",result8=ai,o15=Netincome,o16=CapitalExpenditure)


if __name__ == "__main__": #最後に記述する
    app.run(debug=True)
