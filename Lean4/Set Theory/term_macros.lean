import Lean4.Functions.term_macros
import Mathlib.Data.Set.Basic
import Mathlib.Data.Set.Operations
import Mathlib.Order.SetNotation
import Mathlib.Data.Finite.Defs
import Mathlib.Logic.Pairwise

/-!
# Set-theory terminology (Lean / Mathlib 4.28.0)

Full Expr child indices include implicit type parameters. These registrations
are for the native declarations, not newly defined mathematical aliases.
`SurjOn` only asserts coverage of the target: unlike `BijOn`, it does not assert
that every source element maps into that target. `InvOn` similarly asserts the
two inverse identities, not additional set-mapping hypotheses.
-/

namespace SNL4Lean

-- Formula defaults formerly supplied by SNL4Lean.TermMacros.Mathlib.
-- Keep these before the consumer-owned named English styles below.
-- Match Mathlib.Data.SProd's right-associative binding power 82; the full
-- child vector includes the two implicit carrier types.

-- Surface syntax `s ×ˢ t` elaborates to the overloaded projection, not Set.prod.

-- Existing upstream formula defaults remain intact; only named styles are new.

-- Mathlib/
--   Data/
--     Finite/
--       Defs.lean
snl_notation Set.Finite => %#1 is finite%
snl_notation Set.Infinite => %#1 is infinite%

-- Mathlib/
--   Data/
--     SProd.lean
snl_notation SProd.sprod => $#4 \times #5$ : [0, 0, 0, 0, 83, 82] -> 82

-- Mathlib/
--   Data/
--     Set/
--       CoeSort.lean
snl_macro { name := "Set.Elem", kind := "const", mode := "formula_inline", template := "\\operatorname{Elem}(#1)" }

-- Mathlib/
--   Data/
--     Set/
--       Defs.lean
snl_notation Set => $\operatorname{Set} #0$
snl_macro { name := "setOf", kind := "const", mode := "formula_inline", template := "\\operatorname{setOf}\\left(#1\\right)" }
snl_macro { name := "Set.Mem", kind := "const", mode := "formula_inline", template := "#2 \\in #1" }
snl_notation Set.Subset => $#1 \subseteq #2$
snl_notation Set.Subset[english] => %#1 is a subset of #2%
snl_macro { name := "Set.univ", kind := "const", mode := "formula_inline", template := "\\mathsf{U}" }
snl_macro { name := "Set.insert", kind := "const", mode := "formula_inline", template := "\\left\\{#1\\right\\} \\cup #2" }
snl_macro { name := "Set.singleton", kind := "const", mode := "formula_inline", template := "\\left\\{#1\\right\\}" }
snl_notation Set.union => $#1 \cup #2$
snl_notation Set.inter => $#1 \cap #2$
snl_notation Set.compl => $#1^{\mathsf c}$
snl_notation Set.diff => $#1 \setminus #2$
snl_macro { name := "Set.powerset", kind := "const", mode := "formula_inline", template := "\\mathcal{P}(#1)" }
snl_macro { name := "Set.image", kind := "const", mode := "formula_inline", template := "#2 '' #3" }
snl_macro { name := "Set.Nonempty", kind := "const", mode := "formula_inline", template := "#1 \\ne \\varnothing" }
snl_notation Set.Nonempty[english] => %#1 is nonempty%

-- Mathlib/
--   Data/
--     Set/
--       Operations.lean
snl_macro { name := "Set.preimage", kind := "const", mode := "formula_inline", template := "#2^{-1}(#3)" }
snl_notation Set.range => $\operatorname{range}(#2)$
snl_notation Set.prod => $#2 \times #3$ : [0, 0, 83, 82] -> 82
snl_notation Set.diagonal => $\Delta_{#0}$
snl_notation Set.offDiag => $\operatorname{offDiag}(#1)$
snl_notation Set.EqOn => %#2 and #3 agree on #4%
snl_notation Set.MapsTo => %#2 maps #3 into #4%
snl_notation Set.InjOn => %#2 is injective on #3%
snl_notation Set.graphOn => $\operatorname{graph}_{#3}(#2)$
snl_notation Set.SurjOn => %every element of #4 is the image under #2 of an element of #3%
snl_notation Set.BijOn => %#2 is a bijection from #3 onto #4%
snl_notation Set.LeftInvOn => %#2 is a left inverse of #3 on #4%
snl_notation Set.RightInvOn => %#2 is a right inverse of #3 on #4%
snl_notation Set.InvOn => %#2 is a left inverse of #3 on #4 and a right inverse of #3 on #5%

-- Mathlib/
--   Logic/
--     Pairwise.lean
snl_notation Set.Pairwise => %#2 holds for every ordered pair of distinct elements of #1%

-- Mathlib/
--   Order/
--     Notation.lean
snl_notation Compl.compl => $#2^{\mathsf c}$

-- Mathlib/
--   Order/
--     SetNotation.lean
snl_macro { name := "Set.sInter", kind := "const", mode := "formula_inline", template := "\\bigcap #1" }
snl_macro { name := "Set.sUnion", kind := "const", mode := "formula_inline", template := "\\bigcup #1" }
snl_macro { name := "Set.iUnion", kind := "const", mode := "formula_inline", template := "\\bigcup #2" }
snl_macro { name := "Set.iInter", kind := "const", mode := "formula_inline", template := "\\bigcap #2" }


-- Canonical authoring alignment: native full slots and retained named styles.
snl_macro { name := "Fulcrum.BinaryOperation", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{Bop}(#0)" }
snl_macro { name := "Fulcrum.BinaryOperation", style := "authored", kind := "const", mode := "formula_inline", template := "\\operatorname{Bop}(#0)" }
snl_macro { name := "Fulcrum.BinaryOperation.apply", style := "default", kind := "const", mode := "formula_inline", template := "#2#1#3" }
snl_macro { name := "Fulcrum.BinaryOperation.apply", style := "conj", kind := "const", mode := "formula_inline", template := "#2#1#3" }
snl_macro { name := "Fulcrum.BinaryOperation.apply", style := "paren", kind := "const", mode := "formula_inline", template := "\\left(#2#1#3\\right)" }
snl_macro { name := "SetRel", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{SetRel}(#0,#1)" }
snl_macro { name := "SetRel", style := "authored", kind := "const", mode := "formula_inline", template := "\\operatorname{Rl}(#0, #1)" }
snl_macro { name := "Set", style := "text", kind := "const", mode := "formula_inline", template := "\\operatorname{Set}#0" }
snl_macro { name := "Set", style := "paren", kind := "const", mode := "formula_inline", template := "\\operatorname{Set}\\left(#0\\right)" }
snl_macro { name := "Set.Mem", style := "authored", kind := "const", mode := "formula_inline", template := "#2 \\in #1" }
snl_macro { name := "Set.Mem", style := "single", kind := "const", mode := "formula_inline", template := "\\in" }
snl_macro { name := "Set.Subset", style := "infix", kind := "const", mode := "formula_inline", template := "#1 \\subseteq #2" }
snl_macro { name := "EmptyCollection.emptyCollection", style := "round", kind := "const", mode := "formula_inline", template := "\\varnothing" }
snl_macro { name := "EmptyCollection.emptyCollection", style := "slim", kind := "const", mode := "formula_inline", template := "\\emptyset" }
snl_macro { name := "Set.univ", style := "typed", kind := "const", mode := "formula_inline", template := "\\mathcal{U}_{#0}" }
snl_macro { name := "Set.univ", style := "untyped", kind := "const", mode := "formula_inline", template := "\\mathcal{U}" }
snl_macro { name := "Set.union", style := "authored", kind := "const", mode := "formula_inline", template := "#1 \\cup #2" }
snl_macro { name := "Set.inter", style := "authored", kind := "const", mode := "formula_inline", template := "#1 \\cap #2" }
snl_macro { name := "Set.compl", style := "sup", kind := "const", mode := "formula_inline", template := "#1^{\\mathrm{C}}" }
snl_macro { name := "Set.compl", style := "prefix", kind := "const", mode := "formula_inline", template := "\\complement #1" }
snl_macro { name := "Set.compl", style := "overline", kind := "const", mode := "formula_inline", template := "\\overline{#1}" }
snl_macro { name := "Set.diff", style := "backslash", kind := "const", mode := "formula_inline", template := "#1 \\setminus #2" }
snl_macro { name := "Set.diff", style := "sub", kind := "const", mode := "formula_inline", template := "#1 - #2" }
snl_macro { name := "Set.diff", style := "relative_sup", kind := "const", mode := "formula_inline", template := "#2^{\\mathrm{C}}" }
snl_macro { name := "Set.diff", style := "relative_prefix", kind := "const", mode := "formula_inline", template := "\\complement #2" }
snl_macro { name := "Set.diff", style := "relative_overline", kind := "const", mode := "formula_inline", template := "\\overline{#2}" }
snl_macro { name := "Set.powerset", style := "script", kind := "const", mode := "formula_inline", template := "\\mathcal{P}(#1)" }
snl_macro { name := "Set.powerset", style := "exponential", kind := "const", mode := "formula_inline", template := "2^{#1}" }
snl_macro { name := "Set.prod", style := "authored", kind := "const", mode := "formula_inline", template := "#2 \\times #3" }
snl_macro { name := "symmDiff", style := "default", kind := "const", mode := "formula_inline", template := "#3\\mathbin{\\triangle}#4" }
snl_macro { name := "symmDiff", style := "infix", kind := "const", mode := "formula_inline", template := "#3 \\triangle #4" }
snl_macro { name := "Fulcrum.SetFunction.domain", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{dom}(#4)" }
snl_macro { name := "Fulcrum.SetFunction.domain", style := "authored", kind := "const", mode := "formula_inline", template := "\\operatorname{dom}#4" }
snl_macro { name := "Fulcrum.SetFunction.codomain", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{codom}(#4)" }
snl_macro { name := "Fulcrum.SetFunction.codomain", style := "authored", kind := "const", mode := "formula_inline", template := "\\operatorname{codom}#4" }
snl_macro { name := "Set.range", style := "op_im", kind := "const", mode := "formula_inline", template := "\\operatorname{im}#2" }
snl_macro { name := "Set.range", style := "op_ran", kind := "const", mode := "formula_inline", template := "\\operatorname{ran}#2" }
snl_macro { name := "Set.image", style := "authored", kind := "const", mode := "formula_inline", template := "#2(#3)" }
snl_macro { name := "Set.preimage", style := "authored", kind := "const", mode := "formula_inline", template := "#2^{-1}(#3)" }
snl_macro { name := "Function.graph", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{graph}(#2)" }
snl_macro { name := "Function.graph", style := "authored", kind := "const", mode := "formula_inline", template := "\\Gamma(#2)" }
snl_macro { name := "Function.Injective", style := "authored", kind := "const", mode := "formula_inline", template := "#2\\text{ 是单射}" }
snl_macro { name := "Function.Surjective", style := "authored", kind := "const", mode := "formula_inline", template := "#2\\text{ 是满射}" }
snl_macro { name := "Function.Surjective", style := "arrow", kind := "const", mode := "formula_inline", template := "#2:#0\\twoheadrightarrow #1" }
snl_macro { name := "Function.Bijective", style := "authored", kind := "const", mode := "formula_inline", template := "#2\\text{ 是双射}" }
snl_macro { name := "Equiv.symm", style := "default", kind := "const", mode := "formula_inline", template := "#2^{-1}" }
snl_macro { name := "Equiv.symm", style := "authored", kind := "const", mode := "formula_inline", template := "#2 ^{-1}" }
snl_macro { name := "Equiv.symm", style := "paren", kind := "const", mode := "formula_inline", template := "(#2)^{-1}" }
snl_macro { name := "Cardinal.mk", style := "default", kind := "const", mode := "formula_inline", template := "\\# #0" }
snl_macro { name := "Cardinal.mk", style := "op_card", kind := "const", mode := "formula_inline", template := "\\operatorname{card}#0" }
snl_macro { name := "Cardinal.mk", style := "vert", kind := "const", mode := "formula_inline", template := "\\left\\lvert #0 \\right\\rvert" }
snl_macro { name := "Set.Finite", style := "text", kind := "const", mode := "formula_inline", template := "#1\\text{ 是有限集}" }
snl_macro { name := "Set.Countable", style := "default", kind := "const", mode := "formula_inline", template := "#1\\text{ is at most countable}" }
snl_macro { name := "Prod.mk", style := "authored", kind := "const", mode := "formula_inline", template := "\\left(#2, #3\\right)" }
snl_macro { name := "RelIso", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{RelIso}(#2,#3)" }
snl_macro { name := "IsStrictOrder", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{IsStrictOrder}(#0,#1)" }
snl_macro { name := "IsStrictOrder", style := "variant", kind := "const", mode := "formula_inline", template := "\\operatorname{IsStrictOrder}(#0,#1)" }
snl_macro { name := "IsStrictTotalOrder", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{IsStrictTotalOrder}(#0,#1)" }
snl_macro { name := "IsStrictTotalOrder", style := "variant", kind := "const", mode := "formula_inline", template := "\\operatorname{IsStrictTotalOrder}(#0,#1)" }
snl_macro { name := "IsGreatest", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is greatest in }#2" }
snl_macro { name := "IsGreatest", style := "text", kind := "const", mode := "formula_inline", template := "#3\\text{ is greatest in }#2" }
snl_macro { name := "IsGreatest", style := "simple", kind := "const", mode := "formula_inline", template := "#3\\text{ is greatest in }#2" }
snl_macro { name := "IsLeast", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is least in }#2" }
snl_macro { name := "IsLeast", style := "text", kind := "const", mode := "formula_inline", template := "#3\\text{ is least in }#2" }
snl_macro { name := "IsLeast", style := "simple", kind := "const", mode := "formula_inline", template := "#3\\text{ is least in }#2" }
snl_macro { name := "Maximal", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is maximal in }#2" }
snl_macro { name := "Maximal", style := "full", kind := "const", mode := "formula_inline", template := "#3\\text{ is maximal in }#2" }
snl_macro { name := "Minimal", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is minimal in }#2" }
snl_macro { name := "Minimal", style := "full", kind := "const", mode := "formula_inline", template := "#3\\text{ is minimal in }#2" }
snl_macro { name := "upperBounds", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{upperBounds}(#2)" }
snl_macro { name := "upperBounds", style := "simple", kind := "const", mode := "formula_inline", template := "\\operatorname{upperBounds}(#2)" }
snl_macro { name := "lowerBounds", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{lowerBounds}(#2)" }
snl_macro { name := "lowerBounds", style := "simple", kind := "const", mode := "formula_inline", template := "\\operatorname{lowerBounds}(#2)" }
snl_macro { name := "IsLUB", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is a least upper bound of }#2" }
snl_macro { name := "IsLUB", style := "full", kind := "const", mode := "formula_inline", template := "#3\\text{ is a least upper bound of }#2" }
snl_macro { name := "IsGLB", style := "default", kind := "const", mode := "formula_inline", template := "#3\\text{ is a greatest lower bound of }#2" }
snl_macro { name := "IsGLB", style := "full", kind := "const", mode := "formula_inline", template := "#3\\text{ is a greatest lower bound of }#2" }
snl_macro { name := "setOf", style := "builder", kind := "const", mode := "formula_inline", template := "\\left\\{#0\\mid #2\\right\\}" }
snl_macro { name := "setOf", style := "typedBuilder", kind := "const", mode := "formula_inline", template := "\\left\\{#0:#1\\mid #2\\right\\}" }
snl_macro { name := "Cardinal", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{Cardinal}" }
snl_macro { name := "Countable", style := "default", kind := "const", mode := "formula_inline", template := "#0\\text{ is at most countable}" }
snl_macro { name := "Denumerable", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{Denumerable}(#0)" }
snl_macro { name := "Rel", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{Rel}(#0,#1)" }
snl_macro { name := "sSup", style := "default", kind := "const", mode := "formula_inline", template := "\\sup #2" }
snl_macro { name := "Nat.succ", style := "function", kind := "const", mode := "formula_inline", template := "\\operatorname{succ}" }
snl_macro { name := "PSet.ofNat", style := "default", kind := "const", mode := "formula_inline", template := "\\operatorname{PSet.ofNat}(#0)" }
snl_macro { name := "Set.Elem", style := "coerce", kind := "const", mode := "formula_inline", template := "#1" }
snl_macro { name := "Set.insert", style := "enumOuter", kind := "const", mode := "formula_inline", template := "\\left\\{#1,#2\\right\\}" }
snl_macro { name := "Set.insert", style := "enumInner", kind := "const", mode := "formula_inline", template := "#1,#2" }
snl_macro { name := "Set.singleton", style := "enumInner", kind := "const", mode := "formula_inline", template := "#1" }

/-- A set builder is a presentation view of `setOf`, not a new logical constant.
The original expression and lambda's binding evidence remain on the raw tree. -/
@[snl_app_delab setOf]
meta def delabSetBuilder : SnlAppDelab := fun expr tree => do
  let args := expr.consumeMData.getAppArgs
  unless args.size == 2 && tree.children.size == 2 do return none
  let .lam .. := args[1]!.consumeMData | return none
  let family := tree.children[1]!
  unless family.kind == "rule" && family.macro_name == "Type.lambda" &&
      family.children.size == 3 do return none
  return some {
    macro_name := "setOf", kind := "const", style_name? := some "typedBuilder"
    children := #[withLeanSourcePath family.children[0]! #[1, 0],
      withLeanSourcePath family.children[1]! #[1, 1],
      withLeanSourcePath family.children[2]! #[1, 2]]
    mdata := Lean.Json.mkObj [
      ("leanDelabOrigin", Lean.toJson "setOf"),
      ("leanBinderScope", Lean.Json.mkObj [
        ("binder", Lean.toJson (0 : Nat)), ("bodies", Lean.toJson (#[2] : Array Nat))])]
  }

-- Structural primitives used in the native set/order declarations.
snl_macro { name := "LE.le", kind := "const", mode := "formula_inline", template := "#2\\le #3" }
snl_macro { name := "LT.lt", kind := "const", mode := "formula_inline", template := "#2<#3" }
snl_macro { name := "LE", kind := "const", mode := "formula_inline", template := "\\operatorname{LE}(#0)" }
snl_macro { name := "LT", kind := "const", mode := "formula_inline", template := "\\operatorname{LT}(#0)" }
snl_macro { name := "Finite", kind := "const", mode := "formula_inline", template := "\\operatorname{Finite}(#0)" }
snl_macro { name := "Equiv.mk", kind := "const", mode := "formula_inline", template := "\\left\\langle #2,#3,#4,#5\\right\\rangle" }
snl_macro { name := "Equiv.toFun", kind := "const", mode := "formula_inline", template := "#2" }
snl_macro { name := "Equiv.invFun", kind := "const", mode := "formula_inline", template := "#2^{-1}" }
snl_macro { name := "Equiv.left_inv", kind := "const", mode := "formula_inline", template := "\\mathsf{left\\_inv}(#2)" }
snl_macro { name := "Equiv.right_inv", kind := "const", mode := "formula_inline", template := "\\mathsf{right\\_inv}(#2)" }
snl_macro { name := "Std.Irrefl", kind := "const", mode := "formula_inline", template := "\\operatorname{Irrefl}(#1)" }
snl_macro { name := "IsTrans", kind := "const", mode := "formula_inline", template := "\\operatorname{IsTrans}(#1)" }
snl_macro { name := "PartialOrder", kind := "const", mode := "formula_inline", template := "\\operatorname{PartialOrder}(#0)" }
snl_macro { name := "LinearOrder", kind := "const", mode := "formula_inline", template := "\\operatorname{LinearOrder}(#0)" }

end SNL4Lean
