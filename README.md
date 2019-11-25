# CSS436_FinalProject

<!DOCTYPE html>
<!-- Website Homepage-->
<html>
    <!-- Header Area -->
    <head>
        <!-- Getting Fonts from Google Fonts API -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Dosis:800">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Karla">

        <link href="../static/index_bg.css" rel="stylesheet" type="text/css">

        <!-- Linking External CSS File for Navigation Bar -->
        <link href="../static/nav.css" rel="stylesheet" type="text/css">
        <!-- Creation of Top Navigation Bar -->
        <nav>
            <div class="navBar">
            <li><a href="index.html">Price Checker</a></li>
            <li>Contact Us</a></li>
            <li>Login/Sign Up</a></li>
            </div>
        </nav>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        
        <center>
            <h1>Stock and Cryptocurrency Price Checker</h1>
        </center>
        
    </head>
    <!-- Body Area -->
    <body>
        <form action="/obtain_ticker" method="POST">
            <input type="text" name="tickerval" placeholder="Ticker">
            <input type="submit" id="action" value="Set Ticker">
        </form>

        <!-- Get Price Button -->
        <button id='myButton' type="button">Get Price!</button>
          <script>
            $('#myButton').click(function() {
                $.ajax({
                    type:'GET',
                    url: "{{ url_for('price')}}",
                    dataType:"text",
                    success: function(response){
                        console.log(response);
                        alert(response);
                    }
                });
            });
        </script>
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
            <div id="tradingview_8ae14"></div>
            <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/symbols/NASDAQ-MSFT/" rel="noopener" target="_blank">
            <span class="blue-text">MSFR Chart</span>
            </a> by TradingView
        </div>

        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {
            "width": 980,
            "height": 610,
            "symbol": "NYSE:M",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "Light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_8ae14"
        }
        );
        </script>
        </div>
        <!-- TradingView Widget END -->
    </body>
</html>