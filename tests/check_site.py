"""Smoke-check the actual Jekyll output, including retained public URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
errors = []
required = ['index.html', '404.html', 'feed.xml',
            '2020-01-05-frost-paper/index.html', '2021-04-28-xai-for-nlp/index.html']
for name in required:
    if not (root / name).is_file():
        errors.append(f'Missing preserved route: {name}')

for route in ('aboutme', 'tags'):
    if not any((root / name).is_file() for name in (f'{route}.html', f'{route}/index.html')):
        errors.append(f'Missing preserved route: /{route}')

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.h1, self.main = [], set(), 0, 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.h1 += tag == 'h1'
        self.main += tag == 'main'
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'img' and 'alt' not in attrs:
            errors.append('Image missing alt text')
        if tag == 'iframe' and not attrs.get('title'):
            errors.append('Iframe missing title')

pages = {}
for file in root.rglob('*.html'):
    page = Page()
    text = file.read_text()
    page.feed(text)
    pages[file] = page
    if page.h1 != 1 or page.main != 1:
        errors.append(f'{file.relative_to(root)}: expected one h1 and main, got {page.h1}/{page.main}')
    if '{{' in text or '{%' in text:
        errors.append(f'Unrendered Liquid in {file.relative_to(root)}')
    if 'jquery' in text.lower() or 'bootstrap.min' in text.lower():
        errors.append(f'Legacy runtime dependency in {file.relative_to(root)}')

for file, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        path = unquote(url.path)
        target = (root / path.lstrip('/') if path.startswith('/') else file.parent / path).resolve() if path else file
        candidates = [target, target / 'index.html', target.with_suffix('.html')]
        target = next((p for p in candidates if p.is_file()), None)
        if target is None:
            errors.append(f'{file.relative_to(root)}: missing local link {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{file.relative_to(root)}: missing anchor {link}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'Checked {len(pages)} HTML pages: preserved routes, links, landmarks, image alt text and embeds pass.')
