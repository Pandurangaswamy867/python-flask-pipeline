from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ============================================================
# BUBU × DUDU — GLOBAL COUPLE UNIVERSE
# Production-style single-file Flask prototype.
#
# For real production: move HTML/CSS/JS into templates/static,
# add PostgreSQL, authentication, object storage, HTTPS, CSRF,
# rate limiting, backups and proper image licensing.
# ============================================================

HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ff6fa8">
<meta name="description" content="Bubu × Dudu — a private-inspired digital universe for memories, dates, moods, questions and little love rituals.">
<meta property="og:title" content="Bubu × Dudu — Our Little Universe">
<meta property="og:description" content="Memories, moods, dates, bucket lists, questions and love notes in one beautiful space.">
<title>Bubu × Dudu — Our Little Universe</title>

<style>
:root{
 --bg:#fffaf7;--surface:#fff;--ink:#251c21;--muted:#75666d;
 --pink:#ff6fa8;--pink2:#ff9ac3;--rose:#ffe0eb;--line:#f2d9e3;
 --purple:#9275ff;--green:#63b99a;--gold:#e8ae4c;
 --shadow:0 20px 70px rgba(62,25,43,.10);
 --radius:26px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--ink);overflow-x:hidden}
button,input,textarea,select{font:inherit}
button{cursor:pointer}
a{text-decoration:none;color:inherit}
.container{width:min(1180px,92%);margin:auto}
.topbar{height:70px;position:sticky;top:0;z-index:900;background:rgba(255,250,247,.82);backdrop-filter:blur(20px);border-bottom:1px solid var(--line);display:flex;align-items:center}
.nav{display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{font-weight:1000;font-size:22px;letter-spacing:-1px}
.brand b{color:var(--pink)}
.navlinks{display:flex;gap:20px;font-size:13px;font-weight:800;color:#5d4c54}
.navlinks a:hover{color:var(--pink)}
.nav-actions{display:flex;gap:8px}
.icon-btn{width:40px;height:40px;border:1px solid var(--line);background:#fff;border-radius:50%;display:grid;place-items:center}
.hero{min-height:calc(100vh - 70px);display:grid;grid-template-columns:1.08fr .92fr;align-items:center;gap:50px;padding:70px 0;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;width:600px;height:600px;background:#ffd8e8;filter:blur(30px);opacity:.55;border-radius:50%;left:-250px;top:-250px}
.hero-copy{position:relative;z-index:2}
.kicker{font-size:11px;letter-spacing:3px;font-weight:1000;color:var(--pink)}
.hero h1{font-size:clamp(54px,8vw,100px);letter-spacing:-6px;line-height:.88;margin:18px 0}
.hero h1 span{color:var(--pink)}
.hero p{font-size:18px;line-height:1.75;color:var(--muted);max-width:650px}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}
.btn{border:0;border-radius:999px;padding:13px 20px;font-weight:900;transition:.2s}
.btn:hover{transform:translateY(-2px)}
.btn-primary{background:linear-gradient(135deg,var(--pink),var(--pink2));color:#fff;box-shadow:0 12px 30px #ff6fa83b}
.btn-soft{background:#fff;border:1px solid var(--line);color:#694758}
.hero-art{height:520px;display:grid;place-items:center;position:relative}
.blob{position:absolute;width:430px;height:430px;background:linear-gradient(135deg,#ffd6e6,#e9ddff);border-radius:45% 55% 60% 40%;animation:morph 8s infinite}
.hero-photo{position:relative;width:min(390px,75vw);height:450px;border-radius:35px;overflow:hidden;box-shadow:0 35px 80px #4b263b2b;transform:rotate(3deg);background:#eee}
.hero-photo img{width:100%;height:100%;object-fit:cover}
.float{position:absolute;font-size:42px;animation:float 3s ease-in-out infinite;z-index:3}
.f-a{top:45px;left:15px}.f-b{right:15px;bottom:75px;animation-delay:.8s}.f-c{right:5px;top:80px;animation-delay:1.5s}
@keyframes float{50%{transform:translateY(-15px) rotate(7deg)}}@keyframes morph{50%{border-radius:60% 40% 45% 55%;transform:rotate(8deg) scale(1.03)}}
.section{padding:100px 0}
.section-head{text-align:center;margin-bottom:35px}
.section-head h2{font-size:clamp(34px,5vw,58px);letter-spacing:-2px;margin:8px 0}
.section-head h2 span{color:var(--pink)}
.section-head p{color:var(--muted);line-height:1.7}
.eyebrow{font-size:10px;letter-spacing:3px;color:var(--pink);font-weight:1000}
.section-soft{background:#fff3f7}
.horizontal{display:flex;overflow-x:auto;gap:18px;scroll-snap-type:x mandatory;scrollbar-width:none;padding:8px 4% 30px}
.horizontal::-webkit-scrollbar{display:none}
.slide{min-width:min(1060px,86vw);scroll-snap-align:center;border-radius:36px;min-height:560px;padding:55px;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:35px;box-shadow:var(--shadow);overflow:hidden}
.slide.love{background:linear-gradient(135deg,#ffd6e6,#fff7f2)}
.slide.fight{background:linear-gradient(135deg,#30232a,#77475b);color:white}
.slide.cry{background:linear-gradient(135deg,#d7e9ff,#f1e7ff)}
.slide.happy{background:linear-gradient(135deg,#ffe99b,#ffd0e1)}
.slide h3{font-size:clamp(42px,5vw,70px);line-height:.94;margin:15px 0}
.slide p{max-width:550px;line-height:1.8;color:inherit;opacity:.78}
.visual-card{height:400px;border-radius:30px;overflow:hidden;position:relative;background:#fff;box-shadow:0 25px 55px #4b263b20}
.visual-card img{width:100%;height:100%;object-fit:cover}
.quote{padding:24px;border:1px solid #ffffff88;background:#ffffff33;backdrop-filter:blur(12px);border-radius:24px;margin-top:22px;font-weight:800}
.fight-ui{height:380px;display:grid;place-items:center;position:relative}
.bubble{position:absolute;background:#fff;color:#573a47;padding:18px 22px;border-radius:20px;box-shadow:0 15px 35px #0003;font-weight:1000}
.b1{top:25px;left:0;transform:rotate(-6deg)}.b2{right:0;bottom:35px;transform:rotate(6deg)}
.vs{font-size:60px;color:#ff9cbc;font-weight:1000}
.big-emoji{font-size:110px;text-align:center;animation:float 3s infinite}
.progress{height:13px;background:#ffffffaa;border-radius:99px;overflow:hidden;margin:20px 0}
.progress span{display:block;height:100%;width:88%;background:linear-gradient(90deg,#9ac1ff,#c29aff,#ff8db7);border-radius:99px}
.orbit{width:350px;height:350px;border:2px dashed #6e4a5a44;border-radius:50%;position:relative;margin:auto;animation:spin 18s linear infinite}
.orbit span{position:absolute;width:65px;height:65px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:30px;box-shadow:0 10px 25px #4b263b1c}
.orbit .a{top:-10px;left:142px}.orbit .b{right:-10px;top:142px}.orbit .c{bottom:-10px;left:142px}.orbit .d{left:-10px;top:142px}
@keyframes spin{to{transform:rotate(360deg)}}
.section-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:25px;box-shadow:0 10px 30px #4b263b0a}
.card:hover{box-shadow:0 20px 45px #4b263b12;transform:translateY(-3px)}
.card{transition:.2s}
.card h3{margin:10px 0;font-size:21px}.card p{color:var(--muted);line-height:1.65;font-size:14px}
.card-icon{font-size:38px}
.input{width:100%;padding:13px 14px;border:1px solid var(--line);border-radius:13px;background:#fff;outline:none;margin:7px 0}
.output{margin-top:12px;background:#fff6f9;border-radius:15px;padding:15px;min-height:50px;line-height:1.6}
.memory{display:flex;align-items:center;gap:8px;background:#fff7fa;padding:10px 12px;border-radius:13px;margin-top:7px}
.memory span{flex:1}.memory small{display:block;color:#999;font-size:10px}.danger{border:0;background:none;color:var(--pink);font-size:19px}
.game-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}
.game{background:#fff;border:1px solid var(--line);border-radius:22px;padding:24px;text-align:center;cursor:pointer;font-size:28px}
.game strong{display:block;font-size:15px;margin-top:8px}.game small{color:#888}
.big-result{text-align:center;background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;margin-top:18px;font-size:19px}
.gallery{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x proximity;scrollbar-width:none;padding:8px 4% 30px}
.gallery::-webkit-scrollbar{display:none}
.gallery-card{min-width:280px;height:400px;border:0;border-radius:28px;overflow:hidden;position:relative;background:#eee;cursor:pointer;scroll-snap-align:start;padding:0}
.gallery-card img{width:100%;height:100%;object-fit:cover;transition:.5s}.gallery-card:hover img{transform:scale(1.06)}
.gallery-card span{position:absolute;left:13px;right:13px;bottom:13px;background:#ffffffe8;padding:12px;border-radius:13px;font-weight:900;text-align:left}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}
.stat{background:#fff;border:1px solid var(--line);border-radius:24px;padding:25px;text-align:center}
.stat b{display:block;font-size:36px;color:var(--pink)}.stat small{color:#7b6870}
.countdown{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:20px}
.timebox{min-width:95px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:15px;text-align:center}.timebox b{display:block;font-size:30px;color:var(--pink)}.timebox small{color:#777}
.playlist{display:flex;gap:10px}.playlist .input{margin:0}.song{display:flex;justify-content:space-between;padding:13px 15px;border:1px solid var(--line);border-radius:12px;margin-top:8px;background:#fff}
.modal{display:none;position:fixed;inset:0;background:#160e14c9;z-index:5000;align-items:center;justify-content:center;padding:20px}
.modal-box{max-width:650px;width:100%;background:#fff8fb;border-radius:30px;padding:42px;position:relative;box-shadow:0 35px 100px #0005}.close{position:absolute;right:18px;top:15px;border:0;background:#0001;width:40px;height:40px;border-radius:50%;font-size:25px}
.modal-box h3{font-size:38px;margin:10px 0}.modal-box p{line-height:1.8;color:#67545d}
.lightbox img{max-width:90vw;max-height:80vh;border-radius:25px}
.toast{position:fixed;right:20px;bottom:20px;background:#251c21;color:white;padding:14px 18px;border-radius:999px;z-index:7000;transform:translateY(100px);opacity:0;transition:.3s}.toast.show{transform:none;opacity:1}
.hearts{position:fixed;inset:0;pointer-events:none;z-index:8000}.heart{position:absolute;bottom:-40px;animation:rise 2s ease-out forwards;font-size:25px}@keyframes rise{to{transform:translateY(-110vh) rotate(30deg);opacity:0}}
footer{padding:50px 0;background:#251c21;color:#fff;text-align:center}footer p{opacity:.7;margin-top:8px;font-size:13px}
.mobile-menu{display:none}
@media(max-width:900px){
 .hero{grid-template-columns:1fr;padding:55px 0}.hero-art{height:400px}
 .slide{grid-template-columns:1fr;min-height:700px;padding:35px}.visual-card{height:300px}.fight-ui{height:260px}
 .section-grid{grid-template-columns:1fr 1fr}.game-grid{grid-template-columns:1fr 1fr}.stats{grid-template-columns:1fr 1fr}
 .navlinks{display:none}.mobile-menu{display:grid}
}
@media(max-width:600px){
 .hero h1{letter-spacing:-3px}.hero-photo{height:360px}.blob{width:310px;height:310px}
 .section-grid,.game-grid,.stats{grid-template-columns:1fr}
 .slide{min-width:92vw}.orbit{width:250px;height:250px}.orbit .a,.orbit .c{left:92px}.orbit .b,.orbit .d{top:92px}
 .chapter-controls{display:none}
}
body.dark{--bg:#151015;--surface:#211a20;--ink:#fff4f8;--muted:#b9aab2;--line:#3b2933}
body.dark .topbar,body.dark .pro-white{background:#181218}body.dark .card,body.dark .gallery-card,body.dark .game,body.dark .stat,body.dark .song,body.dark .timebox,body.dark .input{background:#211a20;color:#fff}
body.dark .navlinks{color:#ddd}body.dark .output{background:#2a1d25}
</style>
</head>

<body>

<header class="topbar">
<div class="container nav">
<a class="brand" href="#">🐼 Bubu <b>×</b> Dudu</a>

<nav class="navlinks">
<a href="#story">Story</a>
<a href="#memories">Memories</a>
<a href="#daily">Daily</a>
<a href="#dates">Dates</a>
<a href="#bucket">Bucket List</a>
<a href="#games">Games</a>
</nav>

<div class="nav-actions">
<button class="icon-btn" onclick="toggleTheme()" title="Theme">🌙</button>
<button class="icon-btn mobile-menu" onclick="scrollToId('story')">☰</button>
</div>
</div>
</header>

<main>

<section class="hero">
<div class="container" style="display:contents">
<div class="hero-copy">
<span class="kicker">BUBU × DUDU • YOUR PRIVATE LITTLE UNIVERSE</span>
<h1>Love is made of <span>little things.</span></h1>
<p>
A beautiful space for two people to keep their memories, answer questions,
plan dates, build dreams, share moods and collect the tiny moments that
eventually become a whole story.
</p>

<div class="actions">
<button class="btn btn-primary" onclick="scrollToId('story')">Explore Our Story →</button>
<button class="btn btn-soft" onclick="surprise()">✨ Surprise Me</button>
</div>

<div style="margin-top:25px;color:#907782;font-size:13px">
🔒 Designed around private couple experiences • 🌎 Global-friendly • 📱 Mobile-first
</div>
</div>

<div class="hero-art">
<div class="blob"></div>
<div class="hero-photo">
<img src="https://i.pinimg.com/736x/b2/b7/66/b2b7666fb81587373c74c4fc6fa7181e.jpg"
alt="Bubu Dudu couple illustration">
</div>
<div class="float f-a">❤️</div>
<div class="float f-b">🌸</div>
<div class="float f-c">✨</div>
</div>
</div>
</section>

<!-- STORY -->
<section id="story" class="chapter-app section-soft">
<div class="container section-head">
<span class="eyebrow">SWIPE • SCROLL • DISCOVER</span>
<h2>Our story, <span>one chapter at a time.</span></h2>
<p>Use your finger on mobile, mouse wheel on desktop, or the buttons to move between chapters.</p>
</div>

<div class="horizontal" id="storyRail">

<article class="slide love">
<div>
<span class="eyebrow">01 • THE BEGINNING</span>
<h3>Two little weirdos.<br>One big story.</h3>
<p>
Every relationship starts somewhere: one conversation, one joke,
one unexpected connection. This chapter is yours to customize.
</p>
<div class="quote">“The best stories are the ones we didn't plan.” ❤️</div>
<button class="btn btn-primary" style="margin-top:20px" onclick="openStory('begin')">Read chapter</button>
</div>
<div class="visual-card">
<img src="https://i.pinimg.com/736x/b2/b7/66/b2b7666fb81587373c74c4fc6fa7181e.jpg"
alt="Bubu Dudu">
</div>
</article>

<article class="slide fight">
<div>
<span class="eyebrow">02 • THE CHAOS</span>
<h3>“I'm fine.”<br>We both know you're not. 😤</h3>
<p>
Arguments happen. What matters is how the story continues after the
argument. Fight, cool down, talk, laugh and come back stronger.
</p>
<button class="btn btn-soft" onclick="openStory('fight')" style="margin-top:20px">Replay the chaos</button>
</div>
<div class="fight-ui">
<div class="bubble b1">I'M FINE 😤</div>
<div class="vs">VS</div>
<div class="bubble b2">NO YOU'RE NOT 😭</div>
</div>
</article>

<article class="slide cry">
<div>
<span class="eyebrow">03 • THE SOFT SIDE</span>
<h3>Sometimes we cry.<br>Then we hug harder.</h3>
<p>
Not every difficult moment needs a solution. Sometimes staying,
listening and giving someone space is the most loving thing.
</p>
<div class="progress"><span></span></div>
<small>Hug comfort level: 88%</small>
</div>
<div class="big-emoji">🥺🫂</div>
</article>

<article class="slide happy">
<div>
<span class="eyebrow">04 • THE HAPPY PART</span>
<h3>Small moments.<br>Huge memories. ✨</h3>
<p>
Food. Calls. Reels. Random walks. Inside jokes. These ordinary
things become the memories you don't want to lose.
</p>
<button class="btn btn-primary" onclick="burstHearts()">Create happiness storm ✨</button>
</div>
<div class="orbit">
<span class="a">🍦</span><span class="b">🎬</span><span class="c">📱</span><span class="d">🫂</span>
<div style="position:absolute;inset:0;display:grid;place-items:center;font-size:85px">❤️</div>
</div>
</article>

</div>
</section>

<!-- DAILY QUESTION -->
<section id="daily" class="section">
<div class="container section-head">
<span class="eyebrow">DAILY CONNECTION</span>
<h2>One question. <span>Two honest answers.</span></h2>
<p>A lightweight daily ritual inspired by the best-performing couple-app pattern: answer first, reveal after.</p>
</div>

<div class="card" style="max-width:800px;margin:auto;text-align:center">
<div class="card-icon">💭</div>
<h3 id="questionText">What tiny thing made you smile today?</h3>
<p id="questionCategory">Daily connection</p>

<input class="input" id="answerInput" placeholder="Write your answer privately...">

<div class="actions" style="justify-content:center">
<button class="btn btn-primary" onclick="saveAnswer()">Lock My Answer 🔒</button>
<button class="btn btn-soft" onclick="newQuestion()">New Question</button>
</div>

<div class="output" id="answerOutput">Your answer stays in this browser until you choose to replace it.</div>
</div>
</section>

<!-- MEMORIES -->
<section id="memories" class="section section-soft">
<div class="container section-head">
<span class="eyebrow">YOUR SHARED TIMELINE</span>
<h2>Turn moments into <span>memories.</span></h2>
<p>A timeline should contain the context around a photo, not just the photo itself.</p>
</div>

<div class="section-grid container">
<div class="card">
<div class="card-icon">📸</div>
<h3>Add a memory</h3>
<input class="input" id="memoryTitle" placeholder="Memory title">
<input class="input" id="memoryDate" type="date">
<textarea class="input" id="memoryNote" rows="3" placeholder="What happened? Why was it special?"></textarea>
<button class="btn btn-primary" onclick="addMemory()">Save memory ❤️</button>
</div>

<div class="card" style="grid-column:span 2">
<h3>Memory Timeline</h3>
<div id="memoryList"></div>
</div>
</div>
</section>

<!-- COUNTDOWN -->
<section class="section">
<div class="container section-head">
<span class="eyebrow">MILESTONES</span>
<h2>Count down to your <span>next moment.</span></h2>
</div>

<div class="card" style="max-width:800px;margin:auto;text-align:center">
<h3>Choose your next special date</h3>
<input class="input" id="targetDate" type="datetime-local" onchange="saveTargetDate()">
<div class="countdown">
<div class="timebox"><b id="days">0</b><small>Days</small></div>
<div class="timebox"><b id="hours">0</b><small>Hours</small></div>
<div class="timebox"><b id="mins">0</b><small>Minutes</small></div>
<div class="timebox"><b id="secs">0</b><small>Seconds</small></div>
</div>
</div>
</section>

<!-- DATE IDEAS -->
<section id="dates" class="section section-soft">
<div class="container section-head">
<span class="eyebrow">DATE DISCOVERY</span>
<h2>Stop asking <span>“what should we do?”</span></h2>
<p>Generate ideas based on mood, budget and energy.</p>
</div>

<div class="section-grid container">
<div class="card">
<div class="card-icon">🎯</div>
<h3>Date generator</h3>

<select class="input" id="dateMood">
<option value="any">Any mood</option>
<option value="cozy">Cozy</option>
<option value="adventure">Adventure</option>
<option value="food">Food</option>
<option value="cheap">Low budget</option>
<option value="longdistance">Long distance</option>
</select>

<button class="btn btn-primary" onclick="generateDate()">Find our date →</button>
<div class="output" id="dateOutput">Your next plan will appear here.</div>
</div>

<div class="card">
<div class="card-icon">🗺️</div>
<h3>Love Map</h3>
<p>Keep the places that matter to your story. This prototype stores them locally; production can connect them to a real map provider.</p>
<input class="input" id="placeInput" placeholder="e.g. Our first café">
<button class="btn btn-primary" onclick="addPlace()">Pin place 📍</button>
<div class="output" id="placeList"></div>
</div>

<div class="card">
<div class="card-icon">🎵</div>
<h3>Our playlist</h3>
<input class="input" id="songInput" placeholder="Song — Artist">
<button class="btn btn-primary" onclick="addSong()">Add to our soundtrack 🎶</button>
<div id="songList"></div>
</div>
</div>
</section>

<!-- BUCKET LIST -->
<section id="bucket" class="section">
<div class="container section-head">
<span class="eyebrow">DREAMS → PLANS → MEMORIES</span>
<h2>Our <span>couple bucket list.</span></h2>
<p>Add dreams, mark them completed and watch your relationship archive grow.</p>
</div>

<div class="section-grid container">
<div class="card">
<div class="card-icon">🌍</div>
<h3>Add a dream</h3>
<input class="input" id="wishInput" placeholder="See the Northern Lights">
<select class="input" id="wishCategory">
<option>Travel</option><option>Food</option><option>Adventure</option><option>Home</option><option>Funny</option><option>Romantic</option>
</select>
<button class="btn btn-primary" onclick="addWish()">Add to bucket list</button>
</div>

<div class="card" style="grid-column:span 2">
<h3>Things we want to do</h3>
<div id="wishList"></div>
</div>
</div>
</section>

<!-- OPEN WHEN -->
<section class="section section-soft">
<div class="container section-head">
<span class="eyebrow">FOR THE HARD DAYS</span>
<h2>Open when <span>you need me.</span></h2>
</div>

<div class="section-grid container">
<div class="card" onclick="openLetter('sad')"><div class="card-icon">🥺</div><h3>Open when you're sad</h3><p>A little reminder that you're not alone.</p></div>
<div class="card" onclick="openLetter('miss')"><div class="card-icon">🌙</div><h3>Open when you miss me</h3><p>For those long-distance moments.</p></div>
<div class="card" onclick="openLetter('fight')"><div class="card-icon">😤</div><h3>Open after a fight</h3><p>Because being right isn't more important than being us.</p></div>
<div class="card" onclick="openLetter('happy')"><div class="card-icon">🥰</div><h3>Open when you're happy</h3><p>Save the happiness and celebrate it twice.</p></div>
</div>
</section>

<!-- GAMES -->
<section id="games" class="section">
<div class="container section-head">
<span class="eyebrow">PLAY TOGETHER</span>
<h2>Little games for <span>two.</span></h2>
</div>

<div class="game-grid container">
<button class="game" onclick="catchHearts()">💗<strong>Catch Hearts</strong><small>Random surprise</small></button>
<button class="game" onclick="compliment()">🥰<strong>Compliment</strong><small>Make them smile</small></button>
<button class="game" onclick="fightResolver()">⚖️<strong>Fight Resolver</strong><small>Who says sorry?</small></button>
<button class="game" onclick="fortune()">🔮<strong>Love Fortune</strong><small>Ask the universe</small></button>
</div>

<div class="big-result container" id="gameResult">Choose a game 👆</div>
</section>

<!-- GALLERY -->
<section class="section section-soft">
<div class="container section-head">
<span class="eyebrow">VISUAL UNIVERSE</span>
<h2>Bubu × Dudu <span>Gallery.</span></h2>
<p>Swipe horizontally. Tap an image to open it.</p>
</div>

<div class="gallery">
<button class="gallery-card" onclick="openImage(this)">
<img src="https://i.pinimg.com/736x/b2/b7/66/b2b7666fb81587373c74c4fc6fa7181e.jpg" alt="Bubu Dudu">
<span>🌸 Together</span>
</button>

<button class="gallery-card" onclick="openImage(this)">
<img src="https://static.wixstatic.com/media/5d1e18_a6c2587b37e145f2981f1beb15e01c67~mv2.avif/v1/fill/w_640,h_640,al_c,q_85,enc_avif,quality_auto/5d1e18_a6c2587b37e145f2981f1beb15e01c67~mv2.avif" alt="Bubu Dudu">
<span>🧸 Cozy days</span>
</button>

<button class="gallery-card" onclick="openImage(this)">
<img src="https://i.pinimg.com/736x/b2/b7/66/b2b7666fb81587373c74c4fc6fa7181e.jpg" alt="Bubu Dudu">
<span>💕 Our vibe</span>
</button>
</div>
</section>

<!-- STATS -->
<section class="section">
<div class="container section-head">
<span class="eyebrow">OUR UNIVERSE</span>
<h2>Built from <span>little moments.</span></h2>
</div>

<div class="stats container">
<div class="stat"><b id="memoryCount">0</b><small>Memories</small></div>
<div class="stat"><b id="wishCount">0</b><small>Dreams</small></div>
<div class="stat"><b id="songCount">0</b><small>Songs</small></div>
<div class="stat"><b id="dayCount">0</b><small>Days together</small></div>
</div>
</section>

</main>

<footer>
<div class="container">
<div style="font-size:25px;font-weight:1000">🐼 Bubu <span style="color:#ff6fa8">×</span> Dudu</div>
<p>A little digital universe for two.</p>
<p>© 2026 Bubu × Dudu • Fan-style interactive experience</p>
<p style="font-size:11px;margin-top:12px">
Images shown from publicly accessible web sources for prototype/demo use.
For public commercial deployment, replace them with assets you have permission to use.
</p>
</div>
</footer>

<div class="modal" id="storyModal">
<div class="modal-box">
<button class="close" onclick="closeModal('storyModal')">×</button>
<span class="eyebrow">YOUR STORY</span>
<h3 id="storyTitle"></h3>
<p id="storyBody"></p>
<button class="btn btn-primary" style="margin-top:20px" onclick="closeModal('storyModal')">Keep this memory ❤️</button>
</div>
</div>

<div class="modal" id="letterModal">
<div class="modal-box">
<button class="close" onclick="closeModal('letterModal')">×</button>
<span class="eyebrow">OPEN WHEN</span>
<h3 id="letterTitle"></h3>
<p id="letterBody"></p>
</div>
</div>

<div class="modal" id="imageModal" onclick="if(event.target.id==='imageModal')closeModal('imageModal')">
<div class="modal-box lightbox">
<button class="close" onclick="closeModal('imageModal')">×</button>
<img id="lightboxImage" src="" alt="">
</div>
</div>

<div class="toast" id="toast"></div>
<div class="hearts" id="hearts"></div>

<script>
/* ==========================================================
   BUBU × DUDU FRONTEND ENGINE
   ========================================================== */

const $ = id => document.getElementById(id);

function scrollToId(id){
    const el=$(id);
    if(el) el.scrollIntoView({behavior:"smooth"});
}

function showToast(message){
    const t=$("toast");
    t.textContent=message;
    t.classList.add("show");
    setTimeout(()=>t.classList.remove("show"),2500);
}

function burstHearts(){
    const box=$("hearts");
    for(let i=0;i<25;i++){
        const h=document.createElement("span");
        h.className="heart";
        h.textContent=["❤️","💕","💗","💖","✨"][Math.floor(Math.random()*5)];
        h.style.left=Math.random()*100+"%";
        h.style.animationDelay=Math.random()*.7+"s";
        box.appendChild(h);
        setTimeout(()=>h.remove(),2300);
    }
}

function surprise(){
    const choices=[
        "Send your person a random “I love you.” ❤️",
        "Plan a surprise food date. 🍕",
        "Call them instead of texting. 📞",
        "Send an old favorite photo. 📸",
        "Ask: “What do you need from me today?” 🫂",
        "Make a new bucket-list dream together. 🌍"
    ];

    showToast(choices[Math.floor(Math.random()*choices.length)]);
    burstHearts();
}

/* ================= STORY ================= */

const stories={
begin:{
 title:"The beginning",
 body:"Every relationship starts somewhere. Maybe it was a message, a joke, a random conversation or one moment that neither person realized would become important. This chapter is where you write what actually happened."
},
fight:{
 title:"The chaos chapter",
 body:"Someone got annoyed. Someone said “I'm fine.” Someone definitely was not fine. Then came silence, food, a random meme and eventually the conversation that mattered. The goal isn't never fighting. The goal is learning how to return to each other."
}
};

function openStory(key){
    $("storyTitle").textContent=stories[key].title;
    $("storyBody").textContent=stories[key].body;
    $("storyModal").style.display="flex";
}

/* ================= DAILY QUESTIONS ================= */

const questions=[
["What tiny thing made you smile today?","Daily"],
["What is one thing you appreciate about me?","Connection"],
["What place should we visit together?","Future"],
["What is one memory you would relive?","Memories"],
["What food should we try together?","Fun"],
["What do you need more of from me lately?","Honesty"],
["What silly thing about me secretly makes you happy?","Playful"]
];

let currentQuestion=0;

function newQuestion(){
    currentQuestion=Math.floor(Math.random()*questions.length);
    $("questionText").textContent=questions[currentQuestion][0];
    $("questionCategory").textContent=questions[currentQuestion][1];
    $("answerInput").value="";
    $("answerOutput").textContent="Write your answer before revealing anything.";
}

function saveAnswer(){
    const value=$("answerInput").value.trim();
    if(!value){
        showToast("Write something first ❤️");
        return;
    }

    localStorage.setItem("bubu_daily_answer",value);
    $("answerOutput").innerHTML="🔒 <b>Answer locked.</b><br>Your answer is saved locally in this browser.";
    showToast("Your answer is locked ❤️");
}

/* ================= MEMORIES ================= */

function getMemories(){
    return JSON.parse(localStorage.getItem("bubu_memories")||"[]");
}

function addMemory(){
    const title=$("memoryTitle").value.trim();
    const date=$("memoryDate").value;
    const note=$("memoryNote").value.trim();

    if(!title){
        showToast("Give this memory a title.");
        return;
    }

    const memories=getMemories();

    memories.unshift({
        title,
        date:date || new Date().toISOString().slice(0,10),
        note
    });

    localStorage.setItem("bubu_memories",JSON.stringify(memories));

    $("memoryTitle").value="";
    $("memoryDate").value="";
    $("memoryNote").value="";

    renderMemories();
    burstHearts();
}

function deleteMemory(index){
    const memories=getMemories();
    memories.splice(index,1);
    localStorage.setItem("bubu_memories",JSON.stringify(memories));
    renderMemories();
}

function renderMemories(){
    const memories=getMemories();

    $("memoryList").innerHTML=memories.length
    ? memories.map((m,i)=>`
        <div class="memory">
            <span>📌 <b>${escapeHTML(m.title)}</b>
            <small>${escapeHTML(m.date)} • ${escapeHTML(m.note||"A beautiful moment.")}</small>
            </span>
            <button class="danger" onclick="deleteMemory(${i})">×</button>
        </div>
    `).join("")
    : "<p style='color:#999;margin-top:12px'>No memories yet. Add your first one ❤️</p>";

    $("memoryCount").textContent=memories.length;
}

/* ================= COUNTDOWN ================= */

function saveTargetDate(){
    localStorage.setItem("bubu_target",$("targetDate").value);
}

function updateCountdown(){
    const target=localStorage.getItem("bubu_target");

    if(!target){
        return;
    }

    $("targetDate").value=target;

    const diff=new Date(target).getTime()-Date.now();

    if(diff<=0){
        $("days").textContent="0";
        $("hours").textContent="0";
        $("mins").textContent="0";
        $("secs").textContent="0";
        return;
    }

    $("days").textContent=Math.floor(diff/86400000);
    $("hours").textContent=Math.floor(diff/3600000)%24;
    $("mins").textContent=Math.floor(diff/60000)%60;
    $("secs").textContent=Math.floor(diff/1000)%60;
}

/* ================= DATES ================= */

const dateIdeas={
any:[
"Sunset walk + favorite food 🌅",
"Movie night with phones away 🎬",
"Try a completely new café ☕",
"Cook something neither of you knows 🍳",
"Take a random train/bus ride and explore 🚆",
"Make a shared playlist and listen together 🎵"
],
cozy:[
"Blanket + movie + snacks 🍿",
"Cook dinner together 🍳",
"Long call with no distractions 📞",
"Make a silly photo album 📸"
],
adventure:[
"Explore a place neither of you knows 🗺️",
"Try a new activity together 🎯",
"Sunrise/sunset adventure 🌅",
"Plan a spontaneous day trip 🚗"
],
food:[
"Try each other's favorite food 🍜",
"Rate five desserts brutally 😂",
"Cook a three-course meal together 🍝",
"Find the best street food nearby 🌮"
],
cheap:[
"Park walk + homemade snacks 🌳",
"Free museum/gallery day 🖼️",
"Cook using only what is already at home 🍳",
"Watch the sunset with chai ☕"
],
longdistance:[
"Virtual dinner date 🍕📱",
"Watch the same movie together 🎬",
"Play an online game 🎮",
"Open an old memory and talk about it 📸"
]
};

function generateDate(){
    const mood=$("dateMood").value;
    const list=dateIdeas[mood]||dateIdeas.any;
    $("dateOutput").innerHTML="💡 <b>"+list[Math.floor(Math.random()*list.length)]+"</b>";
}

/* ================= LOVE MAP ================= */

function addPlace(){
    const place=$("placeInput").value.trim();

    if(!place){
        showToast("Enter a place.");
        return;
    }

    const places=JSON.parse(localStorage.getItem("bubu_places")||"[]");
    places.push(place);

    localStorage.setItem("bubu_places",JSON.stringify(places));
    $("placeInput").value="";
    renderPlaces();
}

function renderPlaces(){
    const places=JSON.parse(localStorage.getItem("bubu_places")||"[]");

    $("placeList").innerHTML=places.length
    ? places.map((p,i)=>`📍 ${escapeHTML(p)}
        <button class="danger" onclick="deletePlace(${i})">×</button><br>`
      ).join("")
    : "No places yet.";
}

function deletePlace(i){
    const places=JSON.parse(localStorage.getItem("bubu_places")||"[]");
    places.splice(i,1);
    localStorage.setItem("bubu_places",JSON.stringify(places));
    renderPlaces();
}

/* ================= PLAYLIST ================= */

function addSong(){
    const value=$("songInput").value.trim();

    if(!value)return;

    const songs=JSON.parse(localStorage.getItem("bubu_songs")||"[]");
    songs.push(value);

    localStorage.setItem("bubu_songs",JSON.stringify(songs));

    $("songInput").value="";
    renderSongs();
}

function renderSongs(){
    const songs=JSON.parse(localStorage.getItem("bubu_songs")||"[]");

    $("songList").innerHTML=songs.length
    ? songs.map((s,i)=>`
        <div class="song">
        🎵 ${escapeHTML(s)}
        <button class="danger" onclick="deleteSong(${i})">×</button>
        </div>
    `).join("")
    : "<p style='color:#999;margin-top:10px'>Your soundtrack is empty.</p>";

    $("songCount").textContent=songs.length;
}

function deleteSong(i){
    const songs=JSON.parse(localStorage.getItem("bubu_songs")||"[]");
    songs.splice(i,1);
    localStorage.setItem("bubu_songs",JSON.stringify(songs));
    renderSongs();
}

/* ================= BUCKET LIST ================= */

function addWish(){
    const text=$("wishInput").value.trim();
    const category=$("wishCategory").value;

    if(!text){
        showToast("Add a dream first.");
        return;
    }

    const wishes=JSON.parse(localStorage.getItem("bubu_wishes")||"[]");

    wishes.push({
        text,
        category,
        done:false
    });

    localStorage.setItem("bubu_wishes",JSON.stringify(wishes));

    $("wishInput").value="";
    renderWishes();
}

function toggleWish(i){
    const wishes=JSON.parse(localStorage.getItem("bubu_wishes")||"[]");
    wishes[i].done=!wishes[i].done;

    localStorage.setItem("bubu_wishes",JSON.stringify(wishes));

    if(wishes[i].done)burstHearts();

    renderWishes();
}

function deleteWish(i){
    const wishes=JSON.parse(localStorage.getItem("bubu_wishes")||"[]");
    wishes.splice(i,1);
    localStorage.setItem("bubu_wishes",JSON.stringify(wishes));
    renderWishes();
}

function renderWishes(){
    const wishes=JSON.parse(localStorage.getItem("bubu_wishes")||"[]");

    $("wishList").innerHTML=wishes.length
    ? wishes.map((w,i)=>`
        <div class="memory">
            <span>
            ${w.done?"✅":"⬜"} <b style="${w.done?'text-decoration:line-through;color:#999':''}">
            ${escapeHTML(w.text)}</b>
            <small>${escapeHTML(w.category)}</small>
            </span>
            <button class="btn btn-soft" onclick="toggleWish(${i})">${w.done?"Undo":"Done"}</button>
            <button class="danger" onclick="deleteWish(${i})">×</button>
        </div>
    `).join("")
    : "<p style='color:#999'>No dreams yet. Add something you want to experience together.</p>";

    $("wishCount").textContent=wishes.length;
}

/* ================= OPEN WHEN ================= */

const letters={
sad:[
"You don't have to be okay every second. Take a breath. Eat something. Rest. And remember: one difficult day doesn't define your whole story. 🫂"
],
miss:[
"If you miss me, imagine me sitting beside you, stealing your snacks and annoying you until you smile. ❤️"
],
fight:[
"We can disagree without becoming enemies. Let's solve the problem, not attack each other. I choose us over winning. 🫂"
],
happy:[
"Keep this moment. Take a photo. Laugh loudly. Tell your person. Happiness becomes even better when it is shared. 🥰"
]
};

function openLetter(type){
    $("letterTitle").textContent=
        type==="sad"?"Open when you're sad":
        type==="miss"?"Open when you miss me":
        type==="fight"?"Open after a fight":
        "Open when you're happy";

    $("letterBody").textContent=
        letters[type][Math.floor(Math.random()*letters[type].length)];

    $("letterModal").style.display="flex";
}

/* ================= MINI GAMES ================= */

function catchHearts(){
    const n=Math.floor(Math.random()*91)+10;
    $("gameResult").innerHTML=`You caught <b>${n} hearts</b>! 💗`;
    burstHearts();
}

function compliment(){
    const list=[
        "Your smile is someone's favorite notification. 📱❤️",
        "You make ordinary moments feel special. 🥹",
        "You deserve an unreasonable amount of hugs today. 🫂",
        "You're the plot twist someone didn't know they needed. 💕"
    ];

    $("gameResult").textContent=list[Math.floor(Math.random()*list.length)];
}

function fightResolver(){
    const winner=Math.random()<.5?"Bubu":"Dudu";
    $("gameResult").innerHTML=`Today's official ruling: <b>${winner}</b> says sorry first. ⚖️😂`;
}

function fortune(){
    const list=[
        "A surprise hug is coming. 🔮",
        "Food will solve your next disagreement. 🔮🍕",
        "Someone is secretly missing the other person right now. 🥺",
        "Your next memory will be completely unplanned. ✨"
    ];

    $("gameResult").textContent=list[Math.floor(Math.random()*list.length)];
}

/* ================= IMAGE LIGHTBOX ================= */

function openImage(card){
    const img=card.querySelector("img");

    $("lightboxImage").src=img.src;
    $("imageModal").style.display="flex";
}

/* ================= THEME ================= */

function toggleTheme(){
    document.body.classList.toggle("dark");

    localStorage.setItem(
        "bubu_theme",
        document.body.classList.contains("dark")?"dark":"light"
    );
}

/* ================= UTILITY ================= */

function escapeHTML(value){
    return String(value).replace(/[&<>"']/g,c=>({
        "&":"&amp;",
        "<":"&lt;",
        ">":"&gt;",
        '"':"&quot;",
        "'":"&#039;"
    }[c]));
}

function closeModal(id){
    $(id).style.display="none";
}

/* ================= INITIALIZATION ================= */

function restore(){
    if(localStorage.getItem("bubu_theme")==="dark"){
        document.body.classList.add("dark");
    }

    if(localStorage.getItem("bubu_daily_answer")){
        $("answerOutput").innerHTML="🔒 <b>Previous answer saved locally.</b>";
    }

    renderMemories();
    renderPlaces();
    renderSongs();
    renderWishes();
    updateCountdown();
}

setInterval(updateCountdown,1000);

restore();

/* ESC CLOSE */
document.addEventListener("keydown",e=>{
    if(e.key==="Escape"){
        ["storyModal","letterModal","imageModal"].forEach(closeModal);
    }
});

/* horizontal wheel navigation */
document.querySelectorAll(".horizontal").forEach(rail=>{
    rail.addEventListener("wheel",e=>{
        if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){
            e.preventDefault();
            rail.scrollLeft+=e.deltaY;
        }
    },{passive:false});
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return jsonify({
        "status":"healthy",
        "application":"Bubu Dudu Couple Universe",
        "timestamp":datetime.utcnow().isoformat()+"Z"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
