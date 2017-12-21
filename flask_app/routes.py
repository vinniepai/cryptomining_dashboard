from Updates import totalCAD, totalmBTC, btc, Zbal, MPHbal, HRbal, error
from flask_app import app

@app.route('/')
@app.route('/index')
def index():
    print("Starting Flask")
    balances = {'fiat': totalCAD, 'mBTC': totalmBTC, 'BTCprice': btc, 'zpool': Zbal, 'MPH': MPHbal, 'HR': HRbal, 'errors' : error}
    return '''
    <html>
        <head>
            <title>Mining Balances</title>
        </head>
        <body>         
            <h1>''' "$" + balances['fiat'] + " CAD / " + balances['mBTC'] + " mBTC" + '''</h1>
            <h2>''' + "1 BTC = $" + balances['BTCprice'] + " CAD" + '''</h2>
            <p>''' + balances['zpool'] + '''</p>
            <p>''' + balances['MPH'] + '''</p>
            <p>''' + balances['HR'] + '''</p>
            <p>''' + balances['errors'] + '''</p>
        </body>
    </html>'''

print("routes")