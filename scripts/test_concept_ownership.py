#!/usr/bin/env python3
"""Preserve declared teaching homes, not an invented exclusive-ownership schema.

Run: python3 scripts/test_concept_ownership.py [workspace-root]
The declaration table travels with this test. Primary means the authored main
teaching location; other occurrences remain allowed. This is an author-content
oracle, not a replacement for official Toolkit workspace validation.

Original assertions: f511f15532614cb502cfdc9240f3a3aad5b330f2,
scripts/verify_fulcrum_i18n_inductives.py, concept_ownership loop.
Current identities: Logic.def.eq -> Eq; Type.rl.Expr-LC/STLC ->
Syntax.def.expression-UTLC/STLC. Secondary roles are preserved verbatim.
"""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONCEPTS = [
    ('W-type', 'Type_Theory', 'Type.def.W', []),
    ('enumeration type', 'Type_Theory', 'Type.def.enum', []),
    ('sum type', 'Type_Theory', 'Type.def.sum', []),
    ('product type', 'Type_Theory', 'Type.def.prod', []),
    ('Sigma type', 'Type_Theory', 'Type.def.Sigma', []),
    ('structure type', 'Type_Theory', 'Type.def.structure', []),
    ('natural numbers', 'Type_Theory', 'Type.def.nat', []),
    ('list', 'Type_Theory', 'Type.def.list', [('Functional_Programming', 'FP.def.list', 'functional-programming instance')]),
    ('syntax expression', 'Type_Theory', 'Syntax.def.expression-UTLC', [('Type_Theory', 'Syntax.def.expression-STLC', 'typed syntax variant')]),
    ('binary tree', 'Type_Theory', 'Type.def.bin-tree', []),
    ('vector', 'Type_Theory', 'Type.def.vector', []),
    ('measure space', 'measure-theory', 'Measure.def.measureSpace', [('Type_Theory', 'Measure.def.measureSpace', 'structure example')]),
    ('equality', 'logic', 'Eq', [('Type_Theory', 'Eq', 'inductive-family example')]),
]


def no_duplicates(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate JSON key: ' + key)
        value[key] = item
    return value


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicates)


def load_workspace(root):
    entries = {}
    for path in sorted((root / '.SNL_Doc' / 'entries').glob('*.json')):
        value = read_json(path)['entry']
        if value['id'] in entries:
            raise ValueError('Duplicate Entry identity: ' + value['id'])
        entries[value['id']] = value
    graphs = {path.parent.name: read_json(path)
              for path in sorted((root / '.SNL_Doc' / 'libraries').glob('*/graph.json'))}
    return entries, graphs


def check_locations(entries, graphs, concepts=CONCEPTS):
    names = set()
    for concept, primary, entry_id, secondary in concepts:
        assert all(isinstance(v, str) for v in (concept, primary, entry_id))
        assert concept not in names, 'Multiple primary declarations: ' + concept
        names.add(concept)
        assert isinstance(secondary, list)
        references = [(primary, entry_id)]
        for library, secondary_id, role in secondary:
            assert all(isinstance(v, str) for v in (library, secondary_id, role))
            references.append((library, secondary_id))
        for library, identity in references:
            assert identity in entries, 'Missing Entry: ' + identity
            assert library in graphs, 'Missing Library: ' + library
            assert any(node.get('props', {}).get('entryId') == identity
                       for node in graphs[library].get('nodes', [])), (library, identity)


class ConceptOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, cls.graphs = load_workspace(ROOT)

    def test_all_declared_primary_and_secondary_locations(self):
        check_locations(self.entries, self.graphs)

    def test_missing_entry_is_detected_for_every_declared_reference(self):
        for _, primary, identity, secondary in CONCEPTS:
            for _, eid in [(primary, identity)] + [(a, b) for a, b, _ in secondary]:
                with self.subTest(entry=eid):
                    entries = dict(self.entries)
                    del entries[eid]
                    with self.assertRaises(AssertionError):
                        check_locations(entries, self.graphs)

    def test_missing_occurrence_is_detected_for_every_declared_reference(self):
        for _, primary, identity, secondary in CONCEPTS:
            for library, eid in [(primary, identity)] + [(a, b) for a, b, _ in secondary]:
                with self.subTest(library=library, entry=eid):
                    graphs = dict(self.graphs)
                    graph = dict(graphs[library])
                    graph['nodes'] = [n for n in graph['nodes'] if n.get('props', {}).get('entryId') != eid]
                    graphs[library] = graph
                    with self.assertRaises(AssertionError):
                        check_locations(self.entries, graphs)

    def test_missing_library_is_detected(self):
        for library in {c[1] for c in CONCEPTS} | {s[0] for c in CONCEPTS for s in c[3]}:
            with self.subTest(library=library):
                graphs = dict(self.graphs)
                del graphs[library]
                with self.assertRaises(AssertionError):
                    check_locations(self.entries, graphs)

    def test_secondary_role_type_is_validated(self):
        for index, item in enumerate(CONCEPTS):
            for j, (library, eid, _) in enumerate(item[3]):
                with self.subTest(concept=item[0], secondary=j):
                    concepts = copy.deepcopy(CONCEPTS)
                    concepts[index][3][j] = (library, eid, None)
                    with self.assertRaises(AssertionError):
                        check_locations(self.entries, self.graphs, concepts)

    def test_other_occurrences_do_not_change_the_declared_home(self):
        graphs = dict(self.graphs)
        graphs['AdditionalTeachingExamples'] = {'nodes': [
            {'id': str(i), 'props': {'entryId': c[2]}}
            for i, c in enumerate(CONCEPTS)]}
        check_locations(self.entries, graphs)

    def test_duplicate_concept_declaration_is_detected(self):
        with self.assertRaises(AssertionError):
            check_locations(self.entries, self.graphs, CONCEPTS + CONCEPTS[:1])

    def test_duplicate_json_key_is_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"role":"first","role":"second"}', object_pairs_hook=no_duplicates)


if __name__ == '__main__':
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        ROOT = Path(sys.argv.pop(1)).resolve()
    unittest.main(verbosity=2)
