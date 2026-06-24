/* Husband for an Hour — site behavior */
(function(){
  "use strict";

  /* ---------- mobile nav ---------- */
  var burger=document.querySelector('.hamburger');
  var links=document.querySelector('.nav-links');
  if(burger&&links){
    burger.addEventListener('click',function(){links.classList.toggle('open');});
    links.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){links.classList.remove('open');});
    });
  }

  /* ---------- reveal on scroll ---------- */
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
  },{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});

  /* ---------- count up ---------- */
  function countUp(el){
    var target=parseFloat(el.dataset.count), suf=el.dataset.suffix||'', pre=el.dataset.prefix||'';
    var dur=1400, start=performance.now();
    function tick(now){
      var p=Math.min((now-start)/dur,1), e=1-Math.pow(1-p,3);
      var v=target*e;
      el.textContent=pre+(target%1?v.toFixed(0):Math.round(v)).toLocaleString()+suf;
      if(p<1)requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  var cio=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){countUp(e.target);cio.unobserve(e.target);}});
  },{threshold:.5});
  document.querySelectorAll('[data-count]').forEach(function(el){cio.observe(el);});

  /* ---------- quote form (demo) ---------- */
  var form=document.getElementById('quoteForm');
  if(form){
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var ok=true;
      form.querySelectorAll('[required]').forEach(function(f){
        var bad=!f.value.trim()||(f.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.closest('.field').classList.toggle('invalid',bad);
        if(bad)ok=false;
      });
      if(!ok)return;
      form.style.display='none';
      var done=document.getElementById('formOk');
      if(done){done.classList.add('show');done.scrollIntoView({behavior:'smooth',block:'center'});}
      /* NOTE: demo only. To receive submissions, wire to Formspree/Netlify Forms
         or a server endpoint and remove this handler's preventDefault path. */
    });
    form.querySelectorAll('[required]').forEach(function(f){
      f.addEventListener('input',function(){f.closest('.field').classList.remove('invalid');});
    });
  }

  /* ---------- price book: search + category chips ---------- */
  var pbSearch=document.getElementById('pbSearch');
  if(pbSearch){
    var cats=[].slice.call(document.querySelectorAll('.pb-cat'));
    var noRes=document.getElementById('pbNoResult');
    var defOpen=cats.map(function(c){return c.open;});
    pbSearch.addEventListener('input',function(){
      var q=pbSearch.value.trim().toLowerCase();
      var anyVisible=false;
      cats.forEach(function(c,i){
        var m=0;
        [].forEach.call(c.querySelectorAll('tbody tr'),function(r){
          var show=!q||r.getAttribute('data-s').indexOf(q)>-1;
          r.hidden=!show; if(show)m++;
        });
        c.hidden=!!q&&m===0;
        c.open=q?(m>0):defOpen[i];
        if(m>0||!q)anyVisible=true;
      });
      if(noRes)noRes.hidden=!(q&&!anyVisible);
    });
    [].forEach.call(document.querySelectorAll('.pb-chip'),function(ch){
      ch.addEventListener('click',function(e){
        e.preventDefault();
        var t=document.getElementById(ch.getAttribute('data-target'));
        if(t){t.open=true;
          var y=t.getBoundingClientRect().top+window.pageYOffset-130;
          window.scrollTo({top:y,behavior:'smooth'});}
      });
    });
  }

  /* ---------- language switcher (Google Translate, headless) ---------- */
  // Comprehensive list of major world languages: code, English name, native name.
  var LANGS=[
    ["en","English","English"],["es","Spanish","Español"],["zh-CN","Chinese (Simplified)","简体中文"],
    ["zh-TW","Chinese (Traditional)","繁體中文"],["hi","Hindi","हिन्दी"],["ar","Arabic","العربية"],
    ["bn","Bengali","বাংলা"],["pt","Portuguese","Português"],["ru","Russian","Русский"],
    ["ja","Japanese","日本語"],["pa","Punjabi","ਪੰਜਾਬੀ"],["de","German","Deutsch"],
    ["jw","Javanese","Basa Jawa"],["ko","Korean","한국어"],["fr","French","Français"],
    ["te","Telugu","తెలుగు"],["mr","Marathi","मराठी"],["tr","Turkish","Türkçe"],
    ["ta","Tamil","தமிழ்"],["vi","Vietnamese","Tiếng Việt"],["ur","Urdu","اردو"],
    ["it","Italian","Italiano"],["th","Thai","ไทย"],["gu","Gujarati","ગુજરાતી"],
    ["fa","Persian","فارسی"],["pl","Polish","Polski"],["uk","Ukrainian","Українська"],
    ["ro","Romanian","Română"],["nl","Dutch","Nederlands"],["id","Indonesian","Bahasa Indonesia"],
    ["ms","Malay","Bahasa Melayu"],["tl","Filipino","Filipino"],["my","Burmese","မြန်မာ"],
    ["km","Khmer","ខ្មែរ"],["ne","Nepali","नेपाली"],["si","Sinhala","සිංහල"],
    ["el","Greek","Ελληνικά"],["hu","Hungarian","Magyar"],["cs","Czech","Čeština"],
    ["sv","Swedish","Svenska"],["fi","Finnish","Suomi"],["da","Danish","Dansk"],
    ["no","Norwegian","Norsk"],["he","Hebrew","עברית"],["sk","Slovak","Slovenčina"],
    ["bg","Bulgarian","Български"],["sr","Serbian","Српски"],["hr","Croatian","Hrvatski"],
    ["lt","Lithuanian","Lietuvių"],["lv","Latvian","Latviešu"],["et","Estonian","Eesti"],
    ["sl","Slovenian","Slovenščina"],["sw","Swahili","Kiswahili"],["am","Amharic","አማርኛ"],
    ["ha","Hausa","Hausa"],["yo","Yoruba","Yorùbá"],["ig","Igbo","Igbo"],
    ["zu","Zulu","isiZulu"],["af","Afrikaans","Afrikaans"],["sq","Albanian","Shqip"],
    ["hy","Armenian","Հայերեն"],["az","Azerbaijani","Azərbaycan"],["ka","Georgian","ქართული"],
    ["kk","Kazakh","Қазақ"],["uz","Uzbek","Oʻzbek"],["mn","Mongolian","Монгол"],
    ["lo","Lao","ລາວ"],["ml","Malayalam","മലയാളം"],["kn","Kannada","ಕನ್ನಡ"],
    ["ca","Catalan","Català"],["gl","Galician","Galego"],["is","Icelandic","Íslenska"],
    ["ga","Irish","Gaeilge"],["cy","Welsh","Cymraeg"],["mt","Maltese","Malti"],
    ["mk","Macedonian","Македонски"],["be","Belarusian","Беларуская"],["bs","Bosnian","Bosanski"],
    ["ht","Haitian Creole","Kreyòl"],["so","Somali","Soomaali"],["ps","Pashto","پښتو"],
    ["sd","Sindhi","سنڌي"],["ku","Kurdish","Kurdî"],["la","Latin","Latina"]
  ];
  var INCLUDE=LANGS.map(function(l){return l[0];}).join(',');

  window.googleTranslateElementInit=function(){
    /* eslint-disable no-undef */
    new google.translate.TranslateElement({
      pageLanguage:'en',includedLanguages:INCLUDE,autoDisplay:false
    },'google_translate_element');
  };
  (function(){
    var s=document.createElement('script');
    s.src='//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(s);
  })();

  function getCookie(n){var m=document.cookie.match('(^|;)\\s*'+n+'\\s*=\\s*([^;]+)');return m?m.pop():'';}
  function currentLang(){
    var c=decodeURIComponent(getCookie('googtrans'));
    if(c){var p=c.split('/');return p[p.length-1]||'en';}
    return 'en';
  }
  function nameFor(code){
    for(var i=0;i<LANGS.length;i++)if(LANGS[i][0]===code)return LANGS[i][1];
    return 'English';
  }
  function setLang(code){
    var host=location.hostname;
    if(code==='en'){
      document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
      document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain='+host;
      document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.'+host;
    }else{
      var v='/en/'+code;
      document.cookie='googtrans='+v+';path=/';
      document.cookie='googtrans='+v+';path=/;domain='+host;
      document.cookie='googtrans='+v+';path=/;domain=.'+host;
    }
    location.reload();
  }

  document.querySelectorAll('.lang').forEach(function(root){
    var btn=root.querySelector('.lang-btn');
    var panel=root.querySelector('.lang-panel');
    var list=root.querySelector('.lang-list');
    var search=root.querySelector('.lang-search');
    var label=root.querySelector('.lang-label');
    var cur=currentLang();
    if(label)label.textContent=nameFor(cur);
    function render(filter){
      filter=(filter||'').toLowerCase();
      list.innerHTML='';
      LANGS.filter(function(l){
        return !filter||l[1].toLowerCase().indexOf(filter)>-1||l[2].toLowerCase().indexOf(filter)>-1;
      }).forEach(function(l){
        var li=document.createElement('li');
        li.className='lang-item'+(l[0]===cur?' sel':'');
        li.innerHTML='<span>'+l[1]+'</span><span class="nat">'+l[2]+'</span>';
        li.addEventListener('click',function(){setLang(l[0]);});
        list.appendChild(li);
      });
    }
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var open=panel.classList.toggle('open');
      if(open){render('');if(search){search.value='';setTimeout(function(){search.focus();},30);}}
    });
    if(search)search.addEventListener('input',function(){render(search.value);});
    document.addEventListener('click',function(e){
      if(!root.contains(e.target))panel.classList.remove('open');
    });
  });

})();
