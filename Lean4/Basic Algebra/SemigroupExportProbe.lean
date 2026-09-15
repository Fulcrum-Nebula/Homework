import SNL4Lean
import Mathlib.Algebra.Group.Defs

-- This diagnostic needs only the native declaration and the production HMul
-- registry. Do not pull in every algebra/field/Finset terminology module.
snl_notation Semigroup => %#0 is a semigroup%
snl_notation "Semigroup" CN => %#0 是半群%

/-!
Combines the historical ProbeSemigroup and ProbeHMul diagnostics. This is a
native-export regression, not a handwritten replacement for a native AST.
Run from the repository root with its pinned dependencies:
  lake env lean -j2 'Lean4/Basic Algebra/SemigroupExportProbe.lean'
-/
open Lean Elab Command Term Meta
open SNL4Lean

private partial def collectHMul (tree : SnlSyntaxTree) : List SnlSyntaxTree :=
  let below := tree.children.toList.flatMap collectHMul
  if tree.macro_name == "HMul.hMul" then tree :: below else below

#print Semigroup
#snl_print Semigroup

#eval show CommandElabM Unit from liftTermElabM do
  let entry ← declarationToSnlEntry ``Semigroup
  let some tree := entry.declarationTree?
    | throwError "Semigroup declaration tree missing"
  let nodes := collectHMul tree
  if nodes.isEmpty then
    throwError "Semigroup declaration contains no HMul.hMul nodes"
  let some m := findSnlMacroInEnv? (← getEnv) "HMul.hMul"
    | throwError "HMul macro missing"
  if m.styles.isEmpty then
    throwError "HMul styles missing"
  for node in nodes do
    -- The registered native HMul template selects the two trailing factors.
    if node.children.size != 6 then
      throwError "HMul.hMul must retain six semantic arguments, got {node.children.size}"
    IO.println s!"HMul children: {node.children.map (·.macro_name) |>.toList}"
  IO.println s!"HMul template: {m.styles[0]!.template}"
  IO.println (Lean.toJson entry).compress
