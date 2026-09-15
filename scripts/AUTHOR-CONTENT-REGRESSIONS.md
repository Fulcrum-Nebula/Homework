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
checks; additional exact migration-method controls are documented below.

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


## Bounded iota/let and Church closure (2026-09-15)

`author_content_targets.json` is consumed by the existing public-control runner.
It records six captured staged layers from `/tmp/fulcrum-iota-let` and the 17
working + 17 loose layers from `/tmp/fulcrum-church-impl-20260819`; it is not a
family-wide retirement certificate. Full source/body and fresh-CAS readbacks
are in the parent campaign's `Notes-dangling-close` evidence.

- The staged iota and combined let/zeta Entries really had empty bodies. Iota
  remains after the recursor. The combined placeholder stays honest; the actual
  let/zeta exposition is in the two populated UTLC-design children, not a
  restored duplicate graph occurrence.
- Closed expressions do not acquire `fvar`. The current separate open signature
  carries the free-variable constructor. Two current remarks now explain the
  well-scoped/closed distinction and the scope of open-expression recursion.
- The four beta constructors remain contraction, abstraction congruence,
  function-position congruence and argument-position congruence. The relation
  symbol is separate from binary application; multi-step reduction uses strict
  transitive closure, not a newly asserted reflexive step.
- Four existing bilingual constant/delta/let/zeta bodies retain their text and
  now include the donor's missing noncapture, transparency and surface-expansion
  qualifications. Church's existing biography remains authoritative; its name
  macro retains its default style and gains the missing Chinese `zh_CN` style.
- Retired migration scripts' lexical/structural shape selectors, predecessor
  snapshots, fixed totals and hash writers are not runtime APIs. Their resulting
  concepts, package activation, source entries, nested graph placement and
  ordered children are checked by `AuthorSemantics`; schema, fresh/stale CAS,
  localized/structural styles and reference rejection use `PublicAuthorControls`.
  No old coordinator is imported or executed.

### Portable declaration and binding audits

Both Toolkit handoff scripts now live in this runner, not just in a checksum
ledger. `test_author_convergence.py <official snl.mjs>` discovers the installed
Basics core next to that CLI; `SNL_BASICS_CORE` can select another maintained
core explicitly. The audit commands themselves are read-only:

```
node scripts/audit_decl_semantics.mjs input.json census.json /path/to/core.js
node scripts/audit_binding_semantics.mjs input.json bindings.json /path/to/core.js
node scripts/audit_binding_semantics.mjs input.json proposal.json /path/to/core.js legacy-proposal
```

Input contains `entries` and `macros` arrays of entity values (not storage
wrappers). Output paths are caller-owned evidence files. Identity mode does not
rename declarations. `legacy-proposal` only evaluates the historical family
proposal; even a passing comparison is **not** authorization to migrate current
identities or replay old schema/macros.

Full capability correspondence:

| Donor check | Maintained implementation |
|---|---|
| All Entry AST nodes, family name/arity/style and affected Entry census | declaration `walk`, `uses`, `counts` |
| Parse failures and resolver diagnostic totals | declaration `errors`, `diags` (nonzero exit on errors) |
| env declarations, explicit binder children, postfix exceptions | declaration `special` |
| Macro/template strings and non-content Entry metadata | declaration `stringsWalk`, `strings` |
| Historical declaration family → variable wrapper, opaque/notation styles | binding `trans`, explicit `legacy-proposal` only |
| Old→new node origin map, env-ID remapping | binding `origins`, `oldToNew`, `env_mode` walk |
| Binder normalization, serialization/reparse, complete AST equality/diffs | binding `serialTree`, `reparse`, `syntax-roundtrip` |
| Diagnostic equality and node-kind census/comparison | binding resolver pair, `diagnostics`, `nodeKinds`, `kind` |
| Local binding targets translated through origin map | binding `tree_path`, `want`, `binding` |
| External source identity | binding `entry source` comparison |
| Postfix totals, wrapper/node totals, empty hypotheses, full samples | binding `postfixes`, `wrappers`, `totalNodes`, `emptyH`, `samples` |
| Continue and retain failures instead of silently skipping Entries | binding per-Entry catch and nonzero exit |

The maintained parser executed both the real current corpus and the real frozen
historical input: current identity audit covered 480 Entries, 12,809 nodes,
2,718 local bindings and 1,873 postfixes; the historical proposal covered 439
Entries and 272 wrappers. Both had zero comparison failures. This is an AST
and binding audit, not a Lean proof or a runtime-exporter acceptance claim.

## Retained author-method controls (2026-09-15)

The existing runner now imports `test_author_methods.py` (27 total tests,
including the previous 16). No historical writer is imported or executed.

- `strict_json` rejects duplicate keys, non-finite constants and overflow; it
  reads current Entry/Macro/Package JSON, not a stored source hash.
- `placeholders` retains the sorted unique unescaped numbered/star contract;
  the bilingual non-exhaustive signature has equal slots, with a failing mutant.
- Public CAS rejects duplicate Library nodes, multi-parent occurrences and
  invalid style names without changing the value/revision. Boolean envelope
  versions and missing Library metadata are rejected by current public reads.
- Independent semantic assertions preserve the limit variable/destination
  direction, Church's exact parent and each repeated option occurrence's three
  children. Rewriting an old receipt cannot change these oracles.
- The read-only tree-manifest helper retains complete directory/file comparison
  and rejects dangling links and FIFO/special inodes. These checks use a caller's
  manifest, not a frozen repository hash or a new production transaction writer.
- The old bilingual `Algebra.Subgroup` lexical output is retained in an additive
  `text` style via fresh public CAS. The current default predicate rendering and
  source Entry are unchanged. The test first failed on the missing `text` style.

One-shot localeCompare ordering, raw hash filenames, receipt reconstruction,
virtual preflight maps and renameat2/lock-token choreography are not public
interfaces to restore. Current Package canonical ordering, typed CAS/batch
operations and parser-based references supersede them. An algorithm replacement
is distinct from certifying every mathematical body/role or historical generator
output: those exact exceptions remain in the private consolidation evidence.
