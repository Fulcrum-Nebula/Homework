"""Independent controls retained from the retired i18n/namespace/topology tools.
Imported by test_author_convergence.py; never imports or runs a legacy writer.
"""
import copy
import json
import math
import hashlib
import os
import stat
from pathlib import Path
import re
from typing import Any


def strict_json(text):
    """JSON text -> value; reject duplicate names and every non-finite number."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('non-finite JSON number: ' + value)
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    def finite(v):
        if isinstance(v, float) and not math.isfinite(v):
            raise ValueError('non-finite JSON number')
        if isinstance(v, dict):
            for child in v.values(): finite(child)
        elif isinstance(v, list):
            for child in v: finite(child)
    finite(value)
    return value


def placeholders(text):
    return tuple(sorted(set(re.findall(r'(?<!\\)#(?:\*|\d+)', text))))


def scan_document_tree(root, *, allow_writer_lock=False):
    """Read-only exact file/dir manifest; reject links and special inodes."""
    files, directories = {}, set()
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            path = Path(directory) / name
            relative = str(path.relative_to(root))
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ValueError('symlink: ' + relative)
            if stat.S_ISDIR(mode):
                directories.add(relative)
            elif stat.S_ISREG(mode):
                if allow_writer_lock and relative == '.data-write.lock':
                    continue
                files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
            else:
                raise ValueError('special inode: ' + relative)
    return files, directories


def expected_directories(files):
    return {str(parent) for name in files for parent in Path(name).parents
            if str(parent) != '.'}


def assert_document_tree(root, files):
    observed, directories = scan_document_tree(root)
    if observed != files or directories != expected_directories(files):
        raise ValueError('document manifest drift')


class AuthorMethodControls:
    """Mixin: self.get/cli/root/reject_mutation use the existing public runner."""
    def test_strict_json_independent_controls(self: Any):
        self.assertEqual(strict_json('{"x":[1,true,null,"中文"]}'), {'x':[1,True,None,'中文']})
        for bad in ['{"x":1,"x":2}', '{"a":{"x":1,"x":2}}', '[NaN]', '[Infinity]', '[-Infinity]', '[1e999]']:
            with self.subTest(bad=bad), self.assertRaises(ValueError): strict_json(bad)
        # Read current authored files, not a frozen predecessor/hash oracle.
        for folder in ['entries', 'macros', 'packages']:
            for path in (self.root / '.SNL_Doc' / folder).glob('*.json'):
                strict_json(path.read_text())

    def test_document_tree_links_special_inodes_and_directory_drift(self: Any):
        root = self.root / 'tree-control'; root.mkdir()
        (root / 'nested').mkdir(); (root / 'nested/value.json').write_text('{}')
        files, directories = scan_document_tree(root)
        self.assertEqual(directories, {'nested'})
        self.assertEqual(directories, expected_directories(files))
        assert_document_tree(root, files)
        (root / 'extra').mkdir()
        with self.assertRaisesRegex(ValueError, 'manifest drift'):
            assert_document_tree(root, files)
        (root / 'extra').rmdir()
        (root / 'link').symlink_to('absent')
        with self.assertRaisesRegex(ValueError, 'symlink'): scan_document_tree(root)
        (root / 'link').unlink()
        os.mkfifo(root / 'pipe')
        with self.assertRaisesRegex(ValueError, 'special inode'): scan_document_tree(root)
        (root / 'pipe').unlink()
        self.assertEqual(scan_document_tree(root), (files, directories))

    def test_missing_library_metadata_rejected(self: Any):
        path = self.root / '.SNL_Doc/libraries/Type_Theory/meta.json'
        path.unlink()  # Disposable non-Git copy only.
        self.assertFalse(self.cli('library', 'get', 'Type_Theory')['ok'])
        self.assertFalse(self.cli('validate')['ok'])

    def test_boolean_storage_version_rejected(self: Any):
        path = next((self.root / '.SNL_Doc/entries').glob('*.json'))
        self.reject_mutation(str(path.relative_to(self.root)), lambda v: v.__setitem__('version', True))

    def test_library_multi_parent_rejected_without_write(self: Any):
        old = self.get('library', 'Type_Theory'); value = copy.deepcopy(old['value'])
        graph = value['graph']; edge = next(r for r in graph['relationships'] if r['label'] == 'branch')
        other = next(n['id'] for n in graph['nodes'] if n['id'] not in [edge['from'], edge['to']])
        mutant = copy.deepcopy(edge); mutant['from'] = other
        graph['relationships'].append(mutant)
        self.assertFalse(self.cli('library', 'update', 'Type_Theory', '--if-match', old['revision'], value=value)['ok'])
        self.assertEqual(old, self.get('library', 'Type_Theory'))

    def test_library_duplicate_node_rejected_without_write(self: Any):
        old = self.get('library', 'Type_Theory'); value = copy.deepcopy(old['value'])
        value['graph']['nodes'].append(copy.deepcopy(value['graph']['nodes'][0]))
        self.assertFalse(self.cli('library', 'update', 'Type_Theory', '--if-match', old['revision'], value=value)['ok'])
        self.assertEqual(old, self.get('library', 'Type_Theory'))

    def test_invalid_style_identity_rejected_without_write(self: Any):
        old = self.get('macro', 'Topology::Topology.mapLimit'); value = copy.deepcopy(old['value'])
        value['styles'][0]['style_name'] = 'not a style'
        self.assertFalse(self.cli('macro', 'update', old['id'], '--if-match', old['revision'], value=value)['ok'])
        self.assertEqual(old, self.get('macro', old['id']))

    def test_map_limit_direction_independent_semantic_oracle(self: Any):
        value = self.get('macro', 'Topology::Topology.mapLimit')['value']
        def check(v):
            self.assertEqual(v['source']['entries'], ['Topology.def.mapLimit'])
            self.assertEqual(v['styles'][0]['template']['body'], r'\lim_{#0\to #1}#2(#0)=#3')
        check(value)
        mutant = copy.deepcopy(value)
        mutant['styles'][0]['template']['body'] = r'\lim_{#1\to #0}#2(#0)=#3'
        with self.assertRaises(AssertionError): check(mutant)
        # Even a coherently rewritten receipt cannot change this independent oracle.

    def test_signature_fragment_locales_slots_and_nonexhaustiveness(self: Any):
        value = self.get('macro', 'TypeTheory::Syntax.signatureFragment')['value']
        locales = value['styles'][0]['template']['values']
        self.assertEqual(value['source']['entries'], ['Syntax.def.signatureFragment'])
        self.assertIn('non-exhaustive', locales['en']['body'])
        self.assertIn('非穷尽', locales['zh-CN']['body'])
        self.assertEqual(placeholders(locales['en']['body']), ('#0', '#1'))
        self.assertEqual(placeholders(locales['en']['body']), placeholders(locales['zh-CN']['body']))
        self.assertNotEqual(placeholders(locales['en']['body']), placeholders(locales['zh-CN']['body'].replace('#1','#2')))
        self.assertEqual(placeholders(r'\#3 #1 #1 #*'), ('#*', '#1'))

    def test_church_exact_parent_and_repeated_option_occurrences(self: Any):
        result = self.cli('library', 'list'); self.assertTrue(result['ok'], result)
        church = option = 0
        for library in result['data']['entities']:
            graph = library['value']['graph']; ids = {n['id']: n['props']['entryId'] for n in graph['nodes']}
            edges = [r for r in graph['relationships'] if r['label'] == 'branch']
            for node, entry in ids.items():
                if entry == 'Type.rmk.lambdaTuringComplete':
                    self.assertEqual([ids[r['from']] for r in edges if r['to'] == node], ['Type.subsec.Church']); church += 1
                if entry == 'FP.def.option':
                    children = [ids[r['to']] for r in edges if r['from'] == node]
                    for child in ['FP.def.option.ctor.none','FP.def.option.ctor.some','FP.def.option.recursor']:
                        self.assertEqual(children.count(child), 1)
                    option += 1
        self.assertGreater(church, 0); self.assertGreater(option, 1)

    def test_legal_expression_authored_are_is_survive(self: Any):
        value = self.get('macro', 'TypeTheory::Syntax.LegalExpr-UTLC')['value']
        styles = {s['style_name']: s['template'] for s in value['styles']}
        self.assertEqual(styles['default']['body'], r'\mathcal{E}_{\lambda}^{\checkmark}')
        for name, en in [('are', '#0 are legal'), ('is', '#0 is legal')]:
            self.assertEqual(styles[name]['values']['en']['body'], en)
            self.assertEqual(styles[name]['values']['zh-CN']['body'], r'#0 是合法 $\lambda$-表达式')
        self.assertEqual(value['source']['entries'], ['Syntax.def.legalExpression-UTLC'])
        self.assertIn('x_fulcrum_typst', value)

    def test_subgroup_authored_text_style_survives(self: Any):
        value = self.get('macro', 'Algebra::Algebra.Subgroup')['value']
        styles = {s['style_name']: s['template'] for s in value['styles']}
        self.assertEqual(styles['default']['body'], r'#0 \leqslant #1')
        self.assertIn('text', styles)
        self.assertEqual(styles['text']['values']['en']['body'], 'Subgroup')
        self.assertEqual(styles['text']['values']['zh-CN']['body'], '子群')
        self.assertEqual(value['source']['entries'], ['Algebra.def.subgroup'])
