#!/usr/bin/env python3
"""
Rasooi - Fooding Made Easy
Dedicated Homestyle Tiffin Service for Off-Campus Students
Serving Law Gate, Green Valley, Hardaspur & Nearby PGs
WhatsApp: +91 97078 89516
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")

class RasooiHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json_response(self, data, status_code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        # Health endpoint
        if parsed.path == "/api/health":
            self._send_json_response({
                "status": "online",
                "brand": "Rasooi",
                "tagline": "Fooding Made Easy",
                "whatsapp": "9707889516",
                "coverage": "Law Gate, Green Valley, Hardaspur & Nearby Off-Campus PGs (Not in LPU campus)",
                "hub": "Shop 14, Main Market, Law Gate, Phagwara",
                "refundableTiffinSecurityDeposit": 1000,
                "firstTimeUserSecurityFee": "₹1,000 (100% Refundable Tiffin Container Deposit)",
                "plans": {
                    "onetime_veg": "₹2,599/month (Lunch: 12:30-2:00 PM OR Dinner: 8:00-9:00 PM)",
                    "onetime_nonveg": "₹2,999/month (Lunch: 12:30-2:00 PM OR Dinner: 8:00-9:00 PM)"
                },
                "paymentLinks": {
                    "veg": "https://rzp.io/rzp/ALIkEfoh",
                    "nonveg": "https://rzp.io/rzp/5T62orL"
                },
                "servingHours": {
                    "lunch": "12:30 PM - 2:00 PM",
                    "dinner": "8:00 PM - 9:00 PM"
                }
            })
            return

        # Menu and Plans endpoint (Strictly Monthly Subscriptions)
        if parsed.path == "/api/menu":
            self._send_json_response({
                "success": True,
                "brand": "Rasooi",
                "tagline": "Fooding Made Easy",
                "whatsapp": "+91 97078 89516",
                "businessModel": "100% Monthly Subscription Only (No daily orders)",
                "refundableTiffinSecurityDeposit": 1000,
                "firstTimeUserSecurityFee": "₹1,000 (100% Refundable Tiffin Container Deposit)",
                "areasServed": ["Law Gate", "Green Valley", "Hardaspur", "Maheru PGs"],
                "plans": [
                    {
                        "id": "sub-1time-veg",
                        "name": "1-Time Daily Pure Veg Monthly Plan",
                        "price": 2599,
                        "duration": "30 Days (Lunch: 12:30-2:00 PM OR Dinner: 8:00-9:00 PM)",
                        "diet": "veg",
                        "perMeal": "₹86 / meal",
                        "razorpayLink": "https://rzp.io/rzp/ALIkEfoh",
                        "refundableDeposit": 1000,
                        "description": "Weekly: 2 Din Paneer (Wed & Sun) + 5 Din Daily Market Fresh Sabzis (Aloo Gobi, Bhindi, Mix Veg), Dal, 4 Ghee Phulkas, Rice, Salad & Sunday Sweet."
                    },
                    {
                        "id": "sub-1time-nonveg",
                        "name": "1-Time Daily Non-Veg Delight Monthly Plan",
                        "price": 2999,
                        "duration": "30 Days (Lunch: 12:30-2:00 PM OR Dinner: 8:00-9:00 PM)",
                        "diet": "non-veg",
                        "perMeal": "₹99 / meal",
                        "razorpayLink": "https://rzp.io/rzp/5T62orL",
                        "refundableDeposit": 1000,
                        "description": "Weekly: 3 Din Chicken, 1 Din Anda, 1 Din Fish ya Paneer, plus Pure Veg on other days. 4 Ghee Phulkas, Rice & Salad."
                    },
                    {
                        "id": "sub-full-veg",
                        "name": "Full Board Pure Veg Monthly Pass",
                        "price": 4899,
                        "duration": "30 Days (Lunch + Dinner - 60 Meals)",
                        "diet": "veg"
                    },
                    {
                        "id": "sub-full-nonveg",
                        "name": "Full Board Non-Veg Club Monthly Pass",
                        "price": 5699,
                        "duration": "30 Days (Lunch + Dinner - 60 Meals)",
                        "diet": "non-veg"
                    }
                ]
            })
            return

        # Orders list endpoint
        if parsed.path == "/api/orders":
            try:
                with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                    orders = json.load(f)
                self._send_json_response(orders)
            except Exception as e:
                self._send_json_response({"error": str(e)}, 500)
            return

        # Specific order status endpoint /api/orders/<id>
        if parsed.path.startswith("/api/orders/"):
            order_id = parsed.path.split("/")[-1].upper()
            try:
                with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                    orders = json.load(f)
                match = next((o for o in orders if o.get("id", "").upper() == order_id or o.get("id", "").upper() == f"RASOOI-{order_id}"), None)
                if match:
                    self._send_json_response(match)
                else:
                    self._send_json_response({"error": "Order not found", "queryId": order_id}, 404)
            except Exception as e:
                self._send_json_response({"error": str(e)}, 500)
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/orders":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                new_order = json.loads(post_data.decode("utf-8"))
                with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                    orders = json.load(f)

                orders.insert(0, new_order)

                with open(ORDERS_FILE, "w", encoding="utf-8") as f:
                    json.dump(orders, f, indent=2)

                self._send_json_response({
                    "status": "success",
                    "brand": "Rasooi",
                    "whatsapp": "9707889516",
                    "message": "Order placed successfully with Rasooi - Fooding Made Easy!",
                    "order": new_order
                }, 201)
            except Exception as e:
                self._send_json_response({"error": "Failed to process order", "details": str(e)}, 400)
            return

        self._send_json_response({"error": "Endpoint not found"}, 404)


def run_server(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RasooiHandler)
    print("=" * 68)
    print("  🍲 Rasooi — Fooding Made Easy")
    print("  Dedicated Homestyle Tiffin Service for Off-Campus Students")
    print("  📍 Serving: Law Gate • Green Valley • Hardaspur & Nearby PGs")
    print("  📱 WhatsApp Orders & Support: +91 97078 89516")
    print("  🌟 1-Time Daily Plans: Veg @ ₹2,599 | Non-Veg @ ₹2,999")
    print("  📦 First-Time User Deposit: ₹1,000 (100% Refundable Tiffin Container Fee)")
    print("  ⏰ Serving Hours: Lunch (12:30-2:00 PM) | Dinner (8:00-9:00 PM)")
    print(f"  🌐 Running locally at: http://localhost:{port}")
    print("  📁 Hub Location: Shop 14, Main Market, Law Gate, Phagwara")
    print("=" * 68)
    print("  Press Ctrl+C to stop the server\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  🛑 Shutting down server gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
