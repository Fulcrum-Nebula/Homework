#!/usr/bin/env python3
"""Validate the explicitly admitted subset of the historical Typst declarations."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

EXTENSION_KEY = "x_fulcrum_typst"
LOCALES = ("zh-CN", "en")
DEFAULT_LANGUAGE = "zh-CN"
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
LET_RE = re.compile(r"(?m)^\s*#let\s+")

CLOSURE: tuple[tuple[str, str], ...] = (
    ("BasicOperators", "Eq"), ("BasicOperators", "Nat"), ("BasicOperators", "parentheses"),
    ("FulcrumsMathNotes", "def"), ("FulcrumsMathNotes", "def-hyp"),
    ("FulcrumsMathNotes", "def-hyp-opq"), ("FulcrumsMathNotes", "def-inductive"),
    ("FulcrumsMathNotes", "def-inductive-hyp"), ("FulcrumsMathNotes", "list-partial"),
    ("FulcrumsMathNotes", "thm-hyp"), ("Logic", "Eq.refl"), ("Logic", "Logic.and"),
    ("Logic", "Logic.false"), ("Logic", "Logic.forall"), ("Logic", "Logic.forall-typed"),
    ("MeasureTheory", "Measure.Measure"), ("MeasureTheory", "Measure.MeasureSpace"),
    ("MeasureTheory", "Measure.SigmaAlgebra"), ("SetTheory", "Set.sep-typed"),
    ("TypeTheory", "Church.Nat"), ("TypeTheory", "Church.add"), ("TypeTheory", "Church.and"),
    ("TypeTheory", "Church.false"), ("TypeTheory", "Church.mul"), ("TypeTheory", "Church.not"),
    ("TypeTheory", "Church.or"), ("TypeTheory", "Church.succ"), ("TypeTheory", "Church.true"),
    ("TypeTheory", "Lambda.Expr"), ("TypeTheory", "Lambda.I"), ("TypeTheory", "Lambda.K"),
    ("TypeTheory", "Lambda.LegalExpr"), ("TypeTheory", "Lambda.Omega"), ("TypeTheory", "Lambda.S"),
    ("TypeTheory", "Lambda.apply"), ("TypeTheory", "Lambda.beta"),
    ("TypeTheory", "Lambda.beta-closure"), ("TypeTheory", "Lambda.defeq"),
    ("TypeTheory", "Lambda.defeq.app-cong"), ("TypeTheory", "Lambda.defeq.beta"),
    ("TypeTheory", "Lambda.defeq.eta"), ("TypeTheory", "Lambda.defeq.lam-cong"),
    ("TypeTheory", "Lambda.defeq.refl"), ("TypeTheory", "Lambda.defeq.symm"),
    ("TypeTheory", "Lambda.defeq.trans"), ("TypeTheory", "Lambda.eta"),
    ("TypeTheory", "Lambda.iota"), ("TypeTheory", "Lambda.omega"), ("TypeTheory", "Nat.succ"),
    ("TypeTheory", "Type"), ("TypeTheory", "Type.Expr"),
    ("TypeTheory", "Type.Expr-UTLC.apply"), ("TypeTheory", "Type.Expr-UTLC.bvar"),
    ("TypeTheory", "Type.Expr-UTLC.lambda"), ("TypeTheory", "Type.Pi"),
    ("TypeTheory", "Type.Term"), ("TypeTheory", "Type.apply"), ("TypeTheory", "Type.judge"),
    ("TypeTheory", "Type.to"), ("TypeTheory", "cases"), ("TypeTheory", "ctors"),
    ("TypeTheory", "deBruijnIndex"), ("TypeTheory", "match"),
)

# Historical 63-identity input is retained explicitly; removed identities are
# NOT automatically mapped by Git similarity or silently re-created.
ORIGINAL_CLOSURE = CLOSURE
CLOSURE = (('BasicOperators', 'Nat'), ('BasicOperators', 'parentheses'), ('BasicOperators', 'Eq'), ('FulcrumsMathNotes', 'def'), ('Logic', 'Logic.forall-typed'), ('Logic', 'Eq.refl'), ('Logic', 'Logic.forall'), ('MeasureTheory', 'Measure.Measure'), ('MeasureTheory', 'Measure.MeasureSpace'), ('MeasureTheory', 'Measure.SigmaAlgebra'), ('TypeTheory', 'deBruijnIndex'), ('TypeTheory', 'Type.judge'), ('TypeTheory', 'Lambda.beta'), ('TypeTheory', 'Type.to'), ('TypeTheory', 'Church.and'), ('TypeTheory', 'Church.Nat'), ('TypeTheory', 'Nat.succ'), ('TypeTheory', 'Lambda.Omega'), ('TypeTheory', 'Lambda.omega'), ('TypeTheory', 'Lambda.S'), ('TypeTheory', 'Lambda.defeq.trans'), ('TypeTheory', 'Type.Pi'), ('TypeTheory', 'Church.add'), ('TypeTheory', 'Church.true'), ('TypeTheory', 'Lambda.defeq.eta'), ('TypeTheory', 'Lambda.eta'), ('TypeTheory', 'Type.apply'), ('TypeTheory', 'Lambda.I'), ('TypeTheory', 'Church.not'), ('TypeTheory', 'Church.false'), ('TypeTheory', 'Lambda.defeq.app-cong'), ('TypeTheory', 'Lambda.K'), ('TypeTheory', 'Lambda.defeq'), ('TypeTheory', 'Lambda.defeq.beta'), ('TypeTheory', 'Lambda.defeq.lam-cong'), ('TypeTheory', 'Church.or'), ('TypeTheory', 'Church.mul'), ('TypeTheory', 'Lambda.defeq.symm'), ('TypeTheory', 'cases'), ('TypeTheory', 'match'), ('TypeTheory', 'Lambda.defeq.refl'), ('TypeTheory', 'Type'), ('TypeTheory', 'Church.succ'), ('TypeTheory', 'Lambda.beta-closure'), ('TypeTheory', 'ctors'), ('TypeTheory', 'Lambda.iota'))

# Explicitly reviewed identity migrations; not a name-similarity fallback.
SURVIVING_CLOSURE = CLOSURE
MIGRATIONS = {
    ('FulcrumsMathNotes', 'def-inductive'): ('FulcrumsMathNotes', 'inductive'),
    ('FulcrumsMathNotes', 'list-partial'): ('FulcrumsMathNotes', '__list__'),
    ('Logic', 'Logic.false'): ('Logic', 'False'),
    ('Logic', 'Logic.and'): ('SetTheory', 'And'),
    ('SetTheory', 'Set.sep-typed'): ('SetTheory', 'setOf'),
    ('TypeTheory', 'Type.Term'): ('TypeTheory', 'Syntax.Term'),
    ('TypeTheory', 'Type.Expr'): ('TypeTheory', 'Syntax.Expr'),
    ('TypeTheory', 'Lambda.Expr'): ('TypeTheory', 'Syntax.Expr-UTLC'),
    ('TypeTheory', 'Lambda.LegalExpr'): ('TypeTheory', 'Syntax.LegalExpr-UTLC'),
    ('TypeTheory', 'Lambda.apply'): ('TypeTheory', 'Syntax.apply-UTLC'),
    ('TypeTheory', 'Type.Expr-UTLC.apply'): ('TypeTheory', 'Syntax.Expr-UTLC.apply'),
    ('TypeTheory', 'Type.Expr-UTLC.bvar'): ('TypeTheory', 'Syntax.Expr-UTLC.bvar'),
    ('TypeTheory', 'Type.Expr-UTLC.lambda'): ('TypeTheory', 'Syntax.Expr-UTLC.lambda'),
}
RETIRED = tuple(('FulcrumsMathNotes', name) for name in
                ('def-hyp', 'thm-hyp', 'def-inductive-hyp', 'def-hyp-opq'))
CLOSURE = SURVIVING_CLOSURE + tuple(MIGRATIONS.values())

# These are the established labels in Mathematics/03-TypeTheory/export.typ.
TARGET_OVERRIDES = {
    ("BasicOperators", "Nat"): "NaturalNumber",
    ("TypeTheory", "Type"): "Type",
}


class ValidationError(ValueError):
    pass


def _logical_key(package: str, name: str) -> str:
    return f"{package}:{name}"


def expected_binding(package: str, name: str) -> str:
    """Return the stored identifier; exporters consume it and never derive it."""
    slug = re.sub(r"[^A-Za-z0-9_]", "_", f"{package}_{name}")
    digest = hashlib.sha256(_logical_key(package, name).encode("utf-8")).hexdigest()[:10]
    binding = f"snl_macro_{slug}_{digest}"
    if not IDENTIFIER_RE.fullmatch(binding):
        raise AssertionError(f"internal invalid Typst binding {binding!r}")
    return binding


def option_link_target(package: str, name: str) -> str:
    return TARGET_OVERRIDES.get((package, name), name)


def expected_declaration_text(package: str, name: str) -> str:
    binding = expected_binding(package, name)
    target = option_link_target(package, name)
    return (
        f'#let {binding} = (children, style: none) => '
        f'optionLink({json.dumps(target, ensure_ascii=False)}, '
        f'snl-render-macro-template({json.dumps(package)}, {json.dumps(name)}, '
        'children, style: style))'
    )


def expected_extension(package: str, name: str) -> dict[str, Any]:
    text = expected_declaration_text(package, name)
    return {
        "binding": expected_binding(package, name),
        "declaration": {
            "type": "i18n",
            "default_language": DEFAULT_LANGUAGE,
            "values": {locale: text for locale in LOCALES},
        },
    }


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def validate_extension(package: str, name: str, value: Any) -> None:
    extension = _require_dict(value, EXTENSION_KEY)
    if set(extension) != {"binding", "declaration"}:
        raise ValidationError(f"{_logical_key(package, name)} extension must contain binding and declaration only")
    binding = extension.get("binding")
    expected = expected_binding(package, name)
    if binding != expected or not isinstance(binding, str) or not IDENTIFIER_RE.fullmatch(binding):
        raise ValidationError(f"{_logical_key(package, name)} binding must be {expected!r}")

    declaration = _require_dict(extension.get("declaration"), "declaration")
    if set(declaration) != {"type", "default_language", "values"} or declaration.get("type") != "i18n":
        raise ValidationError(f"{_logical_key(package, name)} declaration must be an exact i18n declaration")
    default = declaration.get("default_language")
    values = _require_dict(declaration.get("values"), "declaration.values")
    if default != DEFAULT_LANGUAGE or default not in values:
        raise ValidationError(f"{_logical_key(package, name)} declaration default projection is missing or wrong")
    if set(values) != set(LOCALES):
        raise ValidationError(f"{_logical_key(package, name)} declaration must have exactly zh-CN and en values")

    expected_text = expected_declaration_text(package, name)
    signatures: set[str] = set()
    for locale in LOCALES:
        text = values.get(locale)
        if not isinstance(text, str) or len(LET_RE.findall(text)) != 1:
            raise ValidationError(f"{_logical_key(package, name)} {locale} must contain exactly one #let")
        match = re.fullmatch(
            rf'#let\s+{re.escape(binding)}\s*=\s*(\(children, style: none\))\s*=>\s*(.+)',
            text,
        )
        if not match:
            raise ValidationError(f"{_logical_key(package, name)} {locale} has signature drift or malformed declaration")
        signatures.add(match.group(1))
        if text != expected_text:
            raise ValidationError(f"{_logical_key(package, name)} {locale} declaration does not match its stored target/runtime contract")
    if len(signatures) != 1:
        raise ValidationError(f"{_logical_key(package, name)} locale projections have signature drift")


def validate_binding_set(items: Iterable[tuple[str, str, Any]]) -> None:
    owners: dict[str, str] = {}
    for package, name, extension in items:
        binding = _require_dict(extension, EXTENSION_KEY).get("binding")
        if not isinstance(binding, str):
            raise ValidationError(f"{_logical_key(package, name)} binding must be a string")
        previous = owners.get(binding)
        if previous is not None:
            raise ValidationError(f"duplicate binding {binding!r}: {previous} and {_logical_key(package, name)}")
        owners[binding] = _logical_key(package, name)


def entity_identity_hash(kind: str, *segments: str) -> str:
    raw = f"snl-doc/v1\0{kind}\0" + "\0".join(segments)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def expected_macro_filename(package: str, name: str) -> str:
    return f"{package}-{entity_identity_hash('macro', package, name)}.json"


def _macro_index(root: Path) -> dict[tuple[str, str], tuple[Path, dict[str, Any]]]:
    index: dict[tuple[str, str], tuple[Path, dict[str, Any]]] = {}
    for path in sorted((root / ".SNL_Doc" / "macros").glob("*.json")):
        envelope = json.loads(path.read_text(encoding="utf-8"))
        package = envelope.get("package")
        macro = envelope.get("macro")
        name = macro.get("name") if isinstance(macro, dict) else None
        if isinstance(package, str) and isinstance(name, str):
            key = (package, name)
            if key in index:
                raise ValidationError(f"duplicate Macro identity {_logical_key(*key)}")
            index[key] = (path, envelope)
    return index


def validate_workspace(root: Path | str) -> dict[str, Any]:
    root = Path(root)
    index = _macro_index(root)
    wanted = set(CLOSURE)
    if len(CLOSURE) != 59 or len(wanted) != 59:
        raise ValidationError("reviewed closure must contain exactly 59 unique Macro identities")
    missing = sorted(wanted - set(index))
    if missing:
        raise ValidationError(f"missing closure Macros: {missing}")

    items: list[tuple[str, str, Any]] = []
    identity_errors: list[str] = []
    for package, name in CLOSURE:
        path, envelope = index[(package, name)]
        if path.name != expected_macro_filename(package, name):
            identity_errors.append(f"{_logical_key(package, name)} -> {path.name}")
        if envelope.get("format") != "snl-macro" or envelope.get("version") != 1 or envelope.get("package") != package:
            raise ValidationError(f"invalid Macro envelope for {_logical_key(package, name)}")
        macro = _require_dict(envelope.get("macro"), "macro")
        if "typst" in macro:
            raise ValidationError("reserved Macro-level typst key: use x_fulcrum_typst")
        validate_extension(package, name, macro.get(EXTENSION_KEY))
        items.append((package, name, macro[EXTENSION_KEY]))
    validate_binding_set(items)
    if identity_errors:
        raise ValidationError(f"hashed filename identity errors: {identity_errors}")

    extras = []
    for (package, name), (_, envelope) in index.items():
        macro = envelope["macro"]
        if EXTENSION_KEY in macro and (package, name) not in wanted:
            extras.append(_logical_key(package, name))
    if extras:
        raise ValidationError(f"extension appears outside the exact closure: {sorted(extras)}")
    return {
        "macro_count": len(items),
        "package_count": len({package for package, _ in CLOSURE}),
        "bindings": len(items),
        "duplicate_bindings": [],
        "identity_errors": identity_errors,
    }



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate_workspace(args.workspace)
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
