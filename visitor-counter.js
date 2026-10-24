/* Agent Stopover: account-free, approximate browser session counters.
   Public third-party aggregate counters; no cookies, identifiers or IPs stored here.
   Agents that do not execute JavaScript are NOT counted. Classification is heuristic. */
(()=>{"use strict";
const base="https://countapi.mileshilliard.com/api/v1/";
const prefix="chapelgate_agent_stopover_20261024_";
const ua=navigator.userAgent||"";
const declared=new URLSearchParams(location.search).get("visitor")==="agent";
const agent=declared||/\b(bot|crawler|spider|headless|playwright|puppeteer|selenium|lighthouse|gptbot|chatgpt|claudebot|googlebot|bingbot)\b/i.test(ua);
const group=agent?"agent_browser":"regular_browser";
const facility=(location.pathname.split("/").pop()||"index.html").replace(/[^a-z0-9.-]/gi,"_");
const facilityKey=prefix+"facility_"+facility.replace(".html","")+"_"+group;
try{const marker="stopover_facility_"+facilityKey;if(!sessionStorage.getItem(marker)){sessionStorage.setItem(marker,"1");fetch(base+"hit/"+facilityKey,{cache:"no-store"}).catch(()=>{});}}catch(e){}
const key=prefix+group;
const sessionKey="stopover_counted_"+group;
const update=()=>{
const total=document.getElementById("visitor-total");
const human=document.getElementById("visitor-browser");
const bots=document.getElementById("visitor-agent");
if(!total&&!human&&!bots)return;
Promise.all(["regular_browser","agent_browser"].map(k=>fetch(base+"get/"+prefix+k,{cache:"no-store"}).then(r=>r.ok?r.json():{value:0}).then(d=>Number(d.value)||0).catch(()=>null))).then(([a,b])=>{
if(human)human.textContent=a===null?"Unavailable":a.toLocaleString();
if(bots)bots.textContent=b===null?"Unavailable":b.toLocaleString();
if(total)total.textContent=a===null||b===null?"Unavailable":(a+b).toLocaleString();
});
};
try{if(!sessionStorage.getItem(sessionKey)){sessionStorage.setItem(sessionKey,"1");fetch(base+"hit/"+key,{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Counter unavailable");update()}).catch(()=>{sessionStorage.removeItem(sessionKey);update()});}else update();}catch(e){update();}
})();
