# 提交模型第六修订版：认识闭合纠偏增补

## 提案信息

```text
Proposal ID: CR-0003-R6
Title: Commit Model — Epistemic Closure Amendment
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: CORRECTIVE_OVERLAY
Applies To: CR-0003-R4 + CR-0003-R5
Revises: CR-0003-R5 within epistemic closure scope only
Review Basis: CR-0003-R5-LOCAL-REVIEW
Reviewer: Codex
External Approval Required: NO
Consolidation Required Before Freeze: YES
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
```

> 本文件是小范围纠偏草案，不是冻结制度。它不修改 `R4` 的提交主干，也不覆盖 `R5` 已经成立的认识上限、历史不可变和投影分权原则。

## 使用方式

下一轮复核对象是：

```text
CR-0003-R4 Commit Core
+ CR-0003-R5 Epistemic Evolution Amendment
+ CR-0003-R6 Epistemic Closure Amendment
```

发生冲突时，本文件只在以下范围收紧 `R5`：

1. 时间坐标；
2. 当前证明资格投影；
3. 传递依赖闭包完整性；
4. 恢复路径、契约出处和投影审计发布条件。

其他条款继续由 `R4` 和 `R5` 提供。三份草案通过组合复核后，仍必须合并为单一候选文档。

## 修订范围

本版只关闭 `CR-0003-R5-LOCAL-REVIEW` 的三项阻断：

```text
Bitemporal Semantics
Qualification Projection Determinism and Scope Identity
Dependency Closure Completeness and Omission Resistance
```

并完成三项非阻断精确化：

```text
Projection Recovery Path Logic
Compatibility and Exclusion Contract Provenance
Projection Audit Publication Failure Semantics
```

本版不处理：

- 提交尝试、写入和归因原子性；
- 提交结果值域；
- 决策模型冻结；
- 全局来源传播算法；
- 制度冻结证据包。

## 新增类型边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Temporal Query Coordinate` | 复合值对象 | 分离现实有效时点与认识截点 | 依附于解析请求 |
| `Projection View Mode` | 枚举值 | 区分历史认识视图与当前重述视图 | 投影规则制度 |
| `Qualification Projection Key` | 复合标识值 | 唯一标识一项当前证明资格投影 | 证明资格投影规则 |
| `Qualification Semantic Compatibility Record` | 版本化制度记录 | 声明资格结果是否可比较 | 资格治理制度 |
| `Candidate Dependency Closure Record` | 不可变候选记录 | 保存候选传递依赖集合及边界 | 未登记闭包账本 |
| `Registered Dependency Closure Record` | 不可变派生记录 | 保存内容相同的获登记闭包 | 依赖闭包账本 |
| `Candidate Closure Completeness Record` | 不可变候选记录 | 保存闭包完整性候选结论 | 未登记完整性账本 |
| `Registered Closure Completeness Record` | 不可变派生记录 | 保存获登记的闭包完整性结论 | 闭包完整性账本 |
| `Projection Publication Envelope` | 派生发布外壳 | 耦合投影快照和变化审计的可消费发布 | 投影发布边界 |

## EC-01 时间坐标必须双轴化

资格适用性、依赖闭包、规则解释和当前投影必须使用：

```text
Temporal Query Coordinate:
  Validity As Of
  Knowledge Cutoff
  Produced At
```

- `Validity As Of`：查询对象在被描述现实中的有效时点；
- `Knowledge Cutoff`：本次计算允许消费的最晚登记边界；
- `Produced At`：本次候选计算实际产生的时间。

三者不得互相替代。`Produced At` 较晚不允许自动消费超过 `Knowledge Cutoff` 的来源。

## EC-02 认识截点必须由来源登记边界实现

`Knowledge Cutoff` 不能只有一个无来源含义的时间戳。它必须引用每个权威来源注册表的稳定登记边界：

```text
Registry ID
Registry Scope
Inclusive Watermark or Exact Source Set
Boundary Established At
Boundary Authority Reference
```

只有时间戳而没有注册表边界，不能证明当时可见来源集合完整。

## EC-03 同一有效时点允许多个合法认识快照

```text
Same Validity As Of
+ Different Knowledge Cutoff
-> Different legitimate projection snapshots may exist
```

这些快照表达不同认识截点下的可用结论，不表示目标现实在同一有效时点发生了多次迁移。

## EC-04 投影视图模式必须显式声明

合法模式只有：

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

- `HISTORICAL_KNOWLEDGE_VIEW`：只消费不晚于指定 `Knowledge Cutoff` 登记的记录；
- `CURRENT_RESTATEMENT_VIEW`：以当前明确边界消费后续更正和适用性变化，重新陈述指定 `Validity As Of` 的当前认识。

当前重述不得被标注或展示为历史当时认识。

## EC-05 后来证据不能静默进入历史认识视图

```text
Source Registered After Knowledge Cutoff
  -/-> HISTORICAL_KNOWLEDGE_VIEW input
```

后来更正可以进入当前重述视图，但必须保留原证据、更正记录、新截点和来源边界。

## EC-06 时间字段旧名必须规范映射

合并时，`R4` 和 `R5` 中含义宽泛的 `As Of` 必须映射为：

```text
Validity As Of
Knowledge Cutoff
or NOT_APPLICABLE with reason
```

无法确定旧字段语义时使用 `UNRESOLVED`，不得依靠字段名称猜测。

## EC-07 当前证明资格投影必须拥有唯一作用域键

```text
Qualification Projection Key:
  Candidate Proof ID
  Commit Key
  Commit Contract Version or Compatibility Domain
  Validity As Of
  Knowledge Cutoff
  Qualification Projection Rule Version
```

任何一项不同都属于不同投影键。一个证明的投影不得支持另一个证明、提交键或契约作用域。

## EC-08 资格结果比较必须先通过语义兼容性

不同资格规则版本的结果只有引用 `Qualification Semantic Compatibility Record` 后才能比较。

兼容关系沿用：

```text
IDENTICAL_SEMANTICS
FORWARD_INTERPRETABLE
REQUIRES_RERESOLUTION
INCOMPATIBLE
UNKNOWN_COMPATIBILITY
```

`INCOMPATIBLE` 或 `UNKNOWN_COMPATIBILITY` 不能制造资格冲突，也不能选择其中一个结果；当前证明资格投影必须保持 `INDETERMINATE`。

## EC-09 当前证明资格投影必须使用完备真值表

在相同 `Qualification Projection Key`、语义可比较且依赖完整时：

```text
Applicable comparable QUALIFIED only
  -> QUALIFIED

Applicable comparable DISQUALIFIED only
  -> DISQUALIFIED

Applicable comparable QUALIFIED
+ Applicable comparable DISQUALIFIED
  -> CONFLICTED

Required applicability, lineage or compatibility unresolved
  -> INDETERMINATE

No applicable qualification record
  -> INDETERMINATE
```

“至少存在一个 `QUALIFIED`”不是产生 `QUALIFIED` 投影的充分条件。

## EC-10 资格适用性冲突与资格结果冲突必须分离

```text
Applicability Conflict
!= Qualification Outcome Conflict
```

- 适用性冲突回答某记录能否进入来源集合；
- 资格结果冲突回答可比较的适用记录是否给出相反资格结果。

两者分别保存来源和冲突引用，不得用一个 `CONFLICTED` 字段隐藏冲突层级。

## EC-11 ABORTED 只能消费精确匹配的资格投影

提交解析使用 `Current Proof Qualification Projection = QUALIFIED` 支持 `ABORTED` 时，必须完整匹配：

```text
Qualification Projection Key
Temporal Query Coordinate
Candidate Proof ID
Commit Key
Compatible Commit Contract Version
Registered Closure Completeness = COMPLETE
```

跨键复用、截点不明或闭包资格不明时，提交解析只能保持 `INDETERMINATE`。

## EC-12 依赖闭包必须声明根作用域和权威来源全集

每项候选闭包至少声明：

```text
Root Scope
Root Record IDs
Authoritative Source Registry IDs
Required Registry Scopes
Required Edge Types
Traversal Rule Version
Temporal Query Coordinate
Closed-world or Open-world Semantics
```

闭包构建器不得临时增加或删除应消费的注册表、边类型或根作用域。

## EC-13 每个来源注册表必须提供独立完整性边界

对每个必需注册表，候选闭包必须引用以下一种边界：

```text
Complete Prefix Proof
Exact Registered Source Set with authoritative digest
Frozen Snapshot Boundary
Institutionally equivalent completeness proof
```

一个注册表的完整性不能替代另一个注册表。解析账本水位不能自动证明证据、更正、资格、兼容和排除账本完整。

## EC-14 开放世界中的缺失不能证明不存在

```text
Open-world Scope
+ Source Not Found
  -/-> Source Absent
  -/-> Source Inapplicable
```

开放世界作用域只有在来源制度另外提供权威枚举边界后，才能对该边界内的来源建立完整性结论。否则：

```text
Closure Completeness = INDETERMINATE
Projection = INDETERMINATE
```

## EC-15 新增执行、登记和发布必须显式授权并分权

`Commit Contract` 或适用治理制度必须声明：

```text
Temporal Query Resolution Execution Authority Type
Qualification Projection Execution Authority Type
Dependency Closure Build Execution Authority Type
Dependency Closure Registration Authority Type
Closure Completeness Qualification Execution Authority Type
Closure Completeness Registration Authority Type
Projection Publication Authority Type
Projection Change Audit Registration Authority Type
```

每项授权仍必须满足 `R4` 的完整作用域要求，明确允许的输入来源、输出记录、规则版本、有效窗口以及 `Can Change` 和 `Cannot Change`。

路径为：

```text
Authorized Closure Build
  -> Candidate Dependency Closure Record

Independent Closure Registration
  -> Registered Dependency Closure Record

Authorized Completeness Qualification
  -> Candidate Closure Completeness Record

Independent Completeness Registration
  -> Registered Closure Completeness Record
```

每次登记保持候选内容摘要同一性。构建器不能登记自身闭包，也不能证明自身完整。

## EC-16 闭包完整性结果必须三值化

```text
COMPLETE
INCOMPLETE
INDETERMINATE
```

- `COMPLETE`：全部必需注册表边界、根、边和传递固定点均被证明覆盖；
- `INCOMPLETE`：能够证明至少一项必需来源或边被遗漏；
- `INDETERMINATE`：无法证明前两者。

只有已登记 `COMPLETE` 能支持终局投影。

## EC-17 摘要只证明内容同一性，不证明全集完整

```text
Closure Digest
  -> identifies supplied closure content

Closure Digest alone
  -/-> proves source universe completeness
```

完整性资格必须引用权威注册表边界和遍历固定点证据。

## EC-18 依赖闭包必须证明传递固定点

闭包完整性至少要求：

```text
Every required root visited
Every required outgoing edge type evaluated
Every discovered required node included or institutionally excluded
No frontier remains UNRESOLVED
All registry boundaries match Knowledge Cutoff
```

任一前沿未解析时，完整性结果只能是 `INDETERMINATE`。

## EC-19 投影恢复采用显式替代路径

投影恢复不是要求所有依据同时出现，也不是任意一项出现就自动恢复。合法路径只有：

```text
PATH_A_NEW_SUPPORT
PATH_B_AUTHORIZED_EXCLUSION_OR_INVALIDATION
PATH_C_COMPATIBILITY_OR_LEGALITY_RESOLUTION
```

每次恢复必须声明唯一主路径；辅助依据可以附加，但不能代替主路径的最低条件。

## EC-20 新支持恢复路径必须满足最低充分条件

```text
PATH_A_NEW_SUPPORT:
  New registered resolution or qualification
  Qualified and applicable supporting evidence
  Compatible rule versions
  Registered closure completeness = COMPLETE
  Projection recomputed under authorized rule
```

只有新证据但没有新的合格解析或资格，不能直接恢复终局投影。

## EC-21 排除或失效恢复路径必须满足最低充分条件

```text
PATH_B_AUTHORIZED_EXCLUSION_OR_INVALIDATION:
  Institutional exclusion or source invalidation basis
  Applicable authority reference
  Supporting evidence
  Effective scope and Temporal Query Coordinate
  Remaining source closure = COMPLETE
  No remaining comparable terminal conflict
```

来源被排除或失效不会删除其历史。

## EC-22 兼容性或合法性恢复路径必须满足最低充分条件

```text
PATH_C_COMPATIBILITY_OR_LEGALITY_RESOLUTION:
  New registered compatibility or legality resolution
  Governing institution and version
  Applicable authority and evidence references
  No certainty amplification by interpretation
  Re-resolution when required
  Recomputed closure = COMPLETE
```

投影器不得自行产生兼容性或合法性结论。

## EC-23 解释与来源排除契约必须具有制度出处

`Forward Interpretation Contract`、`Qualification Semantic Compatibility Record` 和 `Institutional Source Exclusion Basis` 至少绑定：

```text
Governing Institution ID
Institution Version
Contract or Record Version
Effective Scope
Temporal Query Coordinate
Applicable Authority Type
Authority Reference
Evidence References
Institution Status
```

只有适用的冻结制度或由冻结制度明确授权产生的记录才能进入运行时投影。草案、知识条目或投影器临时配置不能创建这些契约。

## EC-24 投影变化审计必须先于可消费发布闭合

投影构建器可以产生候选投影和候选变化审计，但新的物化投影只有在审计追加成功后才能进入可消费发布外壳：

```text
Candidate Projection Snapshot
+ Candidate Projection Change Audit Record
+ Projection Publication Authority
+ Projection Change Audit Registration Authority
-> Projection Publication Envelope
```

若审计追加失败：

```text
Projection may remain locally recomputable
Projection Publication = BLOCKED
Previously published projection remains historical
```

审计记录不证明投影正确，不成为正式目标事实，也不授予未来行动权威。

## 完整认识闭合路径

```text
Temporal Query Coordinate
  -> bind Validity As Of
  -> bind Knowledge Cutoff to authoritative registry boundaries
  -> select Projection View Mode

Registered Sources
  -> source applicability
  -> qualification semantic compatibility
  -> exact Qualification Projection Key
  -> qualification projection truth table

Root Scope
  -> registered dependency closure
  -> independent closure completeness qualification
  -> COMPLETE | INCOMPLETE | INDETERMINATE

Applicable Qualified Sources
+ Compatible Rules
+ Registered COMPLETE Closure
  -> epistemically bounded candidate projection
  -> candidate projection change audit
  -> authorized audit registration
  -> consumable Projection Publication Envelope
```

## 权威操作矩阵增补

| 角色 | 可以 | 不得 |
|---|---|---|
| `Temporal Query Resolver` | 绑定有效时点、认识截点和来源边界 | 用产生时间替代认识截点 |
| `Qualification Projection Builder` | 对精确投影键执行完备真值表 | 跨键复用、忽略相反资格结果 |
| `Dependency Closure Builder` | 按冻结根、边和注册表范围构建候选闭包 | 登记自身闭包、证明自身完整 |
| `Dependency Closure Registrar` | 登记内容相同的候选闭包 | 修改闭包、宣布完整性 |
| `Closure Completeness Qualifier` | 根据权威边界计算完整性候选 | 修改闭包或来源注册表 |
| `Closure Completeness Registrar` | 登记内容相同的完整性候选 | 改写候选、创建投影 |
| `Projection Publisher` | 在审计登记完成后发布派生读面 | 把投影升级为正式事实 |

同一主体可以持有多项独立授权，但必须使用独立任务契约、输入边界、输出记录和执行身份。

## 非法状态候选增补

- 用一个 `As Of` 同时表达现实有效时间和认识截点；
- 让晚于认识截点登记的来源进入历史认识视图；
- 把当前重述视图冒充历史认识视图；
- 跨证明、提交键或契约作用域复用资格投影；
- 仅凭一个适用 `QUALIFIED` 忽略适用的相反资格结果；
- 把规则不兼容误报为资格结果冲突；
- 用摘要证明来源全集完整；
- 用一个注册表水位证明多个注册表完整；
- 在开放世界中用未找到记录证明来源不存在；
- 依赖闭包构建器证明并登记自身完整性；
- 传递遍历仍有未解析前沿却登记 `COMPLETE`；
- 不声明恢复主路径就把投影恢复为终局；
- 只有新证据但没有新合格解析或资格就恢复终局；
- 投影器临时创建解释、兼容或来源排除契约；
- 投影变化审计未追加却发布新的可消费投影；
- 把审计记录当作投影正确性的最终证明。

## 对第五修订版的收紧映射

| `R5` 位置 | `R6` 收紧 |
|---|---|
| `EPI-03`、`EPI-06` 至 `EPI-08` | 分离有效时点和认识截点，增加精确资格投影键与真值表 |
| `EPI-09` 至 `EPI-13` | 将资格结果冲突与适用性冲突分层 |
| `EPI-15` 至 `EPI-18` | 增加兼容、解释和排除契约的制度出处 |
| `EPI-19` 至 `EPI-21` | 明确三条恢复路径和审计失败关闭 |
| `EPI-23` 至 `EPI-27` | 增加多注册表边界、独立完整性资格和开放世界语义 |

## 保留的冻结门槛

即使本增补通过复核，仍必须满足：

1. `R4 + R5 + R6` 已合并为单一候选文档；
2. 合并稿已经通过完整一致性审查；
3. `CR-0002-R1` 或兼容决策模型已经冻结；
4. 通用来源注册表能够提供所需完整性边界；
5. 已建立满足 `IF-0007` 的制度证据包、冻结权威、冻结决定和唯一版本边界。

## 当前审查状态

```text
Revision Scope: PASS
Bitemporal Semantics: PASS_WITH_REVIEW
Qualification Projection Determinism: PASS_WITH_REVIEW
Qualification Scope Identity: PASS_WITH_REVIEW
Dependency Closure Completeness: PASS_WITH_REVIEW
Omission Resistance: PASS_WITH_REVIEW
Recovery Path Logic: PASS_WITH_REVIEW
Contract Provenance: PASS_WITH_REVIEW
Projection Audit Publication Semantics: PASS_WITH_REVIEW
Historical Immutability: PASS
Projection / Formal Fact Separation: PASS
Policy Separation: PASS
Consolidation Status: REQUIRED
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Model Review Readiness: REVIEW_REQUIRED
Institution Freeze Eligibility: FAIL
```

建议动作：由 Codex 对 `R4 + R5 + R6` 执行一次本地独立认识闭合复核。若三项新阻断全部关闭且没有新增阻断，再合并为单一宪法候选；本增补不能自动产生合并或制度冻结。
