import requests
from constant.app_constant import USER_TOKEN, BROKER_TO_COPY
from collections import Counter
from datetime import datetime, timedelta
from ollama_model import get_analysis
from constant.app_constant import LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE

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

def main():
    all_list = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for broker in BROKER_TO_COPY:
        all_list.append(get_buy_sell_broker(broker=broker, current_date=current_date))
    response_analysis = get_analysis(request_message=f'Please analyze this list of broker buying activity from this data {all_list} and make a summary to list of stock_code that appear at least on 3 different broker_code and then provide in this json format {LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE}')
    if response_analysis is not None:
        similar_stock = response_analysis['data']['detail']
        print(similar_stock)

if __name__ == "__main__":
    main()