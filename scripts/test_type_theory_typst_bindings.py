#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "type_theory_typst_bindings.py"
spec = importlib.util.spec_from_file_location("type_theory_typst_bindings", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
bindings = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bindings
spec.loader.exec_module(bindings)


class ExtensionValidationTests(unittest.TestCase):
    def setUp(self):
        self.package = "TypeTheory"
        self.name = "Type"
        self.extension = bindings.expected_extension(self.package, self.name)

    def assert_invalid(self, extension, pattern):
        with self.assertRaisesRegex(bindings.ValidationError, pattern):
            bindings.validate_extension(self.package, self.name, extension)

    def test_expected_extension_has_fixed_i18n_contract(self):
        bindings.validate_extension(self.package, self.name, self.extension)
        declaration = self.extension["declaration"]
        self.assertEqual(declaration["type"], "i18n")
        self.assertEqual(declaration["default_language"], "zh-CN")
        self.assertEqual(set(declaration["values"]), {"zh-CN", "en"})
        self.assertEqual(declaration["values"]["zh-CN"], declaration["values"]["en"])
        self.assertIn('optionLink("Type",', declaration["values"]["en"])
        self.assertIn('snl-render-macro-template("TypeTheory", "Type", children, style: style)', declaration["values"]["en"])

    def test_rejects_malformed_extension(self):
        self.assert_invalid({"binding": "x"}, "declaration")

    def test_rejects_wrong_binding(self):
        value = copy.deepcopy(self.extension)
        value["binding"] = "wrong_binding"
        self.assert_invalid(value, "binding")

    def test_rejects_missing_default_projection(self):
        value = copy.deepcopy(self.extension)
        del value["declaration"]["values"]["zh-CN"]
        self.assert_invalid(value, "default")

    def test_rejects_no_let(self):
        value = copy.deepcopy(self.extension)
        value["declaration"]["values"]["en"] = "optionLink(\"Type\", [])"
        self.assert_invalid(value, "exactly one #let")

    def test_rejects_multiple_lets(self):
        value = copy.deepcopy(self.extension)
        value["declaration"]["values"]["en"] += "\n#let extra = 1"
        self.assert_invalid(value, "exactly one #let")

    def test_rejects_signature_drift(self):
        value = copy.deepcopy(self.extension)
        value["declaration"]["values"]["en"] = value["declaration"]["values"]["en"].replace(
            "(children, style: none)", "children"
        )
        self.assert_invalid(value, "signature|declaration")

    def test_natural_number_target_preserves_original_export_mapping(self):
        value = bindings.expected_extension("BasicOperators", "Nat")
        self.assertIn('optionLink("NaturalNumber",', value["declaration"]["values"]["zh-CN"])


class CorpusValidationTests(unittest.TestCase):
    def test_historical_contract_is_explicit_not_silently_filtered(self):
        self.assertEqual(len(bindings.ORIGINAL_CLOSURE), 63)
        self.assertEqual(len(set(bindings.ORIGINAL_CLOSURE) - set(bindings.CLOSURE)), 17)
        self.assertTrue(set(bindings.CLOSURE) < set(bindings.ORIGINAL_CLOSURE))
        items = []
        for package, name in bindings.ORIGINAL_CLOSURE:
            extension = bindings.expected_extension(package, name)
            bindings.validate_extension(package, name, extension)
            items.append((package, name, extension))
        bindings.validate_binding_set(items)

    def test_real_workspace_is_exact_validated_closure(self):
        report = bindings.validate_workspace(ROOT)
        self.assertEqual(report["macro_count"], 46)
        self.assertEqual(report["package_count"], 5)
        self.assertEqual(report["bindings"], 46)
        self.assertEqual(report["duplicate_bindings"], [])
        self.assertEqual(report["identity_errors"], [])

    def test_validator_rejects_copied_macro_binding_collision(self):
        first = bindings.expected_extension("TypeTheory", "Type")
        second = copy.deepcopy(first)
        with self.assertRaisesRegex(bindings.ValidationError, "duplicate binding"):
            bindings.validate_binding_set([
                ("TypeTheory", "Type", first),
                ("TypeTheory", "CopiedType", second),
            ])


if __name__ == "__main__":
    unittest.main()
