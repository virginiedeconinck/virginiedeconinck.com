/* Barre téléphone et volet « Qu'est-ce qui vous amène ? », sur toutes les pages publiques.
   Demande de Virginie, 04/11/2026 : une lectrice arrivée par un lien sur un article doit pouvoir continuer sur le site.
   La barre apparaît après le premier écran et s'efface tant que le pop-up du test est ouvert (parcours.css). */
(function(){
  if(!window.matchMedia('(max-width:900px)').matches) return;
  var slug=(location.pathname.replace(/^\/|\.html$|\/$/g,'').replace(/\//g,'-'))||'accueil';
  function test(){
    var m='organique', a=document.querySelector('a[href*="utm_source=site"]');
    if(a){ try{ m=new URL(a.href).searchParams.get('utm_medium')||m; }catch(e){} }
    return 'https://quizzvdck.netlify.app/?utm_source=site&utm_medium='+encodeURIComponent(m)+'&utm_content='+encodeURIComponent(slug+'-barre');
  }
  var T=[['/blog/ventre-gonfle-menopause','Mon ventre a changé','Gonflement ou graisse ?'],
    ['/blog/sommeil-menopause-reveils-nocturnes','Je me réveille la nuit','Ce que les hormones changent'],
    ['/collagene-peau',"Ma peau n'est plus la même",'Ce qui se joue après 40 ans'],
    ['/perimenopause','Je ne me reconnais plus','Les signes de la périménopause'],
    ['/resistance-insuline','Je grossis sans manger plus',"Le rôle de l'insuline"],
    ['/glp1-femmes-perimenopause','On me parle du GLP-1','La question du muscle']];
  var bar=document.createElement('div'); bar.className='pbar';
  bar.innerHTML='<button type="button" aria-haspopup="dialog">Explorer le site</button><a href="'+test()+'">Test gratuit</a>';
  var sh=document.createElement('div'); sh.className='psheet'; sh.setAttribute('role','dialog'); sh.setAttribute('aria-modal','true'); sh.setAttribute('aria-label','Explorer le site');
  sh.innerHTML='<div class="psheet-in"><button type="button" class="psheet-x" aria-label="Fermer">×</button>'+
    '<p class="aig-title">Qu\'est-ce qui vous <em>amène ?</em></p><div class="aig-grid">'+
    T.map(function(t){return '<a class="aig-tile" href="'+t[0]+'"><span class="aig-q">'+t[1]+'</span><span class="aig-go">'+t[2]+' →</span></a>';}).join('')+
    '</div><a class="psheet-main" href="/travailler-avec-moi">Travailler avec moi</a><div class="psheet-links"><a href="/#sujets">Tous les sujets</a><a href="/blog/">Tous les articles</a><a href="/a-propos">Qui suis-je ?</a><a href="/">Accueil</a></div></div>';
  document.body.appendChild(bar); document.body.appendChild(sh);
  function open(){ sh.classList.add('on'); document.body.style.overflow='hidden'; }
  function close(){ sh.classList.remove('on'); document.body.style.overflow=''; }
  bar.querySelector('button').addEventListener('click',open);
  sh.querySelector('.psheet-x').addEventListener('click',close);
  sh.addEventListener('click',function(e){ if(e.target===sh) close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') close(); });
  function onScroll(){ bar.classList.toggle('on',scrollY>innerHeight*0.8); }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
})();
