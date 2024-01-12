import json
import requests
import asyncio
import websockets

async def get_exchange_rate(crypto):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    print(data)
    return data[crypto]['usd']

async def convert_to_crypto(amount, crypto):
    rate = await get_exchange_rate(crypto)
    converted_amount = amount / rate
    return converted_amount

async def main():
    amount_in_usd = 100
    cryptocurrencies = ['bitcoin', 'ethereum', 'ripple']  # Add more as needed

    for crypto in cryptocurrencies:
        converted_amount = await convert_to_crypto(amount_in_usd, crypto)
        print(f'$100 in {crypto.capitalize()}: {converted_amount:.6f} {crypto.upper()}')

if __name__ == "__main__":
    asyncio.run(main())
