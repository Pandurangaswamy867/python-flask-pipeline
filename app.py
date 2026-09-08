from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SecureTrust Bank</title>

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}
html{scroll-behavior:smooth}
body{background:#f4f7fb;color:#1f2937}
header{background:#0b3d91;color:white;padding:18px 40px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:1000}
.logo{font-size:28px;font-weight:bold}
nav a{color:white;text-decoration:none;margin-left:18px;font-size:16px}
nav a:hover{color:#ffd166}
.hero{min-height:82vh;background:linear-gradient(rgba(0,0,0,.58),rgba(0,0,0,.58)),url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=80') center/cover;display:flex;justify-content:center;align-items:center;flex-direction:column;color:white;text-align:center;padding:30px}
.hero h1{font-size:60px;max-width:900px}
.hero p{font-size:22px;margin-top:18px}
.btn{margin:20px 8px 0;padding:13px 25px;border:0;border-radius:8px;background:#ffd166;color:#0b3d91;font-size:16px;font-weight:bold;cursor:pointer}
.btn.secondary{background:white}
.notice{background:#123c69;color:white;text-align:center;padding:13px;font-weight:bold}
.section-title{text-align:center;margin:55px 0 25px;font-size:38px;color:#0b3d91}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:22px;padding:20px 45px 55px}
.card{background:white;padding:28px;border-radius:14px;text-align:center;box-shadow:0 5px 18px rgba(0,0,0,.09);transition:.25s}
.card:hover{transform:translateY(-6px)}
.icon{font-size:45px}
.card h3{margin:12px 0;color:#0b3d91}
.card p{line-height:1.6;color:#555}
.stats{background:#0b3d91;color:white;display:flex;justify-content:space-around;gap:20px;flex-wrap:wrap;padding:50px 20px;text-align:center}
.stats h2{font-size:45px}
.panel{max-width:950px;margin:20px auto 55px;background:white;padding:30px;border-radius:15px;box-shadow:0 5px 18px rgba(0,0,0,.08)}
form{max-width:650px;margin:auto}
input,select,textarea{width:100%;padding:13px;margin:8px 0 14px;border:1px solid #ccc;border-radius:7px}
form .btn{width:100%;margin:5px 0}
.result{margin-top:15px;padding:15px;border-radius:8px;background:#eef6ff;display:none}
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;margin-top:15px}
th,td{padding:13px;border-bottom:1px solid #ddd;text-align:left}
th{background:#0b3d91;color:white}
.calculator{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.calculator .full{grid-column:1/-1}
.notice-box{background:#fff8df;border-left:5px solid #ffd166;padding:18px;border-radius:8px}
footer{background:#062c6b;color:white;text-align:center;padding:30px}
#topBtn{position:fixed;bottom:20px;right:20px;display:none;background:#ffd166;color:#0b3d91;border:0;padding:13px;border-radius:50%;cursor:pointer;font-size:18px}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:2000;align-items:center;justify-content:center;padding:20px}
.modal-content{background:white;max-width:500px;width:100%;padding:30px;border-radius:15px}
.close{float:right;font-size:25px;cursor:pointer}
@media(max-width:768px){header{flex-direction:column}.hero h1{font-size:40px}nav{margin-top:14px}.calculator{grid-template-columns:1fr}.grid{padding:15px 20px 40px}}
</style>
</head>

<body>

<header>
<div class="logo">🏦 SecureTrust Bank</div>
<nav>
<a href="#">Home</a>
<a href="#services">Services</a>
<a href="#accounts">Accounts</a>
<a href="#tools">Tools</a>
<a href="#apply">Apply</a>
<a href="#contact">Contact</a>
</nav>
</header>

<div class="notice">🔐 Secure Banking • 24/7 Support: 1800-123-4567 • UPI • Net Banking • Mobile Banking</div>

<section class="hero">
<h1>Banking Made Simple, Smart & Secure</h1>
<p>Accounts • Cards • Loans • Investments • Digital Payments</p>
<div>
<button class="btn" onclick="scrollToId('apply')">Open an Account</button>
<button class="btn secondary" onclick="openLogin()">🔑 Internet Banking</button>
</div>
</section>

<h2 class="section-title" id="services">Banking Services</h2>
<section class="grid">
<div class="card"><div class="icon">💳</div><h3>Debit & Credit Cards</h3><p>Manage cards, payments, limits and secure transactions.</p></div>
<div class="card"><div class="icon">📱</div><h3>Mobile Banking</h3><p>Check balances, transfer money and pay bills from anywhere.</p></div>
<div class="card"><div class="icon">🏠</div><h3>Home Loans</h3><p>Flexible home financing options with convenient repayment plans.</p></div>
<div class="card"><div class="icon">🚗</div><h3>Vehicle Loans</h3><p>Finance your new or used vehicle with competitive options.</p></div>
<div class="card"><div class="icon">💰</div><h3>Fixed Deposits</h3><p>Invest your savings for a fixed tenure and plan your returns.</p></div>
<div class="card"><div class="icon">📈</div><h3>Investments</h3><p>Explore recurring deposits, mutual funds and long-term savings.</p></div>
<div class="card"><div class="icon">🔄</div><h3>Fund Transfer</h3><p>Transfer funds using UPI, IMPS, NEFT and RTGS.</p></div>
<div class="card"><div class="icon">🧾</div><h3>Bill Payments</h3><p>Pay electricity, mobile, broadband and other bills online.</p></div>
</section>

<h2 class="section-title" id="accounts">Account Types</h2>
<section class="grid">
<div class="card"><div class="icon">👤</div><h3>Savings Account</h3><p>Everyday banking with digital access, ATM services and secure payments.</p><button class="btn" onclick="selectAccount('Savings Account')">Choose</button></div>
<div class="card"><div class="icon">🏢</div><h3>Current Account</h3><p>Business banking designed for frequent transactions and business needs.</p><button class="btn" onclick="selectAccount('Current Account')">Choose</button></div>
<div class="card"><div class="icon">🎓</div><h3>Student Account</h3><p>Simple banking for students with convenient digital payment facilities.</p><button class="btn" onclick="selectAccount('Student Account')">Choose</button></div>
<div class="card"><div class="icon">💼</div><h3>Salary Account</h3><p>Convenient salary banking with digital access and card services.</p><button class="btn" onclick="selectAccount('Salary Account')">Choose</button></div>
</section>

<section class="stats">
<div><h2 id="customers">0</h2><p>Customers</p></div>
<div><h2 id="branches">0</h2><p>Branches</p></div>
<div><h2 id="atms">0</h2><p>ATMs</p></div>
<div><h2 id="years">0</h2><p>Years of Trust</p></div>
</section>

<h2 class="section-title" id="tools">Banking Tools</h2>
<section class="panel">
<div class="notice-box"><b>Interest Calculator</b><br>Use the calculator below to estimate simple interest. This is a demonstration feature, not a banking quote.</div>
<div class="calculator" style="margin-top:20px">
<div><label>Principal Amount (₹)</label><input id="principal" type="number" value="100000"></div>
<div><label>Annual Interest Rate (%)</label><input id="rate" type="number" value="7"></div>
<div><label>Time (Years)</label><input id="time" type="number" value="5"></div>
<div><label>&nbsp;</label><button class="btn" onclick="calculateInterest()">Calculate</button></div>
<div class="full result" id="interestResult"></div>
</div>
</section>

<section class="panel">
<h3 style="color:#0b3d91">🔎 IFSC / Branch Finder</h3>
<p style="margin:10px 0">Enter a city or branch name to search the demo branch directory.</p>
<input id="branchSearch" oninput="findBranch()" placeholder="Example: Hyderabad">
<div id="branchResult" class="result"></div>
</section>

<section class="panel">
<h3 style="color:#0b3d91">💱 Currency Converter</h3>
<p style="margin:10px 0">Demo converter using fixed sample rates.</p>
<div class="calculator">
<div><label>Amount</label><input id="amount" type="number" value="1000"></div>
<div><label>From</label><select id="from"><option>INR</option><option>USD</option><option>EUR</option><option>GBP</option></select></div>
<div><label>To</label><select id="to"><option>USD</option><option>INR</option><option>EUR</option><option>GBP</option></select></div>
<div><label>&nbsp;</label><button class="btn" onclick="convertCurrency()">Convert</button></div>
<div class="full result" id="currencyResult"></div>
</div>
</section>

<h2 class="section-title" id="apply">Open an Account</h2>
<section class="panel">
<form onsubmit="submitApplication(event)">
<input id="name" type="text" placeholder="Full Name" required>
<input id="email" type="email" placeholder="Email Address" required>
<input id="phone" type="tel" placeholder="Phone Number" required>
<select id="accountType" required>
<option value="">Select Account Type</option>
<option>Savings Account</option>
<option>Current Account</option>
<option>Student Account</option>
<option>Salary Account</option>
</select>
<input type="text" placeholder="City" required>
<textarea rows="3" placeholder="Additional information"></textarea>
<button class="btn" type="submit">Submit Application</button>
<div id="applicationResult" class="result"></div>
</form>
</section>

<h2 class="section-title">Recent Transactions Demo</h2>
<section class="panel table-wrap">
<table>
<tr><th>Date</th><th>Description</th><th>Type</th><th>Amount</th><th>Status</th></tr>
<tr><td>08 Sep 2026</td><td>Salary Credit</td><td>Credit</td><td>₹65,000</td><td>Completed</td></tr>
<tr><td>07 Sep 2026</td><td>UPI Payment</td><td>Debit</td><td>₹2,450</td><td>Completed</td></tr>
<tr><td>05 Sep 2026</td><td>Electricity Bill</td><td>Debit</td><td>₹1,280</td><td>Completed</td></tr>
<tr><td>02 Sep 2026</td><td>Interest Credit</td><td>Credit</td><td>₹750</td><td>Completed</td></tr>
</table>
</section>

<h2 class="section-title">Why SecureTrust?</h2>
<section class="grid">
<div class="card"><div class="icon">🔒</div><h3>Security First</h3><p>Strong authentication and transaction monitoring concepts.</p></div>
<div class="card"><div class="icon">⚡</div><h3>Fast Payments</h3><p>Modern digital payment channels designed for convenience.</p></div>
<div class="card"><div class="icon">🌐</div><h3>Anywhere Access</h3><p>Access your banking services through digital channels.</p></div>
<div class="card"><div class="icon">☎️</div><h3>Customer Support</h3><p>Get assistance through our 24/7 customer support channel.</p></div>
</section>

<footer id="contact">
<h3>🏦 SecureTrust Bank</h3>
<p>Hyderabad, Telangana</p>
<p>📞 1800-123-4567</p>
<p>✉ support@securetrustbank.com</p>
<br>
<p>© 2026 SecureTrust Bank. All Rights Reserved.</p>
<p style="margin-top:10px;font-size:13px">Demo application — no real banking transactions are performed.</p>
</footer>

<button id="topBtn" onclick="window.scrollTo({top:0,behavior:'smooth'})">⬆</button>

<div class="modal" id="loginModal">
<div class="modal-content">
<span class="close" onclick="closeLogin()">×</span>
<h2 style="color:#0b3d91;margin-bottom:15px">🔑 Internet Banking</h2>
<input id="loginUser" placeholder="Customer ID">
<input id="loginPass" type="password" placeholder="Password">
<button class="btn" style="width:100%;margin:5px 0" onclick="loginDemo()">Login</button>
<div id="loginResult" class="result"></div>
</div>
</div>

<script>
function scrollToId(id){document.getElementById(id).scrollIntoView({behavior:'smooth'})}

function selectAccount(type){
document.getElementById('accountType').value=type;
scrollToId('apply');
}

function submitApplication(e){
e.preventDefault();
let name=document.getElementById('name').value;
let type=document.getElementById('accountType').value;
let box=document.getElementById('applicationResult');
box.style.display='block';
box.innerHTML='✅ Application submitted for <b>'+type+'</b>. Thank you, <b>'+name+'</b>! This is a demo and no real account was created.';
}

function calculateInterest(){
let p=parseFloat(document.getElementById('principal').value)||0;
let r=parseFloat(document.getElementById('rate').value)||0;
let t=parseFloat(document.getElementById('time').value)||0;
let interest=p*r*t/100;
let total=p+interest;
let box=document.getElementById('interestResult');
box.style.display='block';
box.innerHTML='Estimated Simple Interest: <b>₹'+interest.toLocaleString('en-IN',{maximumFractionDigits:2})+'</b><br>Total Amount: <b>₹'+total.toLocaleString('en-IN',{maximumFractionDigits:2})+'</b>';
}

const branchData=[
{name:'Hyderabad Main Branch',city:'hyderabad',ifsc:'STBK0001001',address:'Banjara Hills, Hyderabad'},
{name:'Bengaluru Branch',city:'bengaluru',ifsc:'STBK0001002',address:'MG Road, Bengaluru'},
{name:'Chennai Branch',city:'chennai',ifsc:'STBK0001003',address:'Anna Salai, Chennai'},
{name:'Bhubaneswar Branch',city:'bhubaneswar',ifsc:'STBK0001004',address:'Saheed Nagar, Bhubaneswar'}
];

function findBranch(){
let q=document.getElementById('branchSearch').value.toLowerCase().trim();
let box=document.getElementById('branchResult');
if(!q){box.style.display='none';return}
let matches=branchData.filter(x=>x.city.includes(q)||x.name.toLowerCase().includes(q));
box.style.display='block';
box.innerHTML=matches.length ? matches.map(x=>'<b>'+x.name+'</b><br>IFSC: '+x.ifsc+'<br>'+x.address).join('<hr>') : 'No demo branch found.';
}

const rates={INR:1,USD:0.0119,EUR:0.0102,GBP:0.0088};
function convertCurrency(){
let amount=parseFloat(document.getElementById('amount').value)||0;
let from=document.getElementById('from').value;
let to=document.getElementById('to').value;
let result=amount/rates[from]*rates[to];
let box=document.getElementById('currencyResult');
box.style.display='block';
box.innerHTML='<b>'+amount.toLocaleString()+' '+from+' = '+result.toLocaleString(undefined,{maximumFractionDigits:2})+' '+to+'</b><br><small>Demo fixed exchange rate.</small>';
}

function animateCounter(id,target){
let count=0, step=target/100;
let timer=setInterval(()=>{
count+=step;
if(count>=target){count=target;clearInterval(timer)}
document.getElementById(id).innerText=Math.floor(count).toLocaleString()+'+';
},20);
}
animateCounter('customers',250000);
animateCounter('branches',450);
animateCounter('atms',1200);
animateCounter('years',25);

function openLogin(){document.getElementById('loginModal').style.display='flex'}
function closeLogin(){document.getElementById('loginModal').style.display='none'}
function loginDemo(){
let user=document.getElementById('loginUser').value;
let box=document.getElementById('loginResult');
box.style.display='block';
box.innerHTML=user ? '⚠️ Demo login only. No real authentication is connected.' : 'Please enter a Customer ID.';
}

let topBtn=document.getElementById('topBtn');
window.onscroll=function(){
topBtn.style.display=(document.documentElement.scrollTop>300)?'block':'none';
}
</script>
</body>
</html>
"""

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "application": "SecureTrust Bank"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
