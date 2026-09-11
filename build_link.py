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


CSS = """
:root{--ink:#3b2f3a;--sub:#8a7a88;--red:#e8202a;--cy:#3fc8ef}
*{box-sizing:border-box}
body{margin:0;font-family:"Hiragino Kaku Gothic ProN","Noto Sans JP",system-ui,sans-serif;
 color:var(--ink);background:#f6d5e5 url(%(up)simg/bg.png) repeat;background-size:360px}
.w{max-width:520px;margin:0 auto;padding:18px 14px 48px}
.pr{display:inline-block;background:var(--red);color:#fff;font-weight:800;font-size:13px;
 padding:5px 14px;border-radius:999px;letter-spacing:.06em}
.head{display:flex;gap:12px;align-items:center;background:#fff;border-radius:18px;padding:14px;margin:12px 0 16px}
.head img{width:64px;height:64px;object-fit:contain;flex:none}
h1{font-size:21px;margin:0 0 4px;line-height:1.45}
.lead{font-size:13.5px;color:var(--sub);margin:0 0 16px;line-height:1.7}
.c{display:flex;gap:12px;align-items:center;background:#fff;border-radius:18px;padding:12px;
 margin-bottom:11px;text-decoration:none;color:inherit;box-shadow:0 2px 0 rgba(120,90,115,.13)}
.c img{width:78px;height:78px;object-fit:contain;flex:none}
.t{flex:1;min-width:0}
.r{display:inline-block;background:var(--cy);color:#fff;font-weight:800;font-size:12px;
 padding:2px 9px;border-radius:999px;margin-right:6px}
.t b{font-size:14px;line-height:1.4;display:inline}
.p{display:block;margin-top:5px;font-size:15px;font-weight:800}
.p em{font-style:normal;font-size:11px;color:var(--sub);font-weight:600}
.q{display:block;margin-top:3px;font-size:12px;color:var(--sub)}
.go{flex:none;background:var(--red);color:#fff;font-size:12px;font-weight:800;
 padding:9px 11px;border-radius:999px;white-space:nowrap}
.pc{display:flex;gap:13px;align-items:center;background:#fff;border-radius:18px;padding:13px;
 margin-bottom:12px;text-decoration:none;color:inherit;box-shadow:0 2px 0 rgba(120,90,115,.13)}
.pc img{width:84px;height:105px;object-fit:cover;border-radius:11px;flex:none}
.pc b{font-size:16px;line-height:1.4;display:block}
.pc .d{display:block;margin-top:6px;font-size:12px;color:var(--sub)}
.back{display:inline-block;margin-top:6px;font-size:13px;color:var(--sub);text-decoration:none}
.note{background:#fff;border-radius:18px;padding:16px;margin-top:18px;font-size:11.5px;
 color:var(--sub);line-height:1.85}
.note b{color:var(--ink)}
a.src{color:var(--sub)}
"""

PAGE = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
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
    rows = []
    for it in p["items"]:
        rows.append(
            '  <a class="c" href="%s" target="_blank" rel="nofollow sponsored noopener">\n'
            '    <img src="img/%s" alt="">\n'
            '    <div class="t"><span class="r">%s</span><b>%s</b>\n'
            '      <span class="p">¥%s <em>税込 %s</em></span>\n'
            '      <span class="q">%s</span></div>\n'
            '    <span class="go">楽天で見る</span>\n'
            '  </a>' % (aff(it["url"]), it["img"], esc(it["rank"]), esc(it["name"]),
                        it["price"], esc(it["size"]), esc(it["copy"])))
    body = '<p class="lead">%s</p>\n%s\n<a class="back" href="../../">← ほかの回を見る</a>' % (
        esc(p["lead"]), "\n".join(rows))

    src = p["source"]
    notes = [head_note(), "<b>出典</b><br>%s<br><a class=\"src\" href=\"%s\" target=\"_blank\" "
             "rel=\"noopener\">%s</a><br>集計期間：%s" % (
                 esc(src["name"]), src["url"],
                 urllib.parse.urlparse(src["url"]).netloc, esc(src["period"]))]
    n0 = SITE["notes"][0]
    if p.get("price_note"):
        n0 = n0.replace("の記載です。", "の記載です" + p["price_note"] + "。")
    notes.append(n0 + "<br>" + "<br>".join(SITE["notes"][1:]))
    return PAGE % dict(
        title="%s｜%s" % (SITE["name"], p["title"]), css=CSS % {"up": "../../"}, up="../../",
        icon=SITE["icon"],
        tagline='<p class="lead" style="margin:4px 0 0">%s</p>' % esc(SITE["name"]),
        h1=esc(p["title"]),
        body=body, notes="<br><br>".join(notes))


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
    return PAGE % dict(title=SITE["name"], css=CSS % {"up": ""}, up="",
                       icon=SITE["icon"], tagline="",
                       h1=esc(SITE["name"]), body=body, notes="<br><br>".join(notes))


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
