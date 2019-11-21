from flask import Flask
from flask import url_for, jsonify, render_template
import caller
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/price',  methods=['GET'])
def price():
    config = caller.get_config()
    contents = caller.fetch_latest_BTC_JSON(config_file=config)
    data_df = caller.parse_alphaV_JSON(contents)
    close_prices = np.array(data_df['4a. close (USD)'].tolist())
    msg =  jsonify({"Current_Price": close_prices[-1]})
    return msg

if __name__ == "__main__":
    app.run(port=8080, debug=True)