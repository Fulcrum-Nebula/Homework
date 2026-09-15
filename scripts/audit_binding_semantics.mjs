// Read-only audit: the legacy-proposal mode is research, never migration authority.
import fs from 'node:fs';
import {isDeepStrictEqual} from 'node:util';
import {pathToFileURL} from 'node:url';
const [input, output, core, mode='identity'] = process.argv.slice(2);
if (!input || !output || !core || !['identity','legacy-proposal'].includes(mode)) throw new Error('Usage: input.json output.json /maintained/Basics/dist-lib/core.js [identity|legacy-proposal]');
const {parseSnlSyntaxTree:parse,resolveSnlSemantics:resolve,serializeSnlSyntaxTree:serialize}=await import(pathToFileURL(core).href);
const data=JSON.parse(fs.readFileSync(input,'utf8'));
const oldCat=Object.fromEntries(data.macros.map(m=>[m.name,m]));
let newCat={...oldCat,variable:{...oldCat.def,name:'variable'},theorem:{...oldCat['thm-hyp'],name:'theorem'},inductive:{...oldCat['def-inductive'],name:'inductive'},structure:{...oldCat['def-struct'],name:'structure'}};
if(mode==='legacy-proposal') newCat.def={...oldCat.def,styles:[...oldCat.def.styles,{style_name:'declaration',tags:[],template:{mode:'text',body:'Define #0.'}}]};
const family={'def-hyp':'def','def-hyp-opq':'def','def-notation-hyp':'def','thm-hyp':'theorem','def-inductive-hyp':'inductive','def-struct-hyp':'structure'};
const rename={'def-inductive':'inductive','def-struct':'structure','def-notation':'def'};
if(mode==='identity'){newCat=oldCat;for(const k of Object.keys(family))delete family[k];for(const k of Object.keys(rename))delete rename[k];}
function walk(n,f,p=[]){f(n,p);n.children.forEach((c,i)=>walk(c,f,[...p,i]));}
function at(t,p){return p.reduce((t,i)=>t.children[i],t)}
let checked=0,transformed=0,totalNodes=0,bindings=0,postfixes=0,wrappers=0;const failures=[],samples=[],nodeKinds={},emptyH=[];
for(const e of data.entries){const text=e.content?.snl;if(typeof text!=='string'||!text.trim())continue;checked++;
try {
const before=parse(text),origins=new WeakMap(),oldToNew=new Map(); let changes=0;
function trans(n,p=[]){const children=n.children.map((c,i)=>trans(c,[...p,i]));let c={...n,children};let name=n.macro_name;if(!n.env_mode&&Object.hasOwn(family,name)){changes++;wrappers++;if(!children[0]?.macro_name)emptyH.push(e.id);c.macro_name=family[name];c.children=children.slice(1);if(name==='def-hyp-opq')c.style_name='declaration';if(name==='def-notation-hyp')c.style_name='notation';origins.set(c,p);return {macro_name:'variable',kind:'',mdata:null,children:[children[0],c]};}if(!n.env_mode&&Object.hasOwn(rename,name)){changes++;c.macro_name=rename[name];if(name==='def-notation')c.style_name='notation';}origins.set(c,p);return c;}
const after=trans(before);walk(after,(n,p)=>{if(origins.has(n))oldToNew.set(JSON.stringify(origins.get(n)),p)});
walk(after,(n,p)=>{if(n.env_mode)n.macro_name='#'+p.join('.');});
if(changes)transformed++;
const serialTree=structuredClone(after);walk(serialTree,n=>{if(n.binder_explicit&&!n.postfix&&n.binder_name===(n.temporary_source??n.macro_name))delete n.binder_name;});let reparse;try { reparse=parse(serialize(serialTree)); }catch(err){failures.push({id:e.id,reason:'serialize-parse',error:String(err),serialized:serialize(after),original:text});reparse=after;}
if(!isDeepStrictEqual(after,reparse)){const diffs=[];function diff(x,y,p=[]){if(isDeepStrictEqual(x,y))return;if(x&&y&&typeof x==='object'&&typeof y==='object'){for(const k of new Set([...Object.keys(x),...Object.keys(y)]))diff(x[k],y[k],[...p,k]);}else diffs.push({path:p,before:x,after:y});}diff(after,reparse);failures.push({id:e.id,reason:'syntax-roundtrip',diffs});}
const a=resolve(before,oldCat),b=resolve(reparse,newCat);
if(JSON.stringify(a.diagnostics)!==JSON.stringify(b.diagnostics))failures.push({id:e.id,reason:'diagnostics',before:a.diagnostics,after:b.diagnostics});
walk(a.tree,(n,p)=>{totalNodes++;nodeKinds[n.kind]=(nodeKinds[n.kind]||0)+1;const np=oldToNew.get(JSON.stringify(p));const m=at(b.tree,np);if(n.kind!==m.kind)failures.push({id:e.id,p,np,reason:'kind',before:n.kind,after:m.kind});if(n.source){if(n.source.type==='tree_path'){bindings++;const want=oldToNew.get(JSON.stringify(n.source.path));if(JSON.stringify(want)!==JSON.stringify(m.source?.path))failures.push({id:e.id,p,np,reason:'binding',before:n.source,after:m.source,want});}else if(JSON.stringify(n.source)!==JSON.stringify(m.source))failures.push({id:e.id,p,reason:'entry source'});}if(n.postfix)postfixes++;});
if(changes&&samples.length<4)samples.push({id:e.id,before:text,after:serialize(after)});
} catch(error) {failures.push({id:e.id,reason:'entry-exception',error:String(error),original:text});}
}
console.log(JSON.stringify({checked,transformed,totalNodes,bindings,postfixes,wrappers,nodeKinds,emptyH,failures,samples:samples.map(s=>({id:s.id,before:s.before.slice(0,240),after:s.after.slice(0,240)}))},null,2));
fs.writeFileSync(output,JSON.stringify({checked,transformed,totalNodes,bindings,postfixes,wrappers,nodeKinds,emptyH,failures,samples},null,2));

if(failures.length) process.exitCode=1;
