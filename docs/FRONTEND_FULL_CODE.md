# Full code giao diện AutoValue India

Giao diện đen–mint–đỏ và ảnh thật. Dùng cùng app.py, photo_catalog.py và thư mục static/cars có sẵn trong kho; main file Streamlit vẫn là app.py.

## index.html

```html
<!doctype html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#171717">
  <title>AutoValue India · Giá xe cũ</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<!-- av:hero -->
<a class="av-skip" href="#prediction">Thông tin ô tô</a>
<div class="av-progress" aria-hidden="true"></div>
<div class="av-loader" aria-hidden="true">
  <span class="av-wordmark">AUTOVALUE INDIA</span>
  <span class="av-loader-track"><i></i></span><span class="av-percent">0%</span>
</div>
<div class="av-cursor" aria-hidden="true"><span class="av-cursor-label">Xem</span></div>
<header class="av-header">
  <a class="av-brand" href="#home" aria-label="AutoValue India, về đầu trang"><span class="av-symbol" aria-hidden="true">A<span>V</span></span>AUTOVALUE INDIA</a>
  <button class="av-menu-button" aria-label="Mở menu" aria-expanded="false" aria-controls="av-menu"><span></span><span></span></button>
  <nav id="av-menu" class="av-nav" aria-label="Điều hướng chính"><span class="av-nav-indicator" aria-hidden="true"></span>
    <a href="#home" class="is-active">AutoValue India</a>
    <a href="#prediction">Thông tin ô tô</a>
    <a href="#data">Về dữ liệu</a>
    <a href="#prediction" class="av-nav-cta">Dự đoán giá xe <span aria-hidden="true">↗</span></a>
  </nav>
</header>
<div class="av-hero-stage"><section id="home" class="av-hero">
  <div class="av-grid" aria-hidden="true"></div><div class="av-orb" aria-hidden="true"></div>
  <div class="av-hero-copy">
    <p class="av-eyebrow">AUTOVALUE INDIA <span aria-hidden="true">/</span> ẤN ĐỘ · INR (₹)</p>
    <h1 aria-label="Định giá ô tô cũ bằng thuật toán AI"><span class="av-mask"><span class="av-title-line">Định giá ô tô cũ</span></span>
      <span class="av-mask"><span class="av-title-line">bằng thuật toán <em>AI</em></span></span></h1>
    <a href="#prediction" class="av-cta av-magnetic">Dự đoán giá xe <span aria-hidden="true">↗</span></a>
  </div>
  <div class="av-art" data-interactive-car>
    <div class="av-car-halo"></div>
    <img class="av-car av-car-photo" src="static/cars/kwid.webp" alt="Renault Kwid RXT(O), ảnh thật chụp năm 2016" decoding="async" fetchpriority="high" width="1440" height="961">
    <span aria-hidden="true" class="av-spark" style="left:23%;top:42%;--spark-size:33px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:39%;top:34%;--spark-size:46px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:59%;top:28%;--spark-size:35px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:76%;top:41%;--spark-size:49px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:83%;top:60%;--spark-size:31px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:60%;top:69%;--spark-size:41px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:37%;top:70%;--spark-size:31px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span aria-hidden="true" class="av-spark" style="left:15%;top:58%;--spark-size:40px"><svg xmlns="http://www.w3.org/2000/svg" class="av-spark-visual" viewBox="0 0 80 100" fill="none"><path d="M40 8c0 27 4 36 28 42-24 6-28 15-28 42 0-27-4-36-28-42C36 44 40 35 40 8Z" fill="#C8A86B"/><path d="M40 8v84M12 50h56" stroke="#FAF4E7" stroke-width="1.5"/></svg></span><span class="av-art-note">AUTOVALUE <span>INDIA</span></span><p class="av-photo-caption">Renault Kwid RXT(O) · Ảnh: Aswïn KP · <a href="https://commons.wikimedia.org/wiki/File:Renault_KWID_RXT(O).jpg" target="_blank" rel="noopener noreferrer">Nguồn ảnh</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0" target="_blank" rel="noopener noreferrer">CC BY-SA 4.0</a></p>
  </div>
  <a href="#prediction" class="av-scroll" aria-label="Cuộn đến thông tin ô tô"><span aria-hidden="true">↓</span>Thông tin ô tô</a>
  <div class="av-hero-stat av-hero-stat--left"><strong class="av-count" data-stat="usable" data-count="6904">6.904</strong><span class="av-stat-label">Mẫu ô tô sau xử lý</span></div>
  <div class="av-hero-stat av-hero-stat--right"><strong class="av-count" data-stat="test" data-count="1380">1.380</strong><span class="av-stat-label">Mẫu kiểm tra độc lập</span></div>
  <span class="av-hero-index" aria-hidden="true">01 / AUTOVALUE</span>
</section></div>
<!-- /av:hero -->
<!-- av:footer -->
<footer class="av-footer">
  <div data-av-reveal><a class="av-brand" href="#home">AUTOVALUE INDIA <span aria-hidden="true">↗</span></a><p>Định giá ô tô cũ bằng AI.</p></div>
  <div data-av-reveal><a href="#prediction">Thông tin ô tô</a><a href="#data">Về dữ liệu và phạm vi dự đoán</a></div>
  <div data-av-reveal><a href="https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho" target="_blank" rel="noopener noreferrer">Nguồn: Nehal Birla · CarDekho trên Kaggle ↗</a><a href="https://opendatacommons.org/licenses/odbl/1.0/" target="_blank" rel="noopener noreferrer">Giấy phép dữ liệu ↗</a></div>
</footer>
<a class="av-top" href="#home" aria-label="Lên đầu trang">↑</a>
<!-- /av:footer -->
<script src="script.js"></script>
</body>
</html>

```

## style.css

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--av-navy:#15324F;--av-ink:#0F172A;--av-teal:#0F766E;--av-mint:#A8E4D0;--av-paper:#F8FAFC;--av-line:#DCE5EB;--av-radius:24px;--av-shadow:0 18px 60px #15324f0c;--av-speed:.3s;--av-ease:cubic-bezier(.22,1,.36,1);--av-body:'Plus Jakarta Sans',sans-serif;--av-title:'Space Grotesk',sans-serif}
html{scroll-padding-top:100px}body,[data-testid="stApp"]{background:var(--av-paper);color:var(--av-ink);font-family:var(--av-body)}
.stApp [data-testid="stMainBlockContainer"]{max-width:none;padding:0 0 0!important}.stApp [data-testid="stVerticalBlock"]{gap:1rem}
[data-testid="stHeader"]{background:transparent!important;pointer-events:none;z-index:5}[data-testid="stToolbar"]{pointer-events:auto}
.av-header,.av-hero,.av-footer,.av-loader{font-family:var(--av-body)}.av-header a,.av-hero a,.av-footer a,.av-top{color:inherit;text-decoration:none!important}
.av-header a:focus-visible,.av-hero a:focus-visible,.av-footer a:focus-visible,.av-top:focus-visible,button:focus-visible{outline:3px solid var(--av-mint);outline-offset:6px}
.av-skip{position:fixed;top:10px;left:10px;z-index:1100;transform:translateY(-200%);background:white;color:var(--av-ink);padding:12px;border-radius:10px}.av-skip:focus{transform:none}
.av-progress{position:fixed;inset:0 0 auto;height:3px;background:var(--av-teal);transform:scaleX(0);transform-origin:left;z-index:1005;pointer-events:none}
.av-header{position:fixed;inset:0 0 auto;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:26px clamp(24px,5vw,80px);color:#fff;transition:transform var(--av-speed) var(--av-ease)}
.av-header:before{content:'';position:absolute;inset:0;z-index:-1;background:#102a43e8;backdrop-filter:blur(20px);box-shadow:0 6px 32px #07172619;opacity:0;transition:opacity var(--av-speed)}
.av-header.is-scrolled{transform:translateY(-8px)}.av-header.is-scrolled:before{opacity:1}.av-header.is-hidden{transform:translateY(-110%)}
.av-brand{display:inline-flex;align-items:center;gap:12px;white-space:nowrap;font-weight:700;font-size:12px;letter-spacing:1.6px}.av-symbol{font-family:var(--av-title);font-size:27px;letter-spacing:-7px;width:39px}.av-symbol span{color:var(--av-mint)}
.av-nav{display:flex;align-items:center;gap:30px;font-size:12px;font-weight:500}.av-nav a{position:relative;padding:8px 0}.av-nav a:after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:var(--av-mint);transform:scaleX(0);transform-origin:left;transition:transform var(--av-speed)}.av-nav a:hover:after,.av-nav a.is-active:after{transform:scaleX(1)}
.av-nav .av-nav-cta{border:1px solid #ffffff45;border-radius:100px;padding:12px 18px;display:flex;gap:22px}.av-nav .av-nav-cta:after{display:none}.av-menu-button{display:none}
.av-hero{position:relative;isolation:isolate;min-height:750px;min-height:min(850px,100svh);overflow:hidden;background:#102B44;color:#fff;display:flex;align-items:center;padding:145px clamp(24px,7vw,110px) 120px}
.av-hero-copy{position:relative;z-index:2;max-width:680px}.av-eyebrow{font-size:10px;font-weight:600;letter-spacing:2.1px;color:#B3CDD5;margin:0 0 32px}.av-eyebrow span{margin:0 14px;color:var(--av-mint)}
.av-hero h1{font-family:var(--av-title);font-size:clamp(46px,6.5vw,96px);line-height:1.06;letter-spacing:-3.8px;font-weight:500;color:#fff;margin:0 0 28px}.av-mask{display:block;overflow:hidden;padding-bottom:6px;margin-bottom:-6px}.av-mask>span{display:block}.av-hero h1 em{font-style:normal;color:var(--av-mint)}
.av-lead{font-size:15px;line-height:1.9;color:#C7D8E3;max-width:375px;margin:0 0 34px}.av-cta{position:relative;display:inline-flex;align-items:center;gap:34px;background:var(--av-mint);color:#102B44!important;border-radius:100px;padding:18px 25px;font-size:13px;font-weight:700;overflow:hidden}.av-cta:before{content:'';position:absolute;inset:-50%;background:linear-gradient(100deg,transparent 40%,#ffffff80,transparent 60%);transform:translateX(-110%) rotate(12deg);transition:transform .7s}.av-cta:hover:before{transform:translateX(110%) rotate(12deg)}.av-cta:active{scale:.97}.av-cta span{font-size:21px}
.av-grid{position:absolute;inset:0;background-image:linear-gradient(#ffffff03 1px,transparent 1px),linear-gradient(90deg,#ffffff03 1px,transparent 1px);background-size:80px 80px;z-index:-2}.av-orb{position:absolute;width:800px;height:800px;border-radius:50%;right:-150px;top:-20px;background:radial-gradient(circle,#28716d59,transparent 67%);z-index:-1}
.av-art{position:absolute;right:-20px;top:25%;width:53%;max-width:840px;transform:rotate(-6deg);opacity:.95}.av-car{width:100%;position:relative;z-index:1;filter:drop-shadow(0 30px 25px #03132145)}.av-car-halo{position:absolute;inset:10% 0;border:1px solid #9ddac020;border-radius:50%;transform:rotate(-10deg)}.av-car-halo:after{content:'';position:absolute;inset:30px;border:1px solid #9ddac018;border-radius:50%}.av-art-note{position:absolute;right:15%;bottom:-10px;letter-spacing:7px;font-size:9px;color:#B1CBD2}.av-art-note span{color:var(--av-mint)}
.av-scroll{position:absolute;bottom:35px;left:clamp(24px,7vw,110px);display:flex;align-items:center;gap:13px;font-size:10px;color:#C7D8E3!important}.av-scroll>span{display:grid;place-items:center;border:1px solid #ffffff30;border-radius:50%;width:35px;height:35px;animation:av-bob 2s ease-in-out infinite}.av-hero-index{position:absolute;right:6%;bottom:48px;font-size:9px;letter-spacing:3px;color:#89A4B7}
.av-loader{position:fixed;inset:0;background:#102B44;z-index:2000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;color:#fff;pointer-events:none;animation:av-loader-exit .5s 1s forwards}.av-wordmark{font-weight:600;letter-spacing:4px;font-size:13px}.av-loader-track{width:180px;height:2px;background:#ffffff20;overflow:hidden}.av-loader-track i{display:block;height:100%;background:var(--av-mint);transform:scaleX(0);transform-origin:left;animation:av-load .8s forwards}.av-percent{font-size:10px;color:#BDD9DA;letter-spacing:2px}
.av-cursor{position:fixed;top:0;left:0;width:13px;height:13px;margin:-6px;border:1px solid var(--av-teal);border-radius:50%;pointer-events:none;z-index:2100;opacity:0}.av-top{position:fixed;bottom:26px;right:26px;z-index:900;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--av-navy);color:#fff!important;box-shadow:var(--av-shadow);opacity:0;visibility:hidden;transform:translateY(12px);transition:opacity var(--av-speed),transform var(--av-speed),visibility var(--av-speed)}.av-top.is-visible{opacity:1;visibility:visible;transform:none}
.st-key-prediction-panel,.st-key-result-panel,.st-key-about-panel{max-width:1040px;margin:0 auto;width:calc(100% - 64px)!important}.st-key-prediction-panel{padding:34px 40px 40px;background:#fff;border:1px solid var(--av-line);border-radius:var(--av-radius);box-shadow:var(--av-shadow);margin-top:38px;margin-bottom:24px}
.stApp [data-testid="stCaptionContainer"]{font-family:var(--av-body);line-height:1.8}.stApp [data-testid="stMainBlockContainer"]>[data-testid="stVerticalBlock"]>[data-testid="stElementContainer"]:has(>[data-testid="stCaptionContainer"]){max-width:1040px;margin:22px auto 0;width:calc(100% - 64px)}
.st-key-prediction-panel h2,.st-key-result-panel h2{font-family:var(--av-title);font-size:28px;font-weight:500;letter-spacing:-1px;color:var(--av-navy);margin-bottom:20px}.stApp [data-testid="stForm"]{border:0;padding:0}.stApp [data-testid="stSelectbox"],.stApp [data-testid="stNumberInput"]{position:relative}
.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"]) label{font-family:var(--av-body);font-size:12px;font-weight:600;color:#536477;transition:color var(--av-speed),transform var(--av-speed)}.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"]):focus-within label{color:var(--av-teal);transform:translateY(-2px)}
.stApp [data-baseweb="select"]>div,.stApp [data-testid="stNumberInputContainer"]{background:#F7F9FB;border:1px solid var(--av-line);border-radius:12px;min-height:48px;box-shadow:none}.stApp [data-baseweb="select"]:focus-within>div,.stApp [data-testid="stNumberInputContainer"]:focus-within{outline:2px solid #0F766E45;outline-offset:2px}
.stApp input{font-family:var(--av-body)}.stApp [data-testid="stExpander"]{border-color:var(--av-line);border-radius:16px;background:#fff}.stApp [data-testid="stFormSubmitButton"] button{position:relative;overflow:hidden;min-height:54px;border-radius:12px;background:var(--av-teal);color:#fff;border:0;font-family:var(--av-body);font-weight:600}.stApp [data-testid="stFormSubmitButton"] button:before{content:'';position:absolute;inset:-50%;background:linear-gradient(100deg,transparent 40%,#ffffff35,transparent 60%);transform:translateX(-110%);transition:transform .7s}.stApp [data-testid="stFormSubmitButton"] button:hover:before{transform:translateX(110%)}.stApp [data-testid="stFormSubmitButton"] button:active{transform:scale(.99)}
.stApp button[data-av-busy]:after{content:'';position:absolute;right:18px;width:17px;height:17px;border:2px solid #ffffff50;border-top-color:#fff;border-radius:50%;animation:av-spin .7s linear infinite}.stApp [data-testid="stDownloadButton"] button{border-radius:10px;color:var(--av-teal);border-color:var(--av-line);min-height:44px}
.st-key-result-panel{margin:15px auto 30px;padding:30px 0}.stApp [data-testid="stMetric"]{position:relative;overflow:hidden;padding:24px;background:#fff;border:1px solid var(--av-line);border-radius:20px;box-shadow:var(--av-shadow);transition:transform var(--av-speed) var(--av-ease)}.stApp [data-testid="stMetric"]:after{content:'';position:absolute;inset:0;border:1px solid var(--av-teal);border-radius:inherit;opacity:0;pointer-events:none;transition:opacity var(--av-speed)}.stApp [data-testid="stMetric"]:hover{transform:translateY(-8px)}.stApp [data-testid="stMetric"]:hover:after{opacity:.6}.stApp [data-testid="stMetricValue"]{font-family:var(--av-title);color:var(--av-teal);letter-spacing:-1px}
.av-check{width:26px;height:26px;vertical-align:middle;margin-right:12px;stroke:var(--av-teal);fill:none;stroke-width:2;stroke-dasharray:45;animation:av-check .8s var(--av-ease) both}.av-shake{animation:av-shake .3s}.st-key-about-panel{margin-bottom:64px;scroll-margin-top:100px}
.av-footer{background:#102B44;color:#B8CDDA;display:grid;grid-template-columns:1fr .8fr 1.2fr;gap:50px;padding:60px clamp(24px,7vw,110px);font-size:11px;line-height:1.9}.av-footer>div{display:flex;flex-direction:column;gap:14px}.av-footer .av-brand{color:#fff}.av-footer p{margin:0}.av-footer a:hover{color:var(--av-mint)}
@keyframes av-bob{50%{transform:translateY(5px)}}@keyframes av-load{to{transform:scaleX(1)}}@keyframes av-loader-exit{to{opacity:0;visibility:hidden;transform:translateY(-10px)}}@keyframes av-spin{to{transform:rotate(360deg)}}@keyframes av-check{from{stroke-dashoffset:45}to{stroke-dashoffset:0}}@keyframes av-shake{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
@media(min-width:1000px){.av-nav.is-open{display:flex}}@media(max-width:1000px){.av-header{padding:24px}.av-menu-button{display:flex;position:relative;z-index:2;flex-direction:column;justify-content:center;gap:6px;border:1px solid #ffffff40;border-radius:50%;width:44px;height:44px;padding:11px;background:none}.av-menu-button span{height:1px;background:white;width:20px;transition:transform var(--av-speed)}.av-menu-button[aria-expanded="true"] span:first-child{transform:translateY(3.5px) rotate(45deg)}.av-menu-button[aria-expanded="true"] span:last-child{transform:translateY(-3.5px) rotate(-45deg)}.av-nav{display:none;position:fixed;inset:0;height:100dvh;background:#102B44;flex-direction:column;justify-content:center;gap:22px;font-size:22px}.av-nav.is-open{display:flex}.av-nav .av-nav-cta{font-size:15px;margin-top:20px}.av-art{width:56%;right:-10%;top:34%;opacity:.55}.av-hero-copy{max-width:630px}.av-footer{gap:28px}}
@media(max-width:600px){.av-header{padding:18px 20px}.av-brand{font-size:10px;letter-spacing:1px;gap:8px}.av-hero{min-height:760px;padding:145px 24px 270px;align-items:flex-start}.av-hero h1{font-size:49px;letter-spacing:-2.2px}.av-eyebrow{font-size:8px;letter-spacing:1.3px;margin-bottom:26px}.av-eyebrow span{margin:0 7px}.av-lead{font-size:13px;max-width:290px}.av-cta{padding:15px 21px;font-size:12px}.av-art{width:110%;max-width:none;right:-8%;top:auto;bottom:70px;opacity:.75}.av-art-note{font-size:7px;bottom:5px}.av-scroll{left:24px;bottom:25px}.av-hero-index{font-size:7px;bottom:40px}.st-key-prediction-panel,.st-key-result-panel,.st-key-about-panel{width:calc(100% - 32px)!important}.st-key-prediction-panel{padding:22px 18px;margin-top:20px}.stApp [data-testid="stMainBlockContainer"]>[data-testid="stVerticalBlock"]>[data-testid="stElementContainer"]:has(>[data-testid="stCaptionContainer"]){width:calc(100% - 40px)}.st-key-prediction-panel h2,.st-key-result-panel h2{font-size:24px}.stApp [data-testid="stMetric"]{padding:20px}.av-footer{grid-template-columns:1fr;padding:38px 24px;gap:30px}.av-top{right:16px;bottom:16px;width:42px;height:42px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition:none!important}.av-loader,.av-cursor{display:none!important}.av-header,.av-art,.av-mask>span,[data-av-reveal]{transform:none!important;opacity:1!important}.av-top:not(.is-visible){opacity:0!important}.av-progress{transition:none!important}}
@media(hover:none),(pointer:coarse){.av-cursor{display:none!important}}

.st-key-intro-note{max-width:1040px;width:calc(100% - 64px)!important;margin:22px auto 0}.stApp [data-testid="stToolbar"]{display:none}.av-nav-cta span,.av-cta span{font-family:Arial,sans-serif}@media(max-width:600px){.st-key-intro-note{width:calc(100% - 40px)!important}}

.av-menu-open{overflow:hidden!important}.av-cta>span,.av-nav-cta>span{font-size:0!important;position:relative;width:12px;height:12px;border-top:1.5px solid currentColor;border-right:1.5px solid currentColor;display:block}.av-cta>span:after,.av-nav-cta>span:after{content:'';position:absolute;right:0;top:0;width:16px;height:1.5px;background:currentColor;transform:rotate(-45deg);transform-origin:right top}
.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"])>label{position:absolute;top:6px;left:14px;z-index:2;margin:0;font-size:11px;min-height:0;pointer-events:auto;transition:transform var(--av-speed)}.stApp [data-baseweb="select"]>div{min-height:64px;padding-top:16px}.stApp [data-testid="stNumberInputContainer"]{min-height:64px}.stApp [data-testid="stNumberInputContainer"] input{padding-top:20px;padding-bottom:4px}
.stApp [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"]{min-height:64px;height:64px;background:#F7F9FB;border:1px solid var(--av-line);border-radius:12px}.stApp [data-testid="stSelectbox"] input[role="combobox"]{height:62px;padding:21px 13px 5px;background:transparent}.stApp [data-testid="stSelectbox"] .react-aria-ComboBox button{height:62px;background:transparent;border:0;border-radius:0 12px 12px 0}.stApp [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"]:focus-within{outline:2px solid #0F766E45;outline-offset:2px}.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"])>label{pointer-events:none}
@media(max-width:1000px){.av-cursor{display:none!important}}


/* Creative studio edition. Existing form selectors and prediction UI stay intact. */
:root{--av-serif:'Cormorant Garamond',Georgia,serif;--av-studio:#F1F2EA;--av-forest:#143E3C;--av-soft-ink:#4F6663;--av-curtain-radius:32px}
body,[data-testid="stApp"]{background:var(--av-studio)}
.av-header{color:var(--av-forest);min-height:90px;padding:25px clamp(22px,4.5vw,72px);align-items:flex-start;pointer-events:none}
.av-header>*{pointer-events:auto}
.av-header:before{background:#f1f2eae6;box-shadow:0 6px 32px #143e3c09}
.av-header .av-brand{padding-top:9px}
.av-symbol span{color:var(--av-teal)}
.av-nav{position:absolute;left:50%;top:20px;transform:translateX(-50%);padding:6px;gap:2px;min-height:54px;border:1px solid #ffffffa0;border-radius:100px;background:#dce5dc85;backdrop-filter:blur(20px);box-shadow:0 8px 32px #143e3c0a;isolation:isolate;white-space:nowrap}
.av-nav a{z-index:1;position:relative;border-radius:100px;padding:13px 19px;font-size:11px;line-height:1.4;color:var(--av-forest)}
.av-nav a:after{display:none}
.av-nav a.is-active:not(.av-nav-cta){background:#fff}
.av-nav:has(.av-nav-indicator[style]) a.is-active:not(.av-nav-cta),.av-nav.has-indicator a.is-active:not(.av-nav-cta){background:transparent}
.av-nav .av-nav-cta{padding:13px 20px;margin-left:3px;border:0;background:var(--av-forest);color:#fff;gap:14px;font-size:11px;line-height:1.4}
.av-nav-indicator{position:absolute;left:6px;top:6px;z-index:0;display:block;min-height:42px;border-radius:100px;background:#fff;pointer-events:none}
.av-hero{min-height:min(920px,100svh);background:var(--av-studio);color:var(--av-forest);padding:155px clamp(24px,7vw,110px) 190px;align-items:center;transform-origin:center top}
.av-hero-copy{max-width:650px}
.av-eyebrow{color:#58736D;font-size:9px;letter-spacing:2.2px;margin-bottom:26px}
.av-eyebrow span{color:var(--av-teal)}
.av-hero h1{font-family:var(--av-serif);font-size:clamp(64px,7.2vw,112px);font-weight:500;line-height:.95;letter-spacing:-3.5px;color:var(--av-forest);margin-bottom:26px;max-width:650px}
.av-hero h1 em{font-style:normal;color:var(--av-teal)}
.av-mask{padding-top:.12em;padding-bottom:.17em;margin-top:-.12em;margin-bottom:-.17em}
.av-title-line{display:block}
.av-word{display:inline-block;white-space:nowrap}
.char{display:inline-block;position:relative;vertical-align:baseline;line-height:inherit;isolation:isolate}
.av-glyph-normal{display:inline-block;opacity:1;transform:scale(1);transition:opacity .35s var(--av-ease),transform .6s var(--av-ease)}
.av-glyph-italic{position:absolute;inset:0 auto auto 0;display:block;min-width:100%;font-style:italic;font-weight:500;opacity:0;transform:scale(.96);transform-origin:50% 75%;pointer-events:none;transition:opacity .35s var(--av-ease),transform .6s var(--av-ease)}
.char.is-morphed .av-glyph-normal{opacity:0;transform:scale(.98)}
.char.is-morphed .av-glyph-italic{opacity:1;transform:scale(1.08)}
.av-lead{color:var(--av-soft-ink);font-size:14px;line-height:1.9;max-width:360px}
.av-cta{background:var(--av-forest);color:#fff!important;padding:17px 25px;box-shadow:0 10px 30px #143e3c12}
.av-grid{opacity:.6;background-image:linear-gradient(#143e3c06 1px,transparent 1px),linear-gradient(90deg,#143e3c06 1px,transparent 1px);background-size:90px 90px}
.av-orb{background:radial-gradient(circle,#adc9b945,transparent 68%);right:-170px;top:10%;width:950px;height:950px}
.av-art{width:51%;max-width:800px;right:2%;top:31%;transform:none;opacity:1;padding:35px 0;touch-action:pan-y}
.av-car{filter:drop-shadow(0 35px 25px #16332c1f);display:block;height:auto}
.av-car-halo{inset:14% 3% 3%;transform:rotate(-8deg);border-color:#74998726;background:radial-gradient(ellipse at 50% 70%,#b5cdb829,transparent 66%)}
.av-car-halo:after{border-color:#74998720;inset:25px}
.av-art-note{bottom:9px;color:#638077;letter-spacing:6px;font-size:8px}
.av-art-note span{color:var(--av-teal)}
.av-spark{position:absolute;z-index:4;display:block;width:52px;height:52px;opacity:0;transform:scale(0) rotate(-8deg);transform-origin:50% 100%;pointer-events:none}
.av-spark-visual{display:block;width:100%;height:100%;object-fit:contain;transform-origin:50% 90%;filter:drop-shadow(0 4px 7px #143e3c16)}
.av-spark:nth-of-type(2n){width:40px;height:40px}.av-spark:nth-of-type(3n){width:64px;height:64px}
.av-hero-stat{position:absolute;bottom:34px;z-index:3;display:flex;flex-direction:column;gap:7px;max-width:230px;color:var(--av-forest)}
.av-hero-stat--left,.av-hero-stat:first-of-type{left:clamp(24px,7vw,110px)}
.av-hero-stat--right{right:clamp(24px,7vw,110px);text-align:right;align-items:flex-end}
.av-hero-stat .av-count{font-family:var(--av-serif);font-size:51px;line-height:.95;font-weight:500;letter-spacing:-2px;font-variant-numeric:tabular-nums}
.av-hero-stat small,.av-stat-label{font-size:10px;line-height:1.6;letter-spacing:.2px;color:#4F6962}
.av-scroll{left:50%;bottom:42px;transform:translateX(-50%);color:#3E5C55!important}
.av-scroll>span{border-color:#52766b40}
.av-hero-index{right:7%;bottom:146px;color:#638077}
.av-loader{background:var(--av-studio);color:var(--av-forest)}
.av-loader-track{background:#143e3c1c}.av-loader-track i{background:var(--av-teal)}.av-percent{color:#496B61}
.av-cursor{border-color:var(--av-forest);background:#f1f2ea0a;display:grid;place-items:center}
.av-cursor-label{display:block;font-family:var(--av-body);font-size:8px;font-weight:600;line-height:1;color:var(--av-forest);white-space:nowrap;opacity:0;transform:scale(.5);pointer-events:none}
.av-cursor.is-view{width:58px;height:58px;margin:-29px;border-color:var(--av-forest);background:#fff9;backdrop-filter:blur(8px)}
.av-cursor.is-view .av-cursor-label{opacity:1;transform:scale(1)}
.st-key-curtain{position:relative;isolation:isolate;z-index:4;width:100%;margin-top:-1px;padding:38px 0 28px;background:var(--av-forest);border-radius:var(--av-curtain-radius) var(--av-curtain-radius) 0 0;box-shadow:0 -18px 70px #16372e12;transform-origin:50% 0}
.st-key-curtain>.stVerticalBlock,.st-key-curtain>[data-testid="stVerticalBlock"]{gap:1.5rem}
.st-key-curtain .st-key-intro-note{margin-top:0;margin-bottom:16px}
.st-key-curtain .st-key-intro-note [data-testid="stCaptionContainer"],.st-key-curtain .st-key-intro-note p{color:#DBE8E2}
.st-key-curtain .st-key-prediction-panel{margin-top:42px;border-color:#ffffff40;box-shadow:0 22px 70px #041d1920}
.st-key-curtain .st-key-result-panel{color:#E8F0EB}
.st-key-curtain .st-key-result-panel h2{color:#F5F7EE}
.st-key-curtain .st-key-result-panel [data-testid="stMarkdownContainer"] p,.st-key-curtain .st-key-result-panel [data-testid="stCaptionContainer"]{color:#DCE8E2}
.st-key-curtain .st-key-result-panel [data-testid="stMetric"] [data-testid="stMarkdownContainer"] p,.st-key-curtain .st-key-result-panel [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,.st-key-curtain .st-key-result-panel [data-testid="stExpander"] [data-testid="stCaptionContainer"],.st-key-curtain .st-key-result-panel [data-testid="stAlert"] p{color:var(--av-ink)}
.st-key-curtain .st-key-result-panel [data-testid="stDownloadButton"] button{background:#fff}
.st-key-curtain .st-key-about-panel{margin-bottom:36px}
.av-collection{position:relative;isolation:isolate;max-width:1140px;margin:18px auto 0;width:calc(100% - 64px);padding:44px 50px 30px;overflow:hidden;border-radius:24px;background:#E1E8DC;color:#183C35}
.av-collection-background{position:absolute;inset:0;z-index:-1;opacity:0;pointer-events:none}
.av-collection-copy{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;margin-bottom:30px}
.av-collection-copy h2{font-family:var(--av-serif);font-size:clamp(34px,3.5vw,48px);font-weight:500;line-height:1.05;letter-spacing:-1.2px;max-width:450px;margin:0;color:#183C35}
.av-collection-copy p{font-family:var(--av-body);font-size:10px;line-height:1.8;max-width:270px;margin:0;color:#426153}
.av-collection-list{position:relative}
.av-collection-row{position:relative;display:grid;grid-template-columns:minmax(0,1fr) auto minmax(130px,.4fr);column-gap:24px;align-items:center;width:100%;padding:24px 0;border:0;border-top:1px solid #183c352d;background:transparent;color:#183C35;text-align:left;cursor:pointer;font-family:var(--av-body);transition:opacity .4s var(--av-ease);appearance:none;-webkit-tap-highlight-color:transparent}
.av-collection-row:focus-visible{outline:2px solid #183C35;outline-offset:5px;border-radius:6px;opacity:1!important}
.av-collection-row:last-child{border-bottom:1px solid #183c352d}
.av-row-name{display:block;font-family:var(--av-serif);font-size:clamp(28px,3.5vw,52px);font-weight:500;line-height:1.06;letter-spacing:-1px;text-wrap:balance}
.av-row-tag{display:inline-flex;gap:4px;align-items:center;justify-content:center;padding:6px 10px;border:1px solid #183c3540;border-radius:100px;font-size:9px;line-height:1.4;color:#2F5548;white-space:nowrap}
.av-row-price{font-size:12px;font-weight:600;line-height:1.5;text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.av-row-extra{display:none;grid-column:1/-1;width:100%;padding-top:22px;font-size:11px;line-height:1.8;color:#35574C}
.av-row-image{display:block;width:100%;height:180px;object-fit:contain;background:#f7f7ee80;border:1px solid #ffffffa0;border-radius:16px;margin-bottom:10px}
.av-collection.is-engaged .av-collection-row:not(.is-selected){opacity:.3}
.av-collection.is-engaged .av-collection-row.is-selected{opacity:1}
.av-preview{position:fixed;left:0;top:0;z-index:1090;width:260px;height:190px;margin:-110px 0 0 -130px;overflow:hidden;pointer-events:none;border:4px solid #fff;border-radius:16px;background:#F1F2EA;box-shadow:0 20px 65px #0e28292e;opacity:0;transform:scale(0);transform-origin:50% 70%;color:#183C35}
.av-preview-image{position:absolute;inset:0 0 24px;display:block;width:100%;height:calc(100% - 24px);object-fit:contain;transform-origin:50% 60%}
.av-preview-image img{display:block;width:100%;height:100%;object-fit:contain}
.av-preview-caption{position:absolute;left:12px;right:12px;bottom:7px;display:flex;justify-content:space-between;gap:10px;font-size:8px;line-height:1.4;color:#436657}
.av-preview-caption span:last-child{opacity:.75}
.av-footer{border-top:1px solid #ffffff12;background:#102F2F;color:#D1E0D8;padding-top:48px;padding-bottom:48px}
.av-footer .av-brand{color:#F4F6ED}.av-footer a:hover{color:#fff}
.av-header a:focus-visible,.av-hero a:focus-visible,.av-footer a:focus-visible,.av-top:focus-visible{outline-color:var(--av-teal)}
.av-footer a:focus-visible,.av-top:focus-visible{outline-color:var(--av-mint)}
.st-key-prediction-panel button:focus-visible,.st-key-result-panel button:focus-visible{outline:3px solid var(--av-teal);outline-offset:4px}
@media(min-width:1500px){.av-hero-copy{max-width:710px}.av-hero h1{font-size:120px;max-width:710px}.av-art{right:3%;width:50%;top:29%}}
@media(max-width:1150px) and (min-width:1001px){.av-header .av-brand{font-size:10px;letter-spacing:1px}.av-nav{left:auto;right:32px;transform:none}.av-nav a{padding:12px 14px;font-size:10px}.av-hero h1{font-size:82px;max-width:500px}.av-art{right:-3%;width:54%;top:36%}.av-lead{max-width:300px}.av-collection{padding:35px}.av-row-name{font-size:38px}}
@media(max-width:1000px){.av-header{min-height:85px;padding:20px 24px;align-items:center}.av-header .av-brand{padding-top:0}.av-header.is-scrolled{transform:translateY(-4px)}.av-menu-button{border-color:#143e3c40;background:#ffffff50}.av-menu-button span{background:var(--av-forest)}.av-nav{display:none;position:fixed;left:0;right:0;top:0;inset:0;transform:none;padding:90px 26px 50px;height:100dvh;min-height:100dvh;border:0;border-radius:0;box-shadow:none;background:#ECF0E7;white-space:normal;align-items:stretch;gap:14px;z-index:1}.av-nav.is-open{display:flex}.av-nav a{font-family:var(--av-serif);font-size:35px;text-align:center;padding:12px 20px;border-radius:18px;color:var(--av-forest)}.av-nav a.is-active:not(.av-nav-cta){background:#fff}.av-nav-indicator{display:none}.av-nav .av-nav-cta{font-family:var(--av-body);font-size:13px;justify-content:center;margin:20px auto 0;padding:17px 24px;min-width:210px;max-width:270px;background:var(--av-forest);color:#fff;border-radius:100px}.av-menu-button{z-index:3}.av-header .av-brand{position:relative;z-index:3}.av-hero{min-height:960px;padding:150px 7vw 190px;align-items:flex-start}.av-hero-copy{max-width:650px}.av-hero h1{font-size:clamp(70px,10vw,100px);max-width:650px}.av-art{top:auto;bottom:150px;right:3%;width:75%;max-width:700px;opacity:1}.av-art-note{right:6%;bottom:2px}.av-hero-stat{bottom:32px}.av-hero-index{bottom:135px}.av-collection{padding:36px 30px;width:calc(100% - 48px)}.av-collection-copy{display:block;margin-bottom:25px}.av-collection-copy h2{max-width:520px}.av-collection-copy p{max-width:480px;margin-top:15px}.av-collection-row{grid-template-columns:minmax(0,1fr) auto;column-gap:16px;padding:23px 0}.av-row-name{font-size:clamp(32px,4.5vw,46px);grid-column:1;grid-row:1}.av-row-tag{grid-column:1;grid-row:2;justify-self:start;margin-top:9px;font-size:9px}.av-row-price{grid-column:2;grid-row:1/3;font-size:12px}.av-collection-row[aria-expanded="true"] .av-row-extra{display:block}.av-row-extra[hidden]{display:none!important}.av-collection-row[aria-expanded="true"] .av-row-extra[hidden]{display:block!important}.av-preview{display:none!important}.av-cursor{display:none!important}.av-collection.is-engaged .av-collection-row:not(.is-selected){opacity:1}.av-spark{width:43px;height:43px}}
@media(max-width:600px){.av-header{padding:17px 20px;min-height:78px}.av-header .av-brand{font-size:9px;letter-spacing:1px}.av-hero{min-height:940px;padding:132px 24px 210px;overflow:hidden}.av-hero h1{font-size:clamp(57px,15.1vw,80px);line-height:.97;letter-spacing:-2.3px;margin-bottom:23px}.av-hero-copy{max-width:100%}.av-eyebrow{font-size:8px;letter-spacing:1.1px;white-space:nowrap;margin-bottom:24px}.av-eyebrow span{margin:0 7px}.av-lead{font-size:12px;line-height:1.9;max-width:290px;margin-bottom:26px}.av-cta{padding:16px 22px;font-size:11px}.av-art{width:115%;max-width:none;left:-8%;right:auto;top:auto;bottom:196px;padding:24px 0;opacity:1}.av-art-note{font-size:6px;letter-spacing:4px;right:13%;bottom:8px}.av-car-halo{inset:10% 8% 2%}.av-hero-index{bottom:170px;font-size:6px;right:24px}.av-scroll{bottom:137px;left:24px;transform:none;font-size:8px}.av-scroll>span{width:28px;height:28px}.av-hero-stat{bottom:37px;gap:6px;max-width:155px}.av-hero-stat--left,.av-hero-stat:first-of-type{left:24px}.av-hero-stat--right{right:24px}.av-hero-stat .av-count{font-size:43px;letter-spacing:-1.7px}.av-hero-stat small,.av-stat-label{font-size:8px;line-height:1.6}.av-spark{width:32px;height:32px}.av-spark:nth-of-type(2n){width:26px;height:26px}.av-spark:nth-of-type(3n){width:44px;height:44px}.st-key-curtain{padding-top:26px;border-radius:28px 28px 0 0}.st-key-curtain .st-key-intro-note{margin-bottom:10px}.av-collection{width:calc(100% - 32px);padding:28px 20px 22px;border-radius:20px;margin-top:12px}.av-collection-copy h2{font-size:36px;letter-spacing:-1px;line-height:1.03}.av-collection-copy p{font-size:9px;line-height:1.9}.av-collection-row{padding:21px 0;column-gap:12px}.av-row-name{font-size:31px;line-height:1.03;letter-spacing:-.7px;max-width:210px}.av-row-tag{font-size:8px;padding:5px 8px;max-width:200px;white-space:normal}.av-row-price{font-size:10px;align-self:center}.av-row-extra{padding-top:18px;font-size:10px}.av-row-image{height:160px;border-radius:13px}.st-key-curtain .st-key-prediction-panel{margin-top:28px}.st-key-curtain .st-key-about-panel{margin-bottom:20px}.av-footer{padding:35px 24px}}
@media(hover:none),(pointer:coarse){.av-preview,.av-cursor{display:none!important}.av-collection.is-engaged .av-collection-row:not(.is-selected){opacity:1}.av-collection-row[aria-expanded="true"] .av-row-extra{display:block}}
@media(prefers-reduced-motion:reduce){.av-hero,.av-hero-copy,.av-title-line,.av-art,.st-key-curtain,.av-collection-row,.av-hero-stat{transform:none!important;opacity:1!important}.av-glyph-normal{opacity:1!important;transform:none!important}.av-glyph-italic{display:none!important}.av-spark{opacity:.8!important;transform:scale(1)!important}.av-spark-visual{transform:none!important}.av-preview,.av-cursor{display:none!important}.av-nav-indicator{transition:none!important}.av-collection.is-engaged .av-collection-row:not(.is-selected){opacity:1!important}}

.av-art-note,.av-hero-index{color:#526D64}.av-preview-caption span:last-child{opacity:1;color:#4F6A5D}.st-key-curtain .st-key-result-panel [role="alert"] p,.st-key-curtain .st-key-result-panel [data-testid="stAlertContainer"] p{color:var(--av-ink)}

.av-preview{margin:0}.av-preview-image img{position:absolute;inset:0}.av-collection-row[aria-expanded="true"] .av-row-extra:not([hidden]){display:block}.av-collection-copy{flex-wrap:wrap}.av-collection-copy>.av-eyebrow{width:100%;max-width:none}
.st-key-curtain .st-key-intro-note [data-testid="stCaptionContainer"],.st-key-curtain .st-key-result-panel>[data-testid="stVerticalBlock"]>[data-testid="stElementContainer"] [data-testid="stCaptionContainer"]{opacity:1}
.av-collection-copy h2{text-wrap:balance}.av-preview>span{position:absolute;left:12px;right:12px;bottom:7px;font-size:8px;line-height:1.4;color:#436657}

/* Photo edition: palette supplied by the user — charcoal, mint, wine red. */
:root{
  --av-navy:#F1F8F4;--av-ink:#F1F8F4;--av-teal:#88F9C0;--av-mint:#88F9C0;
  --av-paper:#171717;--av-studio:#171717;--av-forest:#171717;
  --av-soft-ink:#B8C8BE;--av-line:#3C4540;--av-wine:#A31C1B;
  --av-shadow:0 20px 65px #00000030;
}
body,[data-testid="stApp"]{background:#171717;color:#F1F8F4}
.av-header{color:#F1F8F4}
.av-header:before{background:#171717e8;box-shadow:0 6px 32px #00000020}
.av-header .av-symbol{color:#F1F8F4}.av-header .av-symbol span{color:#88F9C0}
.av-nav{background:#242424b8;border-color:#88f9c02e;box-shadow:0 8px 32px #00000024}
.av-nav a{color:#E8F1EC}
.av-nav a.is-active:not(.av-nav-cta){background:#88F9C0;color:#171717}
.av-nav.has-indicator a.is-active:not(.av-nav-cta),.av-nav:has(.av-nav-indicator[style]) a.is-active:not(.av-nav-cta){background:transparent;color:#171717}
.av-nav-indicator{background:#88F9C0}
.av-nav .av-nav-cta{background:#A31C1B;color:#fff;border:1px solid #d35e5c40}
.av-hero{background:#171717;color:#F1F8F4}
.av-hero h1{color:#F1F8F4}.av-hero h1 em,.av-glyph-italic{color:#88F9C0}
.av-eyebrow{color:#AEBFB4}.av-eyebrow span{color:#88F9C0}
.av-lead{color:#B8C8BE}
.av-grid{opacity:.45;background-image:linear-gradient(#ffffff05 1px,transparent 1px),linear-gradient(90deg,#ffffff05 1px,transparent 1px)}
.av-orb{background:radial-gradient(circle,#A31C1B24,transparent 68%)}
.av-cta{background:#88F9C0;color:#171717!important;box-shadow:0 10px 35px #88f9c00a}
.av-art{width:46%;right:4%;top:25%;padding:0;transform:none;opacity:1}
.av-car-photo{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;object-position:center;border-radius:28px;filter:none;box-shadow:0 28px 75px #00000045;border:1px solid #88f9c02b}
.av-art:before{content:'';position:absolute;inset:-16px 23% -16px -16px;border-left:3px solid #A31C1B;border-top:1px solid #A31C1B66;border-bottom:1px solid #A31C1B66;border-radius:32px 0 0 32px;pointer-events:none;z-index:-1}
.av-car-halo,.av-car-halo:after{border-color:#88f9c018;background:none}
.av-art-note,.av-hero-index{color:#AEBFB4}.av-art-note span{color:#88F9C0}
.av-art-note{bottom:-25px}
.av-photo-caption{display:block;position:relative;margin:12px 2px 0;color:#B8C8BE;font:9px/1.8 var(--av-body);letter-spacing:.1px}
.av-photo-caption a,.av-photo-credit a,.av-photo-credits a,.credit-links a{color:#88F9C0;text-decoration:underline;text-underline-offset:3px}
.av-photo-caption a:hover,.av-photo-credit a:hover,.av-photo-credits a:hover,.credit-links a:hover{color:#fff}
.av-spark-visual{filter:drop-shadow(0 0 9px #88f9c05c)}
.av-spark:nth-child(2n) .av-spark-visual{filter:drop-shadow(0 0 9px #A31C1B80)}
.av-hero-stat{color:#88F9C0}.av-stat-label,.av-hero-stat small{color:#B8C8BE}
.av-scroll{color:#C5D3CA!important}.av-scroll>span{border-color:#88f9c045}
.av-loader{background:#171717;color:#F1F8F4}.av-loader-track{background:#ffffff20}.av-loader-track i{background:#88F9C0}.av-percent{color:#B8C8BE}
.av-cursor{border-color:#88F9C0;background:#88f9c008}.av-cursor-label{color:#171717}.av-cursor.is-view{border-color:#88F9C0;background:#88F9C0e6}
.av-top{background:#88F9C0;color:#171717!important;box-shadow:0 10px 30px #00000035}
.av-header a:focus-visible,.av-hero a:focus-visible,.av-footer a:focus-visible,.av-top:focus-visible{outline-color:#88F9C0}
.av-skip{background:#88F9C0;color:#171717}
.st-key-curtain{background:#171717;border-top:1px solid #88f9c030;box-shadow:0 -18px 70px #00000020}
.st-key-curtain .st-key-intro-note p,.st-key-curtain .st-key-intro-note [data-testid="stCaptionContainer"]{color:#B8C8BE;opacity:1}
.st-key-curtain .st-key-prediction-panel{background:#202020;color:#F1F8F4;border-color:#3C4540;box-shadow:0 22px 70px #00000024}
.st-key-prediction-panel h2,.st-key-result-panel h2{color:#F1F8F4}
.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"]) label{color:#B8C8BE}
.stApp :is([data-testid="stSelectbox"],[data-testid="stNumberInput"]):focus-within label{color:#88F9C0}
.stApp [data-baseweb="select"]>div,.stApp [data-testid="stNumberInputContainer"],.stApp [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"]{background:#292929;border-color:#4A544E;color:#F1F8F4}
.stApp input,.stApp [data-testid="stSelectbox"] input[role="combobox"]{color:#F1F8F4;background:transparent}
.stApp [data-testid="stNumberInputContainer"] button,.stApp [data-testid="stSelectbox"] .react-aria-ComboBox button{background:transparent;color:#D3E1D8}
.stApp [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"]:focus-within,.stApp [data-testid="stNumberInputContainer"]:focus-within{outline:2px solid #88F9C0;outline-offset:2px}
.stApp [data-testid="stExpander"]{background:#232323;border-color:#414B45;color:#F1F8F4}
.st-key-prediction-panel [data-testid="stCaptionContainer"],.st-key-about-panel [data-testid="stCaptionContainer"]{color:#BCCBC1;opacity:1}
.stApp [data-testid="stFormSubmitButton"] button{background:#88F9C0;color:#171717;border:0}
.stApp [data-testid="stFormSubmitButton"] button:hover{background:#88F9C0;color:#171717}
.stApp button[data-av-busy]:after{border-color:#17171740;border-top-color:#171717}
.st-key-prediction-panel button:focus-visible,.st-key-result-panel button:focus-visible{outline-color:#88F9C0}
.st-key-curtain .st-key-result-panel{color:#F1F8F4}
.st-key-curtain .st-key-result-panel h2{color:#F1F8F4}
.st-key-curtain .st-key-result-panel [data-testid="stMarkdownContainer"] p,.st-key-curtain .st-key-result-panel [data-testid="stCaptionContainer"]{color:#C0CEC5;opacity:1}
.stApp [data-testid="stMetric"]{background:#222;border-color:#414B45;box-shadow:0 18px 50px #00000020}
.st-key-curtain .st-key-result-panel [data-testid="stMetric"] [data-testid="stMarkdownContainer"] p{color:#C0CEC5}
.stApp [data-testid="stMetricValue"]{color:#88F9C0}
.st-key-curtain .st-key-result-panel [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,.st-key-curtain .st-key-result-panel [data-testid="stExpander"] [data-testid="stCaptionContainer"]{color:#C0CEC5;opacity:1}
.st-key-curtain .st-key-result-panel [data-testid="stDownloadButton"] button{background:#242424;border-color:#88f9c060;color:#88F9C0}
.st-key-curtain .st-key-result-panel [role="alert"] p,.st-key-curtain .st-key-result-panel [data-testid="stAlertContainer"] p{color:#F1F8F4}
.st-key-about-panel{color:#DDE9E1}.st-key-about-panel a{color:#88F9C0}
.av-collection{background:#202520;color:#F1F8F4;border:1px solid #88f9c021}
.av-collection-copy h2{color:#F1F8F4}.av-collection-copy p{color:#B8C8BE}
.av-collection-row{color:#F1F8F4;border-color:#C9DDCF2b}
.av-collection-row:last-child{border-color:#C9DDCF2b}
.av-collection-row:focus-visible{outline-color:#88F9C0}
.av-row-name{color:#F1F8F4}.av-row-tag{color:#BCE3CB;border-color:#88f9c044}.av-row-price{color:#88F9C0}
.av-row-extra{color:#C3D4C9}.av-row-extra a{color:#88F9C0;text-decoration:underline;text-underline-offset:3px}
.av-row-image{object-fit:cover;object-position:center;background:#242424;border-color:#ffffff45;height:260px}
.av-preview{background:#171717;color:#F1F8F4;border-color:#fff;box-shadow:0 20px 65px #00000055}
.av-preview-image,.av-preview-image img{object-fit:cover;object-position:center}
.av-preview-caption,.av-preview>span,.av-preview-caption span:last-child{color:#D5E4DA;opacity:1}
.av-photo-credits,.credit-links{color:#B8C8BE;font:10px/1.9 var(--av-body)}
.av-footer{background:#111;color:#B8C8BE;border-color:#88f9c022}.av-footer .av-brand{color:#F1F8F4}.av-footer a:hover{color:#88F9C0}
@media(min-width:1500px){.av-art{right:4%;width:46%;top:24%}}
@media(max-width:1150px) and (min-width:1001px){.av-art{right:3%;width:45%;top:31%}}
@media(max-width:1000px){
 .av-header:before{background:#171717ec}.av-menu-button{border-color:#88f9c04a;background:#242424d9}.av-menu-button span{background:#88F9C0}
 .av-nav{background:#171717;border-color:#88f9c030}.av-nav a{color:#F1F8F4}.av-nav a.is-active:not(.av-nav-cta){background:#88F9C0;color:#171717}.av-nav .av-nav-cta{background:#A31C1B;color:#fff}
 .av-art{width:70%;right:6%;top:auto;bottom:176px;padding:0;opacity:1}.av-car-photo{aspect-ratio:16/9;border-radius:24px}.av-art-note{bottom:-25px}.av-preview{display:none!important}.av-row-image{height:250px}
}
@media(max-width:600px){
 .av-art{width:88%;left:6%;right:auto;bottom:202px;top:auto;padding:0;opacity:1}.av-car-photo{aspect-ratio:3/2;border-radius:20px;box-shadow:0 18px 45px #00000040}
 .av-art:before{inset:-10px 25% -10px -10px;border-radius:24px 0 0 24px}.av-art-note{right:7%;bottom:-25px}.av-photo-caption{font-size:8px;line-height:1.7;margin-top:9px}.av-row-image{height:195px;border-radius:13px}.av-photo-credits,.credit-links{font-size:9px}
}

.av-art{isolation:isolate}

```

## script.js

```javascript
(() => {
  'use strict';
  const VERSION = 'photo-inline-5';
  if (window.__avMotion) {
    if (window.__avMotion.version === VERSION) window.__avMotion.refresh();
    else window.location.reload();
    return;
  }
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const scroller = $('[data-testid="stMain"]') || document.documentElement;
  const isDocument = scroller === document.documentElement;
  const scrollY = () => isDocument ? window.scrollY : scroller.scrollTop;
  const motion = () => !reduced.matches;
  const desktop = () => fine.matches && innerWidth > 1000;
  const seen = new WeakSet(), counters = new Map(), photoSources = new Map();
  function hydratePhotos() {
    $$('[data-photo-key][data-photo-src]').forEach(el => photoSources.set(el.dataset.photoKey, el.dataset.photoSrc));
    $$('img.av-car-photo[data-photo-id]').forEach(el => {
      const src = el.getAttribute('src') || '';
      if (src.startsWith('data:image/')) photoSources.set(el.dataset.photoId, src);
    });
    $$('img[data-photo-id]').forEach(el => {
      const src = photoSources.get(el.dataset.photoId);
      if (src && el.getAttribute('src') !== src) el.src = src;
    });
    $$('.av-collection-row[data-photo-id]').forEach(el => {
      const src = photoSources.get(el.dataset.photoId);
      if (src && el.dataset.image !== src) el.dataset.image = src;
    });
  }
  const state = {hero:null, collection:null, chars:[], pointer:null, sprites:[], winds:[], distance:0, lastPoint:null, insideCar:false, selected:-1, previewSlot:0, pointerQueued:false};
  let gsap, lenis, ticker, heroContext, listContext, resetTimer, refreshTimer, resizeTimer;
  let open = false, lastY = scrollY(), loaded = 0;

  function load(src) {
    return new Promise(resolve => {
      const script = document.createElement('script'); script.src=src; script.async=true;
      let finished=false;
      const done = ok => {
        if (finished) return; finished=true; loaded++;
        const ratio=Math.min(1,loaded/3), label=$('.av-percent'), bar=$('.av-loader-track i');
        if(label) label.textContent=Math.round(ratio*100)+'%';
        if(bar){bar.style.animation='none';bar.style.transform=`scaleX(${ratio})`;}
        resolve(ok);
      };
      const timer=setTimeout(()=>done(false),3500);
      script.onload=()=>{clearTimeout(timer);done(true);}; script.onerror=()=>{clearTimeout(timer);done(false);};
      document.head.append(script);
    });
  }
  function scrollTo(target) {
    if(!target)return;
    if(lenis && motion())lenis.scrollTo(target,{offset:-100,duration:1.1});
    else {
      const top=target.getBoundingClientRect().top+scrollY()-100-(isDocument?0:scroller.getBoundingClientRect().top);
      (isDocument?window:scroller).scrollTo({top,behavior:motion()?'smooth':'auto'});
    }
  }
  function menu(value) {
    open=value; scroller.classList.toggle('av-menu-open',value);
    $('.av-nav')?.classList.toggle('is-open',value);
    const button=$('.av-menu-button'); button?.setAttribute('aria-expanded',String(value));button?.setAttribute('aria-label',value?'Đóng menu':'Mở menu');
    if(value){$('.av-header')?.classList.remove('is-hidden');lenis?.stop();if(gsap&&motion())gsap.fromTo('.av-nav a',{y:18,opacity:0},{y:0,opacity:1,stagger:.08,duration:.45,clearProps:'all'});}
    else lenis?.start();
    indicator();
  }
  function indicator() {
    const nav=$('.av-nav'), active=$('.av-nav a.is-active'), pill=$('.av-nav-indicator');
    if(!nav||!active||!pill||innerWidth<=1000)return;
    nav.classList.add('has-indicator');
    const a=active.getBoundingClientRect(),n=nav.getBoundingClientRect();
    // Dimensions change only when the active item/layout changes; movement uses transforms.
    pill.style.width=a.width+'px';pill.style.height=a.height+'px';
    if(gsap&&motion())gsap.to(pill,{x:a.left-n.left,y:a.top-n.top,duration:.45,ease:'power3.out',overwrite:true});
    else pill.style.transform=`translate(${a.left-n.left}px,${a.top-n.top}px)`;
  }
  function onScroll() {
    const y=scrollY(),header=$('.av-header'); header?.classList.toggle('is-scrolled',y>35);
    if(!open&&!header?.contains(document.activeElement)&&Math.abs(y-lastY)>4)header?.classList.toggle('is-hidden',y>lastY&&y>220);
    $('.av-top')?.classList.toggle('is-visible',y>400);
    const max=Math.max(1,scroller.scrollHeight-(isDocument?innerHeight:scroller.clientHeight));
    if($('.av-progress'))$('.av-progress').style.transform=`scaleX(${Math.min(1,y/max)})`;
    let active='#home';['#home','#prediction','#data'].forEach(id=>{if($(id)?.getBoundingClientRect().top<190)active=id;});
    let changed=false;
    $$('.av-nav a:not(.av-nav-cta)').forEach(a=>{const current=a.hash===active;if(a.classList.contains('is-active')!==current)changed=true;a.classList.toggle('is-active',current);if(current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
    if(changed)indicator();lastY=y;
    const visible=state.hero&&state.hero.getBoundingClientRect().bottom>0&&state.hero.getBoundingClientRect().top<innerHeight;
    state.winds.forEach(t=>visible&&!document.hidden?t.play():t.pause());
  }
  function segmentTitle(hero) {
    const heading=$('h1',hero);if(!heading)return;
    heading.setAttribute('aria-label',heading.textContent.replace(/\s+/g,' ').trim());
    const segmenter=typeof Intl.Segmenter==='function'?new Intl.Segmenter('vi',{granularity:'grapheme'}):null;
    $$('.av-title-line',hero).forEach(line=>{
      if(line.dataset.segmented)return;line.dataset.segmented='true';line.setAttribute('aria-hidden','true');
      const text=line.textContent.normalize('NFC');line.replaceChildren();
      text.split(/(\s+)/u).forEach(word=>{
        if(!word)return;if(/^\s+$/u.test(word)){line.append(document.createTextNode(word));return;}
        const wrap=document.createElement('span');wrap.className='av-word';
        const graphemes=segmenter?[...segmenter.segment(word)].map(x=>x.segment):Array.from(word);
        graphemes.forEach(glyph=>{
          const char=document.createElement('span');char.className='char';
          const normal=document.createElement('span'),italic=document.createElement('span');
          normal.className='av-glyph-normal';italic.className='av-glyph-italic';normal.textContent=glyph;italic.textContent=glyph;
          char.append(normal,italic);wrap.append(char);
        });line.append(wrap);
      });
    });
    measureChars();
  }
  function measureChars() {
    if(!state.hero)return;
    const origin=state.hero.getBoundingClientRect();
    state.chars=$$('.char',state.hero).map(el=>{el.style.width='';const r=el.getBoundingClientRect();el.style.width=r.width+'px';return{el,x:r.left-origin.left+r.width/2,y:r.top-origin.top+r.height/2};});
  }
  function count(el, target, finishText, decimals=0) {
    if(!gsap||!motion())return;
    const node=el.firstChild;if(!node||node.nodeType!==3)return;
    const value={n:0};counters.set(el,{value,node,finishText});
    gsap.to(value,{n:target,duration:1.05,ease:'power3.out',onUpdate:()=>{node.data=value.n.toLocaleString(el.classList.contains('av-count')?'vi-VN':'en-US',{minimumFractionDigits:decimals,maximumFractionDigits:decimals});if(!el.classList.contains('av-count')){const m=finishText.match(/^([^\d]*)([\d,.]+)(.*)$/);node.data=m[1]+node.data+m[3];}},onComplete:()=>{node.data=finishText;counters.delete(el);}});
  }
  function hideSprites() {
    state.distance=0;state.lastPoint=null;state.winds.forEach(t=>t.kill());state.winds=[];
    if(gsap&&motion())gsap.to([...state.sprites].reverse(),{scale:0,opacity:0,rotation:-8,duration:.65,stagger:.06,overwrite:true});
  }
  function growSprites(number) {
    if(!gsap||!motion())return;
    state.sprites.slice(0,number).forEach(sprite=>{
      if(sprite.dataset.bloomed==='true')return;sprite.dataset.bloomed='true';
      gsap.to(sprite,{scale:1,opacity:1,rotation:0,duration:.9,ease:'elastic.out(1,0.6)',overwrite:true});
      const visual=$('.av-spark-visual',sprite);
      if(visual)state.winds.push(gsap.fromTo(visual,{rotation:-2},{rotation:2,duration:2.5+Math.random(),yoyo:true,repeat:-1,ease:'sine.inOut'}));
    });
  }
  function resetSprites() {hideSprites();state.sprites.forEach(el=>delete el.dataset.bloomed);}
  function setupHero(hero) {
    heroContext?.revert();resetSprites();state.heroReady=false;state.hero=hero;state.chars=[];state.insideCar=false;
    if(!hero)return;
    segmentTitle(hero);state.sprites=$$('.av-spark',hero);state.sprites.forEach(el=>delete el.dataset.bloomed);
    if(!gsap||!motion())return;
    state.heroReady=true;
    heroContext=gsap.context(()=>{
      gsap.set(state.sprites,{scale:0,opacity:0,rotation:-8});
      const stage=hero.closest('.av-hero-stage');
      if(window.ScrollTrigger&&stage){
        gsap.timeline({scrollTrigger:{trigger:stage,scroller:isDocument?window:scroller,start:'top top',end:()=>'+='+Math.min(hero.offsetHeight,innerHeight),pin:hero,pinSpacing:false,scrub:.7,invalidateOnRefresh:true}})
          .to(hero,{scale:.96,opacity:.6,ease:'none'},0).to($('.av-art',hero),{y:24,ease:'none'},0);
        if(!desktop())window.ScrollTrigger.create({trigger:$('.av-art',hero),scroller:isDocument?window:scroller,start:'top 90%',once:true,onEnter:()=>state.sprites.forEach((el,i)=>gsap.delayedCall(i*.13,()=>growSprites(i+1)))});
      }else if(!desktop())growSprites(state.sprites.length);
      const intro=sessionStorage.getItem('av-creative-intro')?0:.35;
      gsap.from('.av-title-line',{yPercent:105,opacity:0,duration:1,delay:intro,stagger:.08,ease:'power4.out',onComplete:measureChars});
      gsap.from('.av-eyebrow,.av-lead,.av-cta',{y:18,opacity:0,delay:intro+.25,stagger:.1,duration:.8,clearProps:'all'});
      gsap.from('.av-car',{scale:1.1,duration:1.3,delay:intro,ease:'power3.out'});
      $$('.av-count',hero).forEach(el=>count(el,Number(el.dataset.count),el.textContent));
    },hero);
    sessionStorage.setItem('av-creative-intro','1');
    document.fonts?.ready.then(measureChars);
  }
  function setRow(index, showPreview=true) {
    const section=state.collection;if(!section)return;
    const rows=$$('.av-collection-row',section),row=rows[index];
    if(!row)return;
    const changed=state.selected!==index;state.selected=index;
    section.classList.add('is-engaged');if(changed)rows.forEach((el,i)=>el.classList.toggle('is-selected',i===index));
    if(changed)$$('.av-collection-background',section).forEach((layer,i)=>{
      if(gsap&&motion())gsap.to(layer,{opacity:i===index?1:0,duration:.6,ease:'power2.out',overwrite:true});else layer.style.opacity=i===index?'1':'0';
    });
    if(!showPreview||!desktop())return;
    const preview=$('.av-preview');if(!preview)return;
    preview.classList.add('is-visible');
    if(state.previewIndex!==index){
      state.previewIndex=index;
      const caption=$('.av-preview-caption',preview);if(caption)caption.textContent=row.dataset.photoCaption||'Ảnh thật cùng dòng xe';
      const images=$$('.av-preview-image img',preview),next=state.previewSlot^1;images[next].src=row.dataset.image;images[next].dataset.photoId=row.dataset.photoId;images[next].alt=row.dataset.photoAlt||'';
      if(gsap&&motion()){
        gsap.to(images[state.previewSlot],{opacity:0,scale:1.1,duration:.3,overwrite:true});
        gsap.fromTo(images[next],{yPercent:100,opacity:1,scale:1.05},{yPercent:0,opacity:1,scale:1,duration:.5,ease:'power3.out',overwrite:true});
      }else images.forEach((img,i)=>img.style.opacity=i===next?'1':'0');
      state.previewSlot=next;
    }
    if(gsap&&motion()){if(changed)gsap.to(preview,{scale:1,opacity:1,duration:.3,overwrite:'auto'});}else preview.style.opacity='1';
  }
  function clearRows() {
    const section=state.collection;if(!section)return;
    section.classList.remove('is-engaged');$$('.av-collection-row',section).forEach(el=>el.classList.remove('is-selected'));
    $$('.av-collection-background',section).forEach(el=>{if(gsap&&motion())gsap.to(el,{opacity:0,duration:.6,overwrite:true});else el.style.opacity='0';});
    const preview=$('.av-preview');preview?.classList.remove('is-visible');
    if(gsap&&preview&&motion())gsap.to(preview,{scale:0,opacity:0,duration:.3,overwrite:'auto'});
    if(preview&&!gsap)preview.style.opacity='0';
    $('.av-cursor')?.classList.remove('is-view');state.selected=-1;state.previewIndex=-1;
  }
  function setupCollection(section) {
    listContext?.revert();state.collectionReady=false;state.collection=section;state.selected=-1;state.previewIndex=-1;state.previewSlot=0;
    if(!section||!gsap||!motion())return;
    state.collectionReady=true;
    listContext=gsap.context(()=>{
      gsap.set('.av-preview',{scale:0,opacity:0});
      gsap.set('.av-preview-image img',{opacity:0});
      if(window.ScrollTrigger)gsap.from($$('.av-collection-row',section),{y:24,opacity:0,duration:.75,stagger:.06,ease:'power3.out',clearProps:'transform,opacity',scrollTrigger:{trigger:section,scroller:isDocument?window:scroller,start:'top 85%',once:true}});
    });
  }
  function pointerFrame() {
    state.pointerQueued=false;const p=state.pointer;if(!p)return;
    if(desktop()&&motion()){
      const cursor=$('.av-cursor');if(cursor){cursor.style.opacity='1';cursor.style.transform=`translate(${p.x}px,${p.y}px) scale(${p.target?.closest('button,a')?1.8:1})`;}
      if(state.hero){
        const r=state.hero.getBoundingClientRect();
        state.chars.forEach(c=>c.el.classList.toggle('is-morphed',Math.hypot(p.x-r.left-c.x,p.y-r.top-c.y)<60));
        const art=$('.av-art',state.hero),a=art?.getBoundingClientRect(),inside=a&&p.x>a.left&&p.x<a.right&&p.y>a.top&&p.y<a.bottom;
        if(inside){
          clearTimeout(resetTimer);state.insideCar=true;
          if(state.lastPoint)state.distance+=Math.hypot(p.x-state.lastPoint.x,p.y-state.lastPoint.y);
          state.lastPoint={x:p.x,y:p.y};growSprites(Math.min(state.sprites.length,Math.floor(state.distance/65)));
        }else if(state.insideCar){state.insideCar=false;state.lastPoint=null;resetTimer=setTimeout(resetSprites,2000);}
      }
    }
    const row=p.target?.closest('.av-collection-row');
    if(row&&desktop()){
      setRow(Number(row.dataset.index));$('.av-cursor')?.classList.add('is-view');
      const preview=$('.av-preview');if(preview){
        const width=preview.offsetWidth||260,height=preview.offsetHeight||180;
        const x=Math.max(12,Math.min(innerWidth-width-12,p.x+24)),y=Math.max(12,Math.min(innerHeight-height-12,p.y-height/2));
        const rotation=Math.max(-8,Math.min(8,(p.x-(state.lastPreviewX??p.x))*.12));state.lastPreviewX=p.x;
        if(gsap&&motion())gsap.to(preview,{x,y,rotation,duration:.32,ease:'power3.out',overwrite:'auto'});else preview.style.transform=`translate(${x}px,${y}px)`;
      }
    }else if(state.selected!==-1&&!state.collection?.contains(document.activeElement))clearRows();
  }
  function reveal(el) {
    if(seen.has(el))return;seen.add(el);
    if(gsap&&motion()&&window.ScrollTrigger)gsap.from(el,{y:40,opacity:0,duration:.85,ease:'power3.out',clearProps:'all',scrollTrigger:{trigger:el,scroller:isDocument?window:scroller,start:'top 94%',once:true}});
  }
  function refresh() {
    clearTimeout(refreshTimer);refreshTimer=setTimeout(()=>{
      hydratePhotos();
      window.ScrollTrigger?.getAll().forEach(t=>{if(t.trigger&&!t.trigger.isConnected)t.kill(true);});
      const hero=$('.av-hero'),collection=$('.av-collection');
      if(hero!==state.hero||(gsap&&motion()&&!state.heroReady))setupHero(hero);if(collection!==state.collection||(gsap&&motion()&&!state.collectionReady))setupCollection(collection);
      $$('.st-key-prediction-panel,.st-key-result-panel,.st-key-about-panel,[data-av-reveal]').forEach(reveal);
      $$('[data-testid="stMetricValue"]>div').forEach(el=>{if(seen.has(el))return;seen.add(el);const m=el.textContent.match(/^([^\d]*)([\d,.]+)(.*)$/);if(m)count(el,Number(m[2].replaceAll(',','')),el.textContent,(m[2].split('.')[1]||'').length);});
      const result=$('.st-key-result-panel h2');
      if(result&&!$('.av-check',result)){
        scrollTo($('.st-key-result-panel'));result.insertAdjacentHTML('afterbegin','<svg class="av-check" viewBox="0 0 28 28" aria-hidden="true"><circle cx="14" cy="14" r="12"/><path d="m8 14 4 4 8-8"/></svg>');
        $$('[data-av-busy]').forEach(b=>{b.removeAttribute('data-av-busy');b.removeAttribute('aria-busy');});
      }
      lenis?.resize();window.ScrollTrigger?.refresh();indicator();onScroll();
    },90);
  }
  document.addEventListener('pointermove',event=>{
    state.pointer={x:event.clientX,y:event.clientY,target:event.target};
    if(!state.pointerQueued){state.pointerQueued=true;requestAnimationFrame(pointerFrame);}
    const cta=event.target.closest('.av-magnetic');if(cta&&gsap&&motion()&&desktop()){const r=cta.getBoundingClientRect();gsap.to(cta,{x:(event.clientX-r.left-r.width/2)*.1,y:(event.clientY-r.top-r.height/2)*.1,duration:.3,overwrite:true});}
  },{passive:true});
  document.addEventListener('pointerout',event=>{
    if(!event.relatedTarget){$('.av-cursor')?.style.setProperty('opacity','0');if(state.insideCar){state.insideCar=false;resetTimer=setTimeout(resetSprites,2000);}clearRows();}
    const cta=event.target.closest('.av-magnetic');if(cta&&!cta.contains(event.relatedTarget)&&gsap)gsap.to(cta,{x:0,y:0,duration:.5,overwrite:true});
  });
  document.addEventListener('focusin',event=>{const row=event.target.closest('.av-collection-row');if(row)setRow(Number(row.dataset.index),false);});
  document.addEventListener('focusout',()=>setTimeout(()=>{if(!state.collection?.contains(document.activeElement))clearRows();},0));
  document.addEventListener('click',event=>{
    if(event.target.closest('.av-menu-button')){menu(!open);return;}
    const row=event.target.closest('.av-collection-row');if(row){
      const expand=row.getAttribute('aria-expanded')!=='true';
      $$('.av-collection-row').forEach(el=>{const active=el===row&&expand;el.setAttribute('aria-expanded',String(active));$('.av-row-extra',el).hidden=!active;});
      if(expand)setRow(Number(row.dataset.index),false);else clearRows();lenis?.resize();window.ScrollTrigger?.refresh();return;
    }
    const a=event.target.closest('a[href^="#"]');if(a){const id=a.hash;const target=id&&document.getElementById(decodeURIComponent(id.slice(1)));if(target){event.preventDefault();menu(false);scrollTo(target);}}
    const submit=event.target.closest('[data-testid="stFormSubmitButton"] button');if(submit){submit.setAttribute('data-av-busy','');submit.setAttribute('aria-busy','true');setTimeout(()=>{submit.removeAttribute('data-av-busy');submit.removeAttribute('aria-busy');},8000);}
  });
  document.addEventListener('keydown',event=>{
    if(!open)return;if(event.key==='Escape'){menu(false);$('.av-menu-button')?.focus();}
    if(event.key==='Tab'){const items=[$('.av-menu-button'),...$$('.av-nav a')].filter(Boolean),first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}
  });
  document.addEventListener('invalid',event=>{event.target.classList.add('av-shake');setTimeout(()=>event.target.classList.remove('av-shake'),350);},true);
  (isDocument?window:scroller).addEventListener('scroll',onScroll,{passive:true});
  new MutationObserver(records=>{if(records.some(r=>!r.target.closest?.('.av-hero-stage,.av-preview,.av-collection')&&[...r.addedNodes].some(n=>n.nodeType===1&&!n.classList.contains('pin-spacer'))))refresh();}).observe($('.stMainBlockContainer')||document.body,{childList:true,subtree:true});
  window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(innerWidth>1000&&open)menu(false);measureChars();indicator();refresh();},150);});
  document.addEventListener('visibilitychange',onScroll);
  reduced.addEventListener('change',()=>{
    lenis?.destroy();lenis=null;if(ticker)gsap?.ticker.remove(ticker);heroContext?.revert();listContext?.revert();
    state.winds.forEach(t=>t.kill());state.winds=[];
    counters.forEach(({value,node,finishText})=>{gsap?.killTweensOf(value);node.data=finishText;});counters.clear();
    state.chars.forEach(c=>c.el.classList.remove('is-morphed'));$('.av-loader')?.remove();clearRows();state.hero=null;state.collection=null;refresh();
  });
  window.__avMotion={refresh,version:VERSION};
  async function start(){
    if(reduced.matches||sessionStorage.getItem('av-loaded'))$('.av-loader')?.remove();
    if(motion()){
      await load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js');gsap=window.gsap;
      if(gsap){
        await Promise.all([load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js'),load('https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js')]);
        if(window.ScrollTrigger)gsap.registerPlugin(window.ScrollTrigger);
        if(window.Lenis){lenis=new window.Lenis({wrapper:isDocument?window:scroller,content:$('.stMainBlockContainer')||document.body,duration:1.05,smoothWheel:true,syncTouch:false});lenis.on('scroll',()=>window.ScrollTrigger?.update());ticker=time=>lenis?.raf(time*1000);gsap.ticker.add(ticker);}
      }
    }
    const loader=$('.av-loader');if(loader){if(gsap&&motion())gsap.to(loader,{opacity:0,y:-12,duration:.35,onComplete:()=>loader.remove()});else loader.remove();}
    sessionStorage.setItem('av-loaded','1');refresh();
  }
  hydratePhotos();
  start().catch(()=>{$('.av-loader')?.remove();refresh();});onScroll();
})();

```

## Ảnh và nguồn

Sáu WebP đã có tại static/cars, không cần tải lại hoặc hotlink. Nguồn/giấy phép ở docs/IMAGE_CREDITS.md; mapping mẫu/năm và hash ở static/cars/catalog.json. Ảnh là tham khảo cùng dòng/thế hệ, không xác nhận chính chiếc xe trong dữ liệu giá.

## Chạy và kiểm tra

1. Lấy toàn bộ mã mới từ main, gồm static/cars và cấu hình Streamlit.
2. Chạy python -m streamlit run app.py, hoặc Reboot app trên Streamlit Cloud.
3. Ctrl+F5, thử hover/tap ảnh đúng tên xe và dự đoán/tải CSV.

Ảnh runtime được app.py nhúng từ static/cars bằng data URI và registry dùng chung, không gọi đường dẫn tĩnh /app/static/.
