from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bubu ❤️ Dudu | Our Little World</title>
<style>
:root{
  --pink:#ff6f91; --pink2:#ff93ac; --cream:#fff8f1; --brown:#6b4f45;
  --soft:#ffe8ef; --yellow:#ffd86b; --purple:#b48cff; --blue:#8ed5ff;
  --card:#ffffff; --text:#513d37; --shadow:0 14px 35px rgba(107,79,69,.14);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,ui-rounded,"Segoe UI",Arial,sans-serif;background:linear-gradient(180deg,#fff9f4 0%,#fff3f7 50%,#fff9f4 100%);color:var(--text);overflow-x:hidden}
body.dark{--card:#2d2530;--text:#fff5f8;--cream:#211c22;--soft:#3d2d36;background:#211c22}
header{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,.9);backdrop-filter:blur(13px);display:flex;align-items:center;justify-content:space-between;padding:14px 5%;border-bottom:1px solid #ffe1e9}
body.dark header{background:rgba(33,28,34,.9);border-color:#493641}
.logo{font-weight:900;font-size:24px;color:var(--pink)}
nav{display:flex;gap:17px;flex-wrap:wrap;align-items:center}
nav a{color:var(--text);text-decoration:none;font-weight:700;font-size:14px}
nav a:hover{color:var(--pink)}
.icon-btn{border:0;border-radius:50%;width:40px;height:40px;background:var(--soft);font-size:20px;cursor:pointer}
.hero{min-height:88vh;display:grid;grid-template-columns:1.08fr .92fr;align-items:center;gap:35px;padding:60px 7%;position:relative;overflow:hidden}
.hero:before,.hero:after{content:"";position:absolute;border-radius:50%;filter:blur(2px);z-index:-1}
.hero:before{width:380px;height:380px;background:#ffe2eb;top:-100px;right:-60px}
.hero:after{width:290px;height:290px;background:#fff0b9;left:-100px;bottom:-80px}
.badge{display:inline-block;padding:8px 14px;background:var(--soft);color:var(--pink);border-radius:999px;font-weight:800;margin-bottom:18px}
.hero h1{font-size:clamp(44px,7vw,82px);line-height:.98;color:var(--brown)}
body.dark .hero h1{color:#fff3f7}
.hero h1 span{color:var(--pink)}
.hero p{font-size:19px;line-height:1.8;margin:24px 0;max-width:680px}
.btn{border:0;border-radius:999px;padding:13px 21px;font-weight:800;cursor:pointer;background:var(--pink);color:white;box-shadow:0 8px 20px rgba(255,111,145,.25);transition:.2s;margin:5px}
.btn:hover{transform:translateY(-2px) scale(1.02)}
.btn.alt{background:white;color:var(--pink);border:2px solid var(--pink);box-shadow:none}
body.dark .btn.alt{background:#30262e}
.hero-art{position:relative;min-height:470px;display:flex;justify-content:center;align-items:center}
.bubble{position:absolute;background:white;border-radius:22px;padding:11px 16px;box-shadow:var(--shadow);font-weight:800;animation:float 3s ease-in-out infinite}
body.dark .bubble{background:#332731}
.b1{top:30px;left:5%}.b2{right:2%;top:100px;animation-delay:.8s}.b3{bottom:55px;left:4%;animation-delay:1.4s}
@keyframes float{50%{transform:translateY(-9px)}}
.couple-svg{width:min(100%,510px);filter:drop-shadow(0 18px 18px rgba(92,62,69,.15))}
.section{padding:70px 6%}
.section-title{text-align:center;font-size:clamp(32px,5vw,48px);color:var(--brown);margin-bottom:12px}
body.dark .section-title{color:#fff}
.section-sub{text-align:center;max-width:720px;margin:0 auto 34px;line-height:1.7;color:#806c66}
body.dark .section-sub{color:#dbcdd2}
.filters{text-align:center;margin-bottom:26px}
.filter-btn{border:0;padding:9px 15px;margin:5px;border-radius:999px;background:#fff;color:var(--brown);font-weight:800;cursor:pointer;box-shadow:0 5px 12px rgba(0,0,0,.06)}
.filter-btn.active{background:var(--pink);color:white}
body.dark .filter-btn{background:#392d35;color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}
.card{background:var(--card);border-radius:24px;padding:22px;box-shadow:var(--shadow);transition:.25s;border:1px solid rgba(255,255,255,.6)}
.card:hover{transform:translateY(-6px)}
.mood-card{text-align:center;overflow:hidden}
.mood-visual{height:190px;border-radius:20px;margin-bottom:16px;display:flex;align-items:center;justify-content:center;font-size:82px;position:relative;overflow:hidden}
.mood-visual:after{content:"";position:absolute;width:120px;height:30px;background:rgba(255,255,255,.35);border-radius:50%;bottom:18px;filter:blur(7px)}
.happy{background:linear-gradient(135deg,#fff0a7,#ffd4df)}
.cry{background:linear-gradient(135deg,#cfebff,#e4d9ff)}
.fight{background:linear-gradient(135deg,#ffd2c7,#ffc0ca)}
.sad{background:linear-gradient(135deg,#d7defe,#d1e9ed)}
.love{background:linear-gradient(135deg,#ffe0ea,#ffc3d4)}
.sleep{background:linear-gradient(135deg,#ddd6ff,#c7e4ff)}
.mood-card h3{font-size:21px;margin:8px 0}.mood-card p{line-height:1.6;color:#7a6660}
.quote-box{max-width:900px;margin:auto;text-align:center;background:linear-gradient(135deg,#fff,#fff1f5);padding:45px;border-radius:30px;box-shadow:var(--shadow);position:relative}
body.dark .quote-box{background:#332630}
.quote-mark{font-size:80px;line-height:.5;color:#ffb6c8}.quote-text{font-size:clamp(22px,4vw,34px);line-height:1.45;font-weight:900;margin:15px 0}.quote-author{color:var(--pink);font-weight:800}
.story-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px}
.story-card{position:relative;overflow:hidden}.story-no{font-size:60px;font-weight:900;color:#ffd5df;position:absolute;right:18px;top:6px}.story-card h3{margin:25px 0 10px;color:var(--pink)}.story-card p{line-height:1.75}
.timeline{max-width:850px;margin:auto;position:relative}.timeline:before{content:"";position:absolute;left:24px;top:0;bottom:0;width:4px;background:#ffd4df;border-radius:5px}.moment{padding-left:70px;margin:30px 0;position:relative}.moment:before{content:"💗";position:absolute;left:5px;top:0;background:white;border-radius:50%;width:42px;height:42px;display:grid;place-items:center;box-shadow:var(--shadow)}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:20px}.feature{text-align:center}.feature .big{font-size:62px}.feature h3{margin:10px}.feature p{line-height:1.6;color:#806c66}
.meter{height:18px;background:#f2e8eb;border-radius:999px;overflow:hidden;margin:18px 0}.meter-fill{height:100%;width:0;background:linear-gradient(90deg,#ff93ac,#ff5e88);transition:width .5s;border-radius:999px}
input,textarea,select{width:100%;padding:13px 14px;border:1px solid #ead8de;border-radius:14px;margin:7px 0 12px;background:#fff;color:#49383a;font:inherit}
body.dark input,body.dark textarea,body.dark select{background:#2a2229;color:#fff;border-color:#5a4550}
.note-list{display:grid;gap:10px;margin-top:15px}.note{background:var(--soft);padding:12px 14px;border-radius:13px;text-align:left;display:flex;justify-content:space-between;gap:10px}.note button{border:0;background:transparent;cursor:pointer}
.memory-wall{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px}.polaroid{background:white;padding:11px 11px 24px;box-shadow:0 8px 20px rgba(0,0,0,.1);transform:rotate(-1.5deg);border-radius:8px;text-align:center}.polaroid:nth-child(even){transform:rotate(1.8deg)}.polaroid .pic{height:150px;border-radius:6px;display:grid;place-items:center;font-size:65px}.polaroid p{margin-top:12px;font-weight:800;color:#66504d}
body.dark .polaroid{background:#352a32}.heart{position:fixed;pointer-events:none;z-index:3000;animation:fly 1.7s ease-out forwards;font-size:24px}@keyframes fly{to{transform:translateY(-150px) scale(1.8);opacity:0}}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(90px);background:#4e3840;color:white;padding:12px 20px;border-radius:999px;z-index:4000;opacity:0;transition:.3s}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
footer{padding:45px 20px;text-align:center;background:#6b4f45;color:white;margin-top:35px}footer h2{color:#ffd4df;margin-bottom:8px}
#topBtn{position:fixed;bottom:24px;right:20px;border:0;width:46px;height:46px;border-radius:50%;background:var(--pink);color:#fff;cursor:pointer;display:none;z-index:900}
@media(max-width:860px){header{align-items:flex-start}.hero{grid-template-columns:1fr;text-align:center;padding-top:45px}.hero p{margin-left:auto;margin-right:auto}.hero-art{min-height:390px}nav{display:none}.hero h1{font-size:52px}.b1{left:0}.b2{right:0}.section{padding:55px 5%}}
</style>
</head>
<body>
<header>
  <div class="logo">🐻 Bubu <span>❤️</span> Dudu 🐼</div>
  <nav>
    <a href="#moods">Moods</a><a href="#quotes">Quotes</a><a href="#stories">Stories</a><a href="#features">Features</a><a href="#memories">Memories</a><a href="#play">Play</a><a href="#notes">Love Notes</a>
  </nav>
  <button class="icon-btn" onclick="toggleTheme()" title="Theme">🌙</button>
</header>

<section class="hero" id="home">
  <div>
    <span class="badge">✨ Welcome to our tiny chaotic universe</span>
    <h1>Bubu <span>❤️</span> Dudu</h1>
    <p>A cute little place for love, silly fights, dramatic crying, random sadness, happy hugs, tiny stories and all the moments that somehow make two weirdos inseparable.</p>
    <button class="btn" onclick="document.getElementById('moods').scrollIntoView({behavior:'smooth'})">Explore Our Moods 💞</button>
    <button class="btn alt" onclick="rainHearts()">Send 100 Hugs 🤗</button>
  </div>
  <div class="hero-art">
    <div class="bubble b1">Bubu: “I’m not angry 😤”</div><div class="bubble b2">Dudu: “Then why that face? 😭”</div><div class="bubble b3">5 mins later: 🫂❤️</div>
    <svg class="couple-svg" viewBox="0 0 600 500" aria-label="Cute Bubu and Dudu illustration">
      <ellipse cx="300" cy="445" rx="225" ry="30" fill="#ead9d1" opacity=".5"/>
      <circle cx="175" cy="120" r="52" fill="#a97957"/><circle cx="330" cy="125" r="50" fill="#222"/>
      <circle cx="128" cy="92" r="27" fill="#8f6348"/><circle cx="222" cy="92" r="27" fill="#8f6348"/>
      <circle cx="290" cy="92" r="26" fill="#111"/><circle cx="371" cy="94" r="26" fill="#111"/>
      <ellipse cx="185" cy="265" rx="135" ry="150" fill="#b9825c"/>
      <ellipse cx="343" cy="265" rx="128" ry="148" fill="#fafafa" stroke="#222" stroke-width="12"/>
      <ellipse cx="180" cy="255" rx="93" ry="105" fill="#f3c9ad"/>
      <ellipse cx="343" cy="250" rx="90" ry="100" fill="#fff"/>
      <ellipse cx="320" cy="217" rx="22" ry="34" fill="#111"/><ellipse cx="368" cy="217" rx="22" ry="34" fill="#111"/>
      <circle cx="326" cy="210" r="7" fill="white"/><circle cx="374" cy="210" r="7" fill="white"/>
      <circle cx="157" cy="225" r="9" fill="#3d2d28"/><circle cx="202" cy="225" r="9" fill="#3d2d28"/>
      <ellipse cx="180" cy="253" rx="12" ry="9" fill="#4a332d"/><ellipse cx="344" cy="260" rx="12" ry="9" fill="#222"/>
      <path d="M164 270 Q180 286 198 270" fill="none" stroke="#633f36" stroke-width="5" stroke-linecap="round"/>
      <path d="M327 276 Q344 291 363 276" fill="none" stroke="#222" stroke-width="5" stroke-linecap="round"/>
      <circle cx="135" cy="258" r="18" fill="#ff9eb3" opacity=".7"/><circle cx="225" cy="258" r="18" fill="#ff9eb3" opacity=".7"/>
      <circle cx="300" cy="263" r="17" fill="#ff9eb3" opacity=".75"/><circle cx="390" cy="263" r="17" fill="#ff9eb3" opacity=".75"/>
      <path d="M255 310 C295 280 320 285 348 313" stroke="#b9825c" stroke-width="32" fill="none" stroke-linecap="round"/>
      <path d="M450 310 C407 281 378 289 348 314" stroke="#222" stroke-width="30" fill="none" stroke-linecap="round"/>
      <path d="M265 142 C280 112 323 114 342 143 C360 170 342 202 303 228 C267 201 248 172 265 142" fill="#ff6f91"/>
    </svg>
  </div>
</section>

<section class="section" id="moods">
  <h2 class="section-title">Every Bubu × Dudu Mood</h2><p class="section-sub">Because love is not just cute photos. Sometimes it is “don’t talk to me”, followed by “why aren’t you talking to me?” five minutes later.</p>
  <div class="filters">
    <button class="filter-btn active" onclick="filterMood('all',this)">All</button><button class="filter-btn" onclick="filterMood('happy',this)">Happy</button><button class="filter-btn" onclick="filterMood('fight',this)">Fight</button><button class="filter-btn" onclick="filterMood('cry',this)">Cry</button><button class="filter-btn" onclick="filterMood('sad',this)">Sad</button><button class="filter-btn" onclick="filterMood('love',this)">Love</button>
  </div>
  <div class="grid" id="moodGrid">
    <article class="card mood-card" data-mood="happy"><div class="mood-visual happy">🐻😄🐼</div><h3>Happy Together</h3><p>Laughing at things nobody else would understand.</p></article>
    <article class="card mood-card" data-mood="fight"><div class="mood-visual fight">🐻💢🐼</div><h3>Mini World War</h3><p>Both are right. Both are wrong. Nobody is apologising first.</p></article>
    <article class="card mood-card" data-mood="cry"><div class="mood-visual cry">🐻😭🐼</div><h3>Drama & Tears</h3><p>One cries. The other panics. Then both become soft.</p></article>
    <article class="card mood-card" data-mood="sad"><div class="mood-visual sad">🐻🥺🐼</div><h3>Missing You</h3><p>When one tiny “I miss you” contains an entire paragraph.</p></article>
    <article class="card mood-card" data-mood="love"><div class="mood-visual love">🐻🫶🐼</div><h3>Love Mode</h3><p>Random hugs, forehead kisses and unnecessary cuteness.</p></article>
    <article class="card mood-card" data-mood="happy"><div class="mood-visual happy">🐻🍜🐼</div><h3>Food Date</h3><p>Sharing food until somebody steals the last bite.</p></article>
    <article class="card mood-card" data-mood="fight"><div class="mood-visual fight">🐻🙄🐼</div><h3>Silent Treatment</h3><p>Online. Seen. No reply. Psychological warfare begins.</p></article>
    <article class="card mood-card" data-mood="love"><div class="mood-visual sleep">🐻💤🐼</div><h3>Sleepy Calls</h3><p>“You sleep first.” “No, you.” Repeat for 37 minutes.</p></article>
  </div>
</section>

<section class="section" id="quotes">
  <h2 class="section-title">Bubu Dudu Quotes</h2><p class="section-sub">Tap the button whenever you need a little line for your person.</p>
  <div class="quote-box"><div class="quote-mark">“</div><div class="quote-text" id="quoteText">You are my favourite notification, favourite problem and favourite person.</div><div class="quote-author" id="quoteAuthor">— Bubu to Dudu 💗</div><button class="btn" onclick="newQuote()">Give Me Another Quote ✨</button><button class="btn alt" onclick="copyQuote()">Copy Quote 📋</button></div>
</section>

<section class="section" id="stories">
  <h2 class="section-title">Tiny Stories From Our World</h2><p class="section-sub">Short scenes about two stubborn cuties who somehow keep choosing each other.</p>
  <div class="story-grid">
    <div class="card story-card"><span class="story-no">01</span><h3>The Last Bite 🍕</h3><p>Dudu said she was not hungry. Bubu ordered one plate. Dudu ate the last bite. Bubu stared in betrayal. Ten seconds later he ordered dessert for both.</p></div>
    <div class="card story-card"><span class="story-no">02</span><h3>The 2-Minute Fight 😤</h3><p>Bubu said “fine”. Dudu said “fine”. Nobody was fine. Two minutes later Dudu sent a sad sticker. Bubu replied with a hug. Peace treaty signed.</p></div>
    <div class="card story-card"><span class="story-no">03</span><h3>The Rainy Day ☔</h3><p>They had one umbrella and absolutely no coordination. Both got wet, blamed each other, laughed like idiots, and still called it a perfect day.</p></div>
    <div class="card story-card"><span class="story-no">04</span><h3>The Goodnight Trap 🌙</h3><p>“Good night” was sent at 11:12 PM. Actual sleeping happened at 1:03 AM after memes, complaints, one fight and six “okay last message” messages.</p></div>
  </div>
</section>

<section class="section" id="memories">
  <h2 class="section-title">Memory Wall</h2><p class="section-sub">A playful polaroid wall for the little moments worth remembering.</p>
  <div class="memory-wall">
    <div class="polaroid"><div class="pic happy">🐻🤗🐼</div><p>Best Hug Ever</p></div><div class="polaroid"><div class="pic fight">🐻😠🐼</div><p>Fight #999</p></div><div class="polaroid"><div class="pic cry">🐻🧻🐼</div><p>Emergency Tissue Day</p></div><div class="polaroid"><div class="pic love">🐻💋🐼</div><p>Unexpected Kiss</p></div><div class="polaroid"><div class="pic happy">🐻🍰🐼</div><p>Sweet Date</p></div><div class="polaroid"><div class="pic sad">🐻📱🐼</div><p>Miss You Call</p></div>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Our Chaos Timeline</h2><p class="section-sub">The usual emotional journey of a perfectly normal Bubu–Dudu day.</p>
  <div class="timeline">
    <div class="moment"><div class="card"><b>08:00 — Good morning ☀️</b><p>Sweet messages, sleepy faces and fake promises to be productive.</p></div></div>
    <div class="moment"><div class="card"><b>13:00 — Food conflict 🍱</b><p>“Anything is fine.” Nothing suggested is actually fine.</p></div></div>
    <div class="moment"><div class="card"><b>18:30 — Tiny fight 💢</b><p>A small misunderstanding somehow becomes a Supreme Court case.</p></div></div>
    <div class="moment"><div class="card"><b>18:47 — Reconciliation 🫂</b><p>One sticker, one soft message, one hug. Case dismissed.</p></div></div>
    <div class="moment"><div class="card"><b>23:55 — Love overload ❤️</b><p>“Okay sleep now.” Followed by another hour of talking.</p></div></div>
  </div>
</section>

<section class="section" id="play">
  <h2 class="section-title">Play With Bubu & Dudu</h2><p class="section-sub">A few silly interactive features because a cute website should do more than just sit there.</p>
  <div class="feature-grid">
    <div class="card feature"><div class="big">🫂</div><h3>Hug Meter</h3><p>How badly does Dudu need a Bubu hug today?</p><div class="meter"><div id="hugFill" class="meter-fill"></div></div><b id="hugText">0% hug emergency</b><br><button class="btn" onclick="hugMeter()">Measure Hug Need</button></div>
    <div class="card feature"><div class="big">💞</div><h3>Love Compatibility</h3><p>Enter two names. This is scientifically useless but emotionally important.</p><input id="name1" placeholder="Bubu"><input id="name2" placeholder="Dudu"><button class="btn" onclick="loveCalc()">Calculate Love</button><h2 id="loveResult" style="color:var(--pink);margin-top:10px">❤️</h2></div>
    <div class="card feature"><div class="big">🎭</div><h3>Today's Mood</h3><p>Let the universe decide your Bubu–Dudu mood.</p><h2 id="dailyMood" style="margin:20px 0">🤔</h2><button class="btn" onclick="pickMood()">Pick Our Mood</button></div>
    <div class="card feature"><div class="big">🎁</div><h3>Surprise Button</h3><p>Never trust a button labelled surprise.</p><h2 id="surpriseText" style="margin:18px 0">👀</h2><button class="btn" onclick="surpriseMe()">Open Surprise</button></div>
  </div>
</section>

<section class="section" id="notes">
  <h2 class="section-title">Love Notes Jar</h2><p class="section-sub">Write tiny notes. They stay in your browser so you can come back to them later.</p>
  <div class="card" style="max-width:760px;margin:auto;text-align:center"><textarea id="noteInput" rows="3" maxlength="180" placeholder="Example: I am still angry, but I also miss you 😤❤️"></textarea><button class="btn" onclick="addNote()">Drop Note Into Jar 💌</button><button class="btn alt" onclick="clearNotes()">Clear Jar</button><div id="noteList" class="note-list"></div></div>
</section>

<section class="section">
  <div class="quote-box"><div class="quote-mark">♥</div><div class="quote-text">No perfect relationship. Just two imperfect people who keep finding their way back to each other.</div><button class="btn" onclick="rainHearts()">Make It Rain Hearts 💖</button></div>
</section>


<section id="features" class="section">
  <div class="section-head">
    <span class="eyebrow">MORE THAN A LOVE PAGE</span>
    <h2>✨ Little Things That Make Us <span>Us</span></h2>
    <p>Play around, save memories, and make your own Bubu–Dudu world.</p>
  </div>

  <div class="feature-grid">
    <div class="feature-card">
      <div class="feature-icon">💌</div>
      <h3>Love Letter Generator</h3>
      <p>Choose a mood and get a cute message instantly.</p>
      <select id="letterMood">
        <option>Sweet</option><option>Romantic</option><option>Funny</option>
        <option>Apology</option><option>Good Night</option>
      </select>
      <button class="primary-btn" onclick="generateLetter()">Write for Me 💕</button>
      <div class="output-box" id="letterOutput">Your message will appear here...</div>
    </div>

    <div class="feature-card">
      <div class="feature-icon">🎡</div>
      <h3>Couple Wheel</h3>
      <p>Spin the wheel when you can't decide what to do.</p>
      <button class="primary-btn" onclick="spinWheel()">SPIN ❤️</button>
      <div class="wheel" id="wheel">❤️</div>
      <div class="output-box" id="wheelResult">Ready?</div>
    </div>

    <div class="feature-card">
      <div class="feature-icon">🎯</div>
      <h3>Random Date Idea</h3>
      <p>Need a cute plan? Let Bubu & Dudu choose one.</p>
      <button class="primary-btn" onclick="dateIdea()">Give Us a Date 💗</button>
      <div class="output-box" id="dateOutput">Press the button...</div>
    </div>

    <div class="feature-card">
      <div class="feature-icon">🧠</div>
      <h3>How Well Do You Know Us?</h3>
      <p>Answer a tiny quiz and see your relationship score.</p>
      <button class="primary-btn" onclick="startQuiz()">Start Quiz 🐼</button>
      <div class="output-box" id="quizOutput">No cheating! 😌</div>
    </div>

    <div class="feature-card">
      <div class="feature-icon">📸</div>
      <h3>Memory Booth</h3>
      <p>Add your own memory and keep it in this browser.</p>
      <input id="memoryText" placeholder="e.g. Our first long call ❤️">
      <button class="primary-btn" onclick="saveMemory()">Save Memory 📌</button>
      <div id="memoryList" class="memory-list"></div>
    </div>

    <div class="feature-card">
      <div class="feature-icon">⏳</div>
      <h3>Relationship Counter</h3>
      <p>Set your special date and watch the counter grow.</p>
      <input id="specialDate" type="date" onchange="saveDate()">
      <div class="counter-big" id="relationshipCounter">0 days</div>
      <small id="counterHint">Choose your special date above.</small>
    </div>
  </div>
</section>

<section class="section mini-games">
  <div class="section-head">
    <span class="eyebrow">PLAY TOGETHER</span>
    <h2>🎮 Bubu & Dudu Mini Games</h2>
  </div>
  <div class="game-grid">
    <button class="game-card" onclick="catchHearts()">💗<b>Catch Hearts</b><span>Tap for a random heart surprise</span></button>
    <button class="game-card" onclick="compliment()">🥰<b>Compliment Machine</b><span>Get today's compliment</span></button>
    <button class="game-card" onclick="fightResolver()">🥺<b>Fight Resolver</b><span>Who should say sorry?</span></button>
    <button class="game-card" onclick="fortune()">🔮<b>Love Fortune</b><span>Ask Bubu & Dudu</span></button>
  </div>
  <div id="gameResult" class="big-result">Choose a game 👆</div>
</section>

<section class="section playlist">
  <div class="section-head">
    <span class="eyebrow">OUR VIBE</span>
    <h2>🎵 Couple Playlist</h2>
    <p>Save songs that remind you of each other.</p>
  </div>
  <div class="song-form">
    <input id="songInput" placeholder="Song name — Artist">
    <button class="primary-btn" onclick="addSong()">Add Song 🎶</button>
  </div>
  <div id="songList" class="song-list"></div>
</section>

<footer><h2>🐻 Bubu ❤️ Dudu 🐼</h2><p>Made with unnecessary drama, unlimited hugs and a dangerous amount of cuteness.</p><p style="opacity:.75;margin-top:12px">Fan-style demo website • 2026</p></footer>
<button id="topBtn" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button><div class="toast" id="toast"></div>

<script>
const quotes=[
 ["You are my favourite notification, favourite problem and favourite person.","— Bubu to Dudu 💗"],
 ["I may fight with you all day, but I still want you beside me at night.","— Dudu 🐼"],
 ["My mood improves suspiciously fast when you text me.","— Bubu 🐻"],
 ["We are 50% love, 30% food, 20% unnecessary arguments.","— Relationship Mathematics 😌"],
 ["Even after a fight, my heart still checks whether you ate.","— Soft Bubu 💕"],
 ["I don't need a perfect day. I just need a little time with you.","— Dudu 🌷"],
 ["You annoy me professionally and love me personally.","— Bubu 😤❤️"],
 ["Home is not a place. Sometimes it is one ridiculously cute person.","— Bubu × Dudu 🏡"],
 ["If we stop teasing each other, please check whether we are okay.","— Chaos Department 😂"],
 ["Come here. I am still angry, but I need a hug.","— Every Bubu Dudu Fight 🫂"]
];
let qIndex=0;
function newQuote(){let n;do{n=Math.floor(Math.random()*quotes.length)}while(n===qIndex);qIndex=n;document.getElementById('quoteText').textContent=quotes[n][0];document.getElementById('quoteAuthor').textContent=quotes[n][1]}
function copyQuote(){navigator.clipboard.writeText(document.getElementById('quoteText').textContent+' '+document.getElementById('quoteAuthor').textContent);toast('Quote copied 💗')}
function filterMood(mood,btn){document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');document.querySelectorAll('.mood-card').forEach(c=>c.style.display=(mood==='all'||c.dataset.mood===mood)?'block':'none')}
function toggleTheme(){document.body.classList.toggle('dark');document.querySelector('.icon-btn').textContent=document.body.classList.contains('dark')?'☀️':'🌙';localStorage.setItem('bubuTheme',document.body.classList.contains('dark')?'dark':'light')}
if(localStorage.getItem('bubuTheme')==='dark'){document.body.classList.add('dark');document.querySelector('.icon-btn').textContent='☀️'}
function hugMeter(){let n=Math.floor(Math.random()*31)+70;document.getElementById('hugFill').style.width=n+'%';document.getElementById('hugText').textContent=n+(n>90?'% — CRITICAL HUG EMERGENCY 🚨':'% — hug required immediately 🫂')}
function loveCalc(){let a=document.getElementById('name1').value.trim(),b=document.getElementById('name2').value.trim();if(!a||!b){toast('Enter both cute names first 😤');return}let s=(a+b).toLowerCase().split('').reduce((x,c)=>x+c.charCodeAt(0),0);let n=88+(s%13);document.getElementById('loveResult').textContent=n+'% ❤️ '+(n>=97?'Dangerously compatible 😳':'Certified cuties 🥰')}
const moods=['🥰 Love overload','😤 Tiny fight incoming','😭 Extra emotional','😂 Uncontrollable giggles','🫂 Need a long hug','🍕 Food date mood','😴 Sleepy together','🥺 Missing each other'];
function pickMood(){document.getElementById('dailyMood').textContent=moods[Math.floor(Math.random()*moods.length)]}
const surprises=['You owe Dudu one hug 🫂','Bubu gets one forehead kiss 😚','No fighting for the next 10 minutes 😌','Send a “miss you” text right now 💌','Snack date unlocked 🍫','One dramatic apology required 😂','Emergency cuddle activated ❤️'];
function surpriseMe(){document.getElementById('surpriseText').textContent=surprises[Math.floor(Math.random()*surprises.length)];rainHearts(18)}
function rainHearts(count=45){for(let i=0;i<count;i++){setTimeout(()=>{let h=document.createElement('div');h.className='heart';h.textContent=['💗','💕','❤️','💖','🩷'][Math.floor(Math.random()*5)];h.style.left=Math.random()*100+'vw';h.style.top=(60+Math.random()*35)+'vh';document.body.appendChild(h);setTimeout(()=>h.remove(),1800)},i*25)}}
function toast(msg){let t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)}
function getNotes(){return JSON.parse(localStorage.getItem('bubuNotes')||'[]')}
function renderNotes(){let box=document.getElementById('noteList'),notes=getNotes();box.innerHTML=notes.length?notes.map((n,i)=>`<div class="note"><span>💌 ${escapeHtml(n)}</span><button onclick="deleteNote(${i})">🗑️</button></div>`).join(''):'<p style="opacity:.65">Your jar is empty. Put something cute in it.</p>'}
function escapeHtml(s){return s.replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
function addNote(){let x=document.getElementById('noteInput'),v=x.value.trim();if(!v){toast('Write something first 💌');return}let n=getNotes();n.unshift(v);localStorage.setItem('bubuNotes',JSON.stringify(n.slice(0,20)));x.value='';renderNotes();toast('Love note saved ❤️')}
function deleteNote(i){let n=getNotes();n.splice(i,1);localStorage.setItem('bubuNotes',JSON.stringify(n));renderNotes()}
function clearNotes(){localStorage.removeItem('bubuNotes');renderNotes();toast('Jar cleared')}
renderNotes();
let topBtn=document.getElementById('topBtn');window.addEventListener('scroll',()=>topBtn.style.display=window.scrollY>400?'block':'none');

const letters = {
  Sweet: [
    "You make ordinary moments feel like my favorite memories. ❤️",
    "If I could choose one place to be, it would be beside you. 🥹💕"
  ],
  Romantic: [
    "I don't need a perfect day. I just need you somewhere in it. 💗",
    "Out of all the stories in the world, I still choose ours. 🐼💞"
  ],
  Funny: [
    "I love you even when you steal my food. That's serious commitment. 😂❤️",
    "We fight, we sulk, we eat, we forget why we fought. Perfect. 😭😂"
  ],
  Apology: [
    "Okay okay... Bubu is sorry. Now come here for a hug. 🥺🤗",
    "We can be right or we can be happy. I choose us. Sorry, Dudu. ❤️"
  ],
  "Good Night": [
    "Sleep peacefully. Tomorrow you still have to deal with me. 🌙😂❤️",
    "Good night, my favorite human. See you in our dreams. 🥹🌙"
  ]
};

const dateIdeas = [
  "🍕 Order food, switch off phones and watch a silly movie.",
  "🌅 Watch the sunset and take one photo together.",
  "☕ Try a café neither of you has visited.",
  "🎮 Play a game where the loser buys dessert.",
  "🚶 Take a random walk and talk about everything.",
  "🍳 Cook something together and rate it brutally.",
  "📸 Recreate an old photo together."
];

const wheelChoices = [
  "Movie Night 🎬","Ice Cream 🍦","Long Call 📱","Go for a Walk 🚶",
  "Cook Together 🍳","Photo Session 📸","Sleep 😴","Surprise Hug 🤗"
];

function generateLetter(){
  const mood=document.getElementById("letterMood").value;
  const arr=letters[mood];
  document.getElementById("letterOutput").innerHTML=arr[Math.floor(Math.random()*arr.length)];
}

function spinWheel(){
  const result=wheelChoices[Math.floor(Math.random()*wheelChoices.length)];
  const wheel=document.getElementById("wheel");
  wheel.classList.remove("spin");
  void wheel.offsetWidth;
  wheel.classList.add("spin");
  document.getElementById("wheelResult").innerHTML="Tonight: <b>"+result+"</b>";
}

function dateIdea(){
  document.getElementById("dateOutput").textContent =
    dateIdeas[Math.floor(Math.random()*dateIdeas.length)];
}

function startQuiz(){
  const questions=[
    ["Who usually says sorry first?",["Bubu","Dudu"]],
    ["Who gets hungry first?",["Bubu","Dudu"]],
    ["Who is more dramatic?",["Bubu","Dudu"]],
    ["Who would survive longer without texting?",["Dudu","Bubu"]]
  ];
  let score=0;
  questions.forEach(q=>{
    if(confirm(q[0]+"\n\nClick OK for "+q[1][0]+" or Cancel for "+q[1][1])) score++;
  });
  document.getElementById("quizOutput").innerHTML =
    "Your totally scientific score: <b>"+score+"/4 ❤️</b><br>"+
    (score>=3?"You two are dangerously compatible. 🥰":"You need more dates. Immediately. 😂");
}

function saveMemory(){
  const input=document.getElementById("memoryText");
  const value=input.value.trim();
  if(!value)return;
  const memories=JSON.parse(localStorage.getItem("bd_memories")||"[]");
  memories.unshift({text:value,date:new Date().toLocaleDateString()});
  localStorage.setItem("bd_memories",JSON.stringify(memories.slice(0,12)));
  input.value="";
  renderMemories();
}

function renderMemories(){
  const memories=JSON.parse(localStorage.getItem("bd_memories")||"[]");
  const box=document.getElementById("memoryList");
  box.innerHTML=memories.length ? memories.map((m,i)=>
    `<div class="saved-memory">💗 <span>${escapeHtml(m.text)}<small>${m.date}</small></span><button onclick="deleteMemory(${i})">×</button></div>`
  ).join("") : "<small>No memories yet. Add your first one 💕</small>";
}

function deleteMemory(i){
  const memories=JSON.parse(localStorage.getItem("bd_memories")||"[]");
  memories.splice(i,1);
  localStorage.setItem("bd_memories",JSON.stringify(memories));
  renderMemories();
}

function escapeHtml(s){
  return s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}

function saveDate(){
  const date=document.getElementById("specialDate").value;
  localStorage.setItem("bd_date",date);
  updateCounter();
}

function updateCounter(){
  const saved=localStorage.getItem("bd_date");
  if(!saved)return;
  document.getElementById("specialDate").value=saved;
  const start=new Date(saved+"T00:00:00");
  const now=new Date();
  const days=Math.max(0,Math.floor((now-start)/(1000*60*60*24)));
  document.getElementById("relationshipCounter").textContent=days+" days";
  document.getElementById("counterHint").textContent="And counting... 💕";
}

function gameMessage(message){
  document.getElementById("gameResult").innerHTML=message;
  burstHearts();
}

function catchHearts(){
  const n=Math.floor(Math.random()*91)+10;
  gameMessage("You caught <b>"+n+" hearts</b>! 💗💗💗");
}

function compliment(){
  const arr=["Your smile could fix a bad day. 🥹","You are someone's favorite notification. 📱❤️",
    "You make love look cute. 🐼💕","You deserve an unreasonable amount of hugs. 🤗"];
  gameMessage(arr[Math.floor(Math.random()*arr.length)]);
}

function fightResolver(){
  const winner=Math.random()<.5?"Bubu":"Dudu";
  gameMessage("<b>"+winner+"</b> should say sorry first. Case closed. ⚖️😂");
}

function fortune(){
  const arr=["A surprise hug is coming. 🔮🤗","A silly fight will become a funny memory. 🔮😂",
    "Food will solve the next disagreement. 🔮🍕","Someone is secretly missing the other one right now. 🔮🥺"];
  gameMessage(arr[Math.floor(Math.random()*arr.length)]);
}

function burstHearts(){
  for(let i=0;i<16;i++){
    const h=document.createElement("span");
    h.className="floating-heart";
    h.textContent=["❤️","💕","💗","💖"][Math.floor(Math.random()*4)];
    h.style.left=Math.random()*100+"vw";
    h.style.animationDelay=Math.random()*0.5+"s";
    document.body.appendChild(h);
    setTimeout(()=>h.remove(),1800);
  }
}

function addSong(){
  const input=document.getElementById("songInput");
  const song=input.value.trim();
  if(!song)return;
  const songs=JSON.parse(localStorage.getItem("bd_songs")||"[]");
  songs.push(song);
  localStorage.setItem("bd_songs",JSON.stringify(songs));
  input.value="";
  renderSongs();
}

function renderSongs(){
  const songs=JSON.parse(localStorage.getItem("bd_songs")||"[]");
  document.getElementById("songList").innerHTML=songs.length
    ? songs.map((s,i)=>`<div class="song">🎵 <span>${escapeHtml(s)}</span><button onclick="removeSong(${i})">×</button></div>`).join("")
    : "<small>Your playlist is empty.</small>";
}

function removeSong(i){
  const songs=JSON.parse(localStorage.getItem("bd_songs")||"[]");
  songs.splice(i,1);
  localStorage.setItem("bd_songs",JSON.stringify(songs));
  renderSongs();
}

document.addEventListener("DOMContentLoaded",()=>{
  renderMemories();
  renderSongs();
  updateCounter();
});

</script>
</body>
</html>
'''


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "application": "Bubu Dudu World"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
