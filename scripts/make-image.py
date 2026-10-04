#!/usr/bin/env python3
"""Generate a page illustration with the OpenAI image API and save it as WebP.

Usage: scripts/make-image.py <name> [--size 1024x1024]
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
args = p.parse_args()

prompt = (root / 'scripts' / 'prompts' / f'{args.name}.txt').read_text()
req = urllib.request.Request(
	'https://api.openai.com/v1/images/generations',
	data=json.dumps({'model': args.model, 'prompt': prompt, 'size': args.size, 'n': 1}).encode(),
	headers={'Authorization': f'Bearer {api_key()}', 'Content-Type': 'application/json'},
)
with urllib.request.urlopen(req, timeout=300) as r:
	b64 = json.load(r)['data'][0]['b64_json']

out = root / 'images' / f'{args.name}.webp'
Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB').save(out, 'WEBP', quality=82)
print(out)
