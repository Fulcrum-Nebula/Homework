# Fulcrum Typst declaration metadata — reviewed historical migration

The contribution at `04f02fe2aef370c7d0820debf38292d2339af614` is accounted for as
46 unchanged surviving declarations, 13 declarations on explicitly migrated
identities, and four intentionally retired composite macros. The current set is
**59**, not the original 63 and not a claim to cover every current Library dependency.
All pre-existing canonical content, including the earlier 46 fields, is retained.

## Callable and consumer contract

`x_fulcrum_typst` stores one collision-free identifier and an I18N declaration
(zh-CN/en), both with `(children, style: none)`. The declaration dispatches the
**current** Package/name to `snl-render-macro-template`, then `optionLink` to the
explicit current target. Exporters consume the stored identifier; they do not
reconstruct it. `Nat` keeps `NaturalNumber`. Styles and operand arrays remain
owned by current canonical templates. No obsolete callable alias is installed.

The historical tip added declarations, validation and a storage-migration probe;
it did not implement `snl-render-macro-template` or an exporter. This repository
contains no Typst exporter runtime. Declaration compiler checks are not rendered
macro/PDF acceptance, and a future exporter is a separate product task. No mock
renderer or stub `optionLink` is substituted as evidence.

## Complete old-slot → current-slot disposition

| Old Package/name | Current slot and operand/style mapping |
|---|---|
| FulcrumsMathNotes/def-hyp | Retired: `variable(h, def(object, explicit-empty-type, content))`; predicate style remains on def. |
| FulcrumsMathNotes/thm-hyp | Retired: `variable(h, theorem(proposition))`; default/display remains on theorem. |
| FulcrumsMathNotes/def-inductive-hyp | Retired: `variable(h, inductive(object, constructors))`; prop belongs to inductive. |
| FulcrumsMathNotes/def-hyp-opq | Retired: `variable(h, def(object, explicit-empty-type, explicit-empty-content))`; never invent a type/body. |
| FulcrumsMathNotes/def-inductive | `inductive`, two presentation operands; localized-default → localized_default; prop retained. |
| FulcrumsMathNotes/list-partial | `__list__`, variadic; same separators, enumerate and none; localized-default → localized_default and 中文 → zh_CN. **Not tuple-partial**. |
| Logic/Logic.false | Logic/False, zero operands; bot/text → authored_Logic_false_bot/text, sourced from native False. |
| Logic/Logic.and | **SetTheory/And**, two operands; infix/cases → authored_Logic_and_infix/cases, sourced from native And. |
| SetTheory/Set.sep-typed | `setOf[typedBuilder](binder,type,predicate)`, three presentation operands. Default `setOf` is NOT the old builder. |
| TypeTheory/Type.Term | `Syntax.Term`, zero-operand Term/项 text; old Type.rl.judge now uses a context Γ and a three-place judgement, not the old two-place metasyntax. |
| TypeTheory/Type.Expr | `Syntax.Expr[text]` for the old zero-operand word; current default is symbolic E. STLC source now records a signature fragment, not an exhaustive datatype. |
| TypeTheory/Lambda.Expr | `Syntax.Expr-UTLC`, zero operands, same Eλ; current closed/open syntax distinction is authoritative. |
| TypeTheory/Lambda.LegalExpr | `Syntax.LegalExpr-UTLC`, zero operands; same legality-class template, current bound-variable-resolution definition. |
| TypeTheory/Lambda.apply | `Syntax.apply-UTLC`, variadic concatenation. Not the binary application constructor. |
| TypeTheory/Type.Expr-UTLC.apply | `Syntax.Expr-UTLC.apply`, two operands; current adjacency replaces old explicit TeX spacing; text uses Unicode λ. |
| TypeTheory/Type.Expr-UTLC.bvar | `Syntax.Expr-UTLC.bvar`, one constructor operand; hash/text preserved. |
| TypeTheory/Type.Expr-UTLC.lambda | `Syntax.Expr-UTLC.lambda`, two presentation operands binder/body; default/maspto/match order preserved. The semantic closed-syntax constructor takes its body; presentation arity is not semantic arity. |

New declarations target current identities; they are not wrappers silently
accepting an old style or old argument list. In particular a historical
Set.sep-typed caller selects typedBuilder, and a Type.Expr word selects text.
The four retired -hyp callables are deliberately not attached to variable or def:
those signatures differ and no one-to-one callable migration exists.

Evidence: `26b2e0244` unifies syntax and typing authorities; `e8151205c`
explicitly renames list-partial to __list__ with legacy styles; `547f48c1c`
factors declaration contexts into variable; `21288328f` makes native Lean/Mathlib
logic and sets authoritative while retaining authored styles. Current
`Lean4/Set Theory/term_macros.lean:189–219` defines the typedBuilder native view.
Current canonical Entries include `Syntax.def.expression-UTLC`, its three
constructors, `Syntax.def.legalExpression-UTLC`, `False`, `And` and `Eq`.
Full old/current templates, original consumer records and current consumer
records are recorded in the round-2 migration evidence, not inferred from names.
The older naming examples in CONVENTIONS.md are historical; they do not override
these later native migrations or the explicit def/theorem/variable contract.

## Verification and authoritative writing

```sh
python3 scripts/test_type_theory_typst_bindings.py
python3 scripts/type_theory_typst_bindings.py
python3 scripts/verify_type_theory_typst_cli.py /path/to/current/snl.mjs .
```

The original mutation assertions remain. Corpus assertions now prove the explicit
63 = 46 surviving + 13 migrated + 4 retired partition, with 59 distinct live
bindings. No live-catalog intersection silently lowers an expected count.

The old Extension script's v11 reader/rewrite, opaque-field retention, duplicate
rejection and reserved-key rejection are mapped to current official CLI
list/get/update/readback/validate plus the declaration mutation tests. Its
0.0.11→0.1.0 marker-only migration is intentionally superseded: canonical current
storage is not downgraded to replay it. Extension is not changed by this task.
Updates use official fresh-CAS Macro CRUD, complete-value preservation and fresh
readback; the old direct-JSON `--apply` writer is not shipped. The campaign also
found that the current CLI accepts a Macro-level `typst` opaque field, unlike
the old v11 host. That probe is removed through fresh CAS and complete final
preimage-plus-metadata comparison. The focused declaration validator now rejects
this reserved field, with a negative regression; no current-CLI rejection is claimed.

This closes the committed declaration tip, not the separately tracked **1572**
unintegrated dirty-source records. Historical dirty sources remain untouched.
