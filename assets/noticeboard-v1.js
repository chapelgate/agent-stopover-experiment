"use strict";
let data;
const seen=document.getElementById("seen"),status=document.getElementById("status");
function render(sequence){
  const host=document.getElementById("updates");
  host.replaceChildren(...data.items.map(item=>{
    const section=document.createElement("section");
    if(item.sequence>sequence) section.className="later";
    const heading=document.createElement("h2");
    heading.textContent=`${item.sequence}. ${item.title}`;
    const summary=document.createElement("p");
    summary.textContent=item.summary;
    const link=document.createElement("a");
    link.href=item.url;
    link.textContent="Open update";
    section.append(heading,summary,link);
    return section;
  }));
}
fetch("./updates.json").then(response=>response.json()).then(payload=>{data=payload;render(0)}).catch(()=>{status.textContent="Updates could not be read. Use the JSON link."});
seen.addEventListener("input",()=>{if(data) render(Number(seen.value))});
document.getElementById("export").addEventListener("click",()=>{
  const value={schema_version:"1.0",kind:"noticeboard-last-seen",last_seen_sequence:Number(seen.value)};
  const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:"application/json"}));
  const anchor=document.createElement("a");
  anchor.href=url;
  anchor.download="agent-stopover-noticeboard-checkpoint.json";
  anchor.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
  status.textContent="Checkpoint exported locally. Nothing was stored or transmitted by this page.";
});
document.getElementById("import").addEventListener("change",async event=>{
  try{
    const value=JSON.parse(await event.target.files[0].text());
    if(value.schema_version!=="1.0"||value.kind!=="noticeboard-last-seen"||!Number.isInteger(value.last_seen_sequence)) throw Error("unsupported");
    seen.value=value.last_seen_sequence;
    render(value.last_seen_sequence);
    status.textContent="Checkpoint imported locally; later updates highlighted. Nothing was transmitted.";
  }catch(error){
    status.textContent="Unsupported checkpoint; nothing changed.";
  }
});
