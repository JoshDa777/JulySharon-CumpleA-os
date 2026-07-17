#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Normalize and decode path
        decoded_path = urllib.parse.unquote(self.path)
        if decoded_path.startswith('/'):
            decoded_path = decoded_path[1:]
        safe_path = decoded_path

        # API media endpoint
        if self.path == '/api/media':
            media_dir = 'imagenes regalo'
            files = []
            if os.path.exists(media_dir):
                for f in sorted(os.listdir(media_dir)):
                    file_path = os.path.join(media_dir, f)
                    if os.path.isfile(file_path):
                        ext = os.path.splitext(f)[1].lower()
                        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
                            file_type = 'image'
                        elif ext in ['.mp4', '.webm', '.ogg', '.mov', '.avi']:
                            file_type = 'video'
                        else:
                            continue
                        files.append({
                            'name': f,
                            'path': f'/imagenes%20regalo/{urllib.parse.quote(f)}',
                            'type': file_type
                        })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
            return

        # Root path default to index.html
        if safe_path == '':
            safe_path = 'index.html'

        # If file doesn't exist, 404
        if not os.path.exists(safe_path):
            self.send_error(404, f"File not found: {safe_path}")
            return

        # Special handling for GLB files
        if safe_path.lower().endswith('.glb'):
            self.send_response(200)
            self.send_header('Content-Type', 'model/gltf-binary')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(os.path.getsize(safe_path)))
            self.end_headers()
            with open(safe_path, 'rb') as f:
                self.wfile.write(f.read())
            return

        # For static files, let SimpleHTTPRequestHandler serve by path
        self.path = '/' + decoded_path
        return super().do_GET()

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == '.glb':
            return 'model/gltf-binary'
        return super().guess_type(path)

    def log_message(self, format, *args):
        # Quiet logging
        pass

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🎮 Servidor corriendo en http://localhost:{PORT}")
        print(f"❤️  Abre http://localhost:{PORT} para ver el regalo de Juli!")
        httpd.serve_forever()