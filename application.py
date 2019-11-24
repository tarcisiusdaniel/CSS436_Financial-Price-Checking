from flask import Flask
from flask import url_for 
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
import caller
import numpy as np
application = Flask(__name__)

# --- Global Variables ---
global ticker_val
global ticker_interval
ticker_val = None
ticker_interval = None


@application.route('/')
def index() -> "html":
    return render_template('index.html')

@application.route('/obtain_ticker',methods=['GET','POST'])
def obtain_ticker():
    global ticker_val
    ticker_val = request.form['tickerval']
    return redirect(url_for('index'))

@application.route('/price',  methods=['GET'])
def price():
    config = caller.get_config()
    global ticker_val
    #global ticker_interval
    if(ticker_val == None):
        ticker_val = config['av_ticker']

    if(ticker_val is not None):
        
        ticker_interval = caller.is_crypto(ticker_val)
    else:
        #global ticker_interval
        ticker_interval = 'DIGITAL_CURRENCY_DAILY'
    
    
    contents = caller.fetch_latest_BTC_JSON(
                    config_file=config,
                    ticker=ticker_val,
                    interval=ticker_interval
                )
    print("TICKER ------> ", ticker_val)
    print("ticker interval is ======> ", ticker_interval)

    data_df = caller.parse_alphaV_JSON(contents,ticker_interval)

    close_prices = None
    msg = None
    if(ticker_interval == 'DIGITAL_CURRENCY_DAILY'):
        close_prices = np.array(data_df['4a. close (USD)'].tolist())
        msg =  jsonify({"Current_Price": close_prices[0]})
    else:
        close_prices = np.array(data_df['4. close'].tolist())
        msg =  jsonify({"Current_Price": close_prices[-1]})
    
    return msg

if __name__ == "__main__":
    debug = True
    if(debug):
        application.run(port=8080, debug=True)
    elif(debug == False):
        application.run(host="0.0.0.0")
