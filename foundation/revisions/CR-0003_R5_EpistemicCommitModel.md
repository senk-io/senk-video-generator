# 提交模型第五修订版：认识演化增补

## 提案信息

```text
Proposal ID: CR-0003-R5
Title: Commit Model — Epistemic Evolution Amendment
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: BOUNDED_OVERLAY
Applies To: CR-0003-R4
Review Basis: CR-0003-R4-EPISTEMIC-REVIEW
Reviewer: Codex
External Approval Required: NO
Consolidation Required Before Freeze: YES
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
```

> 本文件是受限认识层修订提案，不是冻结制度。它只增补 `CR-0003-R4` 的证明资格适用性、认识上限、解释安全、投影演化和依赖失效接口，不重新定义已经通过审查的提交主干。

## 使用方式

本轮审查对象是：

```text
CR-0003-R4 Commit Core
+ CR-0003-R5 Epistemic Evolution Amendment
```

发生冲突时，本文件只在“认识演化”范围内取代 `R4`；其他条款继续由 `R4` 提供。即使本增补通过复审，也必须先合并为单一候选文档，才能进入宪法候选审查。

## 修订范围

本版只处理：

1. 证明资格的版本化适用性生命周期；
2. 投影确定性不得超过适用合格来源；
3. `FORWARD_INTERPRETABLE` 不得放大确定性；
4. 当前投影可以降级、冲突和恢复，但不得覆盖历史；
5. 证据更正和上游失效的最小消费接口。

本版明确不处理：

- 目标迁移原子性；
- 提交结果三值模型；
- 提交尝试身份；
- 未应用证明的三种类型；
- 全局依赖传播算法；
- 决策模型冻结；
- 制度冻结证据包。

## 核心认识边界

```text
Historical Facts and Records
  -> immutable

Source Applicability
+ Qualification Applicability
+ Rule Compatibility
+ Dependency Closure
  -> Applicable Qualified Sources

Applicable Qualified Sources
+ Epistemically Safe Projection Rule
  -> Current Resolution Projection
```

核心上限：

```text
Projection Certainty
<= Strongest Applicable Qualified Source Certainty
```

核心历史边界：

```text
Current Projection Change
-/-> Historical Record Mutation
```

## 新增类型边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Proof Qualification Applicability Resolver` | 执行角色 | 计算指定时点证明资格是否适用 | 无登记权威 |
| `Candidate Qualification Applicability Record` | 不可变候选记录 | 保存候选资格适用性结论 | 未登记适用性账本 |
| `Qualification Applicability Registrar` | 登记角色 | 登记内容相同的适用性候选 | 无证明资格所有权 |
| `Registered Qualification Applicability Record` | 不可变派生记录 | 保存获准登记的资格适用性 | 资格适用性账本 |
| `Current Proof Qualification Projection` | 派生读面 | 表达指定时点的可用证明资格 | 无独立事实所有权，可重建 |
| `Source Applicability Input` | 接口值对象 | 引用上游来源的版本化适用性 | 由来源模型提供 |
| `Applicability Change Record` | 接口记录 | 通知来源适用性发生追加式变化 | 由来源权威边界拥有 |
| `Dependency Closure Reference` | 接口值对象 | 标识本次投影已纳入的依赖闭包 | 依附于投影输入 |
| `Forward Interpretation Contract` | 版本化值对象 | 定义不放大确定性的跨版本映射 | 投影规则制度 |
| `Projection Change Audit Record` | 追加式派生审计记录 | 保存两次投影快照之间的认识变化 | 投影审计账本 |
| `Epistemic Strength` | 偏序值 | 表达可比较认识的确定性上限 | 依附于解析和投影规则 |

## EPI-01 历史事实和记录不可变

以下内容一旦登记即不得被认识演化修改：

```text
Evidence Record
Proof Qualification Record
Commit Resolution Record
Target State Resolution Record
Authoritative Transition Record
Decision Fact
```

新证据、新资格、新解析和新规则只能追加记录。当前投影可以改变，历史记录不能被重写成从未存在。

## EPI-02 历史资格不等于永久适用

```text
Registered Proof Qualification = QUALIFIED at T1
-/-> Qualified for every future As Of
```

证明资格记录只表达在其规则版本、证据版本和资格时点下的历史结论。提交解析必须另外证明该资格在自身 `As Of` 时点仍适用。

## EPI-03 资格适用性必须独立解析

证明资格适用性采用：

```text
Registered Proof Qualification Records
+ Qualification Rule Versions
+ Source Applicability Inputs
+ Evidence Correction References
+ Qualification Applicability Rule Version
+ Applicability As Of
-> Qualification Applicability Resolver
     -> Candidate Qualification Applicability Record
```

资格计算角色不能修改历史资格，也不能产生提交结果。

## EPI-04 资格适用性计算与登记分别授权

`Commit Contract` 或适用证明资格制度必须声明：

```text
Qualification Applicability Resolution Execution Authority Type
Qualification Applicability Registration Authority Type
Dependency Closure Resolution Execution Authority Type
Forward Interpretation Execution Authority Type
```

```text
Authorized Applicability Computation
  -> Immutable Candidate Applicability Record

Independent Applicability Registration
  -> Content-identical Registration Envelope
  -> Registered Qualification Applicability Record
```

执行权威不得隐式传播为登记权威。

## EPI-05 资格适用性结果必须四值化

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

- `APPLICABLE`：指定历史资格在给定 `As Of` 和规则版本下可作为解析输入；
- `INAPPLICABLE`：能够证明历史资格不适用于给定时点或解析范围；
- `INDETERMINATE`：现有输入不能证明前两者；
- `CONFLICTED`：存在可比较但不能消解的适用性终局冲突。

`CONFLICTED` 属于资格适用性投影，不改写原资格结果。

## EPI-06 资格适用性必须绑定完整时点和来源

每项资格适用性记录至少绑定：

```text
Proof Qualification Record IDs
Candidate Proof ID
Commit Contract Version
Qualification Rule Versions
Applicability Rule Version
Source Evidence Versions
Source Applicability Record IDs
Evidence Correction Record IDs
Effective From
Applicability As Of
Observed At
Produced At
Authority References
```

`Effective Until` 不能通过修改旧记录填写。资格后来失效时，必须追加新的适用性记录或失效来源记录。

## EPI-07 当前证明资格是可重建派生读面

```text
Registered Qualification Applicability Records
+ Applicability Lineage
+ Input Completeness
+ Applicability Projection Rule Version
+ Projection As Of
-> Current Proof Qualification Projection
```

投影值为：

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED
```

其中 `QUALIFIED` 只有在至少一项历史资格为 `QUALIFIED` 且其当前适用性为 `APPLICABLE`、全部必需依赖均可确认时成立。

## EPI-08 提交解析只能引用当前可用资格

提交结果为 `ABORTED` 时必须引用：

```text
Historical Proof Qualification = QUALIFIED
+ Current Proof Qualification Projection = QUALIFIED
+ Same Proof ID
+ Same Commit Key
+ Compatible Commit Contract Version
+ Qualification Applicability Interval covers Commit Resolution As Of
+ Qualification Projection Input Completeness is proven
```

历史资格存在但当前适用性不明时，提交结果只能保持 `INDETERMINATE`。

## EPI-09 认识强度采用偏序而非总分

提交结果的最低偏序：

```text
INDETERMINATE <= COMMITTED
INDETERMINATE <= ABORTED
COMMITTED and ABORTED are incomparable terminals
```

目标状态解析的最低偏序：

```text
INDETERMINATE <= RESOLVED
```

`CONFLICTED` 是投影冲突状态，不是比终局结果更高或更低的确定性等级。不得用数值总分把互不相容的终局结果排序后选择一个。

## EPI-10 投影确定性不得超过适用来源

```text
Projection Certainty
<= Strongest Applicable Qualified Source Certainty
```

投影只消费：

```text
Applicable
Qualified
Version-compatible
Dependency-complete
As-of-valid
```

的来源。来源数量、模型置信度、默认偏好或较新登记时间都不能单独提升认识强度。

## EPI-11 全部不确定来源不能产生终局投影

```text
All applicable sources = INDETERMINATE
  -> Projection = INDETERMINATE
```

多个不确定来源不能通过投票、平均、数量叠加或默认值产生 `COMMITTED`、`ABORTED` 或 `RESOLVED`。

## EPI-12 可比较终局冲突必须保持可见

```text
Comparable applicable terminal COMMITTED source
+ Comparable applicable terminal ABORTED source
  -> Current Commit Resolution Projection = CONFLICTED
```

投影规则不得通过以下方式隐藏冲突：

- 选择较新记录；
- 选择置信度较高的模型输出；
- 选择多数来源；
- 忽略不利来源；
- 按来源身份默认优先。

排除某项来源必须引用适用制度预先允许的 `Institutional Source Exclusion Basis`，并保留排除记录和证据。

## EPI-13 必需依赖未决时必须失败关闭

```text
Required dependency applicability = INDETERMINATE
or dependency closure incomplete
  -> Projection = INDETERMINATE
```

投影不得用缓存、旧资格、默认规则或人工直觉补齐未决依赖。

## EPI-14 投影不得用默认值解析未解析字段

```text
UNRESOLVED(reason)
-/-> VALUE(default)
```

只有新合格来源或新授权解析记录才能把未解析字段变为具体值。显示层默认值必须与规范字段分离，不能进入摘要和正式推导。

## EPI-15 来源排除必须受制度约束

`Institutional Source Exclusion Basis` 至少声明：

```text
Allowed Source Types
Exclusion Conditions
Applicable Authority Type
Rule Version
Evidence Requirements
Effective Scope
As Of Semantics
```

投影器不得临时发明排除理由。来源被排除不会删除来源历史，只改变指定投影时点的适用来源集合。

## EPI-16 FORWARD_INTERPRETABLE 只允许非放大解释

每项 `FORWARD_INTERPRETABLE` 关系必须引用 `Forward Interpretation Contract`：

```text
Source Resolution Rule Version
Target Canonical Interpretation Version
Total Deterministic Mapping
Field Presence Preservation
Evidence Reference Preservation
Epistemic Strength Mapping
Mapping Rule Version
Compatibility Evidence References
```

缺少任一项时不得采用前向解释。

## EPI-17 前向解释必须保持认识强度

最低映射不变量：

```text
Interpret(INDETERMINATE) -> INDETERMINATE
Interpret(UNRESOLVED field) -> UNRESOLVED field
Interpret(COMMITTED) -> COMMITTED or INDETERMINATE
Interpret(ABORTED) -> ABORTED or INDETERMINATE
Interpret(CONFLICTED sources) -> CONFLICTED or INDETERMINATE
```

禁止：

```text
Interpret(INDETERMINATE) -> terminal result
Interpret(UNRESOLVED) -> VALUE
Interpret(CONFLICTED) -> one chosen terminal
```

## EPI-18 可能提高确定性时必须重新解析

任何跨规则变化若可能把较弱认识提升为较强认识，兼容关系必须是：

```text
REQUIRES_RERESOLUTION
```

重新解析必须引用原权威来源、新解析执行权威、新规则版本和合格证据，产生新的候选记录与登记历史。旧解析记录保持不变。

## EPI-19 当前投影可以降低认识强度

历史解析的终局性不要求当前投影永久保持终局。

合法派生变化包括：

```text
COMMITTED Projection -> INDETERMINATE
ABORTED Projection -> INDETERMINATE
RESOLVED Projection -> INDETERMINATE
terminal Projection -> CONFLICTED
```

前提是来源资格失效、证据更正、依赖适用性未决、规则不兼容或出现可比较冲突。该变化只影响新的投影快照，不修改历史解析。

## EPI-20 当前投影可以在新依据下恢复

合法恢复包括：

```text
INDETERMINATE -> terminal Projection
CONFLICTED -> terminal or INDETERMINATE Projection
```

恢复必须引用：

- 新的合格证据；
- 新的适用资格；
- 新的合法解析；
- 正式来源失效或排除依据；
- 合法性审查结果；
- 兼容性已经闭合的规则版本。

投影器不能自行裁决冲突。

## EPI-21 投影变化必须追加审计记录

每次物化投影发生变化时，必须在适用投影执行授权允许的输出范围内追加 `Projection Change Audit Record`：

```text
Projection Type
Projection Scope
Previous Projection Digest
New Projection Digest
Previous Projection As Of
New Projection As Of
Projection Rule Version
Added Applicable Source IDs
Removed Applicable Source IDs
Applicability Change Record IDs
Dependency Closure References
Change Reason Code
Generated At
Projection Execution Authority Reference
```

首次投影显式使用 `NOT_APPLICABLE` 作为前一投影摘要。审计记录不是正式目标事实，也不能成为投影来源真值。

## EPI-22 投影变化不是历史状态迁移

```text
Projection Snapshot at T1
-> Projection Snapshot at T2
```

只表达系统在不同时点可重建的认识发生变化，不表示目标对象或历史解析记录发生生命周期迁移。

不得从投影变化反推目标状态被撤销、决策被取消或历史证据被删除。

## EPI-23 来源适用性采用最小消费接口

提交模型只消费以下接口，不定义全局传播算法：

```text
Source Applicability Input:
  Source Record ID
  Source Type
  Source Version
  Applicability = APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
  Applicability As Of
  Applicability Rule Version
  Source Authority Reference
  Evidence References

Applicability Change Record:
  Previous Applicability Reference
  New Applicability Reference
  Change Reason Code
  Changed At
  Source Authority Reference
```

接口记录必须不可变、版本化并可审计。

## EPI-24 证据更正不自动等于证据失效

```text
Evidence Correction exists
-/-> Evidence automatically INAPPLICABLE
```

更正记录只说明出现了新的证据历史。来源所属制度必须通过适用性解析判断原证据是否仍可用于指定目的。

提交模型不得自行解释全局证据更正语义。

## EPI-25 投影必须声明依赖闭包

每次投影必须引用 `Dependency Closure Reference`，至少包含或可重建：

```text
Direct Source Record IDs
Qualification Record IDs
Qualification Applicability Record IDs
Evidence and Correction Record IDs
Rule Compatibility Record IDs
Source Exclusion Record IDs
Transitive Dependency Set Digest
Closure Rule Version
Closure As Of
Completeness Proof Reference
```

依赖闭包不完整、摘要不匹配或完整性证明不足时，投影必须为 `INDETERMINATE`。

## EPI-26 依赖失效只触发重新计算和失败关闭

收到适用性变化时：

```text
Applicability Change
  -> invalidate derived projection cache
  -> recompute dependency closure
  -> rebuild projection
```

它不得：

- 修改历史解析；
- 删除资格记录；
- 自动创建新的提交结果；
- 自动授权重试；
- 直接修改目标状态。

## EPI-27 无法确认来源仍适用时保持不确定

```text
Source applicability cannot be established
  -> Source not usable as terminal support
  -> Projection = INDETERMINATE unless another complete basis exists
```

不能因为来源曾经合格、缓存仍存在或最后一次投影为终局，就默认来源继续适用。

## EPI-28 当前投影永远不是正式事实

```text
Current Resolution Projection
!= Formal Institutional Fact
!= Decision Fact
!= Historical Resolution Record
```

投影是指定规则版本和 `As Of` 下的可重建认识。它可以作为策略输入，但策略必须引用投影来源、时点、规则版本和依赖闭包，不能只引用显示值。

## EPI-29 认识变化不得隐式产生未来行动

```text
Projection = ABORTED
-/-> Retry

Projection = INDETERMINATE
-/-> Cancel Decision

Projection = CONFLICTED
-/-> Select Preferred Source
```

未来行动仍由独立策略或适用决策授权。

## EPI-30 认识演化角色不能自证

- 资格适用性解析器不能登记自身结论；
- 投影器不能创建来源适用性记录；
- 兼容性映射不能证明自身安全；
- 依赖闭包构建器不能把缺失来源标记为不适用；
- 来源排除者不能修改被排除来源；
- 策略不能降低投影确定性标准来获得可执行结果。

## 认识演化完整路径

```text
Evidence / Correction / Qualification / Rule Change
  -> Source-specific Applicability Resolution
  -> Source Applicability Input
  -> Qualification Applicability Resolution
       -> Candidate Applicability Record
       -> Authorized Registration
       -> Registered Applicability Record
  -> Current Proof Qualification Projection
  -> Dependency Closure Rebuild
  -> Cross-rule Compatibility Evaluation
       -> safe interpretation
       or re-resolution required
       or fail closed
  -> Epistemically Bounded Projection
       -> COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
  -> Projection Change Audit Record
  -> Optional independent Policy evaluation
```

## 认识演化操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Qualification Applicability Resolver` | 计算候选资格适用性 | 登记自身结果、修改历史资格 |
| `Qualification Applicability Registrar` | 登记内容相同的适用性候选 | 改写候选、创建提交结果 |
| `Projection Builder` | 消费完整依赖闭包并构建有上限投影 | 排除不利来源、放大确定性 |
| `Forward Interpreter` | 在前向解释执行授权下按非放大映射解释兼容旧记录 | 把不确定解释为终局、继承投影执行权威 |
| `Dependency Closure Builder` | 在依赖闭包解析授权下收集和验证依赖闭包 | 发明缺失来源的适用性、继承解析登记权威 |
| `Source Applicability Provider` | 提供来源所属制度的适用性记录 | 修改消费方历史解析 |
| `Policy Selector` | 依据完整投影证据选择未来行动 | 修改投影、资格或来源事实 |

## 非法状态候选

以下情况应在合并候选稿中明确为非法：

- 把历史 `QUALIFIED` 当作永久适用；
- 资格适用性解析器登记自身结果；
- 没有当前资格投影就用历史证明支持 `ABORTED`；
- 多个不确定来源通过投票产生终局结果；
- 投影忽略适用的不利来源；
- 没有制度排除依据就删除投影来源；
- 用默认值解析 `UNRESOLVED`；
- 前向解释提高认识强度；
- 前向解释删除证据引用或字段存在性；
- 需要重新解析时直接翻译旧结果；
- 当前投影降级时修改历史终局解析；
- 当前投影恢复时没有新合格依据；
- 把投影变化当作目标状态迁移；
- 证据出现更正就自动宣布原证据失效；
- 依赖闭包不完整仍产生终局投影；
- 适用性未知时沿用旧终局缓存；
- 把当前投影提升为正式事实；
- 投影结果自动触发重试、取消或来源选择；
- 认识演化角色为自身输出提供最终有效性证明。

## 对第四修订版的覆盖映射

| `R4` 位置 | `R5` 增补或收紧 |
|---|---|
| `CM-R4-14`、`CM-R4-15` | 增加历史证明资格的当前适用性生命周期 |
| `CM-R4-27` 至 `CM-R4-29` | 增加投影确定性上限、冲突保留和依赖闭包 |
| `CM-R4-30` 至 `CM-R4-33` | 收紧前向解释，任何确定性提升必须重新解析 |
| `CM-R4-34` | 增加投影降级、恢复和变化审计 |
| 依赖接口 | 增加来源适用性和变化记录的最小消费契约 |

## 保留的跨模型与冻结门槛

即使本增补通过复审，仍必须满足：

1. `CR-0002-R1` 或兼容决策模型已经冻结；
2. 通用证据资格或来源适用性模型能够提供本文件要求的接口；
3. 已完成 `R4 + R5` 单一候选稿合并；
4. 已通过合并稿的一致性审查；
5. 已建立满足 `IF-0007` 的制度冻结证据包、冻结权威和冻结决策。

## 当前审查状态

```text
Amendment Scope: PASS
Historical Immutability: PASS
Qualification Applicability Lifecycle: PASS_WITH_REVIEW
Epistemic Ceiling: PASS_WITH_REVIEW
Conflict Preservation: PASS_WITH_REVIEW
Forward Interpretation Safety: PASS_WITH_REVIEW
Projection Downgrade Semantics: PASS_WITH_REVIEW
Projection Recovery Semantics: PASS_WITH_REVIEW
Dependency Invalidation Interface: PASS_WITH_REVIEW
Projection / Formal Fact Separation: PASS
Policy Separation: PASS
Provider Independence: PASS
Domain Portability: PASS
Consolidation Status: REQUIRED
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Model Review Readiness: REVIEW_REQUIRED
Institution Freeze Eligibility: FAIL
```

建议动作：由 Codex 对 `R4 + R5` 执行本地独立认识闭合复审。若没有新的模型阻断，则将二者合并为单一 `CR-0003-CONSTITUTION-CANDIDATE`；合并不能自动产生制度冻结。
