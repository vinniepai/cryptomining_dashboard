import requests
import configparser
from decimal import Decimal

error = ""
config = configparser.ConfigParser()
config.read("config.ini")
wallet_id = config.get("wallet","id")
api_key = config.get("MPH_api_key","key")

try:
    zpool = config.get("API_URLs","zpool")
except Exception as exc:
    zpool = 0
    print(exc)
    print("zpool monitoring disabled.")
try:
    mph = config.get("API_URLs","mph")
except Exception as exc:
    mph = 0
    print(exc)
    print("MiningPoolHub monitoring disabled.")
try:
    hr = config.get("API_URLs","hr")
except Exception as exc:
    hr = 0
    print(exc)
    print("Hash Refinery monitoring disabled.")

# Convert BTC to CAD
def exchange_rate(amount):
    while True:
        try:
            btc = requests.get('https://api.cbix.ca/v1/convert?amount=' + str(amount) + '&from=BTC&to=CAD')
            b_start = btc.text.index('result')
            b_end = btc.text.index(',"meta"')
            btc = btc.text[b_start+8:b_end]
            return btc
        except:
            btc = 0
            err_check("CBIX")
            return btc


# Zpool/HR balance in BTC
def bal(api):
    while True:
        try:
            p = requests.get(api + wallet_id)
            b = p.text.index('balance')
            x = p.text[b + 10:b + 20]
            return x
        except:
            x = 0
            if api != '':
                err_check(api)
            return x


# MPH balance in BTC
def mph_bal():
    while True:
        try:
            p = requests.get(mph + api_key)
            b = p.text.index('confirmed')
            m = p.text[b + 11:b + 21]
            return m
        except ValueError:
            m = 0
            err_check("MiningPoolHub")
            return m


# Total balance in CAD and BTC
def total_bal():
    t = Decimal(float(z) + float(m) + float(h))
    r = Decimal(exchange_rate(t))
    return [r,t]


# Error checking/notification
def err_check(source):
    try:
        global error
        url_end = source.find('?')
        error += "Error: " + source[0:url_end] + " unavailable or rate limited. "
        return error
    except AttributeError:
        error += "Monitoring not enabled for one or more pools - check URL validity in config.ini"
        return error


z = bal(zpool)
h = bal(hr)
m = mph_bal()
btc = exchange_rate(1)
results = total_bal()[0]
total = total_bal()[1]


# Create/print to HTML format
totalCAD = str("{0:.2f}".format(results))
totalmBTC = str("{0:.4f}".format(float(total) * 1000))
BTCprice = str("{:,}".format(float(btc)))


if z != 0:
    Zbal = ("{0:.4f}".format(float(z) * 1000) + " mBTC / " + "{0:.2f}".format(float(exchange_rate(z))) + " CAD - zpool")
else:
    Zbal = ''


if m != 0:
    MPHbal = ("{0:.4f}".format(float(m) * 1000) + " mBTC / " + "{0:.2f}".format(float(exchange_rate(m))) + " CAD - MiningPoolHub")
else:
    MPHbal = ''


if h != 0:
    HRbal = ("{0:.4f}".format(float(h) * 1000) + " mBTC / " + "{0:.2f}".format(float(exchange_rate(h))) + " CAD - Hash Refinery")
else:
    HRbal = ''


# Console outputs (not used for Flask output)

class colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(colors.RED + error + colors.ENDC)
print('')
print(colors.BLUE + "Current balance: $" + totalCAD + " CAD / " + totalmBTC + " mBTC" + colors.ENDC)
print("1 BTC = $" + BTCprice + " CAD")
print('')
print(Zbal)
print(MPHbal)
print(HRbal)