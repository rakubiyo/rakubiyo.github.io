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
:root{--ink:#292027;--muted:#776c74;--rose:#f6edf1;--red:#c71f3d;--aqua:#66bcd5;--paper:#fffefe;--line:#eadde3;--shadow:0 12px 32px rgba(77,40,59,.09)}
*{box-sizing:border-box}body{margin:0;color:var(--ink);font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",system-ui,sans-serif;background:#f9f5f6;background-image:radial-gradient(#eac9d6 1px,transparent 1px);background-size:13px 13px}.w{max-width:560px;margin:0 auto;padding:25px 16px 60px}.pr{display:inline-flex;align-items:center;gap:5px;background:var(--red);color:#fff;font-size:10px;font-weight:800;padding:6px 12px;border-radius:2px;letter-spacing:.1em}.pr:before{content:"AD";font-size:8px;letter-spacing:0}
.head{display:flex;gap:14px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:2px;padding:17px;margin:12px 0 20px;box-shadow:var(--shadow)}.head img{width:52px;height:62px;object-fit:contain;flex:none}h1{font-family:"Hiragino Mincho ProN","Yu Mincho",serif;font-size:23px;margin:0;line-height:1.28;letter-spacing:.06em}.lead{font-size:13px;color:var(--muted);margin:0 0 15px;line-height:1.85}.post-info{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}.chip{font-size:10px;font-weight:700;background:#fff;padding:6px 9px;border:1px solid var(--line);border-radius:2px;color:#665660}.chip.aqua{color:#347b91;border-color:#bfe0e9;background:#f6fcfd}.notice{background:#fffbef;border-left:3px solid #dcb764;padding:9px 11px;font-size:11px;color:#765f35;line-height:1.6;margin:0 0 17px}
.c{position:relative;display:grid;grid-template-columns:98px minmax(0,1fr);gap:14px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:2px;padding:16px 16px 16px 13px;min-height:163px;margin:0 0 13px;text-decoration:none;color:inherit;box-shadow:var(--shadow);transition:transform .16s,box-shadow .16s}.c:hover{transform:translateY(-2px);box-shadow:0 16px 35px rgba(77,40,59,.14)}.c picture,.c img{width:98px;height:126px;display:block}.c img{object-fit:contain}.t{min-width:0;align-self:stretch;padding:0 0 23px;display:block}.r{display:inline-flex;color:#fff;font-family:system-ui,sans-serif;font-size:10px;font-weight:900;padding:3px 8px;border-radius:2px;background:var(--aqua);letter-spacing:.03em}.rank-1 .r{background:#b79033}.rank-2 .r{background:#8d9fa8}.rank-3 .r{background:#bd8765}.brand{display:block;margin-top:7px;font-size:10px;font-weight:800;letter-spacing:.12em;color:#9b7381}.product{display:block;margin-top:1px;font-size:14px;line-height:1.52;font-weight:700;overflow-wrap:anywhere}.p{display:block;margin-top:6px;font-family:system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.025em}.p em{font-style:normal;font-size:9px;color:var(--muted);font-weight:600;letter-spacing:0}.review-label{display:none}.voices{margin:7px 0 0;padding:0;list-style:none;font-size:10.5px;line-height:1.48;color:#675b63}.voices li{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.voices li:before{content:"—";color:#cb8498;margin-right:4px}.voices .caution{color:#967849}.voices .caution:before{content:"※";color:#b89755;font-weight:800}.go{position:absolute;right:15px;bottom:14px;display:inline-flex;align-items:center;gap:4px;padding:7px 10px;border-radius:2px;background:var(--red);color:#fff;font-size:10px;font-weight:800;letter-spacing:.02em}.go br{display:none}.go:after{content:"→";font-family:system-ui;font-size:13px}.pc{display:grid;grid-template-columns:88px minmax(0,1fr) 20px;gap:14px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:2px;padding:11px;margin-bottom:12px;text-decoration:none;color:inherit;box-shadow:var(--shadow)}.pc img{width:88px;height:110px;object-fit:cover;border-radius:0}.pc b{font-family:"Hiragino Mincho ProN","Yu Mincho",serif;font-size:17px;line-height:1.4;display:block;letter-spacing:.03em}.pc .d{display:block;margin-top:6px;font-size:10px;color:var(--muted)}.pc:after{content:"→";font-family:system-ui;font-size:16px;color:var(--red)}.back{display:inline-block;margin:12px 0 0;font-size:12px;font-weight:700;color:#77586a;text-decoration:none;border-bottom:1px solid #bd92a3}.note{background:rgba(255,255,255,.92);border-top:2px solid #d8a9ba;padding:18px;margin-top:26px;font-size:11px;color:var(--muted);line-height:1.9}.note b{color:var(--ink)}a.src{color:#8b5e76;word-break:break-all}@media(max-width:370px){.w{padding-left:12px;padding-right:12px}.c{grid-template-columns:82px minmax(0,1fr);gap:10px;padding:13px 12px 13px 10px}.c picture,.c img{width:82px;height:115px}.product{font-size:12.5px}.voices{font-size:9.5px}.p{font-size:16px}}
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
