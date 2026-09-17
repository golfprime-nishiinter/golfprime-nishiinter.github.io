<script>
(function(){
  var now0=new Date(), mLast=new Date(now0.getFullYear(), now0.getMonth()+1, 0);
  var M=now0.getMonth()+1, D=mLast.getDate(), W='日月火水木金土'[mLast.getDay()];
  document.querySelectorAll('[data-mdw]').forEach(function(e){e.textContent=e.getAttribute('data-mdw').replace('{M}',M).replace('{D}',D).replace('{W}',W);});
  function track(n,p){try{if(typeof gtag==='function')gtag('event',n,p||{});}catch(e){}}
  document.querySelectorAll('a[href*="golfprime.jp/form"]').forEach(function(a){a.addEventListener('click',function(){track('cta_form',{place:a.className||'link',page:location.pathname});});});
  document.querySelectorAll('a[href*="line.me"]').forEach(function(a){a.addEventListener('click',function(){track('cta_line',{place:a.className||'link',page:location.pathname});});});
})();
</script>
<script>(function(){
  // nav toggle
  var t=document.querySelector('[data-nav-toggle]'),n=document.querySelector('[data-nav]');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o);});}

  // exit-intent modal（1セッション1回）
  var m=document.getElementById('exitModal');if(!m)return;
  var shown=false;
  try{shown=sessionStorage.getItem('gp_exit')==='1';}catch(e){}
  function open(){if(shown)return;shown=true;m.classList.add('show');m.setAttribute('aria-hidden','false');try{sessionStorage.setItem('gp_exit','1');}catch(e){}}
  function close(){m.classList.remove('show');m.setAttribute('aria-hidden','true');}
  m.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',close);});
  m.addEventListener('click',function(e){if(e.target===m)close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
  // PC: マウスが画面上端へ
  document.addEventListener('mouseleave',function(e){if(e.clientY<=0)open();});
  // スマホ: 戻る操作をフック
  var isMobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if(isMobile&&history.pushState){
    history.pushState({gp:1},'');
    window.addEventListener('popstate',function(){if(!shown){open();history.pushState({gp:1},'');}});
  }
  // スマホ: 一定以上読んで、スクロールが止まった後に上方向へ素早く戻ったら
  var lastY=window.scrollY,maxY=0;
  window.addEventListener('scroll',function(){
    var y=window.scrollY;maxY=Math.max(maxY,y);
    if(isMobile&&maxY>800&&lastY-y>120&&y<200)open();
    lastY=y;
  },{passive:true});
})();
</script>
