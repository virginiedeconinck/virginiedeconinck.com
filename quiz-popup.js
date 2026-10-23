/* Invitation au test gratuit, sur toutes les pages sauf la page d'arrivée des pubs (les-4-leviers).
   Carte en bas d'écran, jamais en plein écran : Google pénalise les fenêtres qui masquent toute la page
   (developers.google.com/search/docs/appearance/avoid-intrusive-interstitials, ouvert le 23/10/2026).
   Elle apparaît quand la lectrice a parcouru 35 % de la page ou après 20 secondes.
   Fermée : on ne la remontre pas pendant 7 jours. Test cliqué : pendant 60 jours. */
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
    '.vqp{position:fixed;z-index:9999;right:24px;bottom:24px;width:360px;max-width:calc(100vw - 32px);box-sizing:border-box;'+
    'background:#0e0e0e;color:#fff;padding:30px 28px 26px;box-shadow:0 18px 50px rgba(0,0,0,.28);'+
    'transform:translateY(24px);opacity:0;transition:transform .45s ease,opacity .45s ease;font-family:inherit}'+
    '.vqp.on{transform:none;opacity:1}'+
    '.vqp-x{position:absolute;top:8px;right:8px;width:40px;height:40px;background:none;border:0;color:#bfb6aa;font-size:24px;line-height:1;cursor:pointer}'+
    '.vqp-k{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#c4a882;margin:0 0 12px}'+
    '.vqp-t{font-family:"Cormorant Garamond",serif;font-weight:400;font-size:26px;line-height:1.25;margin:0 0 10px;color:#fff}'+
    '.vqp-t em{color:#c4a882}'+
    '.vqp-p{font-size:14px;line-height:1.6;color:#d9d2c8;margin:0 0 20px}'+
    '.vqp-b{display:block;text-align:center;background:#c4a882;color:#0e0e0e;text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;padding:16px 20px}'+
    '.vqp-l{display:block;width:100%;margin-top:10px;background:none;border:0;color:#bfb6aa;font-size:13px;text-decoration:underline;cursor:pointer;padding:6px}'+
    '@media (max-width:600px){.vqp{left:0;right:0;bottom:0;width:auto;max-width:none;padding:26px 20px 18px}.vqp-t{font-size:23px}.vqp-p{margin-bottom:16px}}';
  document.head.appendChild(css);

  var box=document.createElement('div');
  box.className='vqp'; box.setAttribute('role','dialog'); box.setAttribute('aria-label','Le test gratuit');
  box.innerHTML=
    '<button class="vqp-x" type="button" aria-label="Fermer">&times;</button>'+
    '<p class="vqp-k">Le test gratuit</p>'+
    '<p class="vqp-t">Votre corps se répare-t-il encore <em>plus vite qu\'il ne s\'use&nbsp;?</em></p>'+
    '<p class="vqp-p">9 questions, moins de 2 minutes, pour savoir où en est votre corps aujourd\'hui.</p>'+
    '<a class="vqp-b" href="#">Faire le test</a>'+
    '<button class="vqp-l" type="button">Plus tard</button>';

  var shown=false;
  function close(){ box.classList.remove('on'); hold(7); setTimeout(function(){ box.remove(); },500); document.removeEventListener('keydown',esc); }
  function esc(e){ if(e.key==='Escape') close(); }
  function show(){
    if(shown) return;
    /* pas de doublon : si le bandeau ou l'encart du test est déjà à l'écran, on attend qu'il soit passé */
    var vis=[].some.call(document.querySelectorAll('.quiz-band,.quiz-encart'),function(el){ var r=el.getBoundingClientRect(); return r.bottom>0 && r.top<innerHeight; });
    if(vis){ setTimeout(show,4000); return; }
    shown=true;
    window.removeEventListener('scroll',onScroll);
    box.querySelector('.vqp-b').href=href();
    document.body.appendChild(box);
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ box.classList.add('on'); }); });
    document.addEventListener('keydown',esc);
  }
  box.querySelector('.vqp-x').onclick=close;
  box.querySelector('.vqp-l').onclick=close;
  box.querySelector('.vqp-b').onclick=function(){ hold(60); };

  function onScroll(){
    var h=document.documentElement.scrollHeight-innerHeight;
    if(h>0 && scrollY/h>=0.35) show();
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  setTimeout(show,20000);
})();
