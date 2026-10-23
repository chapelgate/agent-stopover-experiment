from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
root=Path(__file__).resolve().parent
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('a','script','link','iframe') and (a.get('href') or a.get('src')): self.links.append((tag,a.get('href') or a.get('src')))
fail=[]
for file in root.glob('*.html'):
 p=Links()
 try:p.feed(file.read_text(encoding='utf-8-sig'))
 except Exception as e:fail.append((file.name,'parse',str(e)));continue
 for tag,link in p.links:
  if not link or link.startswith(('#','http:','https:','mailto:','tel:','data:','javascript:','//')):continue
  target=link.split('#')[0].split('?')[0]
  if target and not (root/target).exists():fail.append((file.name,tag,link))
for file in root.glob('*.json'):
 try:json.loads(file.read_text(encoding='utf-8-sig'))
 except Exception as e:fail.append((file.name,'json',str(e)))
print('HTML',len(list(root.glob('*.html'))),'JSON',len(list(root.glob('*.json'))),'FAILURES',len(fail))
for f in fail:print('FAIL',*f)
sys.exit(bool(fail))
