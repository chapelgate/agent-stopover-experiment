"use strict";
(function(root){
const catalogue=[
["json-format","JSON validator & formatter","Parse and pretty-print JSON.",'{"hello":"agent","count":2}'],
["json-minify","JSON minifier","Remove unnecessary whitespace.",'{ "hello": "agent" }'],
["json-compare","JSON structural comparison","Compare two JSON values ignoring object key order.",'{"a":1,"b":[2,3]}','{"b":[2,3],"a":1}'],
["json-keys","JSON structure inspector","Summarise top-level type, keys and size.",'{"a":1,"b":[2,3]}'],
["json-to-csv","JSON array to CSV","Convert a flat array of objects to CSV.",'[{"name":"A","score":3},{"name":"B","score":4}]'],
["csv-to-json","CSV to JSON","Parse a simple CSV table into an array of objects.",'name,score\nA,3\nB,4'],
["csv-summary","CSV inspector","Summarise column names and row counts.",'name,score\nA,3\nB,4'],
["text-stats","Text statistics","Count characters, words, lines and bytes.","Hello visiting agent!"],
["text-sort","Sort lines","Alphabetically sort non-empty lines.","pear\napple\nbanana"],
["text-unique","Unique lines","Remove duplicate lines, preserving first occurrence.","red\nblue\nred"],
["text-diff","Line comparison","Find additions and removals between two texts.","hello\nold","hello\nnew"],
["url-encode","URL encode","Encode text as a URL component.","hello agent & friends"],
["url-decode","URL decode","Decode a URL component.","hello%20agent%20%26%20friends"],
["base64-encode","Base64 encode","Encode UTF-8 text to Base64.","Hello agent"],
["base64-decode","Base64 decode","Decode Base64 to UTF-8 text.","SGVsbG8gYWdlbnQ="],
["sha256","SHA-256 fingerprint","Compute a SHA-256 digest locally.","public sample"],
["uuid","Random identifier","Generate a random UUID (input ignored).",""],
["timestamp","Time conversion","Convert ISO date/time or Unix milliseconds.",new Date().toISOString()],
["slug","URL slug","Create a simple lowercase URL slug.","Agent Stopover Workshop"],
["html-escape","HTML escape","Escape HTML special characters.","<agent & human>"],
["checklist","Task checklist generator","Turn lines into a Markdown checklist.","Inspect data\nValidate result\nExport report"],
["markdown-table","Markdown table from JSON","Turn a flat JSON object array into a Markdown table.",'[{"name":"A","score":3},{"name":"B","score":4}]']
];
const enc=new TextEncoder();const dec=new TextDecoder("utf-8",{fatal:true});
function equal(a,b){if(a===b)return true;if(!a||!b||typeof a!=="object"||typeof b!=="object"||Array.isArray(a)!==Array.isArray(b))return false;const ak=Object.keys(a),bk=Object.keys(b);return ak.length===bk.length&&ak.every(k=>Object.prototype.hasOwnProperty.call(b,k)&&equal(a[k],b[k]))}
function csvParse(s){const rows=[];let row=[],cell="",quoted=false;for(let i=0;i<s.length;i++){const c=s[i];if(quoted){if(c==='"'&&s[i+1]==='"'){cell+='"';i++}else if(c==='"')quoted=false;else cell+=c}else if(c==='"'){if(cell!=="")throw Error("Unexpected quote in CSV");quoted=true}else if(c===","){row.push(cell);cell=""}else if(c==="\n"){row.push(cell);rows.push(row);row=[];cell=""}else if(c==="\r"){if(s[i+1]==="\n")i++;row.push(cell);rows.push(row);row=[];cell=""}else cell+=c}if(quoted)throw Error("Unclosed CSV quote");if(cell!==""||row.length){row.push(cell);rows.push(row)}return rows.filter(r=>r.some(v=>v!==""))}
function csvQuote(s){s=String(s??"");return /[",\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}
function flatRows(v){if(!Array.isArray(v)||v.some(x=>!x||typeof x!=="object"||Array.isArray(x)))throw Error("Expected an array of objects");const keys=[...new Set(v.flatMap(Object.keys))];return {keys,rows:v.map(x=>keys.map(k=>x[k]===undefined?"":typeof x[k]==="object"?JSON.stringify(x[k]):String(x[k]))) }}
function b64(bytes){let binary="";for(const x of bytes)binary+=String.fromCharCode(x);return btoa(binary)}
function unb64(s){const bytes=Uint8Array.from(atob(s.trim()),c=>c.charCodeAt(0));return dec.decode(bytes)}
function htmlEscape(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}
function lines(s){return s.split(/\r?\n/)}
function mdCell(s){return String(s).replace(/\|/g,"\\|").replace(/\r?\n/g," ")}
async function execute(id,s,t){let x,y,tab;switch(id){
case"json-format":return JSON.stringify(JSON.parse(s),null,2);
case"json-minify":return JSON.stringify(JSON.parse(s));
case"json-compare":return JSON.stringify({equivalent:equal(JSON.parse(s),JSON.parse(t)),object_key_order_ignored:true,array_order_preserved:true},null,2);
case"json-keys":x=JSON.parse(s);return JSON.stringify({type:Array.isArray(x)?"array":x===null?"null":typeof x,keys:x&&typeof x==="object"&&!Array.isArray(x)?Object.keys(x):undefined,length:Array.isArray(x)?x.length:undefined},null,2);
case"json-to-csv":tab=flatRows(JSON.parse(s));return [tab.keys,...tab.rows].map(row=>row.map(csvQuote).join(",")).join("\n");
case"csv-to-json":x=csvParse(s);if(!x.length)return"[]";if(x.slice(1).some(row=>row.length!==x[0].length))throw Error("Inconsistent column count");return JSON.stringify(x.slice(1).map(row=>Object.fromEntries(x[0].map((k,i)=>[k,row[i]]))),null,2);
case"csv-summary":x=csvParse(s);return JSON.stringify({columns:x[0]||[],data_rows:Math.max(0,x.length-1),consistent_columns:x.every(r=>r.length===x[0].length)},null,2);
case"text-stats":return JSON.stringify({characters:[...s].length,words:s.trim()?s.trim().split(/\s+/u).length:0,lines:lines(s).length,utf8_bytes:enc.encode(s).length},null,2);
case"text-sort":return lines(s).filter(Boolean).sort((a,b)=>a.localeCompare(b)).join("\n");
case"text-unique":return [...new Set(lines(s).filter(Boolean))].join("\n");
case"text-diff":x=new Set(lines(s));y=new Set(lines(t));return JSON.stringify({removed:[...x].filter(z=>!y.has(z)),added:[...y].filter(z=>!x.has(z)),note:"Line membership comparison, not positional diff"},null,2);
case"url-encode":return encodeURIComponent(s);
case"url-decode":return decodeURIComponent(s);
case"base64-encode":return b64(enc.encode(s));
case"base64-decode":return unb64(s);
case"sha256":if(!crypto.subtle)throw Error("Secure browser context required");x=await crypto.subtle.digest("SHA-256",enc.encode(s));return [...new Uint8Array(x)].map(v=>v.toString(16).padStart(2,"0")).join("");
case"uuid":if(!crypto.randomUUID)throw Error("Secure browser context required");return crypto.randomUUID();
case"timestamp":x=/^\d{10,13}$/.test(s.trim())?new Date(Number(s.trim())*(s.trim().length===10?1000:1)):new Date(s.trim());if(Number.isNaN(x.getTime()))throw Error("Invalid date or timestamp");return JSON.stringify({iso:x.toISOString(),unix_seconds:Math.floor(x.getTime()/1000),unix_milliseconds:x.getTime()},null,2);
case"slug":return s.toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
case"html-escape":return htmlEscape(s);
case"checklist":return lines(s).filter(v=>v.trim()).map(v=>"- [ ] "+v.trim()).join("\n");
case"markdown-table":tab=flatRows(JSON.parse(s));return "| "+tab.keys.map(mdCell).join(" | ")+" |\n| "+tab.keys.map(()=>"---").join(" | ")+" |\n"+tab.rows.map(row=>"| "+row.map(mdCell).join(" | ")+" |").join("\n");
default:throw Error("Unknown tool")}}
root.AgentStopoverTools=Object.freeze({execute,entries:catalogue,catalogue:catalogue.map(x=>({id:x[0],name:x[1],description:x[2],example:x[3]||"",secondExample:x[4]||""}))});
})(typeof window!=="undefined"?window:globalThis);
