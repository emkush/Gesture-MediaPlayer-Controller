from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
from urllib.parse import urlparse, parse_qs

class GestureAPIHandler(BaseHTTPRequestHandler):
    # Class variable to store the latest gesture
    latest_gesture = None
    gesture_timestamp = 0
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/gesture':
            # Return latest gesture
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'gesture': self.latest_gesture,
                'timestamp': self.gesture_timestamp,
                'status': 'success'
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif parsed_url.path == '/status':
            # Return server status
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'running',
                'latest_gesture': self.latest_gesture,
                'timestamp': self.gesture_timestamp
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/gesture':
            # Receive gesture from Python script
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                GestureAPIHandler.latest_gesture = data.get('gesture')
                GestureAPIHandler.gesture_timestamp = time.time()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {'status': 'received', 'gesture': data.get('gesture')}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Reduce server logging noise
        return

def start_api_server(port=8081):
    """Start the HTTP API server"""
    server = HTTPServer(('localhost', port), GestureAPIHandler)
    print(f"Gesture API server starting on http://localhost:{port}")
    print("Endpoints:")
    print(f"  GET  http://localhost:{port}/status - Server status")
    print(f"  GET  http://localhost:{port}/gesture - Latest gesture")
    print(f"  POST http://localhost:{port}/gesture - Send gesture")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    start_api_server()
