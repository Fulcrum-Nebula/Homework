# SNL writing conventions (SNL 书写规范)

> Scope: **how to write SNL content** in this document — macro-tree-first authoring,
> binder scoping, `def` slots, formula nodes, root uniqueness, punctuation.
> Referenced by `.SNL_Doc/CONVENTIONS.md`, which owns **identities** only.
> Conflicting text elsewhere loses to this file; `FMNeco.md` owns the repository
> convention entry point and outranks both on naming.

Everything here is a rule with a failure mode attached. Each rule states what is
forbidden, what to write instead, and how a reviewer confirms it.

---

## 1. Root uniqueness — one root node per `content.snl`

The SNL parser must reach EOF after the root node (`DSL_manual.md`, Grammar
Overview). A tree therefore has **exactly one root**.

Consequence: consecutive `%…%` text nodes written at top level are **not** a
multi-sentence tree. The second `%…%` is a second root and the parse fails.

```snl
%First sentence.%(%Second sentence.%)   ← illegal: second root
```

Multi-sentence prose uses the text-mode variadic macro `__list__`, whose body is
`#*` and which is a single root:

```snl
__list__(%First sentence.%, %Second sentence.%, %Third sentence.%)
```

`__list__` is owned by `BasicMacros` and is the only sanctioned root for
multi-part text. Nested `__list__` is legal but a tree that is *essentially*
`__list__(%a%, %b%, %c%)` with no structure below it is a string written as a
tree — see §7.

**Review:** `snl entry latex <id>` renders; a root-count error surfaces as
`snl.parse: Expected EOF but got PERCENT_DELIMITED at position N`.

## 2. Punctuation stays inside the text node

`%…%` is a text **leaf**. Punctuation written outside the delimiters is read as
syntax and fails:

```snl
%Identity%: %a tag is exact.%   ← illegal: bare `:` between leaves
%Identity: a tag is exact.%     ← correct
```

Terminal punctuation (`.` `,` `:`) belongs inside the `%…%` that it terminates.
The same applies to `$…$` formula nodes: do not park an operator between two
nodes when it can live inside one.

**Review:** parse-time `snl.parse: Unexpected character "." at position N`.

## 3. Mathematical symbols are formula nodes, never bare Unicode

A bare `γ` in `content.snl` is an **identifier character**, not a formula. It
travels into generated code and LaTeX as a literal codepoint and breaks
downstream links.

```snl
Type.annotation(@γ, Real)              ← wrong: bare Unicode identifier
Type.annotation(@$\gamma$, Real)        ← correct: formula node
```

All mathematical symbols — Greek letters, `𝕂`, `ℝ`, `‖`, `∈` — are written as
`$…$` (inline) or `$$…$$` (display). Binder and source syntax keep the `@`
prefix: `@$\gamma$`, `$\gamma$@Project.ctxt.family`.

The rendered output of the two forms above is **identical**, which is exactly why
this error survives visual review — it must be found in the source.

**Review:** strip every legitimate `$…$` occurrence, then assert no non-ASCII
remains in `content.snl`:

```python
stripped = snl.replace('$\\gamma$', '')   # repeat for every symbol used
assert stripped.count('γ') == 0
```

Careful: `(γ)`, `(γ,`, `,γ)`, `@γ` are distinct argument shapes; a substitution
that handles one leaves the others behind.

## 4. `variable` carries context; declarations carry themselves

- Context is expressed with `variable(context, body)`. The first subtree holds the
  variable declarations and hypotheses, the second is the body in that context.
  Several declarations are grouped with `__list__`.
- `def`, `theorem`, `inductive`, and `structure` express the **declaration
  itself** and do **not** take a hypothesis slot. The composed macros `def-hyp`,
  `thm-hyp`, `def-struct-hyp`, `def-inductive-hyp` are **not** re-introduced for
  this purpose.
- `def` is fixed arity 3: `def(object, type, body)`. The slots keep their meaning
  under every style; only the style may change how they render.
- An unknown type or body keeps an **explicit empty slot** rather than a guess:
  `def(A, , B)` when the type is unwritten, `def(A, , )` when neither type nor
  body is written. Never fill a slot with a guessed `Type`, `Prop`, or invented
  body.
- The old `def-hyp(H, A, B)` migrates to `variable(H, def(A, , B))`. Do not delete
  a hypothesis and do not reorder, re-source, or re-bind the existing subtrees.

**Review:** grep for the banned composed names; check every `def` has exactly
three argument nodes.

## 5. Structures are declared with `structure`, not `And(...)`

A multi-clause definition ("a group is …", "a space curve is …") written as
nested `And(...)` renders as a chain of `∧` and destroys the labelled structure
the reader needs.

```snl
structure[prop](
  Name,
  __enum__[enumerate](
    member[colon](%label%, condition),
    …
  )
)
```

Renders as "定义【X】当且仅当可提供以下所有信息： ① 标签 : 条件 ② …".

- `[prop]` style = the "if and only if" phrasing above. `[default]` /
  `[localized_default]` = "定义结构类型【X】包含以下信息：".
- The reference is `Algebra.def.group` — read it with
  `snl entry get Algebra.def.group --json` before authoring a new structure.
- Structure **property** macros are named `<Structure>.<property>` with a dot
  (`DG.SpaceCurve.smoothness`), and stay in the package owning the structure.
  Identity rules are in `CONVENTIONS.md` §1.

**Review:** `snl entry latex` on a representative structure shows labelled
members, not `∧`.

## 6. Pointwise versus function-level statements

The DSL grammar is `node := name ("(" args? ")")?` — **a node carries at most one
argument parenthesis**. A pointwise expression such as `γ'(s)` (differentiate the
function, then evaluate at `s`) is therefore two applications and is not
expressible as a node.

- Entry-level statements are written at **function level**: `κ_γ`, `t_γ`. Pointwise
  formulas belong in `content.markdown`.
- The exception is a binder: when the variable itself is bound (`@γ`), a first
  application `Type.apply(γ, t)` is legal because the binder is the binding site.
- Granularity is chosen by the **mathematical structure**, not by the order the
  book presents it. A pointwise fact is recovered by supplying the argument via
  `Type.apply`, not by flattening the definition.

## 7. No strings written as trees

A syntax tree whose shape is a string — a root text macro carrying the whole
sentence, or `__list__` over prose fragments with nothing structured below — is
not a refinement. It defeats the notation and SSI does not catch it: a
string-shaped tree can score well while carrying no structure.

When a corpus genuinely resists a syntactic decision, treat the passage as a
whole and accept a **low SSI honestly** rather than making a blind decomposition.
The same prohibition applies to faking a high SSI by promoting every phrase to a
constant macro with a wrong or empty `source.entries` — that turns macro
management into a liability without adding meaning.

**Review:** for every new Entry, verify the tree has real structure under the
root. `snl entry latex` and SSI are necessary but not sufficient.

## 8. `%…%` text has no language projection

Literal `%…%` text embedded in a tree is **not localizable**. Do not claim it is
localized. Where a fragment must be translated, either reuse an existing
localized text macro or introduce a one-off macro in `FulcrumNotesOneOffI18N`
(naming and manifest rules in `CONVENTIONS.md` §7).

Within `%…%`, `#0` / `#1` are **parameter placeholders** referencing the params
table — not literals. In pure-text rendering the placeholders are not substituted
there; filling happens in the KaTeX/React layer. `Skill.SNLeco.cpt.EntryTitle`
behaves the same way; that is existing convention, not a defect.

## 9. Intervals: predicate, not type (`CONVENTIONS.md` §9, restated)

A binder whose value is meant to lie in `[a, b]` declares the primitive type and
states membership separately:

```snl
s : Real   with   s ∈ [a, b]      ← correct
s : Icc(a, b)                     ← wrong: Icc is not a type constructor
```

A function whose **domain** genuinely is an interval may take `Icc(a, b)` as its
domain type (`γ : Icc(a, b) → ℝ³`). The rule governs binders, where the interval
constrains a point rather than typing it. `Ioo`, `Ico`, `Ioc` behave the same.

## 10. Entry content shape

- `section` / `subsection` Entries keep `content` as `{}` — the title shell only.
  Reference: `Topology.sec.topology`.
- An Entry's `content.snl` may be empty; empty Entries are legal and are used
  deliberately for unresolved constructors and recursors (`CONVENTIONS.md` §8).
- `content` dialects are language-invariant `snl` plus optional `markdown` /
  `latex` / `typst` / `text`. Prose that remains prose — motivation, pointwise
  formulas, reading notes — goes in `markdown`, not forced into `snl`.

## 11. Entry tags are short search keywords

`.SNL_Doc` Entry storage has no `tags` field by default. When present it is an
**optional array of strings**, each a short keyword for finding the Entry.

```json
"tags": ["mathlib-divergence"]        ← correct
"tags": [{"key": "...", "value": "..."}]   ← wrong: not a metadata slot
"tags": null                                ← wrong: absent, not null
```

- Explanation belongs in `title` or `content.markdown`, never in a tag.
- Absent means no tags. Do not write `[]` to "clear" it and do not add the field
  to Entries that never had it. An update that **omits** the field preserves the
  stored tags; an explicit `[]` clears them.
- A present non-string-array tag is **rejected before publication** and, if
  already stored, **refuses the entire workspace at read time** — not one Entry.
  Validation passing is therefore **not** evidence that the workspace is
  readable.

**Review:** the client-side check, plus a browser load of the affected Library —
see §12.

## 12. Verification discipline

1. `snl validate --json` must return `ok: true` with `issues: []`, and
   `counts.entry` must move as expected. This catches silent failures.
2. **`validate` passing does not mean the reader can load the document.** Every
   content change is confirmed in the browser at the reader URL with a
   screenshot. Readers watch the workspace and reload on save; no restart is
   needed.
3. The Library page shows the **Entry** tree; macros are not in it. An empty
   `0 entries` page with macros written is expected, not a defect.
4. After a `macro rename`, review **every call site's argument order**. Rename
   changes the name only and never touches arguments, and `validate` does not
   report the resulting mismatch. Confirm with `snl entry latex` per Entry.
5. When a symptom contradicts the source, identify **which binary is executing**
   before doubting the code — see the tooling contract below.

## 13. Tooling contract assumed by this document

The rules above assume the CLI that executes is the one built from the current
Toolkit tree. `PATH` may otherwise resolve to a stale copy that silently accepts
data the current validator rejects, which presents as an unexplainable
source-versus-behaviour contradiction.

```bash
which snl; readlink -f $(which snl)
```

Typical failure: a hand-copied bundle from an earlier date that predates a
validator. It accepts what the current build rejects, and reports `valid: true`
with zero issues.

The Toolkit repository **ships its build output**; `git pull` therefore delivers
the current CLI and no build step is required. Point the launcher at the shipped
bundle rather than keeping a copy:

```bash
cp -p ~/.local/bin/snl.mjs ~/.local/bin/snl.mjs.bak-$(date +%Y%m%d)
ln -sfn ~/workspace/cat/SNL-Agent-Toolkit/dist/cli/snl.mjs ~/.local/bin/snl.mjs
readlink -f ~/.local/bin/snl.mjs
```

Keep the `snl` launcher as a thin wrapper that `exec`s `snl.mjs`; the symlink is
what must be replaced, not the wrapper.

## 14. The reader watches a directory, not a branch

The reader serves whatever is **on disk under `--root`**. It watches the
filesystem and reloads on save, so it never needs a restart — but it also cannot
know that the branch checked out there is not the one you just pushed.

This produces a failure mode that looks like a broken reader and is a wrong
checkout:

1. The reader runs with `--root <repo>` and keeps running for days.
2. Some agent checks out a feature branch in that same directory to do its work.
3. Work lands on `main` elsewhere; the directory under the reader is still on the
   feature branch.
4. The page does not change. Nothing is broken — the reader is faithfully
   serving an older tree.

**Diagnosis.** Identify the serving process and its root first, then ask which
commit that directory is at:

```bash
ps aux | grep "snl.mjs --root" | grep -v grep
cd <root> && git log --oneline -1 && git branch --show-current
```

**Confirmation.** Compare the served tree against the commit you expect:

```bash
git merge-base --is-ancestor <expected-commit> HEAD && echo current || echo stale
```

**Rules.**
- Do not use the reader's `--root` directory as a scratch checkout. Do branch
  work in a separate worktree or a separate clone.
- A long-lived reader should point at a directory that stays on the branch it is
  meant to show. If the branch must move, expect to reconcile the reader root
  explicitly — a reader that has been running for hours is not evidence that its
  tree is current.
- `validate` inside the reader root reports on that tree, so a clean validate
  there certifies only what the reader is already serving.

**Review:** before reporting that "the page did not update", resolve the serving
process, its `--root`, and that directory's current commit — in that order.
