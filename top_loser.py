from helper.core import get_top_loser, get_keystats

def get_filtered_top_loser(min_price: int = 500):
    """
    Get filtered top loser stocks with price > min_price and has_uma = false.
    Returns list of dicts with only 'code' and 'name' fields.
    """
    response = get_top_loser()
    filtered_list = []
    
    if response and 'data' in response and 'mover_list' in response['data']:
        for item in response['data']['mover_list']:
            stock_detail = item.get('stock_detail', {})
            change = item.get('change', {})
            price = item.get('price', 0)
            
            # Filter: price > min_price and has_uma = false
            if price > min_price and not stock_detail.get('has_uma', True):
                filtered_list.append({
                    'code': stock_detail.get('code'),
                    'name': stock_detail.get('name'),
                    'change': round(float(change.get('percentage', 0)), 2),
                    'price': price
                })
    
    return filtered_list

# Get filtered top loser list
top_loser_filtered = get_filtered_top_loser()
selected_stocks = []
for stock in top_loser_filtered:
    # print(f"  {stock['code']} - {stock['name']} - Change: {stock['change']}% - Price: {stock['price']}")
    keystats_response = get_keystats(stock['code'])
    
    # Check if dividend data exists and is not null/empty
    if keystats_response and 'data' in keystats_response:
        dividend_group = keystats_response['data'].get('dividend_group', {})
        dividend_year_values = dividend_group.get('dividend_year_values', [])
        
        # Check if dividend_year_values is not empty
        if dividend_year_values:
            selected_stocks.append(stock)

for loser in selected_stocks:
    print(f"  {loser['code']} - {loser['name']} - Change: {loser['change']}% - Price: {loser['price']}")
    # main(loser['code'])