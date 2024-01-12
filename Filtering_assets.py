#filtering assets.py

def filter_data(ask_price, bid_price, bid_quantity, ask_quantity, price_change, spread_threshold, volume_threshold, volatility_threshold):
    try:
        price_change_abs = abs(price_change)
        rolling_volatility = price_change_abs  # Update this line based on your calculation for rolling volatility

        filtered_symbol = (ask_price - bid_price < spread_threshold) and \
                          ((bid_quantity + ask_quantity) / 2 > volume_threshold) and \
                          (rolling_volatility < volatility_threshold)

        return filtered_symbol

    except Exception as e:
        print("Error:", e)
        return False
