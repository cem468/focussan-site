"""One-off content update: richer TV mount and contract assembly pages, working
contact form (composes a WhatsApp message), legal links in the footer.
Adds the matching English strings to make_en.py.

usage: python _araclar/content_v2.py _kaynak/site-tr.html _araclar/make_en.py
"""
import re
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


# ---------- TV wall mounts ----------
start = s.index('<section class="section"><div class="wrap"><div class="section-head"><h2>Farklı kurulumlara uygun seçenekler.</h2>')
end = s.index('</div></section></section>', start) + len('</div></section></section>')
old_tv = s[start:end]
icons = re.findall(r'<div class="cardtop">(<svg.*?</svg>)</div>', old_tv, flags=re.S)
tv_icon, move_icon, ceiling_icon = icons[0], icons[1], icons[2]


def card(icon, title, text, sizes, use):
    items = ''.join(f'<li>{x}</li>' for x in sizes)
    return (f'<article class="card"><div class="cardtop">{icon}</div><div class="cardbody"><h3>{title}</h3><p>{text}</p>'
            f'<ul>{items}</ul><p class="card-use"><strong>{t("Kullanım alanı", "Typical use")}:</strong> {use}</p></div></article>')


cards = ''.join([
    card(tv_icon, t('Gövde tipi (sabit)', 'Fixed mounts'),
         t('Duvara sabitlenen, hareketsiz askı. Dar gövde TV’yi duvara yakın tutar; geniş gövde büyük ekranlarda denge sağlar.',
           'A fixed, low-profile wall mount. Narrow models keep the TV close to the wall; wide models add stability for large screens.'),
         [t('Dar gövde 35 cm · 24–43″', 'Narrow 35 cm · 24–43″'), t('Dar gövde 70 cm · 43–55″', 'Narrow 70 cm · 43–55″'),
          t('Geniş gövde 85 cm · 55–65″', 'Wide 85 cm · 55–65″'), t('Geniş gövde 100 cm · 65–85″', 'Wide 100 cm · 65–85″')],
         t('Ev salonu, ofis, otel odası', 'Living rooms, offices, hotel rooms')),
    card(move_icon, t('6 kollu hareketli', '6-arm full-motion'),
         t('Altı mafsallı kol ile ileri-geri uzatma, sağa-sola döndürme ve eğim ayarı. Profesyonel kurulumlar için tasarlandı.',
           'Six articulated joints for extension, left-right swivel and tilt. Designed for professional installations.'),
         [t('Tek model · 50–85″', 'Single model · 50–85″')],
         t('Ev sineması, toplantı odası, otel lobisi, yayın stüdyosu', 'Home cinemas, meeting rooms, hotel lobbies, broadcast studios')),
    card(move_icon, t('Kelebek hareketli', 'Swivel (butterfly) mount'),
         t('Çift kollu kelebek mekanizması: kapalıyken duvara yakın, açıkken geniş hareket alanı. Ağır TV’leri taşır.',
           'A double-arm butterfly mechanism: close to the wall when folded, a wide range of motion when open. Supports heavy TVs.'),
         [t('Tek model · 40–75″', 'Single model · 40–75″')],
         t('Yatak odası, küçük salon, esnek kullanım alanları', 'Bedrooms, small living rooms, flexible spaces')),
    card(ceiling_icon, t('Tavan askı', 'Ceiling mount'),
         t('Tavana monte edilir; ayarlanabilir kol boyu farklı tavan yüksekliklerine uyar, 360° döner.',
           'Mounted to the ceiling; the adjustable pole fits different ceiling heights and rotates 360°.'),
         [t('Tek model, ayarlanabilir · 32–65″', 'Single adjustable model · 32–65″')],
         t('Mağaza, restoran, eğitim tesisi, fuar, hastane', 'Shops, restaurants, training centres, trade fairs, hospitals')),
])

specs = [
    (t('Gövde malzemesi', 'Body material'), t('Galvaniz çelik, yüksek paslanma direnci', 'Galvanised steel with high corrosion resistance')),
    (t('Yüzey kaplama', 'Finish'), t('Mat siyah elektrostatik toz boya, kendi tesisimizde', 'Matte black electrostatic powder coating, applied in-house')),
    (t('VESA uyumu', 'VESA compatibility'), t('75×75 ile 600×400 arası evrensel plaka', 'Universal plate from 75×75 to 600×400')),
    (t('Marka uyumu', 'Brand compatibility'), t('Samsung, LG, Sony, Vestel, Arçelik, Beko ve VESA standardına uyan tüm markalar', 'Samsung, LG, Sony, Vestel, Arçelik, Beko and every VESA-compliant brand')),
    (t('Kablo yönetimi', 'Cable management'), t('Standart kablo kanalı', 'Standard cable channel')),
    (t('Montaj kiti', 'Mounting kit'), t('Vidalar ve montaj talimatı kutuda', 'Screws and installation instructions in the box')),
]
vesa = [('75×75 / 100×100', t('15–32 inç', '15–32 inches')), ('200×200', t('32–37 inç', '32–37 inches')),
        ('200×100 / 300×300', t('37–50 inç', '37–50 inches')), ('400×400', t('50–65 inç', '50–65 inches')),
        ('600×400', t('65–75 inç', '65–75 inches'))]
WA = 'https://wa.me/905386847373'
new_tv = (
    '<section class="section"><div class="wrap"><div class="section-head">'
    f'<div class="eyebrow">{t("Ürün aileleri", "Product families")}</div>'
    f'<h2>{t("Dört ürün ailesi, 24–100 inç arası ekranlar.", "Four product families for 24–100 inch screens.")}</h2>'
    f'<p>{t("Tüm modeller galvaniz çelikten üretilir, kendi tesisimizde mat siyah elektrostatik toz boya ile kaplanır ve evrensel VESA plakasıyla çoğu TV markasına uyar.", "Every model is made from galvanised steel, powder-coated matte black in our own facility and fits most TV brands with a universal VESA plate.")}</p>'
    f'</div><div class="cards cards-4">{cards}</div></div></section>'
    '<section class="section shade"><div class="wrap spec-grid"><div>'
    f'<div class="eyebrow">{t("Teknik bilgiler", "Specifications")}</div><h2>{t("Ortak teknik özellikler", "Shared specifications")}</h2>'
    '<dl class="specs">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in specs) + '</dl></div><div>'
    f'<div class="eyebrow">VESA</div><h2>{t("VESA ölçüsü ve ekran boyutu", "VESA size and screen size")}</h2>'
    f'<table class="vesa-table"><thead><tr><th>{t("VESA değeri", "VESA value")}</th><th>{t("Tipik ekran", "Typical screen")}</th></tr></thead><tbody>'
    + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in vesa) + '</tbody></table>'
    f'<p class="table-note">{t("Aparatlarımız 75×75 ile 600×400 arasındaki tüm VESA değerlerini tek plakada destekler. Satın almadan önce TV’nizin VESA ölçüsünü ve ağırlığını, seçtiğiniz modelin taşıma sınırıyla karşılaştırın.", "Our mounts support every VESA value from 75×75 to 600×400 on a single plate. Before buying, compare your TV’s VESA size and weight with the load limit of the model you choose.")}</p>'
    '</div></div></section>'
    '<section class="section"><div class="wrap"><div class="wholesale"><div>'
    f'<div class="eyebrow">{t("Toptan ve proje satışı", "Wholesale and project sales")}</div>'
    f'<h2>{t("Toptan ve proje siparişlerinde özel fiyatlandırma.", "Dedicated pricing for wholesale and project orders.")}</h2>'
    f'<p>{t("AV entegratörleri, otel zincirleri, perakende grupları, mağaza ağları ve distribütörlerle proje bazlı fiyatlandırmayla çalışıyoruz. Teklif için model, adet ve teslimat yerini iletmeniz yeterli.", "We work with AV integrators, hotel chains, retail groups, store networks and distributors on project-based pricing. Just send us the model, quantity and delivery location for a quote.")}</p>'
    f'<div class="checks"><span>{t("Proje bazlı fiyatlandırma", "Project-based pricing")}</span><span>{t("Palet, koli veya konteyner sevkiyat", "Pallet, carton or container shipping")}</span>'
    f'<span>{t("Markalı veya nötr paketleme", "Branded or neutral packaging")}</span><span>{t("Kendi tesisimizde üretim ve toz boya", "In-house manufacturing and powder coating")}</span></div></div>'
    f'<a class="btn orange" href="{WA}" target="_blank" rel="noopener">{t("Toptan Fiyat İsteyin →", "Request Wholesale Pricing →")}</a></div></div></section></section>'
)
s = s[:start] + new_tv + s[end:]

# ---------- Contract assembly ----------
steps = [
    (t('Parça kabul ve envanter', 'Intake and inventory'), t('Boyanacak metal parçalar ve montaj komponentleri teslim alınır; sayım ve hasar kontrolünden sonra üretim emrine bağlanır.', 'Metal parts to be coated and assembly components are received, counted, checked for damage and linked to a production order.')),
    (t('Statik toz boya', 'Powder coating'), t('Yüzey hazırlık, püskürtme, fırınlama ve soğutma kendi tesisimizde yapılır.', 'Surface preparation, spraying, curing and cooling all take place in our own facility.')),
    (t('Montaj', 'Assembly'), t('Boyalı parça hattan ayrılmadan komponentlerle birleştirilir; vida torku, dizilim ve kablo tesisatı şartnameye göre uygulanır.', 'Coated parts are assembled with components without leaving the line; screw torque, sequence and wiring follow your specification.')),
    (t('Kalite kontrol', 'Quality control'), t('Renk, yüzey ve çizik için görsel kontrol; hareket, sıkılık ve ölçü uyumu için fonksiyonel test.', 'Visual checks for colour, surface and scratches, plus functional tests for movement, tightness and dimensional fit.')),
    (t('Etiketleme ve paketleme', 'Labelling and packaging'), t('Markalı ambalaj veya nötr kraft kutu, baskılı etiket, barkod ve kullanım kılavuzu.', 'Branded or neutral kraft boxes, printed labels, barcodes and user manuals.')),
    (t('Sevkiyat', 'Shipping'), t('Adresinize, deponuza veya doğrudan son müşterinize; palet, koli ya da konteyner olarak.', 'To your address, your warehouse or straight to your end customer, by pallet, carton or container.')),
]
products = [
    t('TV askı aparatları: galvaniz çelik gövde, vida seti, duvar plakası ve kılavuz (kendi VESA ürünlerimizi bu hatta üretiyoruz)', 'TV wall mounts: galvanised steel body, screw set, wall plate and manual (we build our own VESA products on this line)'),
    t('Elektrik panosu kabinleri: boyalı sac kabin, DIN ray, menteşe ve etiketleme', 'Electrical enclosures: coated sheet-metal cabinet, DIN rail, hinges and labelling'),
    t('Raf ve depolama sistemleri: boyalı çerçeve, bağlantı elemanları ve ayak seti', 'Shelving and storage systems: coated frames, fasteners and feet'),
    t('Mobilya ve dekorasyon aksesuarları: metal çerçeve, plastik ve ahşap detaylar', 'Furniture and décor accessories: metal frames with plastic and wooden details'),
    t('Otomotiv yan sanayi alt grupları: boyalı şasi parçası, bağlantı kiti, etiket ve barkod', 'Automotive sub-assemblies: coated chassis parts, fixing kits, labels and barcodes'),
    t('Yapı donanımları: korkuluk başlığı, menteşe, kapı kolu', 'Building hardware: railing caps, hinges, door handles'),
]
pricing = [
    t('Parça başı işçilik süresi', 'Labour time per unit'),
    t('Komponent sayısı ve tipi', 'Number and type of components'),
    t('Kalite kontrol gereksinimi: görsel, fonksiyonel test veya sertifika', 'Quality-control requirements: visual, functional testing or certification'),
    t('Paketleme tipi: nötr kraft, markalı kutu veya palet', 'Packaging type: neutral kraft, branded box or pallet'),
]
montaj_end = s.index('</div></section></section>', s.index('id="page-montaj"')) + len('</div></section>')
montaj_add = (
    '<section class="section shade"><div class="wrap"><div class="section-head">'
    f'<div class="eyebrow">{t("Süreç", "Process")}</div><h2>{t("Altı adımda bitmiş ürün.", "From parts to finished product in six steps.")}</h2></div>'
    '<ol class="process">' + ''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a, b in steps) + '</ol></div></section>'
    '<section class="section"><div class="wrap spec-grid"><div>'
    f'<div class="eyebrow">{t("Uygulamalar", "Applications")}</div><h2>{t("Hangi ürünler için uygun?", "Which products is it suitable for?")}</h2>'
    f'<p class="intro">{t("Metal ana yapısı olan ve ek komponent gerektiren her ürün için uygundur. Tipik örnekler:", "Any product with a metal body that needs extra components. Typical examples:")}</p>'
    '<ul class="plain-list">' + ''.join(f'<li>{x}</li>' for x in products) + '</ul></div><div>'
    f'<div class="eyebrow">{t("Fiyatlandırma", "Pricing")}</div><h2>{t("Fiyat nasıl belirlenir?", "How is pricing set?")}</h2>'
    f'<p class="intro">{t("Montaj hattı fiyatı sabit bir liste değildir; ürünün karmaşıklığına göre şu kriterlerle hesaplanır:", "Assembly pricing is not a fixed list; it depends on product complexity and these factors:")}</p>'
    '<ol class="plain-list numbered">' + ''.join(f'<li>{x}</li>' for x in pricing) + '</ol>'
    f'<a class="btn" href="{WA}" target="_blank" rel="noopener">{t("Montaj Projenizi Görüşün", "Discuss Your Assembly Project")}</a></div></div></section>'
)
s = s[:montaj_end] + montaj_add + s[montaj_end:]

# ---------- Contact form: compose a WhatsApp message, KVKK consent ----------
rep('''<form class="form" onsubmit="event.preventDefault();document.getElementById('notice').style.display='block';this.reset()">''',
    f'<form class="form" data-intro="{t("Merhaba, web sitesinden teklif talebi:", "Hello, a quote request from the website:")}" data-l-ad="{t("Ad", "Name")}" data-l-sirket="{t("Şirket", "Company")}" '
    'data-l-eposta="E-posta" data-l-telefon="Telefon" data-l-hizmet="Hizmet" data-l-detay="' + t('Detay', 'Details') + '">')
rep('<button class="btn" type="submit">Talep Gönder →</button><p class="notice wide" id="notice" role="status">Bu form taslak arayüzdür; gönderim için e-posta veya CRM bağlantısı kurulmalıdır.</p>',
    f'<label class="consent wide"><input type="checkbox" name="kvkk" required> <span>{t("Kişisel verilerimin", "I agree to the processing of my personal data under the")} <a href="#/gizlilik">{t("Gizlilik ve KVKK Aydınlatma Metni", "Privacy Notice")}</a> {t("kapsamında işlenmesini kabul ediyorum.", ".")}</span></label>'
    f'<button class="btn" type="submit">{t("WhatsApp ile Gönder →", "Send via WhatsApp →")}</button>'
    f'<p class="notice wide" id="notice" role="status">{t("Talebiniz WhatsApp’ta hazırlandı; göndermek için WhatsApp’taki gönder düğmesine dokunun.", "Your request is ready in WhatsApp; tap send in WhatsApp to deliver it.")}</p>')

# ---------- Footer legal links ----------
rep('<a href="#/anasayfa">Ana sayfaya dön ↑</a></div></footer>',
    f'<span class="legal-links"><a href="#/gizlilik">{t("Gizlilik ve KVKK", "Privacy")}</a><a href="#/cerezler">{t("Çerez Politikası", "Cookie Policy")}</a><a href="#/anasayfa">Ana sayfaya dön ↑</a></span></div></footer>')

# ---------- Scripts: form handler + WhatsApp click hook ----------
rep("document.getElementById('year').textContent=new Date().getFullYear();",
    "document.getElementById('year').textContent=new Date().getFullYear();"
    "(function(){const form=document.querySelector('.form');if(!form)return;form.addEventListener('submit',event=>{event.preventDefault();const data=new FormData(form),d=form.dataset;"
    "const lines=[d.intro].concat([['ad',d.lAd],['sirket',d.lSirket],['eposta',d.lEposta],['telefon',d.lTelefon],['hizmet',d.lHizmet],['detay',d.lDetay]].filter(([k])=>data.get(k)).map(([k,l])=>l+': '+data.get(k)));"
    "window.open('https://wa.me/905386847373?text='+encodeURIComponent(lines.join('\\n')),'_blank','noopener');document.getElementById('notice').style.display='block';});})();"
    "document.addEventListener('click',event=>{const link=event.target.closest('a[href*=\"wa.me/\"]');if(!link)return;(window.dataLayer=window.dataLayer||[]).push({event:'whatsapp_click',page:location.pathname,label:link.textContent.trim()});});")

# ---------- Styles ----------
css = (".cards-4{grid-template-columns:repeat(4,1fr)}.card-use{margin:auto 0 0!important;font-size:14px!important}.card-use strong{color:var(--navy)}"
       ".spec-grid{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}.spec-grid h2{font-size:clamp(26px,3vw,36px);line-height:1.15;color:var(--navy);margin:12px 0 22px;letter-spacing:-.02em}"
       ".specs{margin:0;display:grid;gap:0;border-top:1px solid var(--line)}.specs div{display:grid;grid-template-columns:42% 1fr;gap:16px;padding:14px 0;border-bottom:1px solid var(--line)}.specs dt{font-weight:700;color:var(--navy)}.specs dd{margin:0;color:var(--muted)}"
       ".vesa-table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}.vesa-table th,.vesa-table td{padding:13px 18px;text-align:left;border-bottom:1px solid var(--line)}.vesa-table th{background:var(--navy);color:#fff;font-size:13px;letter-spacing:.5px}.vesa-table tr:last-child td{border-bottom:0}.table-note{color:var(--muted);font-size:14.5px;margin-top:16px}"
       ".wholesale{display:flex;align-items:center;justify-content:space-between;gap:40px;padding:44px 48px;border-radius:20px;background:var(--paper);border:1px solid var(--line)}.wholesale h2{font-size:clamp(26px,3vw,36px);line-height:1.15;color:var(--navy);margin:12px 0 14px;letter-spacing:-.02em}.wholesale p{color:var(--muted);max-width:640px}.wholesale .checks{margin-bottom:0}.wholesale .btn{flex:none}"
       ".process{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;counter-reset:proc}.process li{counter-increment:proc;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px 26px 22px}.process li::before{content:counter(proc,decimal-leading-zero);display:block;color:var(--gold);font-family:'Manrope','Manrope Fallback',sans-serif;font-weight:800;font-size:14px;letter-spacing:2px;margin-bottom:10px}.process h3{margin:0 0 8px;color:var(--navy);font-size:19px}.process p{margin:0;color:var(--muted);font-size:15px}"
       ".plain-list{margin:0 0 26px;padding-left:20px;color:var(--muted)}.plain-list li{padding:6px 0}.plain-list li::marker{color:var(--teal)}"
       ".consent{display:flex;align-items:flex-start;gap:10px;font-weight:400!important;color:var(--muted)!important}.consent input{width:auto!important;margin:4px 0 0!important}.consent a{color:var(--teal);text-decoration:underline}"
       ".legal-links{display:flex;flex-wrap:wrap;gap:20px}"
       "@media(max-width:900px){.cards-4{grid-template-columns:1fr 1fr}.spec-grid{grid-template-columns:1fr;gap:44px}.process{grid-template-columns:1fr 1fr}.wholesale{flex-direction:column;align-items:flex-start;padding:34px 28px}}"
       "@media(max-width:640px){.cards-4,.process{grid-template-columns:1fr}.specs div{grid-template-columns:1fr;gap:4px}}")
k = s.index('.reveal{opacity:0;')
s = s[:k] + css + s[k:]
open(src, 'w', encoding='utf-8', newline='').write(s)

# ---------- English strings for make_en.py ----------
m = open(make_en, encoding='utf-8').read()
anchor = "    'Proses': 'Process',\n"
assert anchor in m
lines = ''.join(f'    {tr!r}: {en!r},\n' for tr, en in EN.items() if repr(tr) + ':' not in m)
m = m.replace(anchor, anchor + lines, 1)
open(make_en, 'w', encoding='utf-8').write(m)
print('ok, english strings added:', len(EN))
