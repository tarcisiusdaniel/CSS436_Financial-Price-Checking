from flask import Flask, url_for, jsonify, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, current_user, logout_user
import caller
import numpy as np
from forms import RegistrationForm, LoginFrom
import authenticater
import re
import codecs
from apscheduler.schedulers.background import BackgroundScheduler
import text_alert
import datetime
import atexit

application = Flask(__name__)

# --- Global Variables ---
global ticker_val
global ticker_interval
ticker_val = None
ticker_interval = None
application.config['SECRET_KEY'] = '206d6d3001b9d58e037440b35e5de78e'
login_manager = LoginManager(application)
sns_config = text_alert.get_config()

@application.route('/')
def index() -> "html":
    return render_template('index.html')

@application.route('/register/', methods=['GET', 'POST'])
def register() -> "html":
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = authenticater.User(form.username.data)
            if user.registerUser(form.password.data, form.phone_number.data):
                success_status = 'Account Created for {}'.format(form.username.data)
                text_alert.signin_text_msg(sns_config, form.phone_number.data, form.password.data, form.username.data)
                flash(success_status, 'success')
                return redirect(url_for('login'))
            else:
                flash('Account already exists, please choose a different username', 'failed')
        return render_template('register.html', title='SignUp', form=form)


@application.route('/login/', methods=['GET', 'POST'])
def login() -> "html":
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = LoginFrom()
        if form.validate_on_submit():
            user = authenticater.User(form.username.data)
            usersession = user.get(form.username.data)
            if user.loginUser(form.password.data):
                login_msg = 'Hello, ' + form.username.data + '... you have been logged in!'
                flash(login_msg, 'success')
                login_user(usersession, remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                flash('Incorrect username or password', 'failed')
        return render_template("login_page.html", title='Login', form=form)

@application.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@application.route('/account/')
def account() -> "html":
    if (current_user.is_authenticated):
        return render_template("account.html", title='Account')
    else:
        return redirect(url_for('index'))


@application.route('/obtain_ticker', methods=['GET', 'POST'])
def obtain_ticker():
    global ticker_val
    ticker_val = request.form['tickerval']
    return redirect(url_for('index'))


@application.route('/test_method', methods=['GET'])
def test_method():
    return jsonify({"Bruh": 100})


@application.route('/price', methods=['GET'])
def price():
    config = caller.get_config()
    global ticker_val
    # global ticker_interval
    if (ticker_val == None):
        ticker_val = config['av_ticker']

    if (ticker_val is not None):

        ticker_interval = caller.is_crypto(ticker_val)
    else:
        # global ticker_interval
        ticker_interval = 'DIGITAL_CURRENCY_DAILY'

    contents = caller.fetch_latest_BTC_JSON(
        config_file=config,
        ticker=ticker_val,
        interval=ticker_interval
    )
    print("TICKER ------> ", ticker_val)
    print("ticker interval is ======> ", ticker_interval)

    data_df = caller.parse_alphaV_JSON(contents, ticker_interval)

    close_prices = None
    msg = None
    if (ticker_interval == 'DIGITAL_CURRENCY_DAILY'):
        close_prices = np.array(data_df['4a. close (USD)'].tolist())
        msg = jsonify({"Current_Price": close_prices[0]})
    else:
        close_prices = np.array(data_df['4. close'].tolist())
        msg = jsonify({"Current_Price": close_prices[-1]})
    update_graph(ticker_val)
    render_template('index.html')
    return msg

@login_manager.user_loader
def load_user (user_id):
    return authenticater.User.get(authenticater.User(user_id), user_id)

@application.route('/')
def update_graph(ticker):
    print('Ticker is = ', ticker)
    if (caller.is_cryptocurrency(ticker)):
        ticker = ticker + 'USD'
    print('Now the ticker is = ', ticker)
    exchange_name = caller.get_index(ticker)
    homepage = codecs.open("templates/index.html", 'rb+', encoding='utf-8').read()
    pattern = re.compile(r'"symbol": "\w+:\w+"')
    test = re.sub(pattern, '"symbol": ' + '"' + exchange_name + ":" + ticker + '"', homepage)
    f = codecs.open("templates/index.html", 'w+', encoding='utf-8')
    f.write(test)
    pass

def send_text():
    config = caller.get_config()
    #text_alert.send_text_msg(config,'+14257700031','app_test text')
    print('test to console')

if __name__ == "__main__":
    debug = False
    if (debug):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=send_text, trigger="interval", seconds=30)
        scheduler.start()
        application.run(port=8080, debug=True,use_reloader=False)
    elif (debug == False):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=send_text, trigger="interval", seconds=30)
        scheduler.start()
        application.run(host="0.0.0.0")
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())