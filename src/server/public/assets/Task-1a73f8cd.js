import{_ as N,c as S,o as a,p as D,a as b,b as T,s as x,u as w,d as i,e as C,f as B,r as m,g as v,w as h,T as y,h as l,i as g}from"./index-ac1dbb22.js";import{C as I,D as j}from"./DecisionNode-89ad19b5.js";import"./index-8ac73e8f.js";const O={name:"LoadingSpinner",setup(){return{}}},$="/img/loading_spinner.svg";const E=t=>(D("data-v-8a68a305"),t=t(),b(),t),M={class:"loadingLayer"},R=E(()=>T("img",{class:"loadingSpinner",src:$},null,-1)),V=[R];function G(t,r,s,e,n,c){return a(),S("div",M,V)}const P=N(O,[["render",G],["__scopeId","data-v-8a68a305"]]),F={name:"Task",components:{Canvas:I,DecisionNode:j,LoadingSpinner:P},setup(){const t=x.taskStore,{store:r,getProperty:s,setProperty:e}=t,n=w(),c=i(()=>s("currentNode")),d=i(()=>{const o=s(`edges__${c.value}`);return o?o.length>1:!1}),_=i(()=>s("isLoading")),p=i(()=>s("restoredFromReplay"));typeof n.params.task=="string"&&!p.value&&(e({path:"currentTask",value:n.params.task}),r.dispatch("fetchTaskGraph",{task:n.params.task}));const L=50;let f=new Date().getTime();const k=o=>{o.preventDefault();const u=new Date().getTime();o.target,!(u-f<L)&&(r.dispatch("trackMouse",{x:o.pageX,y:o.pageY,timestamp:u}),f=u)};return C(()=>{document.addEventListener("mousemove",k)}),B(()=>{document.removeEventListener("mousemove",k)}),{currentNode:c,isDecisionNode:d,taskStore:t,isLoading:_}}};const U={class:"task"};function X(t,r,s,e,n,c){const d=m("LoadingSpinner"),_=m("DecisionNode"),p=m("Canvas");return a(),S("div",U,[v(y,{name:"fade"},{default:h(()=>[e.isLoading?(a(),l(d,{key:0})):g("",!0)]),_:1}),v(y,{name:"slidedown"},{default:h(()=>[e.isDecisionNode?(a(),l(_,{storeObject:e.taskStore,key:e.currentNode},null,8,["storeObject"])):g("",!0)]),_:1}),!e.isDecisionNode&&!e.isLoading?(a(),l(p,{key:e.currentNode,storeObject:e.taskStore},null,8,["storeObject"])):g("",!0)])}const A=N(F,[["render",X],["__scopeId","data-v-1b3726b0"]]);export{A as default};