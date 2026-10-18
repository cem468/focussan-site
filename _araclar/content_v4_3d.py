"""Premium motion layer: 3D buttons (raised edge, press-in, sheen), pointer-tracked 3D tilt with glare on cards,
hero/page-hero entrance, Ken Burns + parallax header images, metric counters, scroll progress bar,
softer reveal, drifting light in dark sections and a "how we work" process section on the home page.

usage: python _araclar/content_v4_3d.py _kaynak/site-tr.html _araclar/make_en.py
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


# ---------- process section (home, after industries) ----------
steps = [
    (t('Talep', 'Request'), t("Parça resmini, çizimini veya numune fotoğrafını WhatsApp'tan iletin.", 'Send a drawing, part photo or sample image via WhatsApp.')),
    (t('Teklif', 'Quote'), t('Ölçü, adet, renk ve bitişe göre fiyat ve termin bildirilir.', 'We quote price and lead time based on size, quantity, colour and finish.')),
    (t('Üretim', 'Production'), t('Kaplama, montaj ve kalite kontrol planlı şekilde yürütülür.', 'Coating, assembly and quality control run to plan.')),
    (t('Teslim', 'Delivery'), t('Ürünleriniz paketlenip zamanında sevke hazırlanır.', 'Your products are packed and ready for dispatch on time.')),
]
process = (
    '<section class="section shade workflow"><div class="wrap"><div class="section-head">'
    f'<div class="eyebrow">{t("Çalışma süreci", "How we work")}</div><h2>{t("Talepten teslimata dört adım.", "Four steps from request to delivery.")}</h2></div>'
    '<ol class="flow">' + ''.join(f'<li class="flow-step"><span class="flow-n">{i}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(steps, 1))
    + '</ol></div></section>'
)
a = s.index('<section class="section sectors">')
b = s.index('</section>', s.index('</div></div>', s.index('class="sector-grid"', a))) + len('</section>')
s = s[:b] + process + s[b:]
rep('.sectors{padding-bottom:20px}', '')

# ---------- softer reveal ----------
rep('.reveal{opacity:0;transform:translateY(16px);transition:opacity .5s var(--ease),transform .5s var(--ease)}.reveal.in{opacity:1;transform:none}',
    '.reveal{opacity:0;transform:translateY(28px) scale(.97);filter:blur(4px);transition:opacity .7s var(--ease),transform .8s var(--ease),filter .7s var(--ease)}.reveal.in{opacity:1;transform:none;filter:none}')
rep('.reveal{opacity:1;transform:none}.hero-video', '.reveal{opacity:1;transform:none;filter:none}.pagehero-img{translate:none!important}.hero-video')
rep("main .bento>*,main .sector,.banner .wrap'", "main .bento>*,main .sector,main .flow-step,.banner .wrap'")

# ---------- styles ----------
EDGE = 'inset 0 1px 0 rgba(255,255,255,.32),inset 0 -1px 0 rgba(0,0,0,.18)'
css = (
    # 3D buttons
    ".btn{position:relative;overflow:hidden;isolation:isolate;background:linear-gradient(180deg,#0f9b8e 0%,var(--teal) 55%,#06665e 100%);"
    f"box-shadow:{EDGE},0 4px 0 #04524b,0 14px 24px -10px rgba(8,120,111,.7);transition:transform .2s var(--ease),box-shadow .2s,background .2s}}"
    f".btn:hover{{background:linear-gradient(180deg,#11a798,#0a8b7f 55%,#065d56);transform:translateY(-2px);box-shadow:{EDGE},0 6px 0 #04524b,0 22px 30px -12px rgba(8,120,111,.8)}}"
    f".btn:active{{transform:translateY(3px);transition-duration:.06s;box-shadow:{EDGE},0 1px 0 #04524b,0 6px 12px -6px rgba(8,120,111,.6)}}"
    ".btn::after{content:'';position:absolute;inset:0;z-index:-1;background:linear-gradient(105deg,transparent 30%,rgba(255,255,255,.4) 48%,transparent 66%);transform:translateX(-130%);transition:transform .8s var(--ease);pointer-events:none}"
    ".btn:hover::after{transform:translateX(130%)}"
    f".btn.orange{{background:linear-gradient(180deg,#f7d389,var(--gold) 60%,#c28a29);box-shadow:{EDGE},0 4px 0 #94661a,0 14px 26px -10px rgba(217,164,65,.8)}}"
    f".btn.orange:hover{{background:linear-gradient(180deg,#f9da98,#dfab4a 60%,#c28a29);box-shadow:{EDGE},0 6px 0 #94661a,0 22px 32px -12px rgba(217,164,65,.9)}}"
    f".btn.orange:active{{box-shadow:{EDGE},0 1px 0 #94661a,0 6px 12px -6px rgba(217,164,65,.7)}}"
    ".banner .btn:not(.ghost-light),.btn.ghost{background:linear-gradient(180deg,#fff,#eaf2f1);color:var(--navy);box-shadow:inset 0 1px 0 #fff,0 4px 0 #a9c1be,0 14px 24px -12px rgba(0,0,0,.45)}"
    ".banner .btn:not(.ghost-light):hover,.btn.ghost:hover{background:linear-gradient(180deg,#fff,#dff2ee);color:var(--navy);box-shadow:inset 0 1px 0 #fff,0 6px 0 #a9c1be,0 22px 30px -12px rgba(0,0,0,.5)}"
    ".banner .btn:not(.ghost-light):active,.btn.ghost:active{box-shadow:inset 0 1px 0 #fff,0 1px 0 #a9c1be,0 6px 12px -6px rgba(0,0,0,.4)}"
    ".btn.ghost-light{background:rgba(255,255,255,.06);box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 4px 0 rgba(0,0,0,.28)}"
    ".btn.ghost-light:hover{background:rgba(255,255,255,.14);box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 6px 0 rgba(0,0,0,.28)}"
    ".btn.ghost-light:active{box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 1px 0 rgba(0,0,0,.28)}"
    # 3D cards (tilt + glare are driven by the script, only on fine pointers)
    ".card,.sector,.flow-step{box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 1px 2px rgba(13,31,41,.05),0 14px 28px -16px rgba(13,31,41,.18)}"
    ".tilt{position:relative;transition:transform .6s var(--ease),box-shadow .5s,border-color .3s,background .3s}"
    ".tilt:hover{transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(-6px);transition:transform .14s linear,box-shadow .25s,border-color .3s,background .3s;"
    "box-shadow:var(--sx,0px) var(--sy,26px) 50px -18px rgba(13,31,41,.38)}"
    ".glare{position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:3;opacity:0;transition:opacity .4s;"
    "background:radial-gradient(420px circle at var(--mx,50%) var(--my,0%),rgba(255,255,255,.16),transparent 50%)}.tilt:hover .glare{opacity:1}"
    ".dark .glare{background:radial-gradient(380px circle at var(--mx,50%) var(--my,0%),rgba(95,214,198,.12),transparent 55%)}"
    ".sector-ic,.card-icon{transition:transform .5s var(--ease)}.sector:hover .sector-ic{transform:translateY(-3px) rotate(-8deg) scale(1.06)}"
    "@media(hover:none){.card:active,.sector:active,.bento-tile:active,.flow-step:active{transform:scale(.985)}}"
    # process
    ".flow{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:22px;position:relative}"
    ".flow::before{content:'';position:absolute;top:44px;left:12.5%;right:12.5%;height:2px;background:linear-gradient(90deg,var(--teal),var(--teal-2),var(--gold));transform:scaleX(0);transform-origin:0 50%;transition:transform 1.6s var(--ease) .2s}"
    ".flow.drawn::before{transform:scaleX(1)}"
    ".flow-step{position:relative;text-align:center;padding:16px 22px 28px;border-radius:18px;background:#fff;border:1px solid var(--line)}"
    ".flow-n{position:relative;z-index:1;display:grid;place-items:center;width:56px;height:56px;margin:0 auto 18px;border-radius:50%;color:#fff;font-family:'Manrope','Manrope Fallback',sans-serif;font-weight:800;font-size:20px;"
    "background:linear-gradient(180deg,#12a596,var(--teal) 60%,#06665e);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 4px 0 #04524b,0 12px 20px -8px rgba(8,120,111,.6)}"
    ".flow-step h3{margin:0 0 6px;color:var(--navy);font-size:19px}.flow-step p{margin:0;color:var(--muted);font-size:14.5px}"
    "@media(max-width:900px){.flow{grid-template-columns:1fr 1fr}.flow::before{display:none}}@media(max-width:640px){.flow{grid-template-columns:1fr;gap:12px}.flow-step{display:grid;grid-template-columns:44px 1fr;column-gap:16px;text-align:left;padding:18px}.flow-n{grid-row:span 2;width:44px;height:44px;margin:0;font-size:17px}.flow-step h3{font-size:17px;margin:2px 0 4px}}"
    # entrance + header motion
    "@keyframes rise{from{opacity:0;transform:translateY(26px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}"
    ".hero-content>*,.pagehero .wrap>*{animation:rise .9s var(--ease) both}"
    ".hero-content>:nth-child(2),.pagehero .wrap>:nth-child(2){animation-delay:.08s}.hero-content>:nth-child(3),.pagehero .wrap>:nth-child(3){animation-delay:.16s}.hero-content>:nth-child(4){animation-delay:.24s}"
    "@keyframes kenburns{from{scale:1.14}to{scale:1.05}}.pagehero-img{animation:kenburns 2.2s var(--ease) both;will-change:translate}"
    # scroll progress + drifting light in dark sections
    ".scroll-progress{position:fixed;top:0;left:0;right:0;height:3px;z-index:100;pointer-events:none;transform-origin:0 50%;transform:scaleX(0);background:linear-gradient(90deg,var(--teal),var(--teal-2),var(--gold))}"
    ".dark{overflow:hidden}.dark::after{content:'';position:absolute;z-index:-1;width:640px;height:640px;left:-12%;bottom:-40%;border-radius:50%;pointer-events:none;"
    "background:radial-gradient(circle,rgba(217,164,65,.13),transparent 65%);animation:drift 20s ease-in-out infinite alternate}"
    "@keyframes drift{to{transform:translate(55vw,-25%)}}"
    "::selection{background:var(--teal);color:#fff}"
    ":focus-visible{outline:3px solid var(--teal-2);outline-offset:3px}"
)
k = s.index('.reveal{opacity:0;')
s = s[:k] + css + s[k:]

# ---------- script ----------
js = (
    "(()=>{const rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(hover:hover) and (pointer:fine)').matches;"
    # scroll progress + header parallax
    "const bar=document.createElement('div');bar.className='scroll-progress';bar.setAttribute('aria-hidden','true');document.body.appendChild(bar);"
    "const ph=document.querySelector('.pagehero-img');let ticking=false;"
    "const upd=()=>{ticking=false;const h=document.documentElement.scrollHeight-innerHeight;bar.style.transform='scaleX('+(h>0?scrollY/h:0)+')';"
    "if(ph&&!rm&&scrollY<1000)ph.style.translate='0 '+(scrollY*.28).toFixed(1)+'px';};"
    "addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(upd);}},{passive:true});upd();"
    # 3D tilt with glare
    "if(fine&&!rm)document.querySelectorAll('.card,.bento-tile,.sector,.flow-step').forEach(el=>{el.classList.add('tilt');const g=document.createElement('span');g.className='glare';g.setAttribute('aria-hidden','true');el.appendChild(g);"
    "el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height,st=el.style;"
    "st.setProperty('--rx',((.5-y)*9).toFixed(2)+'deg');st.setProperty('--ry',((x-.5)*11).toFixed(2)+'deg');st.setProperty('--mx',(x*100).toFixed(1)+'%');st.setProperty('--my',(y*100).toFixed(1)+'%');"
    "st.setProperty('--sx',((.5-x)*26).toFixed(1)+'px');st.setProperty('--sy',(26+(.5-y)*14).toFixed(1)+'px');});"
    "el.addEventListener('pointerleave',()=>{el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg');});});"
    # metric counters
    "if(!rm&&'IntersectionObserver' in window)document.querySelectorAll('.metric strong').forEach(el=>{const txt=el.textContent;if(!/\\d/.test(txt))return;"
    "const o=new IntersectionObserver(([e])=>{if(!e.isIntersecting)return;o.disconnect();const t0=performance.now();"
    "const step=now=>{const k=Math.min(1,(now-t0)/1300),f=1-Math.pow(1-k,3);el.textContent=txt.replace(/\\d+/g,n=>Math.round(n*f));if(k<1)requestAnimationFrame(step);};requestAnimationFrame(step);},{threshold:.6});o.observe(el);});"
    # process line draw
    "const flow=document.querySelector('.flow');if(flow){if(rm||!('IntersectionObserver' in window))flow.classList.add('drawn');"
    "else{const o=new IntersectionObserver(([e])=>{if(e.isIntersecting){flow.classList.add('drawn');o.disconnect();}},{threshold:.35});o.observe(flow);}}"
    "})();"
)
rep('\n</script>\n</body>', '\n' + js + '\n</script>\n</body>')
open(src, 'w', encoding='utf-8', newline='').write(s)

m = open(make_en, encoding='utf-8').read()
anchor = "    'Proses': 'Process',\n"
assert anchor in m
m = m.replace(anchor, anchor + ''.join(f'    {tr!r}: {en!r},\n' for tr, en in EN.items() if repr(tr) + ':' not in m), 1)
open(make_en, 'w', encoding='utf-8').write(m)
print('ok, english strings:', len(EN))
