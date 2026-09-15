# Author-content regression checks

Run with the official SNL Agent Toolkit CLI (not an old migration script):

```sh
python3 scripts/test_author_convergence.py /absolute/path/to/dist/cli/snl.mjs
python3 scripts/test_type_theory_typst_bindings.py
python3 scripts/verify_type_theory_typst_cli.py /absolute/path/to/dist/cli/snl.mjs .
```

`test_author_convergence.py` uses disposable **non-Git** workspace copies and
public CLI read/write/validation. It checks opaque Entry fields, fresh/stale CAS,
whole Macro readback including ordered styles/locales/Typst metadata, schema
markers, retired `partial` kinds, duplicate style names, and dangling endpoints.
The localized list-separator test reproduces the old migration probe’s actual
loss of `、`; the maintained catalog keeps it. These are scoped regression
checks, not a complete replacement for every historical migration test.

Native Semigroup diagnostics live beside the relevant Lean note:

```sh
lake env lean -j2 'Lean4/Basic Algebra/SemigroupExportProbe.lean'
```

This combines full declaration JSON inspection with recursive `HMul.hMul`
children and registered-template inspection. It requires the repository’s pinned
Lean/Mathlib/SNL4Lean dependencies. The probe deliberately imports only
`SNL4Lean` and `Mathlib.Algebra.Group.Defs`, with the existing bilingual
Semigroup notation, rather than the entire algebra terminology closure.
The author-convergence closeout passed on pinned Lean 4.28 with the verified
source-matching SNL4Lean overlay and existing Mathlib objects: four `HMul.hMul`
nodes each retained six children, and the registered template was `#4 \\cdot #5`.
No aggregate rebuild or native AST reconstruction was used. The earlier failed
import attempt remains in the private evidence; public CLI tests alone do not
certify this native result or any browser/runtime-exporter acceptance.

## Replaced historical contracts

- Flat v0.0.8 styles and v0.0.9 nested templates are obsolete persisted formats.
  Preserve their authored values, not their old storage receipts or version tags.
- Locale defaults belong to localized template variants; style array order,
  selected styles, and locale-specific separators must survive a write.
- `partial` is replaced by `sub`. Old definition-with-hypothesis composites are
  replaced by scoped `variable` plus current `def`/`theorem`/`inductive`/`structure`.
- Official CRUD validates current topology and requires opaque revisions. Old
  scripts that rewrite fixed manifests/receipts are not production writers.
- Typst declarations are metadata. Declaration compilation does not establish a
  runtime exporter, macro rendering, or Extension UI acceptance.

The Semigroup Entry contains the bilingual research interpretation of the two
historical probes. Full source/ref/layer dispositions are maintained in the
private consolidation report, not shipped as raw historical dumps.
