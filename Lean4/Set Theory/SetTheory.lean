import Mathlib.Data.Countable.Defs
import Mathlib.Data.Finite.Defs
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Rel
import Mathlib.Data.Set.Countable
import Mathlib.Data.Set.Defs
import Mathlib.Data.Set.Operations
import Mathlib.Logic.Denumerable
import Mathlib.Logic.Equiv.Defs
import Mathlib.Logic.Equiv.Set
import Mathlib.Logic.Function.Defs
import Mathlib.Order.Bounds.Defs
import Mathlib.Order.Defs.Unbundled
import Mathlib.Order.RelClasses
import Mathlib.Order.RelIso.Basic
import Mathlib.Order.SymmDiff
import Mathlib.SetTheory.Cardinal.Defs
import Mathlib.SetTheory.Cardinal.Order
import Mathlib.SetTheory.ZFC.PSet
import Lean4.«Set Theory».term_macros_CN

/-!
# Set theory: native declaration navigation

The mathematical declarations below are imported, not redefined. Each native
print is followed immediately by its SNL view. Canonical document Pointers use
the original declaration when it is available within the workspace.
-/


/-! These accessors retain the original domain/codomain *sets*. They are not
`SetRel.dom`/`SetRel.cod`, and do not confuse a declared codomain with an image. -/
namespace Fulcrum.SetFunction
universe u v
def domain {S : Type u} {T : Type v} {D : Set S} {A : Set T}
    (_f : D → A) : Set S := D
#snl_print domain
def codomain {S : Type u} {T : Type v} {D : Set S} {A : Set T}
    (_f : D → A) : Set T := A
#snl_print codomain
end Fulcrum.SetFunction

namespace Fulcrum
universe u
/-- A binary operation on a carrier, without additional algebraic axioms. -/
def BinaryOperation (α : Type u) := α → α → α
#snl_print BinaryOperation
/-- Evaluation of a binary operation; the named node retains infix display. -/
def BinaryOperation.apply {α : Type u} (op : BinaryOperation α) (a b : α) : α :=
  op a b
#snl_print BinaryOperation.apply
end Fulcrum

namespace Fulcrum.SetTheory

universe u v

section Context
variable (T : Type u)
variable (S : Type v)
variable (A B : Set T)
variable (D : Set S)
variable (f : D → A)
end Context

section Basics
#print Set
#snl_print Set
#print setOf
#snl_print setOf
#print Set.Mem
#snl_print Set.Mem
#print Set.instEmptyCollection
#snl_print Set.instEmptyCollection
#print Set.univ
#snl_print Set.univ
end Basics

section Relations
/-- Nonmembership is negated membership, not an additional set primitive. -/
theorem not_mem_iff {α : Type u} (s : Set α) (a : α) :
    a ∉ s ↔ ¬ a ∈ s := Iff.rfl
#snl_print not_mem_iff
#print Set.Subset
#snl_print Set.Subset
#print Set.ext
#snl_print Set.ext
#print Set.ext_iff
#snl_print Set.ext_iff
#print SetRel
#snl_print SetRel
#print Rel
#snl_print Rel
#print subset_antisymm_iff
#snl_print subset_antisymm_iff
end Relations

section Operations
#print Set.insert
#snl_print Set.insert
#print Set.singleton
#snl_print Set.singleton
#print Set.union
#snl_print Set.union
#print Set.inter
#snl_print Set.inter
#print Set.compl
#snl_print Set.compl
#print Set.diff
#snl_print Set.diff
#print Set.powerset
#snl_print Set.powerset
#print Set.Nonempty
#snl_print Set.Nonempty
#print Set.prod
#snl_print Set.prod
#print symmDiff
#snl_print symmDiff
end Operations

section Functions
#print Set.range
#snl_print Set.range
#print Set.image
#snl_print Set.image
#print Set.preimage
#snl_print Set.preimage
#print Set.graphOn
#snl_print Set.graphOn
#print Function.Injective
#snl_print Function.Injective
#print Function.Surjective
#snl_print Function.Surjective
#print Function.Bijective
#snl_print Function.Bijective
#print Function.graph
#snl_print Function.graph
#print Equiv
#snl_print Equiv
#print Equiv.toFun
#snl_print Equiv.toFun
#print Equiv.right_inv
#snl_print Equiv.right_inv
#print Equiv.left_inv
#snl_print Equiv.left_inv
#print Equiv.invFun
#snl_print Equiv.invFun
#print Equiv.ofInjective
#snl_print Equiv.ofInjective
#print Equiv.symm
#snl_print Equiv.symm
#print Equiv.apply_eq_iff_eq_symm_apply
#snl_print Equiv.apply_eq_iff_eq_symm_apply
end Functions

section Cardinality
/-! Countable means *at most* countable. Denumerable is enumeration data;
its existence is the countably-infinite condition. Cardinal is constructed
from equivalence classes of types, without first constructing Ordinal. -/
#print Cardinal
#snl_print Cardinal
#print Cardinal.mk
#snl_print Cardinal.mk
#print Cardinal.eq
#snl_print Cardinal.eq
#print Set.Finite
#snl_print Set.Finite
#print finite_iff_exists_equiv_fin
#snl_print finite_iff_exists_equiv_fin
#print Countable
#snl_print Countable
#print Countable.exists_injective_nat'
#snl_print Countable.exists_injective_nat'
#print Set.Countable
#snl_print Set.Countable
#print Set.countable_iff_exists_injective
#snl_print Set.countable_iff_exists_injective
#print Denumerable
#snl_print Denumerable
#print Denumerable.decode_inv
#snl_print Denumerable.decode_inv
#print Denumerable.toEncodable
#snl_print Denumerable.toEncodable
#print nonempty_denumerable_iff
#snl_print nonempty_denumerable_iff
#print Cardinal.cantor
#snl_print Cardinal.cantor
#print Cardinal.mk_powerset
#snl_print Cardinal.mk_powerset
end Cardinality

section Order
/-! Strict relations and bundled non-strict orders are different objects.
`partialOrderOfSO r` installs x ≤ y iff x = y ∨ r x y. Bounds use that
particular order when a strict relation is the starting point. A relation
isomorphism includes an equivalence; preservation/reflection alone is not enough.
Greatest/least elements are distinct from maximal/minimal elements; `IsLUB`
and `IsGLB` do not assert existence of a globally defined sup/inf operation. -/
#print IsStrictOrder
#snl_print IsStrictOrder
#print IsStrictOrder.toIsTrans
#snl_print IsStrictOrder.toIsTrans
#print IsStrictOrder.toIrrefl
#snl_print IsStrictOrder.toIrrefl
#print IsStrictTotalOrder
#snl_print IsStrictTotalOrder
#print IsStrictTotalOrder.toTrichotomous
#snl_print IsStrictTotalOrder.toTrichotomous
#print IsStrictTotalOrder.toIsStrictOrder
#snl_print IsStrictTotalOrder.toIsStrictOrder
#print partialOrderOfSO
#snl_print partialOrderOfSO
#print IsGreatest
#snl_print IsGreatest
#print IsLeast
#snl_print IsLeast
#print Maximal
#snl_print Maximal
#print Minimal
#snl_print Minimal
#print upperBounds
#snl_print upperBounds
#print lowerBounds
#snl_print lowerBounds
#print IsGLB
#snl_print IsGLB
#print IsLUB
#snl_print IsLUB
#print RelIso
#snl_print RelIso
#print RelIso.toEquiv
#snl_print RelIso.toEquiv
#print RelIso.map_rel_iff'
#snl_print RelIso.map_rel_iff'
#print Nat.instLinearOrder
#snl_print Nat.instLinearOrder
end Order

section NaturalNumberModel
/-! `PSet.ofNat` is a von Neumann representation. It does not redefine Lean's
primitive `Nat`, its constructors, or the standard `<`/`≤` instance. -/
#print PSet.ofNat
#snl_print PSet.ofNat
#print Nat
#snl_print Nat
#print Nat.zero
#snl_print Nat.zero
#print Nat.succ
#snl_print Nat.succ
#print Nat.zero
#snl_print Nat.zero
#print Nat.succ
#snl_print Nat.succ
end NaturalNumberModel

end Fulcrum.SetTheory
