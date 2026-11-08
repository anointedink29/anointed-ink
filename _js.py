# Front-end JS. Plain string. No backticks and no template literals anywhere, so this
# stays safe to embed in any generator.
JS = """

/* home hero: the altarpiece opens once, then turns toward the pointer; the gallery wall's
   frames tilt the same way. All of it stops for visitors who turn motion off. */
(function(){
 var d=document, root=d.documentElement, hero=d.getElementById('hero'), stage=d.getElementById('stage');
 var mm=function(q){ return !!(window.matchMedia&&window.matchMedia(q).matches); };
 if(mm('(prefers-reduced-motion: reduce)')) return;
 var hover=mm('(hover: hover)');
 if(stage&&hero){
  root.classList.add('js-altar');
  var open=function(){ root.classList.add('altar-open'); };
  requestAnimationFrame(function(){ requestAnimationFrame(open); });
  setTimeout(open,1200);
  if(hover){
   hero.addEventListener('pointermove',function(e){
    var r=hero.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
    stage.style.setProperty('--ry',(x*9).toFixed(2)+'deg');
    stage.style.setProperty('--rx',(-y*5).toFixed(2)+'deg');
    stage.style.setProperty('--sheen',((x+.5)*100).toFixed(1)+'%');
    hero.style.setProperty('--hx',(e.clientX-r.left)+'px');
    hero.style.setProperty('--hy',(e.clientY-r.top)+'px');
   });
   hero.addEventListener('pointerleave',function(){
    stage.style.setProperty('--ry','0deg'); stage.style.setProperty('--rx','0deg');
   });
  }
 }
 if(hover){
  [].slice.call(d.querySelectorAll('.hang figure')).forEach(function(el){
   el.addEventListener('pointermove',function(e){
    var r=el.getBoundingClientRect();
    el.style.setProperty('--ty',(((e.clientX-r.left)/r.width-.5)*10).toFixed(1)+'deg');
    el.style.setProperty('--tx',((.5-(e.clientY-r.top)/r.height)*8).toFixed(1)+'deg');
   });
  });
 }
})();

/* idea builder: no AI and no upload. The picks fill the text to Nestor and pull three of his
   matching pieces from the gallery data on the page; nothing leaves the phone until Text. */
(function(){
 var d=document, b=d.querySelector('.builder'); if(!b) return;
 var data=[]; try{ data=JSON.parse(d.getElementById('idea-data').textContent); }catch(e){}
 var tel=b.getAttribute('data-tel'), thumbs=d.getElementById('idea-thumbs'),
     msg=d.getElementById('idea-msg'), send=d.getElementById('idea-send'), text=d.getElementById('idea-text');
 function picked(g){
  return [].slice.call(b.querySelectorAll('.ichips[data-group="'+g+'"] .ichip[aria-pressed="true"]'));
 }
 function words(list){ return list.map(function(x){ return x.textContent.toLowerCase(); }).join(', '); }
 function update(){
  var st=picked('style'), pl=picked('place'), sz=picked('size'), idea=(text.value||'').trim();
  var lines=['Hi Nestor, I saw your site.'];
  if(idea) lines.push('Idea: '+idea);
  if(st.length) lines.push('Style: '+words(st));
  if(pl.length) lines.push('Placement: '+words(pl));
  if(sz.length) lines.push('Rough size: '+words(sz));
  msg.textContent=lines.join('\\n');
  send.href='sms:'+tel+'?&body='+encodeURIComponent(lines.join('\\n'));
  var tags=st.map(function(x){ return x.getAttribute('data-tag'); });
  var scored=data.map(function(p){
   var n=0; tags.forEach(function(t){ if(p.t.indexOf(t)>-1) n++; }); return {p:p,n:n};
  }).filter(function(x){ return tags.length?x.n>0:true; });
  scored.sort(function(a,c){ return c.n-a.n; });
  thumbs.innerHTML='';
  scored.slice(0,3).forEach(function(x){
   var i=d.createElement('img');
   i.src='img/'+x.p.s+'-400.webp'; i.alt=x.p.a; i.width=x.p.w; i.height=x.p.h;
   i.loading='lazy'; i.decoding='async'; thumbs.appendChild(i);
  });
 }
 b.addEventListener('click',function(e){
  var c=e.target.closest('.ichip'); if(!c) return;
  var grp=c.parentNode, on=c.getAttribute('aria-pressed')==='true';
  if(grp.hasAttribute('data-single')){
   [].slice.call(grp.querySelectorAll('.ichip')).forEach(function(o){ o.setAttribute('aria-pressed','false'); });
  }
  c.setAttribute('aria-pressed',on?'false':'true');
  update();
 });
 text.addEventListener('input',update);
 update();
})();
(function(){
 'use strict';
 var d=document;

 /* mobile nav */
 var burger=d.querySelector('.burger'), links=d.querySelector('.navlinks');
 if(burger&&links){
  burger.addEventListener('click',function(){
   var open=links.classList.toggle('open');
   burger.setAttribute('aria-expanded',open?'true':'false');
  });
  function closeNav(){ links.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }
  links.addEventListener('click',function(e){ if(e.target.closest('a')) closeNav(); });
  d.addEventListener('keydown',function(e){
   if(e.key==='Escape'&&links.classList.contains('open')){ closeNav(); burger.focus(); }
  });
 }

 /* gallery filtering, with the active filter reflected in the URL hash so a
    filtered view can be linked and shared */
 var chips=[].slice.call(d.querySelectorAll('.chip'));
 var figs=[].slice.call(d.querySelectorAll('[data-styles]'));
 var countEl=d.querySelector('.count');

 function apply(tag,push){
  var shown=0;
  figs.forEach(function(f){
   var ok = tag==='all' ||
    (' '+f.dataset.styles+' '+(f.dataset.artist||'')+' ').indexOf(' '+tag+' ')>-1;
   f.hidden=!ok; if(ok) shown++;
  });
  var kind='style';
  chips.forEach(function(c){
   c.setAttribute('aria-pressed', c.dataset.filter===tag?'true':'false');
   if(c.dataset.filter===tag&&c.dataset.kind) kind=c.dataset.kind;
  });
  if(countEl){
   var label=tag==='all'?'pieces':(kind==='artist'?'pieces by this artist':'pieces in this style');
   countEl.textContent='Showing '+shown+' '+label+'.';
  }
  if(push){
   if(tag==='all'){ history.replaceState(null,'',location.pathname); }
   else { history.replaceState(null,'','#'+tag); }
  }
  build();
 }
 chips.forEach(function(c){
  c.addEventListener('click',function(){ apply(c.dataset.filter,true); });
 });
 if(chips.length){
  var initial=(location.hash||'').replace('#','');
  var valid=chips.some(function(c){return c.dataset.filter===initial;});
  apply(valid?initial:'all',false);
 }

 /* lightbox */
 var lb=d.querySelector('.lb'); if(!lb) return;
 var lbImg=lb.querySelector('img'), lbCap=lb.querySelector('figcaption');
 var order=[], at=-1;

 function build(){ order=figs.filter(function(f){return !f.hidden;}); }
 build();

 function show(i){
  if(!order.length) return;
  at=(i+order.length)%order.length;
  var f=order[at];
  lbImg.src=f.dataset.full; lbImg.alt=f.dataset.alt||'';
  lbImg.width=f.dataset.fw||''; lbImg.height=f.dataset.fh||'';
  lbCap.textContent=f.dataset.caption||'';
  lb.classList.add('on'); d.body.style.overflow='hidden';
 }
 function close(){ lb.classList.remove('on'); d.body.style.overflow=''; lbImg.src=''; }

 figs.forEach(function(f){
  f.addEventListener('click',function(){ build(); show(order.indexOf(f)); });
  var btn=f.querySelector('img');
  if(btn){ btn.setAttribute('tabindex','0'); }
  f.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){ e.preventDefault(); build(); show(order.indexOf(f)); }
  });
 });
 lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
 lb.querySelector('.x').addEventListener('click',close);
 lb.querySelector('.prev').addEventListener('click',function(e){e.stopPropagation();show(at-1);});
 lb.querySelector('.next').addEventListener('click',function(e){e.stopPropagation();show(at+1);});
 d.addEventListener('keydown',function(e){
  if(!lb.classList.contains('on')) return;
  if(e.key==='Escape') close();
  if(e.key==='ArrowLeft') show(at-1);
  if(e.key==='ArrowRight') show(at+1);
 });

 /* swipe on touch */
 var x0=null;
 lb.addEventListener('touchstart',function(e){ x0=e.changedTouches[0].clientX; },{passive:true});
 lb.addEventListener('touchend',function(e){
  if(x0===null) return;
  var dx=e.changedTouches[0].clientX-x0;
  if(Math.abs(dx)>48) show(dx>0?at-1:at+1);
  x0=null;
 },{passive:true});
})();
"""
