import Lean4.«Set Theory».term_macros
import Lean4.Functions.term_macros_CN

/-! Chinese projections of the existing text Styles; names, Styles and operand
indices are unchanged. Import after the base; select with `snl.language CN`. -/

-- Mathlib/
--   Data/
--     Finite/
--       Defs.lean
snl_notation "Set.Finite" CN => %#1 是有限集%
snl_notation "Set.Infinite" CN => %#1 是无限集%

-- Mathlib/
--   Data/
--     Set/
--       Defs.lean
snl_notation "Set.Subset"[english] CN => %#1 是 #2 的子集%
snl_notation "Set.Nonempty"[english] CN => %#1 非空%

-- Mathlib/
--   Data/
--     Set/
--       Operations.lean
snl_notation "Set.EqOn" CN => %#2 与 #3 在 #4 上相等%
snl_notation "Set.MapsTo" CN => %#2 将 #3 映入 #4%
snl_notation "Set.InjOn" CN => %#2 在 #3 上是单射%
snl_notation "Set.SurjOn" CN => %#4 的每个元素都是 #3 中某个元素在 #2 下的像%
snl_notation "Set.BijOn" CN => %#2 是从 #3 到 #4 的双射%
snl_notation "Set.LeftInvOn" CN => %#2 在 #4 上是 #3 的左逆%
snl_notation "Set.RightInvOn" CN => %#2 在 #4 上是 #3 的右逆%
snl_notation "Set.InvOn" CN => %#2 在 #4 上是 #3 的左逆，并在 #5 上是 #3 的右逆%

-- Mathlib/
--   Logic/
--     Pairwise.lean
snl_notation "Set.Pairwise" CN => %#2 对 #1 中每一对不同元素组成的有序对成立%

-- Chinese prose for the additional native terminology.
snl_notation "Set.Countable" CN => $#1\text{ 至多可数}$
snl_notation "IsGreatest" CN => $#3\text{ 是下列集合中的最大元：}#2$
snl_notation "IsGreatest"[text] CN => $#3\text{ 是下列集合中的最大元：}#2$
snl_notation "IsGreatest"[simple] CN => $#3\text{ 是下列集合中的最大元：}#2$
snl_notation "IsLeast" CN => $#3\text{ 是下列集合中的最小元：}#2$
snl_notation "IsLeast"[text] CN => $#3\text{ 是下列集合中的最小元：}#2$
snl_notation "IsLeast"[simple] CN => $#3\text{ 是下列集合中的最小元：}#2$
snl_notation "Maximal" CN => $#3\text{ 是下列谓词所确定集合中的极大元：}#2$
snl_notation "Maximal"[full] CN => $#3\text{ 是下列谓词所确定集合中的极大元：}#2$
snl_notation "Minimal" CN => $#3\text{ 是下列谓词所确定集合中的极小元：}#2$
snl_notation "Minimal"[full] CN => $#3\text{ 是下列谓词所确定集合中的极小元：}#2$
snl_notation "IsLUB" CN => $#3\text{ 是下列集合的上确界：}#2$
snl_notation "IsLUB"[full] CN => $#3\text{ 是下列集合的上确界：}#2$
snl_notation "IsGLB" CN => $#3\text{ 是下列集合的下确界：}#2$
snl_notation "IsGLB"[full] CN => $#3\text{ 是下列集合的下确界：}#2$
snl_notation "Countable" CN => $#0\text{ 至多可数}$
snl_notation "HasSubset" CN => %#0 上子集关系结构的类型%
snl_notation "SDiff" CN => %#0 上差运算结构的类型，不附加集合论法则%
snl_notation "EmptyCollection" CN => %在 #0 中指定空元素的结构类型，不附加空性法则%
snl_notation "Std.Refl" CN => %#1 是自反关系%
snl_notation "Std.Antisymm" CN => %#1 是反对称关系%
snl_notation "Std.Trichotomous" CN => %#1 满足三歧性%
snl_notation "Nat.lt_iff_le_not_le" CN => %自然数 #0 与 #1 的严格序刻画的证明%
snl_notation "Nat.instNeZeroSucc" CN => %#0 的后继非零的证明%
snl_notation "Nat.instMax" CN => %自然数上的通常最大值运算结构%
snl_notation "Option.instMembership" CN => %#0 的元素与可选值之间的成员关系结构%
snl_notation "instOrdNat" CN => %自然数上的通常比较运算结构%
snl_notation "Nat.below" CN => %关于动机 #0、位于 #1 之前的强递归假设的类型%
snl_notation "Nat.brecOn" CN => %在 #1 处以动机 #0 和步骤 #2 进行强递归%
snl_notation "instOfNatNat" CN => %在自然数中解释字面量 #0 的 OfNat 实例%
snl_notation "DecidableLT" CN => %#0 上给定严格关系的判定程序类型%
snl_notation "DecidableLE" CN => %#0 上给定非严格关系的判定程序类型%
snl_notation "Max" CN => %#0 上名为 max 的二元运算结构类型，不附加序法则%
snl_notation "instHPow" CN => %由幂运算结构 #2 得到的异质幂运算结构%
snl_notation "instDecidableEqNat" CN => %自然数等式的判定程序%
snl_notation "Nat.decLe" CN => %判定自然数关系 #0 ≤ #1 的程序%
snl_notation "Nat.decLt" CN => %判定自然数关系 #0 < #1 的程序%
snl_notation "instMinNat" CN => %自然数上的通常最小值运算结构%
snl_notation "Infinite" CN => %#0 是无限的%
snl_notation "EquivLike.toFunLike" CN => %#3 所含的函数式结构%
snl_notation "Nat.instLinearOrder" CN => %自然数上的通常线序结构%
snl_notation "instOfNatAtLeastTwo" CN => %由自然数转换结构 #2 和至少为二的证明 #3 提供、在 #0 中解释字面量 #1 的 OfNat 实例%
snl_notation "Nat.instAtLeastTwoHAddOfNat" CN => %由 #0 非零的证明 #1 得到的其后继至少为二的证明%
snl_notation "Set.instMembership" CN => %#0 的元素与其子集之间的成员关系结构%
snl_notation "Set.instHasSubset" CN => %#0 的子集上的包含关系结构%
snl_notation "Set.instEmptyCollection" CN => %#0 的子集类型上的空集结构%
snl_notation "Denumerable.toEncodable" CN => %#1 所含的编码结构%
snl_notation "Encodable" CN => %#0 的带部分逆的自然数编码结构%
snl_notation "Equiv.instEquivLike" CN => %从 #0 到 #1 的等价类型上的等价式结构%
snl_notation "Equiv.ofLeftInverse" CN => %由以 #0 的非空证明为参数的函数族 #3 及对每个参数成立的左逆证明 #4 构造的从 #0 到 #2 的值域的等价%
snl_notation "Equiv.ofInjective" CN => %由单射证明 #3 构造的从 #0 到 #2 的值域的等价%
snl_notation "Function.leftInverse_invFun" CN => %由单射证明 #4 得到的、#3 的选择函数 invFun 构成左逆的证明%
snl_notation "Preorder.toLT" CN => %#1 所含的严格关系结构%
snl_notation "PartialOrder.toPreorder" CN => %#1 所含的预序结构%
snl_notation "partialOrderOfSO" CN => %由关系 #1 和严格序证明 #2 诱导的偏序结构%
snl_notation "RelIso.toEquiv" CN => %关系同构 #4 所含的等价%
snl_notation "Cardinal.isEquivalent" CN => %以存在等价为关系的类型上的 Setoid 结构%
snl_notation "Cardinal.instNatCast" CN => %基数上的自然数转换结构%
snl_notation "Cardinal.instPowCardinal" CN => %基数上的幂运算结构%
snl_notation "Cardinal.partialOrder" CN => %基数上的偏序结构%
snl_notation "PSet.instEmptyCollection" CN => %预集合上的空元素结构%
snl_notation "PSet.instInsert" CN => %预集合上的插入运算结构%
