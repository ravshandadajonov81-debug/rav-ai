html = open("index.html", "w", encoding="utf-8")
html.write("""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAV AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#0a0a0f;color:white;height:100vh;display:flex;flex-direction:column;}
.header{background:linear-gradient(135deg,#1a1a2e,#16213e);padding:12px 20px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #00d4ff44;}
.logo{width:42px;height:42px;background:linear-gradient(135deg,#00d4ff,#0066ff);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;}
.header-info h1{font-size:18px;color:#00d4ff;}
.header-info p{font-size:11px;color:#88aacc;}
.status{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12px;color:#00ff88;}
.status-dot{width:8px;height:8px;background:#00ff88;border-radius:50%;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
.chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:15px;}
.chat::-webkit-scrollbar{width:4px;}
.chat::-webkit-scrollbar-thumb{background:#00d4ff44;border-radius:2px;}
.xabar{display:flex;gap:10px;align-items:flex-start;animation:fadeIn 0.3s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
.xabar.user{flex-direction:row-reverse;}
.avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.avatar.ai{background:linear-gradient(135deg,#00d4ff,#0066ff);}
.avatar.usr{background:linear-gradient(135deg,#ff6b6b,#ff4444);}
.bubble{max-width:75%;padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.6;word-break:break-word;}
.bubble.ai{background:#1a1a2e;border:1px solid #00d4ff22;border-top-left-radius:4px;color:#e0e8ff;}
.bubble.user{background:linear-gradient(135deg,#0066ff,#0044cc);border-top-right-radius:4px;color:white;}
.vaqt{font-size:10px;color:#446688;margin-top:4px;}
.xabar.user .vaqt{text-align:right;}
.yozayapti{display:none;gap:10px;align-items:center;padding:0 20px 5px;}
.yozayapti.ko{display:flex;}
.dots span{display:inline-block;width:6px;height:6px;background:#00d4ff;border-radius:50%;margin:0 2px;animation:bounce 1.2s infinite;}
.dots span:nth-child(2){animation-delay:0.2s;}
.dots span:nth-child(3){animation-delay:0.4s;}
@keyframes bounce{0%,60%,100%{transform:translateY(0);}30%{transform:translateY(-6px);}}
.tezkor{padding:10px 20px;display:flex;gap:8px;overflow-x:auto;border-top:1px solid #ffffff11;}
.tezkor button{background:#1a1a2e;border:1px solid #00d4ff33;color:#88aacc;padding:6px 14px;border-radius:20px;font-size:12px;cursor:pointer;white-space:nowrap;transition:all 0.2s;}
.tezkor button:hover{background:#00d4ff22;border-color:#00d4ff;color:#00d4ff;}
.input-zona{padding:12px 20px;background:#0f0f1a;border-top:1px solid #ffffff11;display:flex;gap:10px;align-items:flex-end;}
.input-wrapper{flex:1;background:#1a1a2e;border:1px solid #00d4ff33;border-radius:24px;padding:10px 16px;display:flex;align-items:center;gap:8px;transition:border-color 0.2s;}
.input-wrapper:focus-within{border-color:#00d4ff;}
#savol{flex:1;background:none;border:none;color:white;font-size:14px;outline:none;resize:none;max-height:100px;font-family:inherit;}
#savol::placeholder{color:#446688;}
.mik-btn{background:none;border:none;color:#446688;font-size:18px;cursor:pointer;}
.mik-btn:hover{color:#00d4ff;}
.mik-btn.tinglayapti{color:#ff4444;}
.yubor-btn{width:44px;height:44px;background:linear-gradient(135deg,#00d4ff,#0066ff);border:none;border-radius:50%;color:white;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.yubor-btn:hover{transform:scale(1.05);}
.xush{text-align:center;padding:40px 20px;color:#446688;}
.xush h2{color:#00d4ff;font-size:28px;margin-bottom:8px;}
.xush p{font-size:14px;}
img.rasm{max-width:280px;border-radius:12px;margin-top:8px;border:1px solid #00d4ff33;}
</style>
</head>
<body>
<div class="header">
<div class="logo">&#129302;</div>
<div class="header-info"><h1>RAV AI</h1><p>Aqlli shaxsiy yordamchi</p></div>
<div class="status"><div class="status-dot"></div>Jonli</div>
</div>
<div class="chat" id="chat">
<div class="xush"><h2>&#129302; RAV AI</h2><p>Salom! Men sizning aqlli yordamchingizman.Har qanday savolingizni yozing!</p></div>
</div>
<div class="yozayapti" id="yozayapti">
<div class="avatar ai">&#129302;</div>
<div class="dots"><span></span><span></span><span></span></div>
</div>
<div class="tezkor">
<button onclick="tezkor('Salom!')">&#128075; Salom</button>
<button onclick="tezkor('Menga motivatsiya ber')">&#128170; Motivatsiya</button>
<button onclick="tezkor('Qiziqarli fakt ayt')">&#129504; Fakt</button>
<button onclick="tezkor('yangiliklar')">&#128240; Yangiliklar</button>
<button onclick="tezkor('Bugun ob havo qanday?')">&#127780; Ob-havo</button>
<button onclick="tezkor('Menga sher yoz')">&#128221; She\\'r</button>
<button onclick="tezkor('Python nima?')">&#128013; Python</button>
<button onclick="rasmSorash()">&#127912; Rasm</button>
</div>
<div class="input-zona">
<div class="input-wrapper">
<textarea id="savol" rows="1" placeholder="Savolingizni yozing..."></textarea>
<button class="mik-btn" id="mikBtn" onclick="ovoz()">&#127908;</button>
</div>
<button class="yubor-btn" onclick="yuborish()">&#10148;</button>
</div>
<script>
var sid='user_'+Math.random().toString(36).substr(2,9);
function vaqt(){var d=new Date();return d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');}
function qosh(rol,matn,img){
var chat=document.getElementById('chat');
var div=document.createElement('div');
div.className='xabar '+(rol==='user'?'user':'ai-msg');
var av='<div class="avatar '+(rol==='user'?'usr':'ai')+'">'+(rol==='user'?'&#128100;':'&#129302;')+'</div>';
var content=matn.replace(/\\n/g,'');
if(img)content+='<img class=\\"rasm\\" src=\\"'+img+'\\" onload=\\"document.getElementById(\\'chat\\').scrollTop=99999\\">';
var bub='<div><div class="bubble '+(rol==='user'?'user':'ai')+'">'+content+'</div><div class="vaqt">'+vaqt()+'</div></div>';
div.innerHTML=rol==='user'?bub+av:av+bub;
chat.appendChild(div);
chat.scrollTop=chat.scrollHeight;
}
async function yuborish(){
var inp=document.getElementById('savol');
var m=inp.value.trim();
if(!m)return;
inp.value='';inp.style.height='auto';
qosh('user',m);
document.getElementById('yozayapti').className='yozayapti ko';
try{
var r=await fetch('/savol',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({matn:m,session_id:sid})});
var d=await r.json();
document.getElementById('yozayapti').className='yozayapti';
qosh('ai',d.javob||'Xato!');
if(window.speechSynthesis){var u=new SpeechSynthesisUtterance(d.javob);u.lang='uz-UZ';speechSynthesis.speak(u);}
}catch(e){document.getElementById('yozayapti').className='yozayapti';qosh('ai','Xato yuz berdi!');}
}
function tezkor(m){document.getElementById('savol').value=m;yuborish();}
async function rasmSorash(){
var m=prompt('Rasm tavsifi:');
if(!m)return;
qosh('user','&#127912; '+m);
document.getElementById('yozayapti').className='yozayapti ko';
try{
var r=await fetch('/rasm',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({matn:m})});
var d=await r.json();
document.getElementById('yozayapti').className='yozayapti';
if(d.rasm_url)qosh('ai','&#127912; Rasm tayyor!',d.rasm_url);
}catch(e){document.getElementById('yozayapti').className='yozayapti';qosh('ai','Rasm yuklanmadi!');}
}
function ovoz(){
var btn=document.getElementById('mikBtn');
if(!('webkitSpeechRecognition' in window||'SpeechRecognition' in window)){alert('Ovoz qollab-quvvatlanmaydi!');return;}
var rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
rec.lang='uz-UZ';rec.start();
btn.className='mik-btn tinglayapti';btn.innerHTML='&#128308;';
rec.onresult=function(e){document.getElementById('savol').value=e.results[0][0].transcript;btn.className='mik-btn';btn.innerHTML='&#127908;';yuborish();};
rec.onerror=rec.onend=function(){btn.className='mik-btn';btn.innerHTML='&#127908;';};
}
var inp=document.getElementById('savol');
inp.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();yuborish();}});
inp.addEventListener('input',function(){inp.style.height='auto';inp.style.height=inp.scrollHeight+'px';});
</script>
</body>
</html>""")
html.close()
print("OK!")