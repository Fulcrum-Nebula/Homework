# Fulcrum Typst binding metadata — partial forward port

This catalog carries the opaque `x_fulcrum_typst` field on **46 surviving logical
Macro identities**, from the original 63-identity contribution in
`04f02fe2aef370c7d0820debf38292d2339af614`. This is not a completed merge of that
branch or the full current Type_Theory dependency closure.

The stored collision-free binding, I18N declarations (zh-CN/en), common
`(children, style: none)` signature, explicit optionLink target, and generic
`snl-render-macro-template` dispatch are unchanged. BasicOperators:Nat retains
the established NaturalNumber target. Current templates, source references,
style order, identity, AST, prose, Pointer and Library order are not replaced.
The field is opaque metadata; these gates do not certify a Typst exporter or PDF.

Run `python3 scripts/test_type_theory_typst_bindings.py` and
`python3 scripts/type_theory_typst_bindings.py`. The validator explicitly retains
ORIGINAL_CLOSURE (63) separately from the admitted CLOSURE (46). It does not
silently filter the live workspace. It validates exact I18N, declarations,
collision-free bindings, current filenames and absence of unexpected bindings.
The old direct-JSON --apply writer is not shipped: use official fresh-revision
SNL Macro CRUD to make changes.

Seventeen historical identities have been removed or refactored. Their callable
contracts require explicit semantic migration, not Git rename similarity; their
bindings are not reintroduced here. The historical Extension v11 marker-migration
script is likewise not a passing current-host gate. Both remain unresolved.
