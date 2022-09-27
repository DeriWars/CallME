from flask import Flask, render_template, request, redirect, session
from waitress import serve
from socket import gethostname, gethostbyname
from random import randint
from requests import post
from os import system

from object.debug import log, warn, error, debug
from object.sql import Database
from object.UniversalTimecode import UniversalTimecode

app = Flask("CallME!")
app.secret_key = "callme-fzfvazfd1sq5f1065eza1f1dsq0f"

system("title CallME! - Web Server (v2022.01.18)")
ACCOUNTS = Database("./static/account.db")

sms_sended:dict = {}


def send_sms_code(phone_number: str):
    sms_time = UniversalTimecode.now()
    code = randint(100000, 999999)
    sms_content = f"CallME! authentification\nYour code is: {code}\nThis code is valid for 5 minutes.\nDo not share this code."
    
    # TODO: send sms to phone number
    # resp = post('https://textbelt.com/text', {
        # 'phone': phone_number,
        # 'message': sms_content,
        # 'key': 'textbelt',
    # })
    
    # debug(resp.json())
    
    sms_sended[phone_number] = (sms_time, code)
    log(f"SMS code sent to {phone_number} with code {code}")



@app.route("/", methods=["GET", "POST"])
def index():
    if not 'account_id' in session:
        return redirect("/login");
    
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Login page

    Returns:
        str: login page or home page if logged in
    """
    
    if request.method == "GET":
        session.pop('account_id', None)
        return render_template("login.html")
    elif request.method == "POST":
        phone_number = str(request.form['phone_number']).strip()
        
        # Check if every field is valid
        if len(phone_number) != 10:
            return render_template("login.html", error="Phone number must be 10 digits long.")
        
        # Check if phone number is in ACCOUNTS
        if ACCOUNTS.get_account_by_phone(phone_number) is not None:
            return redirect(f"/confirm_login?phone={phone_number}")
        else:
            return redirect(f"/signup?phone={phone_number}")


@app.route("/signup", methods=["GET", "POST"])
def signup() -> str:
    """
    Signup page
    
    Returns:
        str: the web page to render
    """
    
    if request.method == "GET":
        session.pop('account_id', None)
        
        if len(request.args) != 0:
            return render_template("signup.html", error=f"Account with phone number \"{request.args.get('phone')}\" does not exist. Please sign up.", phone_number=request.args.get('phone'))
        
        return render_template("signup.html")
    elif request.method == "POST":
        phone_number = str(request.form['phone_number']).strip()
        name = str(request.form['name']).title().strip()
        last_name = str(request.form['last_name']).upper().strip()
        age = int(request.form['age'])
        
        # Check if every field is valid
        if len(phone_number) != 10:
            return render_template("signup.html", error="Phone number must be 10 digits long.")
        
        if len(name) < 2:
            return render_template("signup.html", error="Name must be at least 2 characters long.")

        if len(last_name) < 2:
            return render_template("signup.html", error="Last name must be at least 2 characters long.")
        
        if age < 13:
            return render_template("signup.html", error="You need to be at least 13 years old.")

        # Check if phone number is already taken
        if ACCOUNTS.get_account_by_phone(phone_number) is not None:
            return render_template("signup.html", error="This phone number is already linked to another account!")
        
        # Add user to database
        ACCOUNTS.create_account(phone_number, name, last_name, age)
        
        return redirect(f"/confirm_login?phone={phone_number}")


@app.route("/confirm_login", methods=["GET", "POST"])
def confirm_login() -> str:
    if 'account_id' in session:
        return redirect("/")

    if len(request.args) == 0:
        return redirect("/login")
    
    if request.method == "GET":
        if request.args.get('phone') in sms_sended and (sms_sended[request.args.get('phone')][0] - UniversalTimecode.now()).value > 300:
            send_sms_code(request.args.get('phone'))
        elif request.args.get('phone') not in sms_sended:
            send_sms_code(request.args.get('phone'))
        
        return render_template("confirm_login.html", phone_number=request.args.get('phone'), success="Verification code has been sent to your phone number. This code is valid for 5 minutes.")
    elif request.method == "POST":
        code = int(request.form['code'])
        
        # Check if every field is valid
        if not 100000 <= code < 1000000:
            return render_template("confirm_login.html", phone_number=request.args.get('phone'), error="Code must be 6 digits long.")
        
        if request.args.get('phone') in sms_sended:
            if (sms_sended[request.args.get('phone')][0] - UniversalTimecode.now()).value > 150:
                send_sms_code(request.args.get('phone'))
                return render_template("confirm_login.html", phone_number=request.args.get('phone'), success="Verification code has been sent to your phone number. This code is valid for 5 minutes.", error="Code expired. Please try again.")
            
            if str(code) == str(sms_sended[request.args.get('phone')][1]):
                session['account_id'] = ACCOUNTS.get_account_by_phone(request.args.get('phone'))[0]
                sms_sended.pop(request.args.get('phone'), None)
                return redirect("/")
            else:
                return render_template("confirm_login.html", error="Code is incorrect. Please try again.", phone_number=request.args.get('phone'))
    
    return redirect(f"/confirm_login?phone={request.args.get('phone')}")
    
def main():
    app.run(host=gethostbyname(gethostname()), port=8080, debug=True) # Debug server
    # serve(app, host=gethostbyname(gethostname()), port=80) # Production server

if __name__ == "__main__":
    main()
