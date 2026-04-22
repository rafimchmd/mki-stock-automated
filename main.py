import requests
from constant.app_constant import USER_TOKEN, BROKER_TO_COPY
from collections import Counter
from datetime import datetime, timedelta
from ollama_model import get_analysis
from constant.app_constant import LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE, KEYSTATS_RESPONSE
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

def get_history_data(code: str):
    data = yf.Ticker('code')
    hist = data.history(
        period='1mo',
        interval='1d',     
    )
    return hist.to_json()

def main():
    all_list = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for broker in BROKER_TO_COPY:
        all_list.append(get_buy_sell_broker(broker=broker, current_date=current_date))
    response_analysis = get_analysis(request_message=f'Please analyze this list of broker buying activity from this data {all_list} and make a summary to list of stock_code that appear at least on 3 different broker_code and then provide in this json format {LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE}')
    if response_analysis is not None:
        similar_stock = response_analysis['data']['detail']
        selected_stocks_fundamentally = []
        for stock_detail in similar_stock:
            keystats = get_keystats(stock_detail["stock_code"])
            fundamental = get_analysis(request_message=f'''You are Financial Expert with 20 years experience,
                               know perfectly how to understanding the financial report. You are always gain the profit from understanding the report.
                               So please analyze this financial report from stock code {stock_detail["stock_code"]} from data in json format {keystats}. Provide me a analysis summary in this json format {KEYSTATS_RESPONSE} without any ```json text because it cause failure to export to json''')
            if fundamental is not None:
                if fundamental["is_good_enough"] == "yes":
                    stock = stock_detail
                    stock["keystats_reason"] = fundamental["reason"]
                    stock["is_good"] = fundamental["is_good_enough"]
                    selected_stocks_fundamentally.append(stock)
        # for selected in selected_stocks_fundamentally:
        hist = get_history_data(f"{str(selected_stocks_fundamentally[0]["stock_code"]).replace("$","")}.JK")
        print(hist)
        wyckoff_result = get_analysis(request_message= f'''
      You are a professional trader and analyst with expertise in the Wyckoff method. You are rich because you have mastered the art of analyzing price movements and market trends to make informed trading decisions. You are fully knowledgeable about the Wyckoff method, which is a technical analysis approach that focuses on understanding the relationship between price and volume to identify market trends and potential trading opportunities. 
      You have a deep understanding of the different phases of the Wyckoff method, including accumulation, distribution, and markup/down phases. You are skilled at analyzing historical price data and volume patterns to identify key levels of support and resistance, as well as potential entry and exit points for trades. 
      Your expertise in the Wyckoff method allows you to make informed trading decisions that have consistently yielded profitable results.
      You are also expert on read the financial report such PER, EPS, etc.
      The financial report can be gathered from this data {selected_stocks_fundamentally[0]['keystats_reason']}
      Make a rational analysis of the historical price data of the stock based on the Wyckoff method. Provide the entry points stop loss and target levels and tell me if any requirement to entry for example "Entry if volume hit n billions" in key_observation object. Please provide insights on key levels of support and resistance, volume patterns, and potential trading opportunities. Use the data in JSON format {hist} for the last 1 month with 1 day interval to support your analysis. convert The output should be in JSON format following this structure {response_expectation}.''')


if __name__ == "__main__":
    main()