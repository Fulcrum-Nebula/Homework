// Read-only audit: the legacy-proposal mode is research, never migration authority.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const [input, output, core, mode='identity'] = process.argv.slice(2);
if (!input || !output || !core || !['identity','legacy-proposal'].includes(mode)) throw new Error('Usage: input.json output.json /maintained/Basics/dist-lib/core.js [identity|legacy-proposal]');
const {parseSnlSyntaxTree:parse,resolveSnlSemantics:resolve,serializeSnlSyntaxTree:serialize}=await import(pathToFileURL(core).href);
const data=JSON.parse(fs.readFileSync(input,'utf8'));
const names=['def','def-hyp','def-hyp-opq','def-notation','def-notation-hyp','thm-hyp','def-inductive','def-inductive-hyp','def-struct','def-struct-hyp'];
const catalog=Object.fromEntries(data.macros.map(m=>[m.name,m]));
const uses=[],errors=[],special=[],diags={};
function walk(n,f,p=[]){f(n,p);n.children.forEach((c,i)=>walk(c,f,[...p,i]));}
for(const e of data.entries){
 const snl=e.content?.snl;if(typeof snl!=='string'||!snl.trim())continue;
 try {const tree=parse(snl);const r=resolve(tree,catalog);for(const d of r.diagnostics)diags[d.code]=(diags[d.code]||0)+1;
 walk(tree,(n,p)=>{if(names.includes(n.macro_name)&&!n.env_mode)uses.push({id:e.id,path:p,name:n.macro_name,arity:n.children.length,style:n.style_name??'<implicit>',node:n,snl});if(n.postfix||n.binder_explicit&&n.children.length||n.env_mode&&names.includes(n.macro_name))special.push({id:e.id,path:p,node:n});});
 }catch(err){errors.push({id:e.id,error:String(err)});}
}
const strings=[];function stringsWalk(o,path){if(typeof o==='string'){if(names.some(n=>o.includes(n)))strings.push({path,value:o});}else if(o&&typeof o==='object')for(const[k,v]of Object.entries(o))stringsWalk(v,[...path,k]);}
for(const m of data.macros)stringsWalk(m,['macro',m.name]);
for(const e of data.entries)for(const[k,v]of Object.entries(e))if(k!=='content')stringsWalk(v,['entry',e.id,k]);
const counts=Object.fromEntries(names.map(name=>{let u=uses.filter(u=>u.name===name);return[name,{total:u.length,entries:new Set(u.map(u=>u.id)).size,forms:Object.fromEntries([...new Set(u.map(u=>`${u.arity}/${u.style}`))].map(f=>[f,u.filter(u=>`${u.arity}/${u.style}`===f).length]))}]}));
const result={counts,affectedEntries:new Set(uses.map(u=>u.id)).size,uses,errors,diags,special,strings};
fs.writeFileSync(output,JSON.stringify(result,null,2));
console.log(JSON.stringify({counts,affectedEntries:result.affectedEntries,errors,diags,bare:uses.filter(u=>!u.arity).map(({id,name,style,snl})=>({id,name,style,snl})),postfixes:special.filter(s=>s.node.postfix).map(s=>({id:s.id,path:s.path,postfix:s.node.postfix})),macroTemplateStrings:strings.filter(s=>s.path[0]==='macro'&&s.path.includes('template'))},null,2));

if(errors.length) process.exitCode=1;
