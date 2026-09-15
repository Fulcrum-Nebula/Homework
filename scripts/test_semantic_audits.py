"""Executable characterization of both imported audit capabilities, no old checkout needed."""
import json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run_audit(kind,data,core,mode='identity'):
    with tempfile.TemporaryDirectory(prefix='notes-semantic-audit-') as d:
        inp,out=Path(d)/'input.json',Path(d)/'output.json'
        inp.write_text(json.dumps(data))
        p=subprocess.run(['node',str(ROOT/'scripts'/('audit_'+kind+'_semantics.mjs')),str(inp),str(out),str(core),mode],text=True,capture_output=True,timeout=120)
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
if __name__=='__main__': unittest.main()
