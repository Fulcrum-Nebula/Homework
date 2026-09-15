#!/usr/bin/env python3
"""Portable public-Toolkit controls carried forward from retired migration probes.
No old checkout, migration receipt, or synthetic native AST is an oracle.
Run: python3 scripts/test_author_convergence.py /absolute/dist/cli/snl.mjs
"""
import copy
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = pathlib.Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 else None

def digest(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and p.name != '.data-write.lock'}

class PublicAuthorControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='snl-author-')
        self.root = pathlib.Path(self.temp.name)
        shutil.copytree(ROOT / '.SNL_Doc', self.root / '.SNL_Doc')
    def tearDown(self):
        self.temp.cleanup()
    def cli(self, *args, value=None):
        cmd = ['node', str(CLI), *args, '--root', str(self.root), '--json']
        if value is not None:
            cmd += ['--input', '-']
        p = subprocess.run(cmd, input=json.dumps(value) if value is not None else None,
                           text=True, capture_output=True, timeout=90)
        data = json.loads(p.stdout)
        self.assertEqual(p.returncode == 0, data['ok'], p.stderr)
        return data
    def get(self, kind, identity):
        r = self.cli(kind, 'get', identity)
        self.assertTrue(r['ok'], r)
        return r['data']['entity']
    def reject_mutation(self, relative, mutate):
        p = self.root / relative
        v = json.loads(p.read_text()); mutate(v); p.write_text(json.dumps(v))
        before = digest(self.root / '.SNL_Doc')
        result = self.cli('validate')
        self.assertFalse(result['ok'], result)
        self.assertEqual(before, digest(self.root / '.SNL_Doc'))
    def test_unknown_entry_field_roundtrip_and_stale_cas(self):
        # file-schema-probe used probe_extension as its whole-file-upgrade sentinel.
        old = self.get('entry', 'Algebra.ctxt.G')
        value = copy.deepcopy(old['value'])
        value['x_author_probe'] = {'sentinel': 'whole-file-upgrade', 'ordered': ['first', 'second']}
        result = self.cli('entry', 'update', old['id'], '--if-match', old['revision'], value=value)
        self.assertTrue(result['ok'], result)
        readback = self.get('entry', old['id'])
        self.assertEqual(value, readback['value'])
        before = digest(self.root / '.SNL_Doc')
        stale = self.cli('entry', 'update', old['id'], '--if-match', old['revision'], value=old['value'])
        self.assertFalse(stale['ok'], stale)
        self.assertEqual(before, digest(self.root / '.SNL_Doc'))
    def test_style_order_locales_typst_and_unknown_fields_survive_cas(self):
        old = self.get('macro', 'FulcrumsMathNotes::def')
        value = copy.deepcopy(old['value']); value['x_author_probe'] = 'style-preservation'
        result = self.cli('macro', 'update', old['id'], '--if-match', old['revision'], value=value)
        self.assertTrue(result['ok'], result)
        self.assertEqual(value, self.get('macro', old['id'])['value'])
        self.assertGreater(len(value['styles']), 1)
        self.assertIn('x_fulcrum_typst', value)
    def test_list_locale_separator_regression(self):
        # The old migration probe accidentally changed 中文 separator to ', '.
        value = self.get('macro', 'FulcrumsMathNotes::__list__')['value']
        styles = {s['style_name']: s['template'] for s in value['styles']}
        def check(templates):
            self.assertEqual(templates['localized_default']['values']['en']['separator'], ', ')
            self.assertEqual(templates['localized_default']['values']['zh-CN']['separator'], '、')
            self.assertEqual(templates['zh_CN']['separator'], '、')
        check(styles)
        mutant = copy.deepcopy(styles)
        mutant['zh_CN']['separator'] = ', '
        with self.assertRaises(AssertionError):
            check(mutant)
        # Mutation changes the oracle input, never the maintained catalog.
        check(styles)
    def test_missing_entry_schema_rejected(self):
        p = next((self.root / '.SNL_Doc/entries').glob('*.json'))
        self.reject_mutation(str(p.relative_to(self.root)), lambda v: v.pop('schema_version'))
    def test_missing_macro_schema_rejected(self):
        p = next((self.root / '.SNL_Doc/macros').glob('*.json'))
        self.reject_mutation(str(p.relative_to(self.root)), lambda v: v.pop('schema_version'))
    def test_retired_partial_kind_rejected(self):
        p = next((self.root / '.SNL_Doc/macros').glob('*.json'))
        self.reject_mutation(str(p.relative_to(self.root)), lambda v: v['macro'].__setitem__('kind', 'partial'))
    def test_duplicate_style_identity_rejected(self):
        p = next((self.root / '.SNL_Doc/macros').glob('*.json'))
        self.reject_mutation(str(p.relative_to(self.root)), lambda v: v['macro']['styles'].append(copy.deepcopy(v['macro']['styles'][0])))
    def test_dangling_relationship_rejected(self):
        result = self.cli('relationship', 'list')
        self.assertTrue(result['ok'], result)
        old = result['data']['entities'][0]
        value = copy.deepcopy(old['value'])
        # Discover actual endpoint fields, never assert rejection of an unrelated envelope.
        key = 'source' if 'source' in value else 'from'
        self.assertIn(key, value)
        value[key] = 'AuthorConvergence.nonexistent'
        before = digest(self.root / '.SNL_Doc')
        result = self.cli('relationship', 'update', old['id'], '--if-match', old['revision'], value=value)
        self.assertFalse(result['ok'], result)
        self.assertEqual(before, digest(self.root / '.SNL_Doc'))

if __name__ == '__main__':
    if CLI is None:
        raise SystemExit('Pass the official Toolkit CLI path')
    unittest.main()
