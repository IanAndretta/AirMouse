import enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from subprocess import run

# Define the enum
class Mode(enum.Enum):
    YDOTOOL = 0
    XDOTOOL = 1

# Set your current mode here (or import it from mode.py)
CURRENT_MODE = Mode.YDOTOOL 

PORT = 8000

class MouseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Check which actions are requested
        has_move = 'x' in query_params and 'y' in query_params
        has_click = 'click' in query_params

        if has_move or has_click:
            try:
                # 1. Handle Mouse Movement
                if has_move:
                    x = int(float(query_params['x'][0]))
                    y = int(float(query_params['y'][0]))

                    if CURRENT_MODE == Mode.YDOTOOL:
                        move_cmd = ['ydotool', 'mousemove', '--absolute', '-x', str(x), '-y', str(y)]
                        tool_name = "ydotool"
                    elif CURRENT_MODE == Mode.XDOTOOL:
                        move_cmd = ['xdotool', 'mousemove', str(x), str(y)]
                        tool_name = "xdotool"
                    else:
                        raise ValueError(f"Unknown mode: {CURRENT_MODE}")

                    move_result = run(move_cmd, capture_output=True, text=True)
                    if move_result.returncode != 0:
                        print(f"{tool_name} move error: {move_result.stderr.strip()}")

                # 2. Handle Mouse Click
                if has_click:
                    click_type = query_params['click'][0].lower()
                    
                    if click_type in ['left', '1', 'true']:
                        if CURRENT_MODE == Mode.YDOTOOL:
                            # 0xC0 is the evdev code for BTN_LEFT used by ydotool
                            click_cmd = ['ydotool', 'click', '0xC0']
                            tool_name = "ydotool"
                        elif CURRENT_MODE == Mode.XDOTOOL:
                            # 1 is the left click button for xdotool
                            click_cmd = ['xdotool', 'click', '1']
                            tool_name = "xdotool"
                        
                        click_result = run(click_cmd, capture_output=True, text=True)
                        if click_result.returncode != 0:
                            print(f"{tool_name} click error: {click_result.stderr.strip()}")

                # Send success response once actions are complete
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"OK")
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                print(f"Script error: {e}")
        else:
            # Bad request if neither movement nor click was provided
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing x/y coordinates or click parameter")

    # Suppress the terminal logging for every single request to keep it fast
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, MouseHandler)
    
    print(f"Server running on port {PORT}...")
    print(f"Active Mode: {CURRENT_MODE.name}")
    print(f"Link: http://localhost:{PORT}/?x=100&y=100&click=left")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()