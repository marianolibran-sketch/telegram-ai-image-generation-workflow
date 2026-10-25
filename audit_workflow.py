#!/usr/bin/env python3
"""Basic offline privacy checks for this public n8n workflow.

This is a screening tool, NOT proof that the export contains no secrets.
Run: python3 audit_workflow.py
"""
from pathlib import Path
import json
import re
import sys

FILE = Path(__file__).resolve().parent / "affiliate-content-bot.json"
REQUIRED_PLACEHOLDERS = {"YOUR_CLOUDFLARE_ACCOUNT_ID", "YOUR_TELEGRAM_CHAT_ID"}
SECRET_PATTERNS = {
    "Telegram bot token": re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{25,}\b"),
    "Bearer token": re.compile(r"(?i)\bBearer\s+(?!YOUR_|TU_TOKEN|<)[A-Za-z0-9._~-]{16,}"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{10,}"),
    "Possible email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "Hard-coded long numeric ID": re.compile(r"(?<![\w-])\d{9,14}(?![\w-])"),
    "Private/local/tunnel URL": re.compile(r"(?i)https?://[^\s\"']*(?:ngrok|trycloudflare|localhost|127\.0\.0\.1|loca\.lt|duckdns)[^\s\"']*"),
    "Cloudflare-looking account ID in URL": re.compile(r"https://api\.cloudflare\.com/client/v4/accounts/(?!YOUR_CLOUDFLARE_ACCOUNT_ID)[a-fA-F0-9]{16,}/"),
    "API token in query": re.compile(r"(?i)[?&](?:api[_-]?key|access[_-]?token|secret)=([A-Za-z0-9._-]{10,})"),
}

issues=[]
try:
    doc=json.loads(FILE.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    sys.exit(f"FAIL: Invalid/unreadable workflow JSON ({type(exc).__name__})")

if not isinstance(doc.get('nodes'), list) or not isinstance(doc.get('connections'), dict):
    issues.append('Missing nodes or connections')
if doc.get('pinData'):
    issues.append('Pinned execution data is present: remove it before publishing')
if doc.get('staticData'):
    issues.append('Static workflow data is present')
if doc.get('active'):
    issues.append('Public template is activated')
if doc.get('id'):
    issues.append('Source instance workflow ID is present')

names=[node.get('name') for node in doc.get('nodes', [])]
if len(names)!=len(set(names)):
    issues.append('Duplicate node names')

for node in doc.get('nodes', []):
    name=node.get('name','<unnamed>')
    if node.get('credentials'):
        issues.append(f'Credential binding remains in node: {name}')
    if node.get('webhookId'):
        issues.append(f'Instance webhook ID remains in node: {name}')
    if node.get('pinData'):
        issues.append(f'Pinned data in node: {name}')
    if node.get('type','').endswith('httpRequest'):
        url=node.get('parameters',{}).get('url','')
        if not url.startswith('https://api.cloudflare.com/client/v4/accounts/YOUR_CLOUDFLARE_ACCOUNT_ID/'):
            issues.append(f'Unexpected HTTP destination or Cloudflare ID: {name}')

def strings(value, path='$'):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from strings(item, path+'.'+key)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            yield from strings(item, f'{path}[{idx}]')
    elif isinstance(value, str):
        yield path,value

all_text='\n'.join(value for _,value in strings(doc))
for literal in sorted(REQUIRED_PLACEHOLDERS):
    if literal not in all_text:
        issues.append(f'Missing mandatory placeholder: {literal}')
for path,value in strings(doc):
    for label,regex in SECRET_PATTERNS.items():
        if regex.search(value):
            issues.append(f'{label} detected at {path} (value intentionally hidden)')

for source, branches in doc.get('connections',{}).items():
    if source not in names:
        issues.append(f'Unknown connection source: {source}')
    for edge_list in branches.values():
        for edges in edge_list:
            for edge in edges:
                if edge.get('node') not in names:
                    issues.append(f'Unknown destination from: {source}')

if issues:
    print('FAIL: workflow needs review')
    for issue in issues:
        print(' -',issue)
    sys.exit(1)
print(f'PASS: {len(names)} nodes; no credentials, pins, or known sensitive patterns detected.')
print('IMPORTANT: this automated scan cannot guarantee absence of all secrets.')
