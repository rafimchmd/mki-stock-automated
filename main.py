import requests
from constant import USER_TOKEN, BROKER_TO_COPY
from collections import Counter

def get_buy_sell_broker(broker: str):
    url = f"https://exodus.stockbit.com/order-trade/broker/activity?broker_code={broker}&limit=50&page=1&from=2026-04-15&to=2026-04-15&transaction_type=TRANSACTION_TYPE_NET&market_board=MARKET_TYPE_REGULER&investor_type=INVESTOR_TYPE_ALL"

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
    buy_stocks = [item['stock_code'] for item in response['data']['broker_activity_transaction']['brokers_buy']]
    return buy_stocks

all_list = []
for broker in BROKER_TO_COPY:
    all_list.append(get_buy_sell_broker(broker=broker))

stock_count = Counter()
for lst in all_list:
    for stock in set(lst):  # set() ensures each stock counted only once per list
        stock_count[stock] += 1

# Filter stocks that appear in at least 3 lists
min_lists = 3
common_stocks = [(stock, count) for stock, count in stock_count.items() if count >= min_lists]

# Sort by count (descending), then by stock code (ascending)
common_stocks = sorted(common_stocks, key=lambda x: (-x[1], x[0]))

# Display results
print("=" * 60)
print(f"📊 STOCK CODES APPEARING IN AT LEAST {min_lists} LISTS")
print("=" * 60)
print(f"{'#':<3} {'Stock Code':<10} {'Appearances':<12}")
print("-" * 60)
for i, (stock, count) in enumerate(common_stocks, 1):
    print(f"{i:<3} {stock:<10} {count}/5 lists")

print("-" * 60)
print(f"✅ Total: {len(common_stocks)} stock(s)")
print("=" * 60)