"""Premium refresh of the home page: bento "why us" grid with a real facility photo,
an industries section, an image-backed quote banner with two actions, and global polish.

usage: python _araclar/content_v3_premium.py _kaynak/site-tr.html _araclar/make_en.py
"""
import sys

src, make_en = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
EN = {}


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:90], s.count(old))
    s = s.replace(old, new)


def t(tr, en):
    EN[tr] = en
    return tr


def svg(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'


# ---------- "Why Focussan" -> bento grid ----------
tiles = [
    ('01', '8 metre kapasite', 'Uzun parçalarınızı tek seferde işleyebiliyoruz.'),
    ('02', '2–5 iş günü', 'Standart işler için ortalama teslim süresi.'),
    ('03', 'RAL paleti', t('Mat, parlak, yarı mat ve dokulu bitiş.', 'Matte, gloss, semi-gloss and textured finishes.')),
    ('04', 'Entegre süreç', 'Kaplama, montaj ve paketleme aynı tesiste.'),
]
bento = (
    '<section class="section dark why"><div class="wrap"><div class="section-head"><div class="eyebrow">Neden Focussan?</div><h2>Kapasite, hız ve renk esnekliği.</h2></div>'
    '<div class="bento"><figure class="bento-media">'
    f'<img src="images/header-hizmetler-1280.webp" srcset="images/header-hizmetler-768.webp 768w, images/header-hizmetler-1280.webp 1280w" sizes="(max-width: 900px) 100vw, 560px" width="1280" height="714" '
    f'alt="{t("Focussan toz boya hattında askıdaki parçalar", "Parts hanging on the Focussan powder coating line")}" loading="lazy" decoding="async">'
    f'<figcaption><strong>8 m</strong><span>{t("Uzun parçalar tek seferde boyanır", "Long parts coated in a single pass")}</span></figcaption></figure>'
    + ''.join(f'<div class="bento-tile"><b>{n}</b><h3>{h}</h3><p>{p}</p></div>' for n, h, p in tiles)
    + '</div></div></section>'
)
old_why_start = s.index('<section class="section dark"><div class="wrap"><div class="section-head"><div class="eyebrow">Neden Focussan?')
old_why_end = s.index('</section>', old_why_start) + len('</section>')
s = s[:old_why_start] + bento + s[old_why_end:]

# ---------- Industries ----------
sectors = [
    (svg('<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h6M9 11h6M9 15h3"/>'),
     t('Elektrik panosu', 'Electrical enclosures'), t('Boyalı sac kabin, DIN ray ve menteşe montajı', 'Coated sheet-metal cabinets, DIN rails and hinges')),
    (svg('<path d="M4 4v16M20 4v16M4 8h16M4 13h16M4 18h16"/>'),
     t('Raf ve depolama', 'Shelving and storage'), t('Boyalı çerçeve ve bağlantı elemanları', 'Coated frames and fasteners')),
    (svg('<path d="M6 10V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v5"/><rect x="4" y="10" width="16" height="5" rx="1.5"/><path d="M6 15v5M18 15v5"/>'),
     t('Mobilya ve dekorasyon', 'Furniture and décor'), t('Metal çerçeve, plastik ve ahşap detaylar', 'Metal frames with plastic and wooden details')),
    (svg('<path d="M5 16h14l-1.5-5.5A2 2 0 0 0 15.6 9H8.4a2 2 0 0 0-1.9 1.5L5 16z"/><path d="M4 16h16v3H4z"/><circle cx="8" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/>'),
     t('Otomotiv yan sanayi', 'Automotive suppliers'), t('Boyalı şasi parçaları ve alt gruplar', 'Coated chassis parts and sub-assemblies')),
    (svg('<path d="M3 21h18M6 21V8l6-4 6 4v13"/><path d="M10 21v-5h4v5"/>'),
     t('Yapı donanımları', 'Building hardware'), t('Korkuluk başlığı, menteşe, kapı kolu', 'Railing caps, hinges and door handles')),
    (svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
     t('Otel, perakende ve AV projeleri', 'Hotel, retail and AV projects'), t('VESA TV askı aparatı toptan ve proje tedariki', 'Wholesale and project supply of VESA TV wall mounts')),
]
industries = (
    '<section class="section sectors"><div class="wrap"><div class="section-head">'
    f'<div class="eyebrow">{t("Sektörler", "Industries")}</div><h2>{t("Farklı sektörlere üretim desteği.", "Production support across industries.")}</h2>'
    f'<p>{t("Metal ana yapısı olan ve boya, montaj ya da paketleme gerektiren ürünler için çalışıyoruz.", "We work on products with a metal body that need coating, assembly or packaging.")}</p></div>'
    '<div class="sector-grid">' + ''.join(f'<div class="sector"><span class="sector-ic">{ic}</span><div><h3>{h}</h3><p>{p}</p></div></div>' for ic, h, p in sectors)
    + '</div></div></section>'
)
s = s[:old_why_start + len(bento)] + industries + s[old_why_start + len(bento):]

# ---------- Quote banner: photo background, two actions ----------
rep('''<section class="banner"><div class="wrap"><div><h2>Projeniz için teklif alın.</h2><p>Parça resminizi veya numune fotoğrafınızı WhatsApp'tan iletin.</p></div><a class="btn" href="https://wa.me/905386847373" target="_blank" rel="noopener">WhatsApp'tan Yazın →</a></div></section>''',
    f'''<section class="banner"><div class="wrap"><div><div class="eyebrow">{t("Hızlı teklif", "Fast quote")}</div><h2>Projeniz için teklif alın.</h2><p>Parça resminizi veya numune fotoğrafınızı WhatsApp'tan iletin.</p></div>'''
    f'''<div class="banner-actions"><a class="btn" href="https://wa.me/905386847373" target="_blank" rel="noopener">WhatsApp'tan Yazın →</a><a class="btn ghost-light" href="tel:+902128730734">{t("Bizi Arayın", "Call Us")}</a></div></div></section>''')

# ---------- reveal animation covers the new blocks ----------
rep("main .faq details,main .contact,main .form,.banner .wrap'", "main .faq details,main .contact,main .form,main .bento>*,main .sector,.banner .wrap'")

# ---------- styles ----------
css = (
    "h1,h2,h3{text-wrap:balance}p{text-wrap:pretty}"
    ".dark{position:relative;isolation:isolate}.dark::before{content:'';position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:.07;"
    "background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")}"
    ".bento{display:grid;grid-template-columns:1.3fr 1fr 1fr;grid-template-rows:repeat(2,minmax(220px,auto));gap:20px}"
    ".bento-media{grid-row:1/3;position:relative;margin:0;border-radius:20px;overflow:hidden;min-height:460px;box-shadow:0 30px 60px -30px rgba(0,0,0,.6)}"
    ".bento-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}.bento-media:hover img{transform:scale(1.04)}"
    ".bento-media::after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(8,22,29,.88),rgba(8,22,29,.1) 55%)}"
    ".bento-media figcaption{position:absolute;left:28px;bottom:26px;right:28px;z-index:1;display:flex;flex-direction:column;gap:4px}"
    ".bento-media figcaption strong{font-family:'Manrope','Manrope Fallback',sans-serif;font-size:clamp(44px,5vw,64px);line-height:1;color:#fff;letter-spacing:-.03em}"
    ".bento-media figcaption span{color:#c9dadb;font-size:15px}"
    ".bento-tile{position:relative;padding:28px 26px;border-radius:20px;background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.09);transition:border-color .3s,transform .3s var(--ease),background .3s}"
    ".bento-tile:hover{transform:translateY(-4px);border-color:rgba(95,214,198,.45);background:linear-gradient(160deg,rgba(95,214,198,.12),rgba(255,255,255,.02))}"
    ".bento-tile b{display:inline-block;color:var(--gold);font-family:'Manrope','Manrope Fallback',sans-serif;font-size:13px;letter-spacing:2px;padding-bottom:10px;border-bottom:2px solid var(--gold);margin-bottom:22px}"
    ".bento-tile h3{margin:0 0 8px;color:#fff;font-size:21px;letter-spacing:-.01em}.bento-tile p{margin:0;color:#a9bcbf;font-size:15px}"
    ".sector-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}"
    ".sector{display:flex;gap:18px;align-items:flex-start;padding:24px;border:1px solid var(--line);border-radius:16px;background:#fff;transition:box-shadow .3s,transform .3s var(--ease),border-color .3s}"
    ".sector:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:transparent}"
    ".sector-ic{flex:none;width:48px;height:48px;border-radius:12px;display:grid;place-items:center;background:var(--navy);color:var(--teal-2)}.sector-ic svg{width:24px;height:24px}"
    ".sector h3{margin:2px 0 4px;color:var(--navy);font-size:17px}.sector p{margin:0;color:var(--muted);font-size:14.5px}"
    ".banner .wrap{background:linear-gradient(110deg,rgba(6,79,73,.97) 0%,rgba(8,120,111,.9) 48%,rgba(13,31,41,.55) 100%),url('images/card-toz-boya-800.webp') center/cover}"
    ".banner .eyebrow{color:#bdf2ea;margin-bottom:10px}.banner-actions{display:flex;flex-wrap:wrap;gap:12px;flex:none}"
    ".btn.ghost-light{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.55);box-shadow:none}.btn.ghost-light:hover{background:rgba(255,255,255,.12);border-color:#fff}"
    "@media(max-width:900px){.bento{grid-template-columns:1fr 1fr;grid-template-rows:auto}.bento-media{grid-column:1/-1;grid-row:auto;min-height:300px}.sector-grid{grid-template-columns:1fr 1fr}}"
    "@media(max-width:640px){.bento,.sector-grid{grid-template-columns:1fr}.bento-media{min-height:240px}.banner-actions{width:100%}.banner-actions .btn{flex:1}}"
)
k = s.index('.reveal{opacity:0;')
s = s[:k] + css + s[k:]
open(src, 'w', encoding='utf-8', newline='').write(s)

m = open(make_en, encoding='utf-8').read()
anchor = "    'Proses': 'Process',\n"
assert anchor in m
m = m.replace(anchor, anchor + ''.join(f'    {tr!r}: {en!r},\n' for tr, en in EN.items() if repr(tr) + ':' not in m), 1)
open(make_en, 'w', encoding='utf-8').write(m)
print('ok, english strings:', len(EN))
