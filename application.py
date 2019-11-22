from flask import Flask
from flask import url_for, jsonify, render_template
import caller
import numpy as np
application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')


@application.route('/price',  methods=['GET'])
def price():
    config = caller.get_config()
    contents = caller.fetch_latest_BTC_JSON(config_file=config)
    data_df = caller.parse_alphaV_JSON(contents)
    close_prices = np.array(data_df['4a. close (USD)'].tolist())
    msg =  jsonify({"Current_Price": close_prices[0]})
    return msg

if __name__ == "__main__":
    debug = False
    if(debug):
        application.run(port=8080, debug=True)
    elif(debug == False):
        application.run(host="0.0.0.0")
