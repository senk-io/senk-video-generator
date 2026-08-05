# 决策模型提案第五修订版：提交解析投影闭合增补

## 提案信息

```text
Proposal ID: CR-0002-R5
Title: Decision Model — Commit Resolution Projection Closure
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: BOUNDED_CORRECTION_OVERLAY
Applies To: CR-0002-R2 + CR-0002-R3 + CR-0002-R4
Revises: CR-0002-R3 within commit resolution projection scope only
Review Basis: CR-0002-R4-LOCAL-REVIEW
Independent Review Required: YES
Consolidation Required Before Freeze: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0003 Constitution Candidate R2
Derived From: CR-0002-R4 Independent Review
```

> 本文件是第五修订阶段的单阻断纠偏草案，不是冻结制度。它不创建提交解析、依赖闭包、投影、决策事实、登记权威、合并决定或冻结决定，也不覆盖 `CR-0002-R2` 至 `CR-0002-R4` 及其审查历史。

## 使用方式

下一轮最终组合一致性复审对象是：

```text
CR-0002-R2 Decision Model Core
+ CR-0002-R3 Bounded Blocker Closure
+ CR-0002-R4 Interface and Temporal Closure
+ CR-0002-R5 Commit Resolution Projection Closure
```

发生冲突时，本文件只在提交解析投影范围内收紧 `DM-R3-13`、`DM-R3-14` 及相关类型名称。其他决策、证明、豁免、合法性、更正和失败分支语义继续由 `R2` 至 `R4` 提供。

## 修订范围

本版只处理：

```text
Normalize Decision Commit Resolution Projection Contract
```

具体包括：

1. 使用规范 `Resolution Projection` 类型；
2. 把 `Current Commit Resolution Projection` 限定为当前重述视图的显示别名；
3. 分离单条已登记提交解析三值与解析投影四值；
4. 定义提交解析投影冲突真值表；
5. 闭合精确契约作用域与兼容域快照的字段存在性；
6. 要求终局投影消费已登记依赖闭包和 `COMPLETE` 完整性；
7. 保持投影、历史解析、决策事实和策略授权分离。

本版不处理：

- 单次提交解析三值语义；
- `ABORTED` 未应用证明资格链；
- 证明资格投影；
- 豁免适用性；
- 合法性审查时间规范化；
- 派生登记权威通用契约；
- 组合槽位、更正投影或失败分支类型；
- 投影发布审计的完整实现；
- 全局依赖闭包算法；
- `IF-0001` 至 `IF-0007` 的修改；
- 单一候选、运行时权威或制度冻结。

## 一、规范类型边界

| 节点 | 类型 | 唯一目的 | 权威或逻辑边界 |
|---|---|---|---|
| `Registered Decision Commit Resolution Record` | 不可变派生记录 | 保存一次提交尝试在声明坐标下的三值解析 | 提交解析账本 |
| `Resolution Projection` | 可重建派生读面 | 汇总稳定键下可比较解析的四值认识 | 无提交或决策事实权威 |
| `Candidate Resolution Projection Record` | 候选派生记录 | 固定一次解析投影计算的输入和结果 | 投影候选边界 |
| `Resolution Projection Builder` | 计算角色 | 按稳定键、闭包和真值表构建候选投影 | 无登记、发布或事实权威 |
| `Resolution Projection Scope Mode` | 规范枚举 | 严格选择精确提交契约或兼容域快照 | 投影键 |
| `Resolution Compatibility Domain Snapshot` | 不可变制度快照 | 固定提交解析可比较契约集合 | 兼容治理制度 |
| `Dependency Closure Reference` | 复合接口值 | 绑定已登记闭包、完整性和时间坐标 | 投影输入边界 |
| `Resolution Projection Conflict Set` | 不可变复合值 | 保存可比较相反终局及来源引用 | 投影载荷 |

以下关系必须成立：

```text
Registered Commit Resolution Outcome:
  COMMITTED | ABORTED | INDETERMINATE

Resolution Projection Outcome:
  COMMITTED | ABORTED | INDETERMINATE | CONFLICTED

Current Commit Resolution Projection
= Display Alias only when Projection View Mode = CURRENT_RESTATEMENT_VIEW

Resolution Projection
-/-> Decision Fact Mutation
-/-> Retry Authorization
-/-> Target Transition
```

## 二、规范类型与视图闭合

### DM-R5-01 规范类型只能是 Resolution Projection

合并后的规范类型名称为：

```text
Resolution Projection
```

`R3` 中的：

```text
Current Commit Resolution Projection
```

必须从规范类型表移除，只能作为满足以下条件的显示别名：

```text
Normative Type = Resolution Projection
Projection View Mode = CURRENT_RESTATEMENT_VIEW
Display Alias = Current Commit Resolution Projection
```

显示别名不得进入规范摘要、对象类型判定、授权作用域、持久化类型或跨模型接口。

### DM-R5-02 历史认识与当前重述共享同一规范类型

合法视图模式继续为：

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

两种视图都必须使用 `Resolution Projection`，并把 `Projection View Mode` 作为稳定键字段。

- 历史认识视图只消费不晚于声明认识边界登记的解析和依赖；
- 当前重述视图可以在新认识边界下消费后来合格的解析、更正和适用性变化；
- 当前重述不得被展示为历史当时认识；
- 历史视图不得通过显示别名伪装成当前唯一真值。

### DM-R5-03 投影视图模式不得由查询界面隐式决定

```text
Query Label = current
-/-> Projection View Mode
```

视图模式必须由版本化投影请求和投影规则显式声明，并进入候选载荷、投影摘要及任何兼容发布外壳。

缺少视图模式时不得构建可消费投影。

## 三、历史解析三值与投影四值闭合

### DM-R5-04 单条已登记提交解析保持三值

`Registered Decision Commit Resolution Record` 的规范结果不变：

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED` 必须由权威决策记录和提交归因证明；
- `ABORTED` 必须由 `R3 + R4` 定义的合格、适用、完备未应用证明支持；
- `INDETERMINATE` 表示单次解析无法证明前两者。

单条解析记录不得使用 `CONFLICTED`。冲突只有在投影比较多个已登记解析或兼容来源时成立。

### DM-R5-05 Resolution Projection 使用规范四值

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

- `COMMITTED`：完整来源集合中只有可比较、适用的 `COMMITTED` 终局；
- `ABORTED`：完整来源集合中只有可比较、适用的 `ABORTED` 终局；
- `INDETERMINATE`：来源、闭包、兼容性、时间、字段或终局认识不足；
- `CONFLICTED`：同一稳定作用域内存在可比较、适用的 `COMMITTED` 与 `ABORTED` 终局。

`CONFLICTED` 不是第四种提交现实，也不是单条提交生命周期状态；它是派生投影对相反终局来源的显式认识。

### DM-R5-06 提交投影认识偏序不得选择终局优先级

```text
INDETERMINATE <= COMMITTED
INDETERMINATE <= ABORTED
COMMITTED and ABORTED are incomparable terminals
CONFLICTED is outside the strength ordering
```

`CONFLICTED` 不比终局更强或更弱。系统不得以数值排序、来源数量、登记时间或权威身份把它自动还原为一个终局。

### DM-R5-07 COMMITTED 与 ABORTED 的冲突必须显式可见

```text
Comparable applicable COMMITTED
+ Comparable applicable ABORTED
-> Resolution Projection = CONFLICTED
```

冲突投影必须保存双方全部终局记录、谱系、来源、证据和摘要，不能只保存一个原因码。

```text
COMMITTED + ABORTED
-/-> INDETERMINATE for convenience
-/-> Latest record wins
-/-> COMMITTED preferred
-/-> ABORTED preferred
```

### DM-R5-08 冲突与未知必须保持类型分离

```text
INDETERMINATE:
  cannot establish a unique comparable terminal

CONFLICTED:
  establishes at least two opposite comparable terminals
```

两者都阻断正式消费，但审计证据不同。任何投影、界面或报表不得把 `CONFLICTED` 显示为普通未知而隐藏冲突来源。

## 四、提交解析投影作用域闭合

### DM-R5-09 投影作用域模式必须严格二选一

规范模式只有：

```text
EXACT_COMMIT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

```text
Resolution Projection Scope Mode = EXACT_COMMIT_CONTRACT_VERSION
-> Exact Commit Contract ID and Version required
-> Compatibility Domain fields = NOT_APPLICABLE

Resolution Projection Scope Mode = COMPATIBILITY_DOMAIN_SNAPSHOT
-> Resolution Compatibility Domain Snapshot required
-> Exact Commit Contract fields = NOT_APPLICABLE
```

两组字段同时存在或同时缺失时，投影必须为不可消费候选，不能依靠实现猜测作用域。

### DM-R5-10 兼容域快照必须固定可比较成员

`Resolution Compatibility Domain Snapshot` 至少绑定：

```text
Compatibility Domain ID and Version
Compatibility Semantic Domain = COMMIT_RESOLUTION
Exact Member Commit Contract IDs and Versions
Membership Digest
Membership Rule Version
Resolution Semantic Compatibility Record References
Field Presence Compatibility References
Temporal Compatibility Rule Version
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
Snapshot Digest
```

成员变化必须形成新快照版本、新摘要和新投影键。缺少成员枚举、兼容证据或可验证制度冻结引用时，兼容性保持未知。

本提案只消费兼容域快照，不创建其成员关系、制度资格或冻结引用。

### DM-R5-11 Resolution Projection Key 必须完整稳定

```text
Resolution Projection Key:
  Commit Resolution Subject = Decision Commit Attempt ID
  Decision Key
  Resolution Projection Scope Mode
  Exact Commit Contract ID and Version or NOT_APPLICABLE
  Resolution Compatibility Domain Snapshot ID and Version or NOT_APPLICABLE
  Validity As Of
  Knowledge Boundary Vector
  Projection View Mode
  Source Set Boundary
  Correction View Reference
  Resolution Projection Rule Version
```

任何字段不同都属于不同投影。不得跨提交尝试、决策键、契约作用域、有效时点、认识边界、视图模式、来源边界、更正视图或规则版本复用。

### DM-R5-12 字段存在性必须三分

规范字段只能是：

```text
VALUE(value)
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
```

静默省略、空字符串、零值或显示默认值不能代替规范字段存在性。

投影键任一必需字段为 `UNRESOLVED` 时，候选投影只能为 `INDETERMINATE` 且不可作为终局投影消费。

## 五、依赖闭包完整性闭合

### DM-R5-13 来源集合摘要不证明来源全集完整

```text
Source Set Digest
-/-> Complete Dependency Set
```

摘要只能证明给定来源集合内容同一，不能证明所有必需根、边、注册表和更正已经纳入。

`Coverage Qualification References` 也不能在没有独立资格、适用性和已登记闭包时自行证明完整性。

### DM-R5-14 Resolution Projection 必须绑定 Dependency Closure Reference

`Dependency Closure Reference` 至少绑定：

```text
Registered Dependency Closure Record ID and Digest
Registered Closure Completeness Record ID and Digest
Closure Completeness Outcome
Resolution Projection Key Digest
Root Commit Resolution Record IDs
Required Dependency Edge Types
Source Registry IDs and Scopes
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Closure Digest
Closure Rule Version
Completeness Rule Version
Evidence References
```

闭包、完整性和投影必须具有相同时间坐标、视图模式和来源注册表边界。

### DM-R5-15 终局投影只允许消费 COMPLETE 闭包

```text
Registered Closure Completeness Outcome = COMPLETE
```

是 `COMMITTED`、`ABORTED` 或 `CONFLICTED` 投影的必要条件。

```text
INCOMPLETE
INDETERMINATE
```

都必须产生：

```text
Resolution Projection = INDETERMINATE
```

闭包摘要、来源数量或注册表单一水位不能替代 `COMPLETE`。

### DM-R5-16 每个注册表必须拥有独立边界

`Knowledge Boundary Vector` 必须为每个权威来源注册表保存：

```text
Registry ID
Registry Scope
Inclusive Watermark or Exact Source Set
Boundary Established At
Boundary Authority Reference
```

一个注册表边界不能证明另一个注册表完整。只有时间戳而没有注册表边界向量时，闭包完整性必须保持 `INDETERMINATE`。

### DM-R5-17 开放世界缺失不得证明终局

```text
Open-world Source Not Found
-/-> ABORTED
-/-> Source Inapplicable
-/-> Dependency Complete
```

没有权威枚举边界、封闭前缀或制度等价完整性证明时，投影必须保持 `INDETERMINATE`。

### DM-R5-18 闭包变化只能触发新投影

新增来源、更正、适用性变化、兼容域变化或闭包规则变化必须形成：

```text
New Candidate Dependency Closure
-> Independent Closure Registration
-> New Candidate Closure Completeness
-> Independent Completeness Registration
-> New Candidate Resolution Projection
```

旧闭包、完整性记录和投影保持不变。闭包变化不得修改历史提交解析或决策事实。

## 六、候选投影记录与构建边界

### DM-R5-19 Resolution Projection Builder 只有计算权

构建者可以：

```text
Read authorized registered resolution records
Read compatible source applicability records
Read registered dependency closure and completeness
Apply frozen projection truth table
Produce Candidate Resolution Projection Record
```

构建者不得：

```text
Create or modify registered commit resolution
Create COMMITTED or ABORTED source records
Qualify non-application proof
Register dependency closure or completeness
Exclude sources without institutional basis
Publish projection
Create, revoke or mutate Decision Fact
Authorize retry or target transition
```

### DM-R5-20 Candidate Resolution Projection Record 必须固定完整输入

候选记录至少绑定：

```text
Candidate Resolution Projection ID
Resolution Projection Key and Digest
Resolution Projection Outcome
Outcome Reason Codes
Included Registered Commit Resolution Record IDs and Digests
Excluded Resolution Record IDs and Institutional Exclusion Reasons
Resolution Lineage IDs and Digests
Resolution Projection Conflict Set Reference if applicable
Dependency Closure Reference
Source Registry Snapshot References
Source Set Digest
Correction View Reference
Compatibility Record References
Evidence References
Projection Builder Identity
Projection Build Authority Grant Reference
Projection Rule ID and Version
Produced At
Candidate Projection Payload Digest
```

候选投影不因文件存在、缓存写入或界面显示而取得正式事实权威。

### DM-R5-21 冲突投影必须保存完整冲突集

`Resolution Projection Conflict Set` 至少绑定：

```text
Conflict Set ID
Resolution Projection Key Digest
COMMITTED Resolution Record IDs and Digests
ABORTED Resolution Record IDs and Digests
Resolution Lineage References
Source Applicability References
Evidence References
Compatibility Evidence References
Dependency Closure Reference
Conflict Detection Rule Version
Conflict Set Digest
```

冲突集不得只保存计数、最终原因码或一个代表性来源。

### DM-R5-22 来源排除必须具有制度依据

任何被排除的解析来源必须引用版本化制度排除依据，至少绑定：

```text
Excluded Record ID and Digest
Exclusion Rule ID and Version
Allowed Source Type and Scope
Exclusion Reason Code
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Exclusion Authority Reference
Institution Freeze Reference
Evidence References
```

投影构建者不得因为来源较旧、不方便、数量较少或导致冲突而排除来源。

### DM-R5-23 投影发布必须消费兼容外部接口

本提案不复制投影变化审计和发布外壳模型。若系统发布 `Resolution Projection`，必须消费兼容外部接口并满足：

```text
Candidate Resolution Projection
-> Candidate Projection Change Audit
-> Content-identical Registered Projection Change Audit
-> Projection Publication Envelope
```

发布外壳必须与候选投影使用同一 `Projection View Mode`、投影键和投影摘要。发布能力不创建提交结果或决策事实。

## 七、解析谱系与冲突关系闭合

### DM-R5-24 解析谱系关系必须使用非覆盖语义

单一候选合并时，规范关系为：

```text
INITIAL
REFINES
REAFFIRMS
CONFLICTS_WITH
```

- `REFINES` 只能从 `INDETERMINATE` 提高到一个终局或提供更完整的同向认识；
- `REAFFIRMS` 只重申同一终局，不覆盖其他分支；
- `CONFLICTS_WITH` 显式连接相反可比较终局；
- 并发分支允许引用同一前序记录，不能最后写入获胜。

### DM-R5-25 R3 旧谱系关系必须受控规范化

`R3` 旧关系：

```text
INITIAL
SUPPLEMENTS
REINTERPRETS_UNDER_NEW_KNOWLEDGE
SUPERSEDES_FOR_CURRENT_PROJECTION
PARALLEL_INCOMPATIBLE_VIEW
```

除 `INITIAL` 外不得按名称直接映射。必须通过版本化谱系兼容规则得到：

```text
REFINES
REAFFIRMS
CONFLICTS_WITH
UNRESOLVED_RELATIONSHIP
```

版本化谱系兼容规则至少绑定：

```text
Lineage Compatibility Rule ID and Version
Source Relationship Enum and Contract Version
Target Relationship Enum and Contract Version
Source and Target Semantic Definitions
Allowed Deterministic Relationship Mappings
Non-overwrite Invariant
Conflict Preservation Invariant
Parallel-view Comparability Preconditions
Required Evidence References
Governing Institution ID and Version
Institution Freeze Reference
```

缺少兼容规则、冻结引用或映射证据时不得猜测旧关系语义。

特别禁止：

```text
SUPERSEDES_FOR_CURRENT_PROJECTION
-> delete or hide prior terminal

PARALLEL_INCOMPATIBLE_VIEW
-> silently merge as comparable
```

无法确定旧关系语义时使用 `UNRESOLVED_RELATIONSHIP`，相关投影保持 `INDETERMINATE`。

### DM-R5-26 单条终局不能通过谱系覆盖另一终局

```text
INDETERMINATE -> COMMITTED via REFINES
INDETERMINATE -> ABORTED via REFINES
INDETERMINATE -> INDETERMINATE via REFINES or REAFFIRMS
```

禁止：

```text
COMMITTED -> ABORTED via REFINES
ABORTED -> COMMITTED via REFINES
```

相反终局必须通过 `CONFLICTS_WITH` 保留，并在完整可比较投影中产生 `CONFLICTED`。

## 八、完备投影真值表

### DM-R5-27 完整闭包下的终局真值表

当且仅当投影键稳定、来源语义可比较、来源适用、闭包已登记为 `COMPLETE` 且没有字段未解析时：

```text
Applicable comparable COMMITTED only
-> COMMITTED

Applicable comparable ABORTED only
-> ABORTED

Applicable comparable COMMITTED + ABORTED
-> CONFLICTED

Applicable INDETERMINATE only
-> INDETERMINATE

No applicable registered resolution
-> INDETERMINATE
```

### DM-R5-28 不完整或不可比较输入真值表

任一条件成立：

```text
Dependency Closure != COMPLETE
Compatibility unknown
Projection key field = UNRESOLVED
Source applicability unresolved
Required correction view unresolved
Temporal coordinate mismatch
Projection view mismatch
Legacy lineage relationship unresolved
```

都必须产生：

```text
Resolution Projection = INDETERMINATE
```

若已经证明存在相反可比较终局，但其他非冲突依赖仍不完整，必须保存冲突来源，同时对可消费投影失败关闭；不得用不完整性删除已知冲突证据。

### DM-R5-29 投影结果不授权行动

```text
Resolution Projection = COMMITTED
-/-> Target Execution

Resolution Projection = ABORTED
-/-> Retry

Resolution Projection = INDETERMINATE
-/-> Cancel or Replace Decision

Resolution Projection = CONFLICTED
-/-> Select Preferred Terminal
```

任何行动必须由独立策略或适用治理路径授权。

## 九、与决策事实的最终边界

### DM-R5-30 权威决策记录仍是决策事实唯一正向来源

```text
Authoritative Decision Record
+ Decision Key Attribution
+ Applicable Decision Fact Commit Authority
-> Decision Fact
```

`Resolution Projection = COMMITTED` 只能帮助读取和审计已经存在的权威归因，不能替代权威决策记录或反向创建决策事实。

### DM-R5-31 ABORTED 投影不创建“不存在事实”

```text
Resolution Projection = ABORTED
-> no matched Decision Fact established for declared commit attempt and coordinate
-/-> global nonexistence for every coordinate
-/-> negative Decision Fact object
```

视图、认识边界或契约作用域变化时必须使用新投影键重新解释。

### DM-R5-32 CONFLICTED 投影只表达认识冲突

```text
Resolution Projection = CONFLICTED
-/-> two Decision Facts
-/-> Decision Fact mutation
-/-> automatic invalidation
-/-> evidence deletion
```

它要求失败关闭、保存冲突和进入独立治理处理，但不自行决定哪个终局反映真实权威状态。

## 十、修订后的提交解析投影路径

### DM-R5-33 规范构建路径

```text
Registered Decision Commit Resolution Records
+ Source Applicability Records
+ Correction View
+ Resolution Compatibility Domain if applicable
+ Registered Dependency Closure Record
+ Registered Closure Completeness Record = COMPLETE
+ Resolution Projection Key
-> Resolution Projection Builder
-> Candidate Resolution Projection Record
     -> COMMITTED
     -> ABORTED
     -> INDETERMINATE
     -> CONFLICTED
```

### DM-R5-34 规范视图路径

```text
Resolution Projection
  + Projection View Mode = HISTORICAL_KNOWLEDGE_VIEW
  -> Historical knowledge projection

Resolution Projection
  + Projection View Mode = CURRENT_RESTATEMENT_VIEW
  -> Current restatement projection
  -> may display alias Current Commit Resolution Projection
```

两者都不修改历史解析或决策事实。

## 十一、非法状态候选增补

以下情况在未来合并与冻结时必须明确为非法：

- 把 `Current Commit Resolution Projection` 作为规范类型；
- 省略 `Projection View Mode`；
- 把 `CONFLICTED` 写入单条已登记提交解析；
- 提交解析投影没有 `CONFLICTED`；
- 把相反终局冲突折叠为普通未知；
- 用较新记录、来源多数或身份优先解决冲突；
- 投影键同时填写精确契约和兼容域快照；
- 投影键两类契约作用域都不填写；
- 静默省略规范字段；
- 用来源集合摘要代替依赖闭包完整性；
- 在闭包非 `COMPLETE` 时建立终局投影；
- 用一个注册表边界证明其他注册表完整；
- 开放世界记录缺失被解释为 `ABORTED`；
- 投影构建者登记闭包、资格或自身输出；
- 来源因导致冲突而被临时排除；
- `SUPERSEDES_FOR_CURRENT_PROJECTION` 被实现为覆盖历史；
- 相反终局通过 `REFINES` 互相覆盖；
- 投影结果直接授权执行、重试、取消或终局选择；
- 投影反向创建、撤销或修改决策事实。

发现任一状态时必须失败关闭，保存历史解析、闭包、冲突集、投影候选、来源和证据。

## 十二、对 R4 独立复审唯一阻断的修订映射

| `R4` 复审阻断 | `R5` 修订位置 | 候选闭合方式 |
|---|---|---|
| 提交解析投影契约不完整 | `DM-R5-01` 至 `DM-R5-34` | 规范类型、四值投影、冲突真值表、互斥作用域、闭包完整性、候选载荷、谱系和决策事实边界 |

## 十三、合并与冻结前依赖

本候选即使通过最终组合一致性复审，也不能自动冻结。至少仍需：

```text
Independent R2 + R3 + R4 + R5 Final Composite Consistency Review
Single Candidate Consolidation
Post-consolidation Semantic Diff Review
Frozen or compatible Source Registry Interface
Frozen or compatible Qualification Governance
Frozen or compatible Authority Applicability Governance
Frozen or compatible Derived Record Registration Authority Governance
Frozen or compatible Proof and Exemption Applicability Governance
Frozen or compatible Temporal Mapping Governance
Frozen or compatible Dependency Closure Governance
Frozen or compatible Projection Audit and Publication Interface
Frozen or compatible Institution Registry and Freeze Reference Support
Compatible protected write implementation contract
Repeated and stable runtime evidence
Cross-provider evidence
Cross-project and cross-domain evidence
Applicable Freeze Authority
Independent Freeze Review
Freeze Decision
Successful Institution Commit
```

## 十四、候选自检状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
R4 Review Blocker Mapping: COMPLETE
Resolution Projection Normative Type: DEFINED
Projection View Identity: DEFINED
Registered Resolution Three-value Boundary: DEFINED
Resolution Projection Four-value Outcome: DEFINED
Resolution Projection Conflict Preservation: DEFINED
Resolution Projection Scope Identity: DEFINED
Resolution Projection Field Presence: DEFINED
Resolution Projection Dependency Closure: DEFINED
Candidate Resolution Projection Contract: DEFINED
Resolution Projection Lineage Compatibility: DEFINED
Resolution Projection / Decision Fact Separation: DEFINED
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Independent Final Composite Review: REQUIRED
Consolidation Readiness: NOT_EVALUATED
Model-level Freeze Readiness: NOT_EVALUATED
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

这些自检只说明本草案已经逐项给出候选契约，不构成独立复审、合并、冻结或运行时授权。

## 当前决定

1. 保留 `CR-0002-R2` 至 `CR-0002-R4` 及其审查记录作为不可覆盖历史；
2. 将本文件登记为 `CR-0002-R5` 单阻断纠偏候选；
3. 不修改单条提交解析三值语义；
4. 不重新打开已经闭合的证明、豁免、合法性、更正、登记权威和失败分支契约；
5. 不修改 `IF-0001` 至 `IF-0007`；
6. 不使 `CR-0003` 候选获得冻结制度权威；
7. 不创建 `foundation/07_Decision.md`；
8. 不创建运行时解析、闭包、投影、决策事实或授权；
9. 不创建冻结标识、冻结权威或冻结决定；
10. 下一步只对 `R2 + R3 + R4 + R5` 执行最终组合一致性复审；
11. 最终组合复审通过后才可建立单一候选；
12. 单一候选仍须执行合并后语义差异审查和冻结依赖审计；
13. 在正式冻结以前，本文件不可执行且没有制度权威。
