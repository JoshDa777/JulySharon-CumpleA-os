#!/usr/bin/env python3
"""Genera media-list.json automáticamente escaneando la carpeta 'imagenes regalo'"""
import os
import json

MEDIA_DIR = 'imagenes regalo'
OUTPUT = 'media-list.json'

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
VIDEO_EXTS = {'.mp4', '.webm', '.ogg', '.mov', '.avi'}

files = []
if os.path.exists(MEDIA_DIR):
    for f in sorted(os.listdir(MEDIA_DIR)):
        file_path = os.path.join(MEDIA_DIR, f)
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
                'path': f'{MEDIA_DIR}/{f}',
                'type': file_type
            })

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

print(f'✅ Generado {OUTPUT} con {len(files)} archivos')
for m in files:
    print(f'   - {m["type"]}: {m["name"]}')