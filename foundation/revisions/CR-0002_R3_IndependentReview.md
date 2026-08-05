# CR-0002-R3 决策模型独立一致性复审

## 审查信息

```text
Review ID: CR-0002-R3-LOCAL-REVIEW
Review Type: Independent Composite Foundation Model Consistency Review
Status: COMPLETED
Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
Executable: NO
Reviewed Candidate: CR-0002-R2 + CR-0002-R3
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, R2 review findings, R3 closure clauses and dependent commit candidate interfaces
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是对 `R2 + R3` 组合候选的独立一致性复审记录，不是制度冻结。它不能使 `CR-0002-R2` 或 `CR-0002-R3` 获得运行时权威，不能创建登记权威、证明资格权威、决策事实、投影发布权威或冻结决定。

## 审查命题

本轮独立回答：

1. `R3` 是否只处理 `CR-0002-R2-LOCAL-REVIEW` 的五项有界阻断；
2. 派生记录登记授权是否形成逐类型、不传播且内容同一的完整拓扑；
3. `ABORTED` 是否只能消费合格、适用、完备且版本兼容的未应用证明；
4. 证明资格值域、适用性值域和投影键是否与已通过最终一致性审查的提交候选接口兼容；
5. 组合要求与豁免是否具有完整候选、登记、资格和适用性记录契约；
6. 合法性审查和更正投影是否具有稳定谱系、内容同一性和无歧义双时间边界；
7. 准入失败和提交未知是否已与正式决策语义完全分离；
8. 组合候选是否已经具备进入单一候选合并的条件。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-R2 Decision Model
CR-0002-R2 Independent Review
CR-0002-R3 Decision Model
CR-0003 Constitution Candidate R2
CR-0003 Constitution Candidate R2 Final Review
```

`CR-0003` 候选没有冻结制度权威。本轮只使用其已经通过最终一致性审查的提交证明接口检查跨候选兼容性，不使用它反向授权决策模型。

## 总体裁决

`CR-0002-R3` 遵守了修订范围，没有扩张到来源注册表、通用提交实现、领域决策类型、依赖传播算法或冻结程序。

它已经实质完成：

- 为派生记录登记定义通用但不传播的授权接口；
- 为五类既有登记记录建立逐类型授权实例、登记尝试和内容同一不变量；
- 建立候选未应用证明、历史资格、适用性、资格投影和提交解析谱系；
- 建立组合槽位的候选记录、登记记录、单槽位边界和正向豁免原则；
- 补齐合法性审查候选与登记摘要、审查谱系和稳定投影键；
- 分离更正历史坐标、认识时间、适用时间和投影产生时间；
- 为更正读投影建立构建、发布、谱系、冲突和内容同一边界；
- 将准入失败改为 `NON_ADMISSIBLE_DECISION_ATTEMPT`；
- 将提交未知限定为解析认识，不再作为决策事实生命周期状态。

因此，主体结构、权威分离方向和历史保留方向通过复审。

但组合候选仍有三项有界阻断：

1. 未应用证明资格、适用性值域及资格投影键与提交候选接口不兼容；
2. 豁免依据适用性解析只有名称和一句作用域要求，没有完整候选、登记和来源契约；
3. 合法性审查登记记录沿用 `R2` 的宽泛时间字段，而当前投影使用新的双时间键，两者缺少规范映射。

这些问题不要求推翻 `R2` 或 `R3`，但会阻断安全合并。应建立 `CR-0002-R4` 做第三轮有界闭合。在修订和复审完成前，`R2 + R3` 不具备单一候选合并准备度，也不具备模型级冻结准备度。

```text
Structural Direction: PASS
Five-blocker Scope Discipline: PASS
R2 Blockers Fully Closed: NO
Consolidation Readiness: FAIL
Model-level Freeze Readiness: FAIL
Overall Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
```

## 已通过部分

### 一、派生记录登记权威拓扑通过

`DM-R3-01` 至 `DM-R3-06` 已建立：

```text
One Registration Grant
-> One Candidate Record Type
-> One Registered Record Type
-> One Ledger Scope
```

每个授权实例明确绑定：

```text
Grant ID and Version
Authority Holder
Candidate and Registered Record Types
Object and Version Scope
Outcome and Rule Scope
Effective Interval
Can Change
Cannot Change
Registration Preconditions
Registration Decision Rule
Failure Behavior
Evidence and Institution References
```

`R3` 也区分：

```text
Canonical Derived Payload
Registration Attribution Envelope
```

并建立：

```text
Candidate Payload Digest
= Registered Payload Digest
```

这避免了因登记外壳包含时间、授权和账本位置而错误要求整个登记记录摘要与候选摘要相等，同时禁止登记者修改结果、理由、来源和时间坐标。

登记尝试采用：

```text
REGISTERED
DECLINED
INDETERMINATE
```

且缺少登记记录不能反推 `DECLINED`。登记失败不改变候选记录、正式事实或策略授权。

```text
Registration Authority Completeness: PASS
Authority Non-propagation: PASS
Content Identity Invariant: PASS
Registration Attempt / Registered Record Separation: PASS
```

### 二、未应用证明的主体因果方向通过

`R3` 不再允许证明类型名称直接支持 `ABORTED`，而是建立：

```text
Candidate Non-application Proof Record
-> Candidate Proof Qualification Record
-> Registered Proof Qualification Record
-> Candidate Proof Applicability Resolution
-> Registered Proof Applicability Resolution
-> Proof Qualification Projection
-> Candidate Commit Resolution
-> Registered Commit Resolution
```

证明组装、资格计算、资格登记、适用性解析、适用性登记和提交解析保持分权。完备性证明也必须拥有外部资格与适用性，不能因为被引用就证明来源完整。

提交解析增加不可变谱系、前序引用、关系类型、来源适用性变化输入、资格更正输入和当前投影键。历史记录与当前重述保持分离。

```text
Proof Type / Qualified Proof Separation: PASS
Qualification / Applicability Separation: PASS
Completeness Reference Self-proof Prevention: PASS
Historical Resolution Preservation: PASS
ABORTED Interface Direction: PASS_WITH_COMPATIBILITY_BLOCKER
```

### 三、组合记录主体契约通过

`DM-R3-15` 至 `DM-R3-20` 已明确：

```text
One Composite Resolution Record
-> One Requirement Slot
```

候选与登记组合记录保存目标、迁移、槽位、要求模式、所需决策、决策事实引用、豁免依据引用、结果、理由、双时间、来源、完备性、证据、谱系和摘要。

登记外壳保持候选载荷同一，组合登记者不得修改槽位结果或豁免依据。`EXEMPT` 被明确限定为需要正向、合格、适用且完备证明的否定性结论。

```text
Composite Single-slot Boundary: PASS
Composite Candidate Record Contract: PASS
Composite Registration Content Identity: PASS
Implicit Joint Authority Prevention: PASS
Exemption Semantic Direction: PASS_WITH_APPLICABILITY_RECORD_BLOCKER
```

### 四、合法性审查登记与谱系方向通过

`DM-R3-21` 补充：

```text
Candidate Review Record ID and Digest
Reviewer Identity
Review Authority Grant Reference
Registration Authority Grant Reference
Registered Review Payload Digest
Registered Record Digest
Prior Review References
Review Lineage ID
Review Relationship
```

并要求：

```text
Candidate Review Payload Digest
= Registered Review Payload Digest
```

`DM-R3-22` 和 `DM-R3-23` 为当前合法性投影增加稳定键、来源边界、兼容域、纳入与排除记录、冲突、产生时间和构建者身份。

合法性投影仍然不能创建失效决策或传播依赖失效。

```text
Legality Review Registration Content Identity: PASS
Legality Review Lineage: PASS
Current Legality Projection Stable Key: PASS_WITH_TEMPORAL_MAPPING_BLOCKER
Legality / Invalidation Separation: PASS
```

### 五、更正投影的双时间与分权通过

`DM-R3-24` 至 `DM-R3-29` 已分离：

```text
Corrected Historical Coordinate
Correction Known At
Correction Applicable From
Knowledge Boundary Vector
Projection Produced At
```

更正记录保持候选内容同一和追加谱系。历史认识视图不能消费认识边界之后登记的更正；当前重述可以使用后来更正重新陈述较早历史坐标，但必须显示后来认识和投影产生时间。

更正投影构建与投影发布使用不同授权。投影为可删除、可重建读面，冲突、来源不完整或规则不兼容时保持 `INDETERMINATE`。

```text
Correction Bitemporal Semantics: PASS
Correction Registration Content Identity: PASS
Correction Projection Lineage: PASS
Projection Build / Publication Separation: PASS
Projection / Decision Fact Separation: PASS
```

### 六、失败分支术语类型通过

准入分支已修订为：

```text
INADMISSIBLE
-> NON_ADMISSIBLE_DECISION_ATTEMPT
```

并明确它不是：

```text
Decision Disposition REJECT
ILLEGAL_ACT
Decision Fact
```

提交未知已修订为：

```text
Decision Commit Resolution = INDETERMINATE
Decision Fact Existence = UNRESOLVED_AT_DECLARED_COORDINATE
No Decision Fact Created or Mutated by Resolution
```

未知属于解析认识，不进入决策事实生命周期。

```text
Admissibility / REJECT Type Separation: PASS
Admissibility / Legality Classification Separation: PASS
Commit Unknown / Decision Fact Lifecycle Separation: PASS
Failure Branch Type Safety: PASS
```

## 阻断一：证明资格和适用性接口与提交候选不兼容

### 值域不一致

`R3` 为未应用证明资格定义：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
```

并为适用性定义：

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

已通过最终一致性审查的 `CR-0003-CONSTITUTION-CANDIDATE-R2` 使用：

```text
Qualification:
  QUALIFIED
  DISQUALIFIED
  INDETERMINATE
  CONFLICTED

Applicability:
  APPLICABLE
  INAPPLICABLE
  INDETERMINATE
  CONFLICTED
```

`NOT_QUALIFIED` 与 `DISQUALIFIED`、`NOT_APPLICABLE` 与 `INAPPLICABLE` 没有声明同一性或非放大映射。决策模型不能假设不同名称自动等价。

### 冲突被折叠为未知

`R3` 的资格投影规则写为：

```text
Conflicting terminal outcomes -> INDETERMINATE
```

提交候选要求资格冲突和适用性冲突以 `CONFLICTED` 保留，不能用普通未知隐藏冲突层级。

```text
CONFLICTED
!= INDETERMINATE
```

两者都失败关闭，但审计语义不同：前者证明存在相反终局来源，后者表示无法形成确定认识。把它们合并会丢失证据拓扑。

### 资格投影键缺少两个不可降低字段

`R3` 的 `Proof Qualification Projection` 键使用：

```text
Commit Contract ID and Version or Compatible Contract Domain Snapshot
```

但没有显式声明互斥作用域模式：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

也没有把 `Projection View Mode` 纳入资格投影键。提交候选要求精确契约版本与兼容域快照严格二选一，并要求历史认识与当前重述使用不同投影身份。

缺少这些字段时，同一键可能同时容纳不同契约作用域或不同认识视图。

### 必须补充的兼容闭合

下一修订必须选择一种不降级方式：

1. 直接消费 `CR-0003` 候选接口的规范值域和键；或
2. 定义显式、总函数、非放大的兼容映射，并保留 `CONFLICTED`、作用域模式和视图模式。

最低不得降低：

```text
Qualification Outcome preserves CONFLICTED
Applicability Outcome preserves CONFLICTED
EXACT_CONTRACT_VERSION xor COMPATIBILITY_DOMAIN_SNAPSHOT
Projection View Mode is part of Qualification Projection identity
INDETERMINATE cannot be upgraded
CONFLICTED cannot be collapsed into one terminal
```

```text
Proof Qualification Value Compatibility: FAIL
Proof Applicability Value Compatibility: FAIL
Conflict Preservation: FAIL
Qualification Projection Scope Identity: FAIL
Risk Level: HIGH
Required Action: CR-0002-R4
```

## 阻断二：豁免依据适用性记录契约不完整

### 资格记录完整，适用性记录只有名称

`DM-R3-18` 为 `Registered Exemption Basis Qualification Resolution` 列出了对象、槽位、规则、结果、时间、来源、完备性、更正视图、证据、登记权威、摘要和登记时间。

但 `Registered Exemption Basis Applicability Resolution` 只有对象名称和以下自然语言要求：

> 适用性解析必须证明该合格依据当前仍适用于同一槽位、对象、迁移、规则和时间坐标。

缺少：

```text
Candidate Exemption Basis Applicability Resolution Record
Candidate Payload Digest
Applicability Outcome Value Set
Applicability Reason Codes
Qualification Resolution Reference and Digest
Source Applicability Inputs
Correction View Reference
Coverage or Completeness Proof Reference
Applicability Rule and Institution Version
Resolver Identity
Registration Authority Grant Reference
Registered Payload Digest
Registered At
Prior Applicability Resolution References
Applicability Lineage ID
```

### EXEMPT 依赖一个尚未闭合的输入

`DM-R3-19` 要求：

```text
Registered Exemption Basis Applicability = APPLICABLE
```

但没有完整记录契约时，系统不能确定：

- 哪个候选计算产生该结果；
- 哪个独立登记权威保存该结果；
- 登记内容是否与候选内容相同；
- 来源变化和更正后如何追加新解析；
- 相反适用性来源如何失败关闭；
- 当前适用性如何绑定同一认识边界。

因此，`EXEMPT` 的正向证明方向正确，但输入契约仍未闭合。

### 必须补充的最小契约

下一修订必须为豁免依据适用性建立：

```text
Candidate Exemption Basis Applicability Resolution Record
Registered Exemption Basis Applicability Resolution Record
Independent Applicability Resolver
Independent Applicability Registration Authority Grant
Content Identity Invariant
APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
Stable Temporal and Scope Key
Append-only Applicability Lineage
```

任何来源不完整、冲突或作用域不匹配仍必须失败关闭，不能建立 `EXEMPT`。

```text
Composite Record Contract: PASS
Exemption Qualification Record Contract: PASS
Exemption Applicability Record Contract: FAIL
EXEMPT Positive Proof Closure: FAIL
Risk Level: HIGH
Required Action: CR-0002-R4
```

## 阻断三：合法性审查记录与投影双时间缺少规范映射

### R2 审查时间字段仍被保留

`DM-R2-31` 的合法性审查记录使用：

```text
Original Decision Time
Original Effective Coordinate
Review Effective At
Review As Of
Reviewed At
```

`DM-R3-21` 声明只在 `R2` 字段基础上增加候选摘要、审查者、登记归因和谱系，没有替换或解释上述时间字段。

### R3 投影键使用另一套时间类型

`DM-R3-22` 的稳定投影键改为：

```text
Validity As Of
Knowledge Boundary Vector
```

但没有规定：

```text
Review Effective At -> Validity As Of or NOT_APPLICABLE
Review As Of -> Knowledge Boundary Vector or UNRESOLVED
Reviewed At -> Produced At or Review Act Observed At
```

因此，登记审查记录无法确定性进入投影键。实现可能把 `Reviewed At` 当成认识截点，或把 `Review As Of` 同时解释为有效时点和知识时点。

### 更正时间闭合不能自动补齐审查时间

`DM-R3-24` 对更正记录建立了明确映射，但该条只适用于更正，不适用于合法性审查。不能因为两类对象都进入当前读面，就把更正时间契约隐式传播给审查记录。

### 必须补充的最小映射

下一修订必须为合法性审查记录显式区分：

```text
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Review Act Observed At
Review Record Produced At
Review Registered At
```

并规定旧字段的确定性映射：

```text
Exact Mapping
or NOT_APPLICABLE with reason
or UNRESOLVED
```

不得依据字段名称猜测。无法映射的历史审查记录只能进入 `INDETERMINATE` 投影。

```text
Legality Review Registration Content Identity: PASS
Legality Review Lineage: PASS
Legality Review Bitemporal Record Semantics: FAIL
Legality Record / Projection Key Mapping: FAIL
Risk Level: HIGH
Required Action: CR-0002-R4
```

## R2 五项阻断闭合复核

| `R2` 阻断 | `R3` 处理 | 本轮结论 |
|---|---|---|
| 派生记录登记权威拓扑不完整 | 通用登记契约、逐类型授权、登记尝试、内容同一和失败行为 | `PASS` |
| `ABORTED` 缺少证明资格及解析演进契约 | 候选证明、资格、适用性、资格投影、完备性、谱系和当前投影 | `PASS_WITH_INTERFACE_COMPATIBILITY_BLOCKER` |
| 组合要求与豁免缺少完整记录契约 | 完整组合记录、豁免资格和正向豁免条件 | `PASS_WITH_EXEMPTION_APPLICABILITY_BLOCKER` |
| 合法性审查和更正投影缺少谱系及双时间边界 | 审查同一性、谱系、稳定投影键及更正双时间 | `PASS_WITH_LEGALITY_TEMPORAL_MAPPING_BLOCKER` |
| 准入失败与提交未知存在术语类型歧义 | 非准入尝试类型和提交认识未知类型 | `PASS` |

## 权威拓扑审计矩阵

| 行为 | 执行角色 | 独立授权要求 | 是否可创建正式事实 | 本轮结果 |
|---|---|---|---|---|
| 登记准入 | `Admissibility Registrar` | 准入登记权威 | 否 | `PASS` |
| 登记提交解析 | `Decision Commit Resolution Registrar` | 提交解析登记权威 | 否 | `PASS` |
| 组装未应用证明 | `Proof Assembler` | 证明组装执行授权 | 否 | `PASS` |
| 计算证明资格 | `Proof Qualification Resolver` | 资格计算授权 | 否 | `PASS_WITH_VALUE_BLOCKER` |
| 登记证明资格 | `Proof Qualification Registrar` | 资格登记权威 | 否 | `PASS_WITH_VALUE_BLOCKER` |
| 解析证明适用性 | `Proof Applicability Resolver` | 适用性解析授权 | 否 | `PASS_WITH_VALUE_BLOCKER` |
| 登记证明适用性 | `Proof Applicability Registrar` | 适用性登记权威 | 否 | `PASS_WITH_VALUE_BLOCKER` |
| 解析组合槽位 | `Composite Resolver` | 组合解析授权 | 否 | `PASS` |
| 登记组合解析 | `Composite Resolution Registrar` | 组合解析登记权威 | 否 | `PASS` |
| 解析豁免依据适用性 | 未完整定义 | 豁免适用性解析授权 | 否 | `FAIL` |
| 登记豁免依据适用性 | 未完整定义 | 豁免适用性登记权威 | 否 | `FAIL` |
| 审查合法性 | `Legality Reviewer` | 合法性审查授权 | 否 | `PASS_WITH_TEMPORAL_BLOCKER` |
| 登记合法性审查 | `Legality Review Registrar` | 审查登记权威 | 否 | `PASS_WITH_TEMPORAL_BLOCKER` |
| 登记表示更正 | `Correction Registrar` | 更正登记权威 | 否 | `PASS` |
| 构建更正投影 | `Correction Projection Builder` | 投影构建授权 | 否 | `PASS` |
| 发布更正投影 | `Decision Read Projection Publisher` | 独立投影发布权威 | 否 | `PASS` |

## 与冻结制度的兼容性

| 冻结制度 | 审查结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `PASS_WITH_BLOCKER` | 通用登记权威拓扑通过；豁免适用性解析与登记角色尚未完整定义 |
| `IF-0006 Evidence Model` | `FAIL_WITH_BLOCKERS` | 证明冲突语义可能丢失，豁免适用性谱系不完整，合法性审查时间无法确定性映射 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、无权威、不可执行、提供者独立且不覆盖历史 |
| 五层架构边界 | `PASS_WITH_BLOCKERS` | 新增规则保持基础层范围，但三项接口尚未闭合 |

## 独立裁决矩阵

```text
Proposal Completeness: PASS
Single Purpose: PASS
R3 Scope Discipline: PASS
Provider Independence: PASS
Domain Portability: PASS
Registration Authority Completeness: PASS
Content Identity Invariant: PASS
Registration Authority Non-propagation: PASS
Proof Qualification Chain Direction: PASS
Proof Qualification Value Compatibility: FAIL
Proof Applicability Value Compatibility: FAIL
Proof Conflict Preservation: FAIL
Qualification Projection Scope Identity: FAIL
Commit Resolution Evolution Boundary: PASS
Historical Resolution Preservation: PASS
Composite Candidate and Registered Record Contract: PASS
Exemption Qualification Record Contract: PASS
Exemption Applicability Record Contract: FAIL
Legality Review Registration Content Identity: PASS
Legality Review Lineage: PASS
Legality Review Bitemporal Record Semantics: FAIL
Legality Record / Projection Key Mapping: FAIL
Correction Bitemporal Semantics: PASS
Correction Projection Lineage: PASS
Failure Branch Type Safety: PASS
Consolidation Readiness: FAIL
Model-level Freeze Readiness: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
```

## R4 修订范围约束

`CR-0002-R4` 应只处理本轮三项阻断：

```text
1. Align Non-application Proof Qualification and Applicability Semantics
2. Complete Exemption Basis Applicability Record Contract
3. Normalize Legality Review Bitemporal Record and Projection Mapping
```

`R4` 不得：

- 重写 `R2` 决策主干；
- 扩张派生登记权威通用契约；
- 修改已经通过的组合单槽位记录结构；
- 修改更正投影主干；
- 重新引入 `REJECT` 或决策事实未知状态歧义；
- 复制整个提交模型；
- 使 `CR-0003` 候选获得冻结权威；
- 实现完整来源注册表或资格治理；
- 修改 `IF-0001` 至 `IF-0007`；
- 创建冻结标识或运行时权威。

## 独立决定

1. 接受 `CR-0002-R3` 的主体修订方向和范围纪律；
2. 确认派生记录登记权威拓扑阻断已经闭合；
3. 确认失败分支术语类型阻断已经闭合；
4. 将未应用证明接口兼容性、豁免适用性记录和合法性审查时间映射登记为三项有界阻断；
5. 将本轮结果登记为 `PASS_WITH_THREE_BOUNDED_BLOCKERS`；
6. 不修改 `CR-0002-R2`、`CR-0002-R3` 或任何冻结制度历史；
7. 不合并、不冻结、不执行当前组合候选；
8. 不创建 `foundation/07_Decision.md`；
9. 下一步建立 `CR-0002-R4`，只处理三项有界阻断；
10. `R4` 完成后再次执行组合一致性复审；
11. 模型一致性通过后仍需合并为单一候选并重新执行冻结依赖审计；
12. 在正式冻结以前，全部决策模型提案保持不可执行且没有制度权威。
