from flask import Flask, request, jsonify
import MetaTrader5 as mt5

# Pengaturan akun FBS
AKUN = "100580499"
PASSWORD = "m^In^4HK"
SERVER = "FBS-Demo"

app = Flask(__name__)

# Inisialisasi MetaTrader
def initialize_mt5():
    if not mt5.initialize():
        return False, mt5.last_error()
    if not mt5.login(AKUN, PASSWORD, SERVER):
        return False, mt5.last_error()
    return True, "Initialized successfully"

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    action = data.get("action")  # buy or sell
    symbol = data.get("symbol", "EURUSD")
    lot = data.get("lot", 0.1)
    
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return jsonify({"error": "Invalid symbol or no tick data"}), 400
    
    price = tick.ask if action == "buy" else tick.bid
    request_trade = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Node.js Bot Trading",
        "type_time": mt5.ORDER_TIME_GTC
    }
    
    result = mt5.order_send(request_trade)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({"error": result.comment}), 400

    return jsonify({"message": "Trade successful", "result": result._asdict()}), 200

if __name__ == "__main__":
    success, message = initialize_mt5()
    if not success:
        print(f"Failed to initialize: {message}")
    else:
        app.run(host="0.0.0.0", port=5000)
