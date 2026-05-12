"""Add hreflang links to existing KR zodiac pages."""
import os, re

ANIMALS = ['rat','ox','tiger','rabbit','dragon','snake','horse','goat','monkey','rooster','dog','pig']
PUBLIC = os.path.join(os.path.dirname(__file__), '..', 'public')

def add_hreflang(file_path, kr_url, en_url):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'hreflang' in content:
        print(f"  Skip (already has hreflang): {file_path}")
        return False
    hreflang = f'\n    <link rel="alternate" hreflang="ko" href="{kr_url}">\n    <link rel="alternate" hreflang="en" href="{en_url}">'
    # Insert after canonical
    content = re.sub(
        r'(<link rel="canonical"[^>]+>)',
        r'\1' + hreflang,
        content,
        count=1
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Updated: {file_path}")
    return True

count = 0

# Zodiac index
idx = os.path.join(PUBLIC, 'zodiac', 'index.html')
if os.path.exists(idx):
    if add_hreflang(idx, 'https://saju.gon.ai.kr/zodiac/', 'https://saju.gon.ai.kr/en/zodiac/'):
        count += 1

# Individual animals
for animal in ANIMALS:
    p = os.path.join(PUBLIC, 'zodiac', animal, 'index.html')
    if os.path.exists(p):
        if add_hreflang(p, f'https://saju.gon.ai.kr/zodiac/{animal}/', f'https://saju.gon.ai.kr/en/zodiac/{animal}/'):
            count += 1

print(f"\nUpdated {count} KR pages with hreflang links")
