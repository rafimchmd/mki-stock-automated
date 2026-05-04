import requests
from constant.app_constant import USER_TOKEN
from datetime import datetime, timedelta
import yfinance as yf

def get_buy_sell_broker(broker: str, current_date):
    last_two_weeks = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    url = f"https://exodus.stockbit.com/order-trade/broker/activity?broker_code={broker}&limit=25&page=1&from={last_two_weeks}&to={current_date}&transaction_type=TRANSACTION_TYPE_NET&market_board=MARKET_TYPE_REGULER&investor_type=INVESTOR_TYPE_ALL"

    payload = {}
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
    'authorization': f'Bearer {USER_TOKEN}',
    'origin': 'https://stockbit.com',
    'priority': 'u=1, i',
    'referer': 'https://stockbit.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    buy_stocks = []
    for item in response['data']['broker_activity_transaction']['brokers_buy']:
        stock_detail = {'stock_code': item['stock_code'], 'broker_code': item['broker_code'], 'lot': item['lot'], "avg_price": item['avg_price']}
        buy_stocks.append(stock_detail)
    return buy_stocks

def get_keystats(broker: str):
    url = f"https://exodus.stockbit.com/keystats/ratio/v1/{broker}?year_limit=10"

    payload = {}
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
    'authorization': f'Bearer {USER_TOKEN}',
    'origin': 'https://stockbit.com',
    'priority': 'u=1, i',
    'referer': 'https://stockbit.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def get_keystats_data(keystats_response: dict, stats_name: str = "Current PE Ratio (Annualised)"):
    try:
        fin_items = keystats_response['data']['closure_fin_items_results']
        for group in fin_items:
            for item in group.get('fin_name_results', []):
                fitem = item.get('fitem', {})
                if fitem.get('name') == stats_name:
                    return fitem.get('value')
    except (KeyError, TypeError):
        pass
    return None

def get_history_data(code: str):
    data = yf.Ticker(f'{code}.JK'.replace('$',''))
    hist = data.history(
        period='1mo',
        interval='1d',     
    )
    return hist.to_json()


def get_top_loser():
    url = "https://exodus.stockbit.com/order-trade/market-mover?mover_type=MOVER_TYPE_TOP_LOSER&filter_stocks=FILTER_STOCKS_TYPE_MAIN_BOARD&filter_stocks=FILTER_STOCKS_TYPE_DEVELOPMENT_BOARD&filter_stocks=FILTER_STOCKS_TYPE_ACCELERATION_BOARD&filter_stocks=FILTER_STOCKS_TYPE_NEW_ECONOMY_BOARD"
    payload = {}
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
        'authorization': f'Bearer {USER_TOKEN}',
        'origin': 'https://stockbit.com',
        'priority': 'u=1, i',
        'referer': 'https://stockbit.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()