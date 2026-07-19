#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8000

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
VIDEO_EXTS = {'.mp4', '.webm', '.ogg', '.mov', '.avi'}

def scan_media_folder():
    """Scan the imagenes regalo folder and return list of media files."""
    media_dir = 'imagenes regalo'
    files = []
    if os.path.exists(media_dir):
        for f in sorted(os.listdir(media_dir)):
            file_path = os.path.join(media_dir, f)
            if os.path.isfile(file_path):
                ext = os.path.splitext(f)[1].lower()
                if ext in IMAGE_EXTS:
                    file_type = 'image'
                elif ext in VIDEO_EXTS:
                    file_type = 'video'
                else:
                    continue
                files.append({
                    'name': f,
                    'path': f'imagenes regalo/{f}',
                    'type': file_type
                })
    return files

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        decoded_path = urllib.parse.unquote(self.path)
        if decoded_path.startswith('/'):
            decoded_path = decoded_path[1:]
        safe_path = decoded_path

        # API media endpoint - dynamic scan
        if self.path in ['/api/media', '/media-list.json']:
            files = scan_media_folder()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(files, ensure_ascii=False, indent=2).encode('utf-8'))
            return

        # Root path default to index.html
        if safe_path == '':
            safe_path = 'index.html'

        # If file doesn't exist, 404
        if not os.path.exists(safe_path) and not safe_path.startswith('imagenes%20regalo'):
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
        pass

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🎮 Servidor corriendo en http://localhost:{PORT}")
        print(f"❤️  Abre http://localhost:{PORT} para ver el regalo de Juli!")
        print(f"📸 Detecta automáticamente los archivos en 'imagenes regalo/'")
        httpd.serve_forever()