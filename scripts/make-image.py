#!/usr/bin/env python3
"""Generate a page illustration with the OpenAI image API and save it as WebP.

Usage: scripts/make-image.py <name> [--size 1024x1024] [--edit]
With --edit, the current images/<name>.webp is sent along and changed to match the prompt.
Reads OPENAI_API_KEY from the environment or from .env (never committed).
The prompt lives in scripts/prompts/<name>.txt; the result goes to images/<name>.webp.
"""
import argparse, base64, io, json, os, pathlib, urllib.request
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent

def api_key():
	if os.environ.get('OPENAI_API_KEY'):
		return os.environ['OPENAI_API_KEY']
	env = root / '.env'
	if env.exists():
		for line in env.read_text().splitlines():
			k, _, v = line.partition('=')
			if k.strip() == 'OPENAI_API_KEY':
				return v.strip().strip('"\'')
	raise SystemExit('OPENAI_API_KEY missing: add it to .env')

p = argparse.ArgumentParser()
p.add_argument('name')
p.add_argument('--size', default='1024x1024')
p.add_argument('--model', default='gpt-image-2')
p.add_argument('--edit', action='store_true')
args = p.parse_args()

prompt = (root / 'scripts' / 'prompts' / f'{args.name}.txt').read_text()
out = root / 'images' / f'{args.name}.webp'
fields = {'model': args.model, 'prompt': prompt, 'size': args.size, 'n': '1'}
if args.edit:
	png = io.BytesIO()
	Image.open(out).save(png, 'PNG')
	boundary = 'minhule-image-boundary'
	body = b''
	for k, v in fields.items():
		body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
	body += (f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{args.name}.png"\r\n'
		'Content-Type: image/png\r\n\r\n').encode() + png.getvalue() + f'\r\n--{boundary}--\r\n'.encode()
	url, content_type = 'https://api.openai.com/v1/images/edits', f'multipart/form-data; boundary={boundary}'
else:
	body = json.dumps({**fields, 'n': 1}).encode()
	url, content_type = 'https://api.openai.com/v1/images/generations', 'application/json'
req = urllib.request.Request(url, data=body, headers={'Authorization': f'Bearer {api_key()}', 'Content-Type': content_type})
with urllib.request.urlopen(req, timeout=300) as r:
	b64 = json.load(r)['data'][0]['b64_json']

Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB').save(out, 'WEBP', quality=82)
print(out)
