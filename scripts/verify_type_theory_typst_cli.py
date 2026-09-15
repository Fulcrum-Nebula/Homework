#!/usr/bin/env python3
"""Read the exact reviewed Typst metadata through the official current CLI.

Usage: python3 scripts/verify_type_theory_typst_cli.py <snl.mjs> [workspace]
No v11 migration, direct canonical writes, global installs, or exporter claims.
"""
import json
import subprocess
import sys
from pathlib import Path
import type_theory_typst_bindings as bindings


def verify(cli, root):
    def call(*args):
        p = subprocess.run(['node', str(cli), *args, '--root', str(root), '--json'],
                           capture_output=True, text=True, check=False)
        value = json.loads(p.stdout)
        if p.returncode or not value.get('ok'):
            raise RuntimeError({'args': args, 'exit': p.returncode, 'result': value})
        return value['data']
    validation = call('validate')
    assert validation['valid'] is True, validation
    records, cursor = {}, None
    while True:
        args = ['macro', 'list', '--limit', '100']
        if cursor:
            args.extend(['--cursor', cursor])
        data = call(*args)
        for e in data['entities']:
            records[(e['value']['package'], e['value']['name'])] = e['id']
        cursor = data.get('nextCursor')
        if not cursor:
            break
    raw = bindings._macro_index(root)
    for key in bindings.CLOSURE:
        entity = call('macro', 'get', records[key])['entity']
        assert entity['revision']
        expected = raw[key][1]['macro'][bindings.EXTENSION_KEY]
        assert entity['value'][bindings.EXTENSION_KEY] == expected
        bindings.validate_extension(*key, expected)
    return {'valid': True, 'officialReadbacks': len(bindings.CLOSURE),
            'declarationValidation': bindings.validate_workspace(root),
            'legacyMarkerMigration': 'superseded; not executed',
            'exporterAcceptance': 'not claimed'}


if __name__ == '__main__':
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
    print(json.dumps(verify(Path(sys.argv[1]), root), sort_keys=True))
