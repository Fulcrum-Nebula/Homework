#!/usr/bin/env python3
"""Current-identity regressions for the iota/let and Church authored deltas."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
def entries():
    return {v['entry']['id']: v['entry'] for p in (ROOT/'.SNL_Doc/entries').glob('*.json') for v in [json.loads(p.read_text())]}
class AuthorSemantics(unittest.TestCase):
    def test_surface_let_and_reduction_boundaries(self):
        e=entries()
        for identity, phrase in [('Type.def.utlc-let-expression','presentation syntax'),('Type.ppt.zeta-reduction','no separate'),('Type.ppt.delta-reduction','do not include'),('Type.def.UTLC-const','never captured')]:
            self.assertIn(phrase, e[identity]['content']['markdown']['values']['en'])
    def test_open_closed_distinction(self):
        e=entries()
        self.assertIn('well-scoped',e['Syntax.rmk.closedExpression-UTLC']['content']['markdown']['values']['en'])
        self.assertIn('unchanged',e['Syntax.rmk.freeVariableOpenExpression-UTLC']['content']['markdown']['values']['en'])
    def test_all_bounded_layer_targets_exist(self):
        records=json.loads((ROOT/'scripts/author_content_targets.json').read_text())
        self.assertEqual(len(records),40)
        self.assertEqual(sum(r['layer']=='staged' for r in records),6)
        self.assertEqual(sum(r['layer']=='working' for r in records),17)
        self.assertEqual(sum(r['layer']=='loose' for r in records),17)
        for r in records:
            self.assertTrue(r['currentPaths'])
            for name in r['currentPaths']:
                p=ROOT/name
                self.assertTrue(p.is_file(),(r['oldSource'],r['layer'],name))
                if '/entries/' in name:
                    v=json.loads(p.read_text())['entry']
                    self.assertIn('content',v)
                    self.assertIn('en',v['title']['values'])
                    self.assertIn('zh-CN',v['title']['values'])
    def test_placeholder_truthfulness(self):
        e=entries()
        for identity in ['Type.def.iota-reduction','Lambda.def.let-zeta','Lambda.def.beta-single.recursor']:
            self.assertEqual(e[identity]['content'], {})
    def test_beta_rules_and_strict_transitive_closure(self):
        e=entries(); s=e['Lambda.def.beta-single']['content']['snl']
        for name in ['contract','lambda-congruence','application-left-congruence','application-right-congruence']:
            self.assertIn('Lambda.beta.'+name,s)
        self.assertNotIn('Lambda.beta.application-congruence',s)
        self.assertIn('Syntax.substitution-UTLC',s)
        self.assertIn('Relation.transitiveClosure',e['Lambda.def.beta']['content']['snl'])
        for name in ['betaContraction','lambdaCongruence','applicationFunctionCongruence','applicationArgumentCongruence']:
            self.assertIn('theorem(',e['Lambda.def.beta-single.ctor.'+name]['content']['snl'])
        self.assertNotIn('fvar',e['Syntax.def.expression-UTLC']['content']['snl'])
        self.assertIn('Syntax.Expr-UTLC.fvar',e['Syntax.def.openExpression-UTLC']['content']['snl'])
    def test_current_topology_and_notation_sources(self):
        doc=ROOT/'.SNL_Doc'
        g=json.loads((doc/'libraries/Type_Theory/graph.json').read_text())
        ids={n['id']:n['props']['entryId'] for n in g['nodes']}
        def children(parent):
            return [ids[r['to']] for r in g['relationships'] if r['label']=='branch' and ids[r['from']]==parent]
        inductive=children('Type.subsec.inductive-def')
        self.assertEqual(inductive[inductive.index('Type.def.recursor')+1],'Type.def.iota-reduction')
        design=children('Type.subsec.UTLC-design')
        self.assertEqual(design[design.index('Type.def.utlc-let-expression')+1],'Type.ppt.zeta-reduction')
        self.assertIn('Mathematician.ctxt.alonzoChurch',children('Type.subsec.Church'))
        self.assertIn('Syntax.def.openExpression-UTLC.ctor.freeVariable',children('Syntax.def.openExpression-UTLC'))
        beta=children('Lambda.def.beta-single')
        want=['Lambda.def.beta-single.ctor.'+n for n in ['betaContraction','lambdaCongruence','applicationFunctionCongruence','applicationArgumentCongruence']]+['Lambda.def.beta-single.recursor']
        self.assertEqual([x for x in beta if x in want],want)
        macros={v['macro']['name']:v['macro'] for p in (doc/'macros').glob('*.json') for v in [json.loads(p.read_text())]}
        self.assertIn('MathematicianTerms',json.loads((doc/'config.json').read_text())['active_macro_packages'])
        for name,source in [('Mathematician.alonzoChurch','Mathematician.ctxt.alonzoChurch'),('Syntax.Expr-UTLC.fvar','Syntax.def.openExpression-UTLC.ctor.freeVariable'),('Syntax.substitution-UTLC','Syntax.def.substitution-UTLC'),('Relation.transitiveClosure','Lambda.def.beta')]:
            self.assertEqual(macros[name]['source']['entries'],[source])
        self.assertIn('阿隆佐·邱奇',json.dumps(macros['Mathematician.alonzoChurch'],ensure_ascii=False))
        self.assertEqual(macros['Syntax.substitution-UTLC']['styles'][0]['template']['body'],r'#0[#1 \mapsto #2]')
    def test_church_bilingual_biography(self):
        e=entries()['Mathematician.ctxt.alonzoChurch']
        self.assertEqual(e['package'],'Mathematicians')
        self.assertEqual(set(e['content']['markdown']['values']),{'en','zh-CN'})
        self.assertIn('Church–Turing',e['content']['markdown']['values']['en'])
if __name__=='__main__': unittest.main()
