"""Static beauty journal. Run after adding data/<slug>.json and product assets."""
import json
import re
from pathlib import Path
from html import escape
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
SITE = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
def e(value):
    return escape(str(value), quote=True)

def image(p, it, prefix='', lazy=True):
    base = f"posts/{p['slug']}/img/{it['img']}"
    derivative = str(Path(base).with_suffix('.webp')).replace('\\', '/')
    src = derivative if (ROOT / derivative).exists() else base
    return f'<img src="{prefix}{e(src)}" alt="{e(it["name"])}" width="240" height="240" decoding="async" loading="{"lazy" if lazy else "eager"}">'

def page(title, body, path='', cover=''):
    up = '../../' if path else ''
    url = SITE['site_url'].rstrip('/') + '/' + path
    desc = '動画で気になったコスメを、クチコミとともに。楽天で買える美容アイテムを回ごとにまとめています。'
    notes = ''.join(f'<p>{e(n)}</p>' for n in SITE['notes'])
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}｜{e(SITE['name'])}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(SITE['site_url'])}/{e(cover)}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f8f5f1"><link rel="icon" href="{up}favicon.svg"><link rel="stylesheet" href="{up}style.css">
</head><body><a class="skip" href="#main">本文へ</a><div class="ad"><span>広告</span> 楽天アフィリエイトを利用しています</div>
<header class="masthead"><a href="{up or './'}" aria-label="らく美容コスメまとめ トップ"><span class="wordmark">mai<span class="dot">.</span></span><span class="mast-sub">らく美容コスメまとめ</span></a><span class="edition">BEAUTY JOURNAL</span></header>
<main id="main">{body}</main><footer><div class="footer-brand">mai. <span>気になるコスメを、ゆっくり選ぶ。</span></div><details><summary>広告・価格・クチコミについて</summary><p>リンク先で購入されると、紹介料を受け取ることがあります。</p>{notes}</details><p class="copyright">まい ｜ らく美容コスメまとめ</p></footer></body></html>'''

def post_html(p):
    items = p['items']
    jumps = ''.join(f'<a href="#item-{i}">{e(it["rank"])}<span>{e(it.get("brand", ""))}</span></a>' for i,it in enumerate(items))
    cards = []
    for i,it in enumerate(items):
        voices = it.get('voices', [it.get('copy', '')])
        positive = voices[:-1] if len(voices)>1 else voices
        caution = voices[-1] if len(voices)>1 else ''
        feedback = ''.join(f'<li>{e(v)}</li>' for v in positive)
        caution_html = f'<p class="caution"><span>気になる声</span>{e(caution)}</p>' if caution else ''
        url = it.get('affiliate_url') or 'https://hb.afl.rakuten.co.jp/ichiba/'+SITE['aff_id']+'/?'+urlencode({'pc':it['url'],'m':it['url']})
        words = ''.join(f'<span class="name-part">{e(w)}</span> ' for w in it.get('product', it['name']).split(' '))
        cards.append(f'''<article class="product-card {'winner' if it['rank']=='1位' else ''}" id="item-{i}">
<div class="product-top"><div class="product-photo"><span class="rank">{e(it['rank'])}</span>{image(p,it,'../../',i>1)}</div>
<div class="product-info"><p class="brand">{e(it.get('brand',''))}</p><h2>{words}</h2><p class="size">{e(it['size'])}</p><p class="price">¥{e(it['price'])}<span>税込・出典掲載価格</span></p></div></div>
<div class="review"><p class="review-label">{e(p.get("review_label", "クチコミの要約"))}</p><ul>{feedback}</ul>{caution_html}</div>
<a class="buy" href="{e(url)}" target="_blank" rel="nofollow sponsored noopener" aria-label="{e(it['name'])}：楽天で価格・在庫を見る（新しいタブ）">楽天で価格・在庫を見る <span aria-hidden="true">↗</span></a>
<p class="shop-note">販売価格・容量・送料はリンク先でご確認ください</p></article>''')
    omission = f'<p>{e(p["omission_note"])}</p>' if p.get('omission_note') else ''
    src = p['source']
    title = ''.join(f'<span>{e(s)}</span>' for s in p.get('title_lines',[p['title']]))
    body = f'''<div class="post-intro"><a class="back" href="../../">← 特集一覧</a><p class="eyebrow">THE COSME EDIT / {e(p['date'].replace('-','.'))}</p><h1>{title}</h1><p class="intro-text">{e(p['lead'])}</p><p class="count">{len(items):02d} ITEMS <span>動画で紹介した商品</span></p></div>
<nav class="jump" aria-label="順位から商品を探す"><p>見たい順位から選ぶ</p><div>{jumps}</div></nav>
<div class="selection-note">{omission}<p>価格は出典掲載時のものです。楽天の現在価格とは異なる場合があります。</p></div>
<section class="products" aria-label="紹介商品">{''.join(cards)}</section>
<section class="sources"><p class="eyebrow">SOURCE & NOTES</p><h2>この特集の出典</h2><a href="{e(src['url'])}" target="_blank" rel="noopener">{e(src['name'])} ↗</a><p>集計期間：{e(src['period'])}</p><p>{e(p.get('price_note',''))}</p></section><a class="all-link" href="../../">すべての特集を見る <span>→</span></a>'''
    return page(p['title'],body,f"posts/{p['slug']}/",f"posts/{p['slug']}/thumb.jpg")

def hub_html(posts):
    if not posts:
        return page('コスメ特集','<section class="hero"><h1>特集を準備しています。</h1></section>')
    latest = posts[0]
    picks = sorted(latest['items'],key=lambda it:int(re.sub(r'\D','',it['rank'])))[:3]
    still = ''.join(image(latest,it,lazy=False) for it in picks)
    entries = []
    for i,p in enumerate(posts):
        entries.append(f'''<a class="feature" href="posts/{e(p['slug'])}/"><div class="feature-cover"><img src="posts/{e(p['slug'])}/thumb.jpg" alt="動画の表紙" width="480" height="600" loading="lazy"></div><div><p class="eyebrow">{'LATEST EDIT' if i==0 else 'COSME EDIT'} / {e(p['date'].replace('-','.'))}</p><h3>{e(p['title'])}</h3><p>{len(p['items'])}品を紹介</p><span class="feature-cta">紹介アイテムを見る →</span></div></a>''')
    body = f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">MAI'S BEAUTY SELECTION</p><h1>気になった、を。<br><em>わたしの</em>コスメに。</h1><p>動画で出会ったコスメを、<br>クチコミと一緒に、ゆっくり選ぶ。</p><a href="posts/{e(latest['slug'])}/" class="hero-link">最新の紹介アイテムを見る <span>↗</span></a></div><div class="still-life">{still}<span class="still-caption">FROM THE LATEST EDIT</span></div></section>
<section class="edits"><div class="section-title"><div><p class="eyebrow">THE EDITS</p><h2>動画から、探す。</h2></div><span>{len(posts):02d} EDITS</span></div>{''.join(entries)}</section>
<section class="about"><p class="eyebrow">OUR POINT OF VIEW</p><h2>良かった声も、<br>合わなかった声も。</h2><p>売れているコスメを、公開クチコミから読み解く。<br>自分に合う一本を選ぶ、そのきっかけに。</p><p class="about-note">コメントはクチコミの要約です。<br>まい本人の使用体験ではありません。</p></section>'''
    return page('動画で紹介したコスメ',body,cover=f"posts/{latest['slug']}/thumb.jpg")

def main():
    posts = [json.loads(f.read_text(encoding='utf-8')) for f in sorted((ROOT/'data').glob('*.json'))]
    posts.sort(key=lambda p:p['date'],reverse=True)
    for p in posts:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']):
            raise ValueError('Invalid slug')
        target = ROOT/'posts'/p['slug']
        target.mkdir(parents=True,exist_ok=True)
        (target/'index.html').write_text(post_html(p),encoding='utf-8')
    (ROOT/'index.html').write_text(hub_html(posts),encoding='utf-8')
    print(f'Built {len(posts)} posts and index')

if __name__=='__main__':
    main()
