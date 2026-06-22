from src.etl.loader import *

market_cap = load_market_cap()
peer_groups = load_peer_groups()
sectors = load_sectors()
stock_prices = load_stock_prices()

print("Market Cap:", market_cap.shape)
print("Peer Groups:", peer_groups.shape)
print("Sectors:", sectors.shape)
print("Stock Prices:", stock_prices.shape)