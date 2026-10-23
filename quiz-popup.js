/* Pop-up du test gratuit, sur toutes les pages sauf la page d'arrivée des pubs (les-4-leviers).
   Voulu par Virginie le 23/10/2026 : une vraie fenêtre posée sur le texte, qu'on ne peut pas manquer.
   Limite connue : Google déconseille les fenêtres qui masquent le contenu
   (developers.google.com/search/docs/appearance/avoid-intrusive-interstitials, ouvert le 23/10/2026).
   Pour la réduire : jamais à l'arrivée sur la page, seulement après 12 secondes ou 25 % de lecture,
   et une seule fois par lectrice (fermée : 7 jours de repos ; test cliqué : 60 jours). */
(function(){
  var K='vdck-quiz-popup', now=Date.now();
  try{ var until=+localStorage.getItem(K)||0; if(until>now) return; }catch(e){}
  if(/les-4-leviers|politique-de-confidentialite/.test(location.pathname)) return;

  var slug=(location.pathname.replace(/^\/|\.html$|\/$/g,'').replace(/\//g,'-'))||'accueil';
  function href(){
    /* reprend l'origine posée par le relais sur les autres liens de la page */
    var m='organique', a=document.querySelector('a[href*="utm_source=site"]');
    if(a){ try{ m=new URL(a.href).searchParams.get('utm_medium')||m; }catch(e){} }
    return 'https://quizzvdck.netlify.app/?utm_source=site&utm_medium='+encodeURIComponent(m)+'&utm_content='+encodeURIComponent(slug+'-popup');
  }
  function hold(days){ try{ localStorage.setItem(K, String(now+days*864e5)); }catch(e){} }

  var css=document.createElement('style');
  css.textContent=
    '.vqp-bg{position:fixed;inset:0;z-index:9998;background:rgba(14,14,14,.6);opacity:0;transition:opacity .4s ease;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}'+
    '.vqp-bg.on{opacity:1}'+
    '.vqp{position:relative;width:440px;max-width:100%;max-height:calc(100vh - 32px);overflow:auto;background:#fff;color:#0e0e0e;box-shadow:0 30px 80px rgba(0,0,0,.4);'+
    'transform:translate(60px,-40px) scale(.94);opacity:0;transition:transform .55s cubic-bezier(.2,.9,.3,1.15),opacity .45s ease;font-family:inherit}'+
    '.vqp-bg.on .vqp{transform:none;opacity:1}'+
    '.vqp-img{display:block;width:100%;height:230px;object-fit:cover;object-position:center 22%}'+
    '.vqp-in{padding:26px 30px 24px;text-align:center}'+
    '.vqp-x{position:absolute;top:10px;right:10px;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.92);border:0;color:#0e0e0e;font-size:24px;line-height:40px;cursor:pointer;padding:0}'+
    '.vqp-k{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#fff;background:#a88c63;padding:6px 12px;margin:0 0 16px}'+
    '.vqp-t{font-family:"Cormorant Garamond",serif;font-weight:500;font-size:30px;line-height:1.2;margin:0 0 12px}'+
    '.vqp-t em{color:#a88c63}'+
    '.vqp-p{font-size:15px;line-height:1.6;color:#333;margin:0 0 22px}'+
    '.vqp-b{display:block;background:#0e0e0e;color:#fff;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;padding:18px 20px}'+
    '.vqp-l{display:block;width:100%;margin-top:10px;background:none;border:0;color:#777;font-size:13px;text-decoration:underline;cursor:pointer;padding:6px}'+
    '@media (max-width:600px){.vqp-img{height:190px}.vqp-in{padding:22px 20px 18px}.vqp-t{font-size:26px}}';
  document.head.appendChild(css);

  var bg=document.createElement('div');
  bg.className='vqp-bg';
  bg.innerHTML=
    '<div class="vqp" role="dialog" aria-modal="true" aria-label="Le test gratuit">'+
      '<button class="vqp-x" type="button" aria-label="Fermer">&times;</button>'+
      '<img class="vqp-img" src="/.netlify/images?url=%2Fhero.jpg&w=880&fm=webp&q=78" alt="Virginie Deconinck">'+
      '<div class="vqp-in">'+
        '<p class="vqp-k">Test gratuit · 2 minutes</p>'+
        '<p class="vqp-t">Votre corps se répare-t-il encore <em>plus vite qu\'il ne s\'use&nbsp;?</em></p>'+
        '<p class="vqp-p">9 questions pour savoir où en est votre corps aujourd\'hui.</p>'+
        '<a class="vqp-b" href="#">Faire le test</a>'+
        '<button class="vqp-l" type="button">Plus tard</button>'+
      '</div>'+
    '</div>';

  var shown=false, overflow='';
  function close(){
    bg.classList.remove('on'); hold(7);
    document.documentElement.style.overflow=overflow;
    document.removeEventListener('keydown',esc);
    setTimeout(function(){ bg.remove(); },500);
  }
  function esc(e){ if(e.key==='Escape') close(); }
  function show(){
    if(shown) return; shown=true;
    window.removeEventListener('scroll',onScroll);
    bg.querySelector('.vqp-b').href=href();
    document.body.appendChild(bg);
    overflow=document.documentElement.style.overflow;
    document.documentElement.style.overflow='hidden';
    void bg.offsetWidth; setTimeout(function(){ bg.classList.add('on'); },30);
    document.addEventListener('keydown',esc);
  }
  bg.querySelector('.vqp-x').onclick=close;
  bg.querySelector('.vqp-l').onclick=close;
  bg.onclick=function(e){ if(e.target===bg) close(); };
  bg.querySelector('.vqp-b').onclick=function(){ hold(60); document.documentElement.style.overflow=overflow; };

  function onScroll(){
    var h=document.documentElement.scrollHeight-innerHeight;
    if(h>0 && scrollY/h>=0.25) show();
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  setTimeout(show,12000);
})();
