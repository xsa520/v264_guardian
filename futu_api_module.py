# ======== futu_api_module.py 開始 ========

def place_order(stock_code, price, quantity, direction):
    """
    預設虛擬下單。未來如果接 Futu OpenD，請在這裡填上真實下單指令。
    :param stock_code: 股票代碼 (如 'AAPL')
    :param price: 下單價格
    :param quantity: 股數
    :param direction: 'BUY' 或 'SELL'
    """
    print(f"[虛擬下單] {direction} {quantity} 股 {stock_code} @ {price}")

def close_order(stock_code, quantity):
    """
    預設虛擬平倉。未來如果接 Futu OpenD，請在這裡填上真實平倉指令。
    :param stock_code: 股票代碼 (如 'AAPL')
    :param quantity: 股數
    """
    print(f"[虛擬平倉] 平掉 {quantity} 股 {stock_code}")

# ======== futu_api_module.py 結束 ========
