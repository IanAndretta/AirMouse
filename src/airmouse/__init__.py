from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess

class MouseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if 'x' in query_params and 'y' in query_params:
            try:
                # ydotool expects integers for pixels
                x = int(float(query_params['x'][0]))
                y = int(float(query_params['y'][0]))

                # '--' is crucial so negative numbers aren't treated as invalid command flags
                result = subprocess.run(
                    ['ydotool', 'mousemove', '--absolute', '-x', str(x), '-y', str(y)], 
                    capture_output=True, 
                    text=True
                )
                
                # If ydotoold isn't running or requires sudo, print the error to terminal
                if result.returncode != 0:
                    print(f"ydotool error: {result.stderr.strip()}")

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                print(f"Script error: {e}")
        else:
            self.send_response(400)
            self.end_headers()

    # Suppress the terminal logging for every single request to keep it fast
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, MouseHandler)
    print("Server running on port 8000...")
    print("Test on your PC first: http://localhost:8000/?x=10&y=5")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()