"use strict";
const $=id=>document.getElementById(id);let result="";
const catalogue=AgentStopoverTools.entries;
const execute=AgentStopoverTools.execute;
function refresh(){const d=catalogue.find(x=>x[0]===$("tool").value);$("description").textContent=d[2];$("second-wrap").hidden=!["json-compare","text-diff"].includes(d[0]);}
for(const x of catalogue){const option=document.createElement("option");option.value=x[0];option.textContent=x[1];$("tool").append(option)}$("tool").addEventListener("change",refresh);refresh();
$("example").addEventListener("click",()=>{const d=catalogue.find(x=>x[0]===$("tool").value);$("source").value=d[3]||"";$("second").value=d[4]||"";$("result-status").textContent="Example loaded. Ready to run."});
$("run").addEventListener("click",async()=>{try{const value=await execute($("tool").value,$("source").value,$("second").value);result=String(value);$("output").textContent=result;$("result-status").textContent="Completed locally.";$("copy").disabled=false;$("download").disabled=false}catch(e){result="";$("output").textContent="";$("result-status").textContent="Error: "+(e&&e.message?e.message:"Unable to process input");$("copy").disabled=true;$("download").disabled=true}});
$("clear").addEventListener("click",()=>{$("source").value="";$("second").value="";result="";$("output").textContent="Results will appear here.";$("result-status").textContent="Cleared. Nothing submitted.";$("copy").disabled=true;$("download").disabled=true});
$("copy").addEventListener("click",async()=>{try{await navigator.clipboard.writeText(result);$("result-status").textContent="Copied locally."}catch(e){$("result-status").textContent="Copy unavailable. Select the result text instead."}});
$("download").addEventListener("click",()=>{const url=URL.createObjectURL(new Blob([result],{type:"text/plain;charset=utf-8"}));const a=document.createElement("a");a.href=url;a.download="agent-toolbox-result.txt";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
