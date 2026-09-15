"""Executable characterization of both imported audit capabilities, no old checkout needed."""
import json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run_audit(kind,data,core,mode='identity'):
    with tempfile.TemporaryDirectory(prefix='notes-semantic-audit-') as d:
        inp,out=Path(d)/'input.json',Path(d)/'output.json'
        inp.write_text(json.dumps(data))
        p=subprocess.run(['node',str(ROOT/'scripts'/('audit_'+kind+'_semantics.mjs')),str(inp),str(out),str(core),mode],text=True,capture_output=True,timeout=120)
        if inp.read_text()!=json.dumps(data): raise AssertionError('Audit mutated its input')
        if not out.exists(): raise AssertionError(p.stderr)
        return p.returncode,json.loads(out.read_text())
class SemanticAudits(unittest.TestCase):
    def test_donor_capabilities(self):
        core=Path(os.environ['SNL_BASICS_CORE'])
        # Current real catalog drives resolution; no mocked parser/resolver.
        macros=[json.loads(p.read_text())['macro'] for p in (ROOT/'.SNL_Doc/macros').glob('*.json')]
        fixture={'macros':macros,'entries':[{'id':'binding','title':'def-struct reference','content':{'snl':'def-hyp(Type.annotation(@x,Nat),Eq(,x,x))'}},{'id':'empty','content':{'snl':'def-hyp(,Nat)'}},{'id':'bare','content':{'snl':'def'}}]}
        rc,census=run_audit('decl',fixture,core)
        self.assertEqual(rc,0,census)
        self.assertEqual(census['counts']['def-hyp']['total'],2)
        self.assertEqual(census['counts']['def']['forms'],{'0/<implicit>':1})
        self.assertTrue(census['strings'])
        self.assertIn('diags',census); self.assertIn('special',census)
        # Identity roundtrip checks full AST, all node kinds, local binding paths,
        # diagnostics, and external source identities using the current parser.
        rc,binding=run_audit('binding',fixture,core)
        self.assertEqual(rc,0,binding)
        self.assertGreater(binding['bindings'],0)
        self.assertGreater(binding['totalNodes'],0)
        self.assertTrue(binding['nodeKinds'])
        # Historical proposal remains a diagnostic experiment, not a success oracle.
        rc,proposal=run_audit('binding',fixture,core,'legacy-proposal')
        self.assertEqual(proposal['wrappers'],2)
        self.assertIn('empty',proposal['emptyH'])
        self.assertTrue(proposal['samples'])
        self.assertEqual(rc, bool(proposal['failures']))
        # Parse failures must retain the Entry identity and allow later entries.
        broken={'macros':macros,'entries':[{'id':'broken','content':{'snl':'def('}},fixture['entries'][0]]}
        rc,bad=run_audit('binding',broken,core)
        self.assertEqual(rc,1)
        self.assertIn('broken',[f['id'] for f in bad['failures']])
        self.assertEqual(bad['checked'],2)
        rc,bad=run_audit('decl',broken,core)
        self.assertEqual(rc,1)
        self.assertIn('broken',[f['id'] for f in bad['errors']])
    def test_binding_oracles_reject_resolver_mutations(self):
        core=Path(os.environ['SNL_BASICS_CORE'])
        macros=[json.loads(p.read_text())['macro'] for p in (ROOT/'.SNL_Doc/macros').glob('*.json')]
        fixture={'macros':macros,'entries':[{'id':'oracle','content':{'snl':
            'variable(Type.annotation(@x,Nat),Eq(,x,V@LinearAlgebra.ctxt.vectorSpace))'}}]}
        mutations={
            'kind': "r.tree.kind='mutant'",
            'diagnostics': "r.diagnostics.push({code:'mutant',message:'mutant'})",
            'entry source': "nodes.find(n=>n.source&&n.source.type!=='tree_path').source={type:'mutant',id:'wrong'}",
            'binding': "nodes.find(n=>n.source?.type==='tree_path').source.path=[999]",
            'postfix': "nodes.find(n=>n.postfix).postfix={mutant:true}"}
        with tempfile.TemporaryDirectory(prefix='notes-oracle-mutants-') as d:
            for reason,mutation in mutations.items():
                shim=Path(d)/'core.mjs'
                shim.write_text('import * as core from '+json.dumps(core.as_uri())+';\n'
                    'export const parseSnlSyntaxTree=core.parseSnlSyntaxTree, serializeSnlSyntaxTree=core.serializeSnlSyntaxTree;\n'
                    'let calls=0; export function resolveSnlSemantics(...args){const r=core.resolveSnlSemantics(...args);'
                    'if(++calls%2===0){const nodes=[];function walk(n){nodes.push(n);n.children.forEach(walk)}walk(r.tree);'
                    +mutation+';}return r;}')
                rc,result=run_audit('binding',fixture,shim)
                self.assertEqual(rc,1,(reason,result))
                failures=[f for f in result['failures'] if f['reason']==reason]
                self.assertTrue(failures,(reason,result))
                self.assertIn('before',failures[0]);self.assertIn('after',failures[0])

    def test_full_binding_witnesses_and_failure_payloads(self):
        core=Path(os.environ['SNL_BASICS_CORE'])
        with tempfile.TemporaryDirectory(prefix='notes-audit-guards-') as d:
            inp=Path(d)/'input.json';inp.write_text('{"entries":[],"macros":[]}')
            link=Path(d)/'hardlink.json';os.link(inp,link)
            canonical=Path(d)/'.SNL_Doc';canonical.mkdir()
            for kind in ['decl','binding']:
                for output in [inp,link,canonical/'report.json']:
                    p=subprocess.run(['node',str(ROOT/'scripts'/('audit_'+kind+'_semantics.mjs')),str(inp),str(output),str(core)],capture_output=True,text=True)
                    self.assertNotEqual(p.returncode,0)
                    self.assertIn('Audit output must not overwrite',p.stderr)
                    self.assertEqual(inp.read_text(),'{"entries":[],"macros":[]}')
            self.assertFalse((canonical/'report.json').exists())
        core=Path(os.environ['SNL_BASICS_CORE'])
        macros=[json.loads(p.read_text())['macro'] for p in (ROOT/'.SNL_Doc/macros').glob('*.json')]
        entries=[json.loads(p.read_text())['entry'] for p in (ROOT/'.SNL_Doc/entries').glob('LinearAlgebra-*.json')]
        fixture={'macros':macros,'entries':entries}
        rc,result=run_audit('binding',fixture,core)
        self.assertEqual(rc,0,result['failures'])
        self.assertEqual(len(result['witnesses']),result['totalNodes'])
        self.assertGreater(result['postfixes'],0)
        external=[w for w in result['witnesses'] if w['source'] and w['source']['type']!='tree_path']
        local=[w for w in result['witnesses'] if w['source'] and w['source']['type']=='tree_path']
        self.assertTrue(external); self.assertTrue(local)
        for w in result['witnesses']:
            self.assertEqual(w['path'],w['mappedPath'])
            self.assertEqual(w['postfix'],w['mappedPostfix'])
            self.assertEqual(w['source'],w['mappedSource'])
        rc,census=run_audit('decl',fixture,core)
        self.assertEqual(rc,0)
        self.assertEqual(len(census['diagnostics']),sum(bool(e.get('content',{}).get('snl','').strip()) for e in entries))
        broken={'macros':macros,'entries':[{'id':'broken','content':{'snl':'def('}},entries[0]]}
        for kind,key in [('decl','errors'),('binding','failures')]:
            rc,bad=run_audit(kind,broken,core)
            self.assertEqual(rc,1)
            error=next(f for f in bad[key] if f['id']=='broken')
            self.assertEqual(error['original'],'def(')
            self.assertTrue(error['stack'])

if __name__=='__main__': unittest.main()
