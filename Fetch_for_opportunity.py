# fetch_opportunity.py

def analyze_arbitrage_opportunities(capital, ask_price, bid_price, fee, slippage):

    amount_in_base_currency = capital / ask_price

    # Account for slippage
    effective_bid_price = bid_price * (1 - slippage)
    effective_ask_price = ask_price * (1 + slippage)

    buy_fee = capital * fee
    sell_amount = amount_in_base_currency * effective_bid_price
    sell_fee = sell_amount * fee

    net_gain = sell_amount - capital - buy_fee - sell_fee

    return {
    'net_gain': net_gain
  }  
