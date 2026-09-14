import Lean4.Logic.term_macros
import Lean4.Basics.term_macros_CN

/-!
Chinese projections of the same text Styles, with identical operand indices.
Formula Styles are language-independent and inherited unchanged. Import after
the English base; select with `set_option snl.language CN`. There are no new
full/explicit Styles and no re-registration of imported connective defaults.
-/

-- Init/Prelude.lean: same default Styles as term_macros.lean.
snl_notation True.intro CN => %真命题的标准证明%
snl_notation True.rec CN => %以动机 #0 和构造子分支 #1 消去真命题的证明 #2%
snl_notation False.rec CN => %以动机 #0 消去矛盾 #1%
snl_notation False.elim CN => %由矛盾 #1 得到 #0 的一个元素%
snl_notation Eq.rec CN => %在 #0 中沿等式 #5 从 #1 到 #4 作等式归纳，动机为 #2，自反分支为 #3%
snl_notation Eq.ndrec CN => %在 #0 上的类型族 #2 中沿等式 #5 把 #3 从 #1 输送到 #4%
snl_notation Eq.subst CN => %在 #0 上的谓词 #1 中，利用等式 #4 和证明 #5 将 #2 代换为 #3%
snl_notation And.rec CN => %对 #0 与 #1 作合取消去，动机为 #2，构造子分支为 #3，合取证明为 #4%
snl_notation Or.rec CN => %对 #0 或 #1 作析取消去，动机为 #2，左分支为 #3，右分支为 #4，析取证明为 #5%

snl_notation Nonempty[english] CN => %#0 非空%
snl_notation Decidable CN => %#0 可判定%
snl_notation DecidableEq CN => %#0 上等式可判定%

-- Init/Core.lean: same default Styles and complete slot meanings.
snl_notation Iff.rec CN => %对 #0 与 #1 作等价消去，动机为 #2，构造子分支为 #3，等价证明为 #4%
snl_notation Exists.rec CN => %在 #0 上对谓词 #1 作存在消去，动机为 #2，见证及其证明的分支为 #3，存在证明为 #4%
snl_notation Subsingleton CN => %#0 至多有一个元素%

-- Mathlib/Logic/IsEmpty/Defs.lean
snl_notation IsEmpty CN => %#0 为空%

-- Mathlib/Logic/Nontrivial/Defs.lean
snl_notation Nontrivial CN => %#0 至少有两个不同元素%

-- Mathlib/Logic/Unique.lean
snl_notation Unique CN => %#0 配备指定元素且任意两元素相等%
