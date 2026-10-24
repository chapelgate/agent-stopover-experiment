"use strict";
(()=>{
function clearHash(){history.replaceState(null,"",location.pathname+location.search)}
function apply(){
if(!location.hash.startsWith("#resume="))return;
const encoded=location.hash.slice(8);
try{
if(encoded.length>6000)throw Error("large");
const bytes=Uint8Array.from(atob(encoded.replace(/-/g,"+").replace(/_/g,"/").padEnd(Math.ceil(encoded.length/4)*4,"=")),value=>value.charCodeAt(0));
const value=JSON.parse(new TextDecoder().decode(bytes));
if(!value||typeof value!=="object"||Array.isArray(value)||Object.keys(value).length!==2||typeof value.task_summary!=="string"||typeof value.next_step!=="string"||value.task_summary.length>2000||value.next_step.length>2000)throw Error("invalid");
const main=document.querySelector("main");
[...main.querySelectorAll("section")].forEach(section=>{const heading=section.querySelector("h2");if(heading&&heading.textContent==="Restored checkpoint context")section.remove()});
const section=document.createElement("section"),heading=document.createElement("h2"),summary=document.createElement("p"),next=document.createElement("p");
heading.textContent="Restored checkpoint context";
summary.textContent=`Summary: ${value.task_summary||"None"}`;
next.textContent=`Next step: ${value.next_step||"None"}`;
section.append(heading,summary,next);
main.prepend(section);
clearHash()
}catch(error){clearHash()}
}
apply();
addEventListener("hashchange",apply)
})();
