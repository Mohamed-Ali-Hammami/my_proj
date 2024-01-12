# fetch_info.py

import asyncio
import json
import websockets
import logging
from Fetch_for_opportunity import analyze_arbitrage_opportunities
from Filtering_assets import filter_data

WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"
RECONNECT_INTERVAL = 0  # milliseconds

logging.basicConfig(level=logging.INFO)

async def websocket_handler(socket_io):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            logging.info("WebSocket connection established.")
            parameters = {}  # Dictionary to store dynamic parameters
            while True:
                try:
                    response = await websocket.recv()
                    buffer = response

                    # Check if the buffer starts with '[' and ends with ']'
                    if buffer.startswith("[") and buffer.endswith("]"):
                        try:
                            # Parse the entire array
                            symbol_infos = json.loads(buffer)
                            # Iterate over individual objects in the array
                            symbols_details = []

                            for symbol_info in symbol_infos:
                                # Dynamic calculation of parameters based on data characteristics
                                bid_quantity = float(symbol_info.get('B', 0))
                                ask_quantity = float(symbol_info.get('A', 0))
                                price_change = float(symbol_info.get('p', 0))
                                bid_price = float(symbol_info.get('b', 0))
                                ask_price = float(symbol_info.get('a', 0))

                                # Calculate or estimate dynamic parameters
                                parameters['fee'] = 0.001
                                parameters['amount'] = 100
                                parameters['slippage'] = 0.001
                                parameters['spread_threshold'] = bid_price * 0.001
                                parameters['volume_threshold'] = max(bid_quantity, ask_quantity) * 0.1
                                parameters['volatility_threshold'] = price_change * 0.1

                                # Use the functions from Trading_Algorythms
                                filtered_by_spread = filter_data(
                                    ask_price, bid_price, bid_quantity, ask_quantity, price_change,
                                    parameters['spread_threshold'], parameters['volume_threshold'], parameters['volatility_threshold']
                                )
                                print(filtered_by_spread)
                                calculate_total_gains = analyze_arbitrage_opportunities(
                                    parameters['amount'], ask_price, bid_price, parameters['fee'], parameters['slippage']
                                )
                                total_gains = calculate_total_gains.get('net_gain', 'negatif') \
                                    if calculate_total_gains.get('net_gain', 0) > 0 else 'negatif'

                                symbols_details.append({
                                    'total_gains': total_gains,
                                    'symbol': symbol_info.get('s', ''),
                                    'bid_price': symbol_info.get('b', 0),
                                    'ask_price': symbol_info.get('a', 0),
                                    'price_change': symbol_info.get('p', 0),
                                    'price_change_percent': symbol_info.get('P', 0),
                                    'weighted_avg_price': symbol_info.get('w', 0),
                                    'prev_day_close_price': symbol_info.get('x', 0),
                                    'current_day_close_price': symbol_info.get('c', 0),
                                    'close_trade_quantity': symbol_info.get('Q', 0),
                                    'bid_quantity': symbol_info.get('B', 0),
                                    'ask_quantity': symbol_info.get('A', 0),
                                    'open_price': symbol_info.get('o', 0),
                                    'high_price': symbol_info.get('h', 0),
                                    'low_price': symbol_info.get('l', 0),
                                    'bid_volume': symbol_info.get('v', 0),
                                    'ask_volume': symbol_info.get('q', 0),
                                    'open_time': symbol_info.get('O', 0),
                                    'close_time': symbol_info.get('C', 0),
                                    'first_trade_id': symbol_info.get('F', 0),
                                    'last_trade_id': symbol_info.get('L', 0),
                                    'total_trades': symbol_info.get('n', 0),
                                })

                            # Emit the data to connected clients
                            socket_io.emit('update_data', symbols_details)

                        except json.JSONDecodeError as json_error:
                            logging.error(f"Error decoding JSON array: {json_error}")
                            # Log errors encountered during JSON decoding
                            logging.error(f"Error decoding JSON array: {json_error}")

                except websockets.ConnectionClosedError as closed_error:
                    logging.error(f"WebSocket connection closed unexpectedly: {closed_error}")
                    break  # Break the inner loop and attempt to reconnect

                except Exception as e:
                    logging.error(f"Error in WebSocket connection: {e}")
                    # Log errors encountered during WebSocket connection
                    logging.error(f"Error in WebSocket connection: {e}")
                    # Sleep before attempting to reconnect
                    await asyncio.sleep(RECONNECT_INTERVAL / 1000)  # Convert to seconds

    except Exception as e:
        logging.error(f"Error connecting to WebSocket: {e}")
        # Log errors encountered during WebSocket connection
        logging.error(f"Error connecting to WebSocket: {e}")
        # Sleep before attempting to reconnect
        await asyncio.sleep(RECONNECT_INTERVAL / 1000)

# Run the WebSocket handler when the script is executed
if __name__ == "__main__":
    asyncio.run(websocket_handler())
