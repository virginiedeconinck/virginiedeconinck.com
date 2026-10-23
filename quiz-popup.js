/* Pop-up du test gratuit, sur toutes les pages sauf la page d'arrivée des pubs (les-4-leviers).
   Carte qui glisse depuis la droite et se pose SUR le texte, sans assombrir ni bloquer la page :
   Google déconseille les fenêtres qui masquent le contenu et recommande des encarts qui n'occupent
   qu'une partie de l'écran (developers.google.com/search/docs/appearance/avoid-intrusive-interstitials,
   ouvert le 23/10/2026). Choix validé par Virginie le 23/10/2026 : couleur terracotta, photo différente du site.
   Apparition après 12 secondes ou 25 % de lecture. Fermée : 7 jours de repos. Test cliqué : 60 jours. */
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

  var T='#b4583c';
  var css=document.createElement('style');
  css.textContent=
    '.vqp{position:fixed;z-index:9999;right:24px;bottom:24px;width:380px;box-sizing:border-box;background:#fff;color:#0e0e0e;'+
    'box-shadow:0 24px 60px rgba(0,0,0,.30);border-top:4px solid '+T+';text-align:center;'+
    'transform:translateX(calc(100% + 40px));transition:transform .6s cubic-bezier(.2,.9,.3,1.1);font-family:inherit}'+
    '.vqp.on{transform:none}'+
    '.vqp-img{display:block;width:100%;height:200px;object-fit:cover;object-position:center 30%}'+
    '.vqp-in{padding:20px 24px 18px}'+
    '.vqp-x{position:absolute;top:8px;right:8px;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.95);border:0;color:#0e0e0e;font-size:22px;line-height:36px;padding:0;cursor:pointer;z-index:2}'+
    '.vqp-k{display:inline-block;font-size:10px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#fff;background:'+T+';padding:6px 10px;margin:0 0 12px}'+
    '.vqp-t{font-family:"Cormorant Garamond",serif;font-weight:500;font-size:25px;line-height:1.2;margin:0 0 8px}'+
    '.vqp-t em{color:'+T+'}'+
    '.vqp-p{font-size:14px;line-height:1.5;color:#333;margin:0 0 16px}'+
    '.vqp-b{display:block;background:'+T+';color:#fff;text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;padding:15px 18px;border-radius:999px}'+
    '.vqp-l{display:block;width:100%;margin-top:6px;background:none;border:0;color:#888;font-size:12px;text-decoration:underline;cursor:pointer;padding:6px}'+
    /* mobile : photo à gauche, texte à droite, pour couvrir moins d'un tiers de l'écran */
    '@media (max-width:600px){.vqp{left:10px;right:10px;bottom:10px;width:auto;display:flex;text-align:left}'+
      '.vqp-img{width:112px;height:auto;min-height:100%;flex:0 0 112px;object-position:center 25%}'+
      '.vqp-in{padding:14px 14px 10px 16px}.vqp-k{font-size:9px;margin-bottom:8px;padding:5px 8px}'+
      '.vqp-t{font-size:19px;padding-right:22px}.vqp-p{display:none}.vqp-b{padding:12px 10px;font-size:11px;text-align:center}'+
      '.vqp-l{text-align:center;padding:4px}.vqp-x{top:4px;right:4px;width:30px;height:30px;line-height:30px;font-size:20px}}';
  document.head.appendChild(css);

  var box=document.createElement('div');
  box.className='vqp'; box.setAttribute('role','dialog'); box.setAttribute('aria-label','Le test gratuit');
  box.innerHTML=
    '<button class="vqp-x" type="button" aria-label="Fermer">&times;</button>'+
    '<img class="vqp-img" src="/popup-virginie.jpg" alt="Virginie Deconinck" width="380" height="200" loading="lazy">'+
    '<div class="vqp-in">'+
      '<p class="vqp-k">Test gratuit · 2 minutes</p>'+
      '<p class="vqp-t">Votre corps se répare-t-il encore <em>plus vite qu\'il ne s\'use&nbsp;?</em></p>'+
      '<p class="vqp-p">9 questions pour savoir où en est votre corps aujourd\'hui.</p>'+
      '<a class="vqp-b" href="#">Faire le test</a>'+
      '<button class="vqp-l" type="button">Plus tard</button>'+
    '</div>';

  var shown=false;
  function close(){ box.classList.remove('on'); hold(7); document.removeEventListener('keydown',esc); setTimeout(function(){ box.remove(); },650); }
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
    void box.offsetWidth; setTimeout(function(){ box.classList.add('on'); },30);
    document.addEventListener('keydown',esc);
  }
  box.querySelector('.vqp-x').onclick=close;
  box.querySelector('.vqp-l').onclick=close;
  box.querySelector('.vqp-b').onclick=function(){ hold(60); };

  function onScroll(){
    var h=document.documentElement.scrollHeight-innerHeight;
    if(h>0 && scrollY/h>=0.25) show();
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  setTimeout(show,12000);
})();
