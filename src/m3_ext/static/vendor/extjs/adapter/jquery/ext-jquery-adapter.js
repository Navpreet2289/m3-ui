/*
This file is part of Ext JS 3.4

Copyright (c) 2011-2013 Sencha Inc

Contact:  http://www.sencha.com/contact

Commercial Usage
Licensees holding valid commercial licenses may use this file in accordance with the Commercial
Software License Agreement provided with the Software or, alternatively, in accordance with the
terms contained in a written agreement between you and Sencha.

If you are unsure which license is appropriate for your use, please contact the sales department
at http://www.sencha.com/contact.

Build date: 2013-11-19 14:40:42
*/
window.undefined=window.undefined;Ext={version:"3.4.1.1",versionDetail:{major:3,minor:4,patch:1.1}};Ext.apply=function(d,e,b){if(b){Ext.apply(d,b)}if(d&&e&&typeof e=="object"){for(var a in e){d[a]=e[a]}}return d};(function(){var g=0,f=Object.prototype.toString,y=navigator.userAgent.toLowerCase(),n=function(e){return e.test(y)},s=document,q=s.documentMode,u=s.compatMode=="CSS1Compat",a=n(/opera/),H=n(/\bchrome\b/),z=n(/webkit/),d=!H&&n(/safari/),F=d&&n(/applewebkit\/4/),D=d&&n(/version\/3/),B=d&&n(/version\/4/),j=!a&&n(/msie/),G=j&&((n(/msie 7/)&&q!=8&&q!=9&&q!=10)||q==7),E=j&&((n(/msie 8/)&&q!=7&&q!=9&&q!=10)||q==8),C=j&&((n(/msie 9/)&&q!=7&&q!=8&&q!=10)||q==9),i=j&&((n(/msie 10/)&&q!=7&&q!=8&&q!=9)||q==10),J=j&&n(/msie 6/),K=j&&(J||G||E||C),c=!z&&n(/gecko/),M=c&&n(/rv:1\.8/),L=c&&n(/rv:1\.9/),m=K&&!u,h=n(/windows|win32/),A=n(/macintosh|mac os x/),p=n(/adobeair/),v=n(/linux/),r=/^https/i.test(window.location.protocol),b=[],w=[],o=Ext.emptyFn,x=Ext.apply({},{constructor:o,toString:o,valueOf:o}),l=function(){var e=l.caller.caller;return e.$owner.prototype[e.$name].apply(this,arguments)};if(x.constructor!==o){w.push("constructor")}if(x.toString!==o){w.push("toString")}if(x.valueOf!==o){w.push("valueOf")}if(!w.length){w=null}function k(){}Ext.apply(k,{$isClass:true,callParent:function(e){var t;return(t=this.callParent.caller)&&(t.$previous||((t=t.$owner?t:t.caller)&&t.$owner.superclass.self[t.$name])).apply(this,e||b)}});k.prototype={constructor:function(){},callParent:function(t){var N,e=(N=this.callParent.caller)&&(N.$previous||((N=N.$owner?N:N.caller)&&N.$owner.superclass[N.$name]));return e.apply(this,t||b)}};if(J){try{s.execCommand("BackgroundImageCache",false,true)}catch(I){}}Ext.apply(Ext,{SSL_SECURE_URL:r&&j?'javascript:""':"about:blank",isStrict:u,isSecure:r,isReady:false,enableForcedBoxModel:false,enableGarbageCollector:true,enableListenerCollection:false,enableNestedListenerRemoval:false,USE_NATIVE_JSON:false,applyIf:function(t,N){if(t){for(var e in N){if(!Ext.isDefined(t[e])){t[e]=N[e]}}}return t},id:function(e,t){e=Ext.getDom(e,true)||{};if(!e.id){e.id=(t||"ext-gen")+(++g)}return e.id},extend:function(){var t=function(O){for(var N in O){this[N]=O[N]}};var e=Object.prototype.constructor;return function(S,P,R){if(typeof P=="object"){R=P;P=S;S=R.constructor!=e?R.constructor:function(){P.apply(this,arguments)}}var O=function(){},Q,N=P.prototype;O.prototype=N;Q=S.prototype=new O();Q.constructor=S;S.superclass=N;if(N.constructor==e){N.constructor=P}S.override=function(T){Ext.override(S,T)};Q.superclass=Q.supr=(function(){return N});Q.override=t;Ext.override(S,R);S.extend=function(T){return Ext.extend(S,T)};return S}}(),global:(function(){return this})(),Base:k,namespaceCache:{},createNamespace:function(R,O){var e=Ext.namespaceCache,P=O?R.substring(0,R.lastIndexOf(".")):R,U=e[P],S,N,t,Q,T;if(!U){U=Ext.global;if(P){T=[];Q=P.split(".");for(S=0,N=Q.length;S<N;++S){t=Q[S];U=U[t]||(U[t]={});T.push(t);e[T.join(".")]=U}}}return U},getClassByName:function(N){var O=N.split("."),e=Ext.global,P=O.length,t;for(t=0;e&&t<P;++t){e=e[O[t]]}return e||null},addMembers:function(t,Q,N,e){var P,O,R;for(O in N){if(N.hasOwnProperty(O)){R=N[O];if(typeof R=="function"){R.$owner=t;R.$name=O}Q[O]=R}}if(e&&w){for(P=w.length;P-->0;){O=w[P];if(N.hasOwnProperty(O)){R=N[O];if(typeof R=="function"){R.$owner=t;R.$name=O}Q[O]=R}}}},define:function(R,P,N){var t=P.override,T,Q,e,O;if(t){delete P.override;T=Ext.getClassByName(t);Ext.override(T,P)}else{if(R){O=Ext.createNamespace(R,true);e=R.substring(R.lastIndexOf(".")+1)}T=function S(){this.constructor.apply(this,arguments)};if(R){T.displayName=R}T.$isClass=true;T.callParent=Ext.Base.callParent;if(typeof P=="function"){P=P(T)}Q=P.extend;if(Q){delete P.extend;if(typeof Q=="string"){Q=Ext.getClassByName(Q)}}else{Q=k}Ext.extend(T,Q,P);if(T.prototype.constructor===T){delete T.prototype.constructor}if(!T.prototype.$isClass){Ext.applyIf(T.prototype,k.prototype)}T.prototype.self=T;if(P.xtype){Ext.reg(P.xtype,T)}T=P.singleton?new T():T;if(R){O[e]=T}}if(N){N.call(T)}return T},override:function(P,R){var N,Q;if(R){if(P.$isClass){Q=R.statics;if(Q){delete R.statics}Ext.addMembers(P,P.prototype,R,true);if(Q){Ext.addMembers(P,P,Q)}}else{if(typeof P=="function"){N=P.prototype;Ext.apply(N,R);if(Ext.isIE&&R.hasOwnProperty("toString")){N.toString=R.toString}}else{var e=P.self,t,O;if(e&&e.$isClass){for(t in R){if(R.hasOwnProperty(t)){O=R[t];if(typeof O=="function"){if(e.$className){O.displayName=e.$className+"#"+t}O.$name=t;O.$owner=e;O.$previous=P.hasOwnProperty(t)?P[t]:l}P[t]=O}}}else{Ext.apply(P,R);if(!P.constructor.$isClass){P.constructor.prototype.callParent=k.prototype.callParent;P.constructor.callParent=k.callParent}}}}}},namespace:function(){var O=arguments.length,P=0,t,N,e,R,Q,S;for(;P<O;++P){e=arguments[P];R=arguments[P].split(".");S=window[R[0]];if(S===undefined){S=window[R[0]]={}}Q=R.slice(1);t=Q.length;for(N=0;N<t;++N){S=S[Q[N]]=S[Q[N]]||{}}}return S},urlEncode:function(Q,P){var N,t=[],O=encodeURIComponent;Ext.iterate(Q,function(e,R){N=Ext.isEmpty(R);Ext.each(N?e:R,function(S){t.push("&",O(e),"=",(!Ext.isEmpty(S)&&(S!=e||!N))?(Ext.isDate(S)?Ext.encode(S).replace(/"/g,""):O(S)):"")})});if(!P){t.shift();P=""}return P+t.join("")},urlDecode:function(N,t){if(Ext.isEmpty(N)){return{}}var Q={},P=N.split("&"),R=decodeURIComponent,e,O;Ext.each(P,function(S){S=S.split("=");e=R(S[0]);O=R(S[1]);Q[e]=t||!Q[e]?O:[].concat(Q[e]).concat(O)});return Q},urlAppend:function(e,t){if(!Ext.isEmpty(t)){return e+(e.indexOf("?")===-1?"?":"&")+t}return e},toArray:function(){return j?function(N,Q,O,P){P=[];for(var t=0,e=N.length;t<e;t++){P.push(N[t])}return P.slice(Q||0,O||P.length)}:function(e,N,t){return Array.prototype.slice.call(e,N||0,t||e.length)}}(),isIterable:function(e){if(Ext.isArray(e)||e.callee){return true}if(/NodeList|HTMLCollection/.test(f.call(e))){return true}return((typeof e.nextNode!="undefined"||e.item)&&Ext.isNumber(e.length))},each:function(P,O,N){if(Ext.isEmpty(P,true)){return}if(!Ext.isIterable(P)||Ext.isPrimitive(P)){P=[P]}for(var t=0,e=P.length;t<e;t++){if(O.call(N||P[t],P[t],t,P)===false){return t}}},iterate:function(N,t,e){if(Ext.isEmpty(N)){return}if(Ext.isIterable(N)){Ext.each(N,t,e);return}else{if(typeof N=="object"){for(var O in N){if(N.hasOwnProperty(O)){if(t.call(e||N,O,N[O],N)===false){return}}}}}},getDom:function(N,t){if(!N||!s){return null}if(N.dom){return N.dom}else{if(typeof N=="string"){var O=s.getElementById(N);if(O&&j&&t){if(N==O.getAttribute("id")){return O}else{return null}}return O}else{return N}}},getBody:function(){return Ext.get(s.body||s.documentElement)},getHead:function(){var e;return function(){if(e==undefined){e=Ext.get(s.getElementsByTagName("head")[0])}return e}}(),removeNode:j&&!E?function(){var e;return function(t){if(t&&t.tagName!="BODY"){(Ext.enableNestedListenerRemoval)?Ext.EventManager.purgeElement(t,true):Ext.EventManager.removeAll(t);e=e||s.createElement("div");e.appendChild(t);e.innerHTML="";delete Ext.elCache[t.id]}}}():function(e){if(e&&e.parentNode&&e.tagName!="BODY"){(Ext.enableNestedListenerRemoval)?Ext.EventManager.purgeElement(e,true):Ext.EventManager.removeAll(e);e.parentNode.removeChild(e);delete Ext.elCache[e.id]}},isEmpty:function(t,e){return t===null||t===undefined||((Ext.isArray(t)&&!t.length))||(!e?t==="":false)},isArray:function(e){return f.apply(e)==="[object Array]"},isDate:function(e){return f.apply(e)==="[object Date]"},isObject:function(e){return !!e&&Object.prototype.toString.call(e)==="[object Object]"},isPrimitive:function(e){return Ext.isString(e)||Ext.isNumber(e)||Ext.isBoolean(e)},isFunction:function(e){return f.apply(e)==="[object Function]"},isNumber:function(e){return typeof e==="number"&&isFinite(e)},isString:function(e){return typeof e==="string"},isBoolean:function(e){return typeof e==="boolean"},isElement:function(e){return e?!!e.tagName:false},isDefined:function(e){return typeof e!=="undefined"},isOpera:a,isWebKit:z,isChrome:H,isSafari:d,isSafari3:D,isSafari4:B,isSafari2:F,isIE:j,isIE6:J,isIE7:G,isIE8:E,isIE9:C,isIE10:i,isIE9m:K,isIE10p:j&&!(J||G||E||C),isIEQuirks:j&&(!u&&(J||G||E||C)),isGecko:c,isGecko2:M,isGecko3:L,isBorderBox:m,isLinux:v,isWindows:h,isMac:A,isAir:p});Ext.ns=Ext.namespace})();Ext.ns("Ext.util","Ext.lib","Ext.data","Ext.supports");Ext.elCache={};Ext.apply(Function.prototype,{createInterceptor:function(b,a){var c=this;return !Ext.isFunction(b)?this:function(){var e=this,d=arguments;b.target=e;b.method=c;return(b.apply(a||e||window,d)!==false)?c.apply(e||window,d):null}},createCallback:function(){var a=arguments,b=this;return function(){return b.apply(window,a)}},createDelegate:function(c,b,a){var d=this;return function(){var f=b||arguments;if(a===true){f=Array.prototype.slice.call(arguments,0);f=f.concat(b)}else{if(Ext.isNumber(a)){f=Array.prototype.slice.call(arguments,0);var e=[a,0].concat(b);Array.prototype.splice.apply(f,e)}}return d.apply(c||window,f)}},defer:function(c,e,b,a){var d=this.createDelegate(e,b,a);if(c>0){return setTimeout(d,c)}d();return 0}});Ext.applyIf(String,{format:function(b){var a=Ext.toArray(arguments,1);return b.replace(/\{(\d+)\}/g,function(c,d){return a[d]})}});Ext.applyIf(Array.prototype,{indexOf:function(b,c){var a=this.length;c=c||0;c+=(c<0)?a:0;for(;c<a;++c){if(this[c]===b){return c}}return -1},remove:function(b){var a=this.indexOf(b);if(a!=-1){this.splice(a,1)}return this}});Ext.util.TaskRunner=function(e){e=e||10;var f=[],a=[],b=0,g=false,d=function(){g=false;clearInterval(b);b=0},h=function(){if(!g){g=true;b=setInterval(i,e)}},c=function(j){a.push(j);if(j.onStop){j.onStop.apply(j.scope||j)}},i=function(){var l=a.length,n=new Date().getTime();if(l>0){for(var p=0;p<l;p++){f.remove(a[p])}a=[];if(f.length<1){d();return}}for(var p=0,o,k,m,j=f.length;p<j;++p){o=f[p];k=n-o.taskRunTime;if(o.interval<=k){m=o.run.apply(o.scope||o,o.args||[++o.taskRunCount]);o.taskRunTime=n;if(m===false||o.taskRunCount===o.repeat){c(o);return}}if(o.duration&&o.duration<=(n-o.taskStartTime)){c(o)}}};this.start=function(j){f.push(j);j.taskStartTime=new Date().getTime();j.taskRunTime=0;j.taskRunCount=0;h();return j};this.stop=function(j){c(j);return j};this.stopAll=function(){d();for(var k=0,j=f.length;k<j;k++){if(f[k].onStop){f[k].onStop()}}f=[];a=[]}};Ext.TaskMgr=new Ext.util.TaskRunner();if(typeof jQuery=="undefined"){throw"Unable to load Ext, jQuery not found."}(function(){var b;Ext.lib.Dom={getViewWidth:function(d){return d?Math.max(jQuery(document).width(),jQuery(window).width()):jQuery(window).width()},getViewHeight:function(d){return d?Math.max(jQuery(document).height(),jQuery(window).height()):jQuery(window).height()},isAncestor:function(e,f){var d=false;e=Ext.getDom(e);f=Ext.getDom(f);if(e&&f){if(e.contains){return e.contains(f)}else{if(e.compareDocumentPosition){return !!(e.compareDocumentPosition(f)&16)}else{while(f=f.parentNode){d=f==e||d}}}}return d},getRegion:function(d){return Ext.lib.Region.getRegion(d)},getY:function(d){return this.getXY(d)[1]},getX:function(d){return this.getXY(d)[0]},getXY:function(f){var e,j,l,m,i=(document.body||document.documentElement);f=Ext.getDom(f);if(f==i){return[0,0]}if(f.getBoundingClientRect){l=f.getBoundingClientRect();m=c(document).getScroll();return[Math.round(l.left+m.left),Math.round(l.top+m.top)]}var n=0,k=0;e=f;var d=c(f).getStyle("position")=="absolute";while(e){n+=e.offsetLeft;k+=e.offsetTop;if(!d&&c(e).getStyle("position")=="absolute"){d=true}if(Ext.isGecko){j=c(e);var o=parseInt(j.getStyle("borderTopWidth"),10)||0;var g=parseInt(j.getStyle("borderLeftWidth"),10)||0;n+=g;k+=o;if(e!=f&&j.getStyle("overflow")!="visible"){n+=g;k+=o}}e=e.offsetParent}if(Ext.isSafari&&d){n-=i.offsetLeft;k-=i.offsetTop}if(Ext.isGecko&&!d){var h=c(i);n+=parseInt(h.getStyle("borderLeftWidth"),10)||0;k+=parseInt(h.getStyle("borderTopWidth"),10)||0}e=f.parentNode;while(e&&e!=i){if(!Ext.isOpera||(e.tagName!="TR"&&c(e).getStyle("display")!="inline")){n-=e.scrollLeft;k-=e.scrollTop}e=e.parentNode}return[n,k]},setXY:function(d,e){d=Ext.fly(d,"_setXY");d.position();var f=d.translatePoints(e);if(e[0]!==false){d.dom.style.left=f.left+"px"}if(e[1]!==false){d.dom.style.top=f.top+"px"}},setX:function(e,d){this.setXY(e,[d,false])},setY:function(d,e){this.setXY(d,[false,e])}};function c(d){if(!b){b=new Ext.Element.Flyweight()}b.dom=d;return b}Ext.lib.Event={getPageX:function(d){d=d.browserEvent||d;return d.pageX},getPageY:function(d){d=d.browserEvent||d;return d.pageY},getXY:function(d){d=d.browserEvent||d;return[d.pageX,d.pageY]},getTarget:function(d){return d.target},on:function(h,d,g,f,e){jQuery(h).bind(d,g)},un:function(f,d,e){jQuery(f).unbind(d,e)},purgeElement:function(d){jQuery(d).unbind()},preventDefault:function(d){d=d.browserEvent||d;if(d.preventDefault){d.preventDefault()}else{d.returnValue=false}},stopPropagation:function(d){d=d.browserEvent||d;if(d.stopPropagation){d.stopPropagation()}else{d.cancelBubble=true}},stopEvent:function(d){this.preventDefault(d);this.stopPropagation(d)},onAvailable:function(j,e,d){var i=new Date();var g=function(){if(i.getElapsed()>10000){clearInterval(h)}var f=document.getElementById(j);if(f){clearInterval(h);e.call(d||window,f)}};var h=setInterval(g,50)},resolveTextNode:Ext.isGecko?function(e){if(!e){return}var d=HTMLElement.prototype.toString.call(e);if(d=="[xpconnect wrapped native prototype]"||d=="[object XULElement]"){return}return e.nodeType==3?e.parentNode:e}:function(d){return d&&d.nodeType==3?d.parentNode:d},getRelatedTarget:function(e){e=e.browserEvent||e;var d=e.relatedTarget;if(!d){if(e.type=="mouseout"){d=e.toElement}else{if(e.type=="mouseover"){d=e.fromElement}}}return this.resolveTextNode(d)}};Ext.lib.Ajax=function(){var d=function(f){return function(h,g){if((g=="error"||g=="timeout")&&f.failure){f.failure.call(f.scope||window,e(f,h))}else{if(f.success){f.success.call(f.scope||window,e(f,h))}}}};var e=function(f,l){var h={},j,g,i;try{j=l.getAllResponseHeaders();Ext.each(j.replace(/\r\n/g,"\n").split("\n"),function(m){g=m.indexOf(":");if(g>=0){i=m.substr(0,g).toLowerCase();if(m.charAt(g+1)==" "){++g}h[i]=m.substr(g+1)}})}catch(k){}return{responseText:l.responseText,responseXML:l.responseXML,argument:f.argument,status:l.status,statusText:l.statusText,getResponseHeader:function(m){return h[m.toLowerCase()]},getAllResponseHeaders:function(){return j}}};return{request:function(l,i,f,j,g){var k={type:l,url:i,data:j,timeout:f.timeout,complete:d(f)};if(g){var h=g.headers;if(g.xmlData){k.data=g.xmlData;k.processData=false;k.type=(l?l:(g.method?g.method:"POST"));if(!h||!h["Content-Type"]){k.contentType="text/xml"}}else{if(g.jsonData){k.data=typeof g.jsonData=="object"?Ext.encode(g.jsonData):g.jsonData;k.processData=false;k.type=(l?l:(g.method?g.method:"POST"));if(!h||!h["Content-Type"]){k.contentType="application/json"}}}if(h){k.beforeSend=function(n){for(var m in h){if(h.hasOwnProperty(m)){n.setRequestHeader(m,h[m])}}}}}jQuery.ajax(k)},formRequest:function(j,i,g,k,f,h){jQuery.ajax({type:Ext.getDom(j).method||"POST",url:i,data:jQuery(j).serialize()+(k?"&"+k:""),timeout:g.timeout,complete:d(g)})},isCallInProgress:function(f){return false},abort:function(f){return false},serializeForm:function(f){return jQuery(f.dom||f).serialize()}}}();Ext.lib.Anim=function(){var d=function(e,f){var g=true;return{stop:function(h){},isAnimated:function(){return g},proxyCallback:function(){g=false;Ext.callback(e,f)}}};return{scroll:function(h,f,j,k,e,g){var i=d(e,g);h=Ext.getDom(h);if(typeof f.scroll.to[0]=="number"){h.scrollLeft=f.scroll.to[0]}if(typeof f.scroll.to[1]=="number"){h.scrollTop=f.scroll.to[1]}i.proxyCallback();return i},motion:function(h,f,i,j,e,g){return this.run(h,f,i,j,e,g)},color:function(h,f,j,k,e,g){var i=d(e,g);i.proxyCallback();return i},run:function(g,q,j,p,h,s,r){var l=d(h,s),m=Ext.fly(g,"_animrun");var f={};for(var i in q){switch(i){case"points":var n,u;m.position();if(n=q.points.by){var t=m.getXY();u=m.translatePoints([t[0]+n[0],t[1]+n[1]])}else{u=m.translatePoints(q.points.to)}f.left=u.left;f.top=u.top;if(!parseInt(m.getStyle("left"),10)){m.setLeft(0)}if(!parseInt(m.getStyle("top"),10)){m.setTop(0)}if(q.points.from){m.setXY(q.points.from)}break;case"width":f.width=q.width.to;if(q.width.from){m.setWidth(q.width.from)}break;case"height":f.height=q.height.to;if(q.height.from){m.setHeight(q.height.from)}break;case"opacity":f.opacity=q.opacity.to;if(q.opacity.from){m.setOpacity(q.opacity.from)}break;case"left":f.left=q.left.to;if(q.left.from){m.setLeft(q.left.from)}break;case"top":f.top=q.top.to;if(q.top.from){m.setTop(q.top.from)}break;case"callback":case"scope":case"xy":break;default:f[i]=q[i].to;if(q[i].from){m.setStyle(i,q[i].from)}break}}jQuery(g).animate(f,j*1000,undefined,l.proxyCallback);return l}}}();Ext.lib.Region=function(f,g,d,e){this.top=f;this[1]=f;this.right=g;this.bottom=d;this.left=e;this[0]=e};Ext.lib.Region.prototype={contains:function(d){return(d.left>=this.left&&d.right<=this.right&&d.top>=this.top&&d.bottom<=this.bottom)},getArea:function(){return((this.bottom-this.top)*(this.right-this.left))},intersect:function(h){var f=Math.max(this.top,h.top);var g=Math.min(this.right,h.right);var d=Math.min(this.bottom,h.bottom);var e=Math.max(this.left,h.left);if(d>=f&&g>=e){return new Ext.lib.Region(f,g,d,e)}else{return null}},union:function(h){var f=Math.min(this.top,h.top);var g=Math.max(this.right,h.right);var d=Math.max(this.bottom,h.bottom);var e=Math.min(this.left,h.left);return new Ext.lib.Region(f,g,d,e)},constrainTo:function(d){this.top=this.top.constrain(d.top,d.bottom);this.bottom=this.bottom.constrain(d.top,d.bottom);this.left=this.left.constrain(d.left,d.right);this.right=this.right.constrain(d.left,d.right);return this},adjust:function(f,e,d,g){this.top+=f;this.left+=e;this.right+=g;this.bottom+=d;return this}};Ext.lib.Region.getRegion=function(g){var i=Ext.lib.Dom.getXY(g);var f=i[1];var h=i[0]+g.offsetWidth;var d=i[1]+g.offsetHeight;var e=i[0];return new Ext.lib.Region(f,h,d,e)};Ext.lib.Point=function(d,e){if(Ext.isArray(d)){e=d[1];d=d[0]}this.x=this.right=this.left=this[0]=d;this.y=this.top=this.bottom=this[1]=e};Ext.lib.Point.prototype=new Ext.lib.Region();if(Ext.isIE){function a(){var d=Function.prototype;delete d.createSequence;delete d.defer;delete d.createDelegate;delete d.createCallback;delete d.createInterceptor;window.detachEvent("onunload",a)}window.attachEvent("onunload",a)}})();