# -*- coding: utf-8 -*-
"""リンクまとめページを組み立てる。

  python build_link.py

  site.json          サイト共通（名前・プロフ・ことわり・アフィID）
  data/<slug>.json   動画1本ぶん
  posts/<slug>/img/  その回の商品画像
  posts/<slug>/thumb.jpg  一覧に出す表紙（動画の4:5表紙を幅480に縮めたもの）

出力は index.html（一覧）と posts/<slug>/index.html（1本ぶん）。
新しい動画を出したら data に1つJSONを足して、これを流すだけ。
"""
import io, json, glob, os, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(io.open(os.path.join(ROOT, "site.json"), encoding="utf-8"))


def aff(url):
    q = urllib.parse.urlencode({"pc": url, "m": url})
    return "https://hb.afl.rakuten.co.jp/ichiba/%s/?%s" % (SITE["aff_id"], q)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def product_image(path, alt):
    """Prefer the small WebP derivative when it has been prepared."""
    webp = os.path.splitext(path)[0] + ".webp"
    if os.path.exists(os.path.join(ROOT, "posts", CURRENT_SLUG, "img", webp)):
        return '<picture><source srcset="img/%s" type="image/webp"><img src="img/%s" alt="%s"></picture>' % (webp, path, esc(alt))
    return '<img src="img/%s" alt="%s">' % (path, esc(alt))


CSS = """
:root{--ink:#322635;--muted:#786a78;--pink:#fcebf3;--pink-deep:#f5c8dc;--red:#df2945;--red-dark:#b91835;--aqua:#63cce9;--gold:#f6b946;--paper:#fffdfd;--shadow:0 10px 26px rgba(112,51,82,.13)}
*{box-sizing:border-box} body{margin:0;color:var(--ink);font-family:"M PLUS Rounded 1c","Hiragino Maru Gothic ProN","Hiragino Kaku Gothic ProN",system-ui,sans-serif;background-color:#fbe7f0;background-image:linear-gradient(45deg,rgba(255,255,255,.48) 25%%,transparent 25%%),linear-gradient(-45deg,rgba(255,255,255,.48) 25%%,transparent 25%%),linear-gradient(45deg,transparent 75%%,rgba(255,255,255,.48) 75%%),linear-gradient(-45deg,transparent 75%%,rgba(255,255,255,.48) 75%%);background-size:28px 28px;background-position:0 0,0 14px,14px -14px,-14px 0}
.w{max-width:560px;margin:0 auto;padding:18px 14px 52px}.pr{display:inline-flex;align-items:center;gap:5px;background:var(--red);color:#fff;font-weight:800;font-size:12px;padding:6px 13px;border-radius:999px;letter-spacing:.04em;box-shadow:0 4px 10px rgba(203,25,61,.18)}.pr:before{content:"●";font-size:8px}
.head{position:relative;display:flex;gap:12px;align-items:center;background:rgba(255,253,253,.94);border:1px solid rgba(255,255,255,.9);border-radius:23px;padding:14px;margin:12px 0 14px;box-shadow:var(--shadow);overflow:hidden}.head:after{content:"";position:absolute;width:105px;height:105px;right:-43px;top:-48px;border-radius:50%%;background:#d8f5fc}.head img{position:relative;z-index:1;width:64px;height:64px;object-fit:contain;flex:none;border-radius:50%%;background:#fff2f7;padding:3px}h1{font-size:21px;margin:0;line-height:1.35;letter-spacing:.02em}.lead{font-size:13px;color:var(--muted);margin:0 0 14px;line-height:1.75}.eyebrow{font-family:system-ui,sans-serif;font-size:10px;font-weight:900;letter-spacing:.12em;color:var(--red);margin:0 0 3px}.post-info{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 13px}.chip{display:inline-flex;align-items:center;font-size:11px;font-weight:800;background:rgba(255,253,253,.8);padding:5px 8px;border-radius:999px;color:#665767}.chip.aqua{background:#dff6fc;color:#277b96}.notice{background:#fff8dc;border:1px solid #f5dc95;border-radius:14px;padding:9px 11px;font-size:11.5px;color:#725c36;line-height:1.55;margin:-2px 0 13px}
.c{position:relative;display:grid;grid-template-columns:82px minmax(0,1fr) 76px;gap:9px;align-items:center;background:var(--paper);border:1px solid rgba(255,255,255,.9);border-radius:20px;padding:10px 9px 10px 10px;margin-bottom:10px;text-decoration:none;color:inherit;box-shadow:0 5px 0 rgba(137,70,101,.08),var(--shadow);transition:transform .16s,box-shadow .16s}.c:hover{transform:translateY(-2px);box-shadow:0 7px 0 rgba(137,70,101,.09),0 15px 30px rgba(112,51,82,.17)}.c img{width:82px;height:106px;object-fit:contain;flex:none}.t{min-width:0;align-self:stretch;display:flex;flex-direction:column;justify-content:center}.r{display:inline-flex;align-self:flex-start;color:#fff;font-family:system-ui,sans-serif;font-weight:900;font-size:11px;padding:3px 9px;border-radius:999px;background:var(--aqua);box-shadow:inset 0 -2px rgba(0,0,0,.08)}.rank-1 .r{background:linear-gradient(135deg,#f5b331,#e99322)}.rank-2 .r{background:linear-gradient(135deg,#aac2cf,#7898aa)}.rank-3 .r{background:linear-gradient(135deg,#eab18a,#bd7854)}.brand{display:block;margin-top:4px;font-size:11px;font-weight:900;letter-spacing:.04em;color:#917386}.product{display:block;font-size:13px;line-height:1.38;font-weight:900;overflow-wrap:anywhere}.p{display:block;margin-top:4px;font-size:16px;font-family:system-ui,sans-serif;font-weight:900;letter-spacing:-.02em}.p em{font-family:inherit;font-style:normal;font-size:10px;color:var(--muted);font-weight:700;letter-spacing:0}.review-label{display:block;margin-top:4px;font-size:9px;font-weight:800;letter-spacing:.05em;color:#a08495}.voices{margin:2px 0 0;padding:0;list-style:none;font-size:10.5px;line-height:1.35;color:#635562}.voices li{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.voices li:before{content:"✦";font-size:8px;color:#ec8fae;margin-right:3px}.voices .caution:before{content:"!";display:inline-grid;place-items:center;width:10px;height:10px;border-radius:50%%;background:#f8d477;color:#755d2a;font-weight:900;margin-right:3px}.go{align-self:center;display:grid;place-items:center;width:70px;min-height:70px;border-radius:50%%;background:linear-gradient(145deg,#ed4560,var(--red-dark));color:#fff;font-size:10px;line-height:1.25;text-align:center;font-weight:900;box-shadow:0 5px 10px rgba(201,29,61,.24)}.go:after{content:"↗";font-family:system-ui;font-size:13px;line-height:1}
.pc{display:grid;grid-template-columns:88px minmax(0,1fr) 24px;gap:12px;align-items:center;background:var(--paper);border-radius:20px;padding:10px;margin-bottom:11px;text-decoration:none;color:inherit;box-shadow:var(--shadow);border:1px solid rgba(255,255,255,.9)}.pc img{width:88px;height:110px;object-fit:cover;border-radius:13px;flex:none}.pc b{font-size:16px;line-height:1.35;display:block}.pc .d{display:block;margin-top:6px;font-size:11px;font-weight:700;color:var(--muted)}.pc:after{content:"›";font-family:system-ui;font-size:28px;color:var(--red);font-weight:300}.back{display:inline-block;margin:9px 0 0;font-size:13px;font-weight:800;color:#75586a;text-decoration:none}.note{background:rgba(255,253,253,.92);border-radius:20px;padding:16px;margin-top:20px;font-size:11.5px;color:var(--muted);line-height:1.85;box-shadow:var(--shadow)}.note b{color:var(--ink)}a.src{color:#8b5e76;word-break:break-all}@media(max-width:370px){.c{grid-template-columns:70px minmax(0,1fr) 62px;gap:7px}.c img{width:70px;height:100px}.go{width:59px;min-height:59px;font-size:9px}.product{font-size:12px}.voices{font-size:9.5px}}
"""

PAGE = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title><meta name="description" content="%(description)s">
<meta property="og:type" content="website"><meta property="og:site_name" content="%(site_name)s"><meta property="og:title" content="%(title)s"><meta property="og:description" content="%(description)s"><meta property="og:url" content="%(canonical)s">%(og_image)s
<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="%(up)sfavicon.svg" type="image/svg+xml">
<style>%(css)s</style></head><body><div class="w">
<span class="pr">広告（楽天アフィリエイト）</span>
<div class="head"><img src="%(up)s%(icon)s" alt="">
<div><h1>%(h1)s</h1>%(tagline)s</div></div>
%(body)s
<div class="note">
%(notes)s
</div></div></body></html>
"""


def head_note():
    return "<b>このページについて</b><br>リンクは楽天アフィリエイトの広告です。" \
           "押して購入されると、紹介料を受け取ることがあります。"


def post_html(p):
    global CURRENT_SLUG
    CURRENT_SLUG = p["slug"]
    rows = []
    for it in p["items"]:
        rank_class = "rank-" + it["rank"].replace("位", "")
        voices = it.get("voices", [it["copy"]])
        voice_html = "".join('<li%s>%s</li>' % (' class="caution"' if i == len(voices)-1 and len(voices) > 1 else '', esc(v)) for i, v in enumerate(voices))
        rows.append(
            '  <a class="c %s" href="%s" target="_blank" rel="nofollow sponsored noopener">\n'
            '    %s\n'
            '    <div class="t"><span class="r">%s</span><span class="brand">%s</span><span class="product">%s</span>\n'
            '      <span class="p">¥%s <em>出典掲載時の税込／%s</em></span><span class="review-label">クチコミの要約</span><ul class="voices">%s</ul></div>\n'
            '    <span class="go">楽天で<br>商品を見る</span>\n'
            '  </a>' % (rank_class, aff(it["url"]), product_image(it["img"], it["name"]), esc(it["rank"]), esc(it.get("brand", "")), esc(it.get("product", it["name"])), it["price"], esc(it["size"]), voice_html))
    info = '<div class="post-info"><span class="chip aqua">楽天で買える8品</span><span class="chip">売上順位は出典どおり</span></div><div class="notice">4位・8位は楽天で取り扱いを確認できなかったため、掲載していません。</div>'
    body = '<p class="lead">%s</p>%s\n%s\n<a class="back" href="../../">← ほかのランキングを見る</a>' % (
        esc(p["lead"]), info, "\n".join(rows))

    src = p["source"]
    notes = [head_note(), "<b>出典</b><br>%s<br><a class=\"src\" href=\"%s\" target=\"_blank\" "
             "rel=\"noopener\">%s</a><br>集計期間：%s" % (
                 esc(src["name"]), src["url"],
                 urllib.parse.urlparse(src["url"]).netloc, esc(src["period"]))]
    n0 = SITE["notes"][0]
    if p.get("price_note"):
        n0 = n0.replace("の記載です。", "の記載です" + p["price_note"] + "。")
    notes.append(n0 + "<br>" + "<br>".join(SITE["notes"][1:]))
    description = "%s｜楽天で買える商品を順位どおりにまとめています。" % p["title"]
    return PAGE % dict(
        title="%s｜%s" % (SITE["name"], p["title"]), css=CSS % {"up": "../../"}, up="../../",
        icon=SITE["icon"],
        tagline='<p class="lead" style="margin:4px 0 0">%s</p>' % esc(SITE["name"]),
        h1=esc(p["title"]),
        body=body, notes="<br><br>".join(notes), description=esc(description), site_name=esc(SITE["name"]), canonical=SITE["site_url"]+"/posts/"+p["slug"]+"/", og_image='<meta property="og:image" content="%s/posts/%s/thumb.jpg">' % (SITE["site_url"], p["slug"]))


def hub_html(posts):
    rows = []
    for p in posts:
        rows.append(
            '  <a class="pc" href="posts/%s/">\n'
            '    <img src="posts/%s/thumb.jpg" alt="">\n'
            '    <div><b>%s</b><span class="d">%s ／ %d品</span></div>\n'
            '  </a>' % (p["slug"], p["slug"], esc(p["title"]),
                        p["date"].replace("-", "."), len(p["items"])))
    body = '<p class="lead">%s</p>\n%s' % (esc(SITE["desc"]), "\n".join(rows))
    notes = [head_note(), "<br>".join(SITE["notes"]),
             "出典と集計期間は、それぞれの回のページに書いています。"]
    description = "動画で紹介した、楽天で買える美容アイテムを回ごとにまとめています。"
    return PAGE % dict(title=SITE["name"], css=CSS % {"up": ""}, up="",
                       icon=SITE["icon"], tagline="",
                       h1=esc(SITE["name"]), body=body, notes="<br><br>".join(notes), description=description, site_name=esc(SITE["name"]), canonical=SITE["site_url"]+"/", og_image='<meta property="og:image" content="%s/posts/%s/thumb.jpg">' % (SITE["site_url"], posts[0]["slug"]) if posts else "")


def main():
    posts = [json.load(io.open(f, encoding="utf-8"))
             for f in sorted(glob.glob(os.path.join(ROOT, "data", "*.json")))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    for p in posts:
        d = os.path.join(ROOT, "posts", p["slug"])
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(post_html(p))
        print("posts/%s/index.html  %d品" % (p["slug"], len(p["items"])))
    io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(hub_html(posts))
    print("index.html  %d本" % len(posts))


if __name__ == "__main__":
    main()
