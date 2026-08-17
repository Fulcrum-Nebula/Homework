# Fulcrum Typst Macro bindings

The 63 Macros used by the `Type_Theory` library carry one opaque Macro-payload field:

```json
"x_fulcrum_typst": {
  "binding": "<stored collision-free Typst identifier>",
  "declaration": {
    "type": "i18n",
    "default_language": "zh-CN",
    "values": {
      "zh-CN": "#let ...",
      "en": "#let ..."
    }
  }
}
```

Each locale contains exactly one declaration with the common callable signature
`(children, style: none)`. The declaration wraps the generic
`snl-render-macro-template(package, macro, children, style: style)` result in
`optionLink(explicit-target, ...)`. Consequently the current Macro v11
`styles[].template` data remains authoritative; this extension does not copy or
replace template bodies and does not use the TeX/LaTeX backend.

Bindings are stored in data and include a digest of the logical Package/Macro
identity. Exporters must consume the stored binding rather than derive an
identifier. The explicit link target normally equals the Macro logical name;
the established TypeTheory `export.typ` mapping keeps `BasicOperators:Nat` at
`NaturalNumber` (and `TypeTheory:Type` at `Type`).

Validate the data and mutation-tested declaration contract with:

```sh
python3 scripts/test_type_theory_typst_bindings.py
python3 scripts/type_theory_typst_bindings.py
```

To exercise the production SNL Doc Extension v11 reader, rewrite path, reserved
`typst` rejection, and the existing `0.0.11 -> 0.1.0` marker-only migration:

```sh
node scripts/verify_type_theory_typst_extension.mjs . /path/to/SNL-Doc-Extension
```

The host intentionally treats `x_fulcrum_typst` as opaque. The focused validator
therefore rejects malformed I18N values, missing defaults, zero/multiple `#let`
statements, binding/signature drift, wrong targets, duplicate/copy collisions,
closure drift, and hashed-filename identity drift.
