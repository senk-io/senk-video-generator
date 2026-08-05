# CR-0002-R4 决策模型独立组合一致性复审

## 审查信息

```text
Review ID: CR-0002-R4-LOCAL-REVIEW
Review Type: Independent Composite Foundation Model Consistency Review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Candidate: CR-0002-R2 + CR-0002-R3 + CR-0002-R4
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, R2 and R3 review findings, R4 closure clauses and dependent commit candidate interfaces
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是对 `R2 + R3 + R4` 组合候选的独立一致性复审记录，不是制度冻结。它不能使任一提案获得运行时权威，不能创建提交解析、决策事实、登记、投影发布、合并决定或冻结决定。

## 审查命题

本轮独立回答：

1. `R4` 是否严格限定于 `CR-0002-R3-LOCAL-REVIEW` 的三项阻断；
2. 未应用证明资格和适用性值域是否与兼容提交接口一致；
3. 资格投影是否保留冲突、互斥作用域模式和视图身份；
4. 豁免依据适用性是否具有完整候选、登记、谱系和当前投影契约；
5. 合法性审查旧时间字段是否可以确定性进入规范双时间投影键；
6. `R2 + R3 + R4` 合并后是否还存在相邻模型接口冲突；
7. 当前组合是否已经具备单一候选合并准备度。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-R2 Decision Model
CR-0002-R2 Independent Review
CR-0002-R3 Decision Model
CR-0002-R3 Independent Review
CR-0002-R4 Decision Model
CR-0003 Constitution Candidate R2
CR-0003 Constitution Candidate R2 Final Review
```

`CR-0003` 仍是无制度权威的候选。本轮只使用其已通过最终一致性审查的提交解析、资格投影、视图和闭包接口检查兼容性，不据此创建或冻结任何制度。

## 总体裁决

`CR-0002-R4` 遵守三项有界修订范围，并已实质闭合 `R3` 复审提出的全部三项阻断：

1. 证明资格、证明适用性和资格投影已采用兼容四值语义，保留 `CONFLICTED`，增加互斥作用域模式和 `Projection View Mode`；
2. 豁免依据适用性已拥有稳定键、候选记录、内容同一登记、独立授权、追加谱系和可重建投影；
3. 合法性审查已拥有五类规范时间、版本化映射契约、逐字段映射结果、内容同一规范化登记和失败关闭规则。

因此：

```text
R4 Assigned Blocker Closure: PASS
R4 Scope Discipline: PASS
R4 History Preservation: PASS
```

但在完整组合审计中发现一个此前未单独登记的接口阻断：

```text
R3 Current Commit Resolution Projection
!= Compatible Commit Model Resolution Projection
```

具体表现为：

- `R3` 使用 `Current Commit Resolution Projection` 作为规范对象，而兼容提交接口规定 `Current ...` 只能是 `CURRENT_RESTATEMENT_VIEW` 的显示别名；
- `R3` 没有明确提交投影的四值结果，无法规范表达 `COMMITTED` 与 `ABORTED` 的可比较终局冲突；
- `R3` 保存通用 `Conflict References`，但没有规定冲突时必须得到 `CONFLICTED`；
- `R3` 当前投影字段没有强制引用已登记依赖闭包和已登记 `COMPLETE` 闭包完整性；
- `R3` 的提交投影契约作用域仍使用含义宽泛的“精确版本或兼容域”，没有声明字段存在性和兼容语义域。

该问题不推翻 R4，也不重新打开 R4 已闭合的三项阻断；它属于组合候选进入合并前必须关闭的单一投影兼容性阻断。

```text
Structural Direction: PASS
R4 Blocker Closure: PASS
Original R2 Five-blocker Closure: PASS
New Composite Interface Blocker: ONE
Consolidation Readiness: FAIL
Model-level Freeze Readiness: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 已通过部分

### 一、证明资格和适用性接口兼容通过

`DM-R4-01` 至 `DM-R4-03` 已将规范值域统一为：

```text
Proof Qualification:
  QUALIFIED
  DISQUALIFIED
  INDETERMINATE
  CONFLICTED

Proof Applicability:
  APPLICABLE
  INAPPLICABLE
  INDETERMINATE
  CONFLICTED
```

旧草案名称：

```text
NOT_QUALIFIED
NOT_APPLICABLE
```

不能静默改名。缺少语义兼容记录时只能成为 `UNRESOLVED_LEGACY_VALUE` 并进入 `INDETERMINATE` 投影。

候选和已登记证明适用性对象也被要求与兼容提交接口使用同一规范类型，不能建立第二套竞争对象。

```text
Qualification Value Compatibility: PASS
Applicability Value Compatibility: PASS
Legacy Value Non-silent Mapping: PASS
Normative Object Identity: PASS
```

### 二、证明资格投影身份与冲突保留通过

`DM-R4-04` 至 `DM-R4-09` 已建立：

```text
EXACT_CONTRACT_VERSION
xor COMPATIBILITY_DOMAIN_SNAPSHOT
```

并把以下字段纳入稳定键：

```text
Candidate Proof ID
Commit Attempt ID
Decision Key
Qualification Scope Mode
Exact Contract or Compatibility Domain Snapshot
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Rule Compatibility Domain
Source Set Boundary
Correction View
Projection Rule Version
```

资格冲突和适用性冲突被分别保存。真值表不再把 `CONFLICTED` 折叠为普通未知，也不允许按来源数量、登记时间或实现偏好选择一个终局。

```text
Qualification Scope Identity: PASS
Projection View Identity: PASS
Qualification Conflict Preservation: PASS
Applicability Conflict Preservation: PASS
Projection Truth Table: PASS
```

### 三、ABORTED 证明消费边界通过

`DM-R4-10` 要求 `ABORTED` 同时消费：

```text
Historical Registered Qualification = QUALIFIED
Projected Qualification = QUALIFIED
Aggregate Applicability = APPLICABLE
Exact Projection Key
Allowed Projection View Mode
Same Proof, Attempt, Decision Key and Contract Scope
Same Write-set and Temporal Coordinate
Registered Completeness = COMPLETE
Complete Applicable Source Set
Underlying Records and Evidence
No Qualification Conflict
No Applicability Conflict
No Unresolved Contrary Source
```

任一条件缺失时保持提交解析 `INDETERMINATE`，且解析不得创建或修改决策事实。

```text
ABORTED Proof Qualification: PASS
ABORTED Proof Applicability: PASS
ABORTED Completeness Boundary: PASS
ABORTED / Decision Fact Separation: PASS
```

### 四、豁免依据适用性完整契约通过

`DM-R4-11` 至 `DM-R4-18` 已建立：

```text
Registered Exemption Qualification
-> Candidate Exemption Applicability Resolution
-> Content-identical Registered Exemption Applicability Resolution
-> Append-only Applicability Lineage
-> Exemption Applicability Projection
-> may support EXEMPT only when APPLICABLE and COMPLETE
```

候选记录保存资格引用、槽位、对象、迁移、冻结豁免规则、双时间、视图、来源适用性、更正、完备性、相反来源、证据、规则、授权、谱系和摘要。

登记由独立授权实例执行并保持候选载荷同一。适用性投影保留 `CONFLICTED`，没有已登记解析或来源不完整时保持 `INDETERMINATE`。

```text
Exemption Applicability Stable Key: PASS
Candidate Record Contract: PASS
Registration Content Identity: PASS
Applicability Lineage: PASS
Applicability Projection: PASS
EXEMPT Positive Proof Closure: PASS
```

### 五、合法性审查双时间规范化通过

`DM-R4-19` 至 `DM-R4-28` 已分离：

```text
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Review Act Observed At
Review Record Produced At
Review Registered At
```

旧字段必须通过版本化 `Legality Review Temporal Mapping Contract`，逐字段得到：

```text
EXACT_MAPPED
NOT_APPLICABLE
UNRESOLVED
```

规范化采用候选与内容同一登记链。多个旧字段映射到同一目标字段时必须一致，冲突则为 `UNRESOLVED`。候选合法性审查不得预填未来登记时间；`Review Registered At` 只属于登记归因外壳。

任何必需时间无法规范化时，合法性投影必须为 `INDETERMINATE`，不能支持失效请求或历史认识声明。

```text
Canonical Temporal Field Separation: PASS
Legacy Temporal Mapping Contract: PASS
Per-field Mapping Evidence: PASS
Temporal Normalization Registration: PASS
Candidate / Registration Time Separation: PASS
Legality Projection Key Mapping: PASS
Non-retroactive Knowledge: PASS
```

### 六、R2 原五项阻断主体闭合通过

| `R2` 原阻断 | 最终组合处理 | 本轮结果 |
|---|---|---|
| 派生记录登记权威拓扑不完整 | `R3` 通用接口、逐类型授权、登记尝试和内容同一 | `PASS` |
| `ABORTED` 缺少证明资格及解析演进契约 | `R3` 证明链和谱系，`R4` 规范值域、作用域、视图和完备性 | `PASS` |
| 组合要求与豁免缺少完整记录契约 | `R3` 组合记录，`R4` 豁免适用性完整链 | `PASS` |
| 合法性审查和更正投影缺少谱系及双时间边界 | `R3` 谱系与更正时间，`R4` 审查时间规范化 | `PASS` |
| 准入失败与提交未知存在术语类型歧义 | `R3` 非准入尝试和提交认识未知分离 | `PASS` |

原五项阻断闭合不自动证明所有组合接口均已闭合；下一节登记的是完整组合审计发现的新阻断。

## 唯一阻断：提交解析投影契约仍不完整

### 规范投影类型不一致

`DM-R3-14` 使用：

```text
Current Commit Resolution Projection
```

兼容提交接口使用：

```text
Resolution Projection
+ Projection View Mode
```

并明确：

```text
Current ... Projection
-> display alias for CURRENT_RESTATEMENT_VIEW only
```

若把“当前”写入规范类型名称，历史认识视图和当前重述视图将无法共享同一稳定类型，也可能让实现把当前重述当成唯一真值。

### 提交投影结果缺少 CONFLICTED

单条已登记提交解析保持三值：

```text
COMMITTED
ABORTED
INDETERMINATE
```

但提交解析投影必须保持四值：

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

`R3` 只声明 `Current Resolution Outcome` 和通用 `Conflict References`，没有规定：

```text
Comparable applicable COMMITTED + ABORTED
-> Resolution Projection = CONFLICTED
```

若只使用 `INDETERMINATE`，会把“已证明存在相反终局来源”与“当前证据不足”混为同一认识。

### 依赖闭包完整性未成为投影必需输入

`R3` 当前提交投影保存：

```text
Source Set Digest
Coverage Qualification References
Conflict References
```

但没有强制绑定：

```text
Registered Dependency Closure Record
Registered Closure Completeness Record = COMPLETE
Temporal Query Coordinate
Closure Digest
```

来源集合摘要只证明给定集合内容同一，不能证明依赖全集完整。缺少已登记闭包和完整性时，不得建立终局提交投影。

### 契约作用域字段存在性仍不精确

`R3` 投影键使用：

```text
Commit Contract ID and Version or Compatible Contract Domain Snapshot
```

但没有声明：

```text
Exact Contract Scope
xor Compatible Contract Domain Snapshot
```

也没有要求兼容域声明提交解析语义域、成员版本、成员摘要、规则版本和制度冻结引用。

### 必须补充的最小闭合

下一修订必须只为提交解析投影补齐：

```text
Normative Type: Resolution Projection
Current alias limited to CURRENT_RESTATEMENT_VIEW
Outcome: COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
Conflict truth table
Exact contract scope xor compatible domain snapshot
Projection View Mode
Registered Dependency Closure Reference
Registered Closure Completeness = COMPLETE for terminal projection
Source, lineage, conflict and temporal references
Projection / Decision Fact separation
```

```text
Registered Commit Resolution Three-value Semantics: PASS
Resolution Projection Normative Type: FAIL
Resolution Projection Conflict Outcome: FAIL
Resolution Projection Dependency Closure: FAIL
Resolution Projection Contract Scope Identity: FAIL
Risk Level: HIGH
Required Action: CR-0002-R5
```

## 权威与对象拓扑审计矩阵

| 行为 | 角色或对象 | 所需边界 | 是否可创建正式事实 | 本轮结果 |
|---|---|---|---|---|
| 计算证明资格 | `Proof Qualification Resolver` | 独立资格计算授权 | 否 | `PASS` |
| 登记证明资格 | `Proof Qualification Registrar` | 独立资格登记权威 | 否 | `PASS` |
| 解析证明适用性 | `Qualification Applicability Resolver` | 独立适用性解析授权 | 否 | `PASS` |
| 登记证明适用性 | `Qualification Applicability Registrar` | 独立适用性登记权威 | 否 | `PASS` |
| 构建证明资格投影 | `Qualification Projection Builder` | 投影构建授权 | 否 | `PASS` |
| 解析豁免适用性 | `Exemption Applicability Resolver` | 独立解析授权 | 否 | `PASS` |
| 登记豁免适用性 | `Exemption Applicability Registrar` | 独立登记权威 | 否 | `PASS` |
| 构建豁免适用性投影 | `Exemption Applicability Projection Builder` | 投影构建授权 | 否 | `PASS` |
| 规范化合法性时间 | `Legality Review Temporal Normalizer` | 独立规范化授权 | 否 | `PASS` |
| 登记时间规范化 | `Temporal Normalization Registrar` | 独立登记权威 | 否 | `PASS` |
| 构建提交解析投影 | 未完整规范化 | 提交投影构建授权 | 否 | `FAIL` |
| 提交解析投影 | `Current Commit Resolution Projection` | 规范类型、闭包、冲突和作用域 | 否 | `FAIL` |

## 与冻结制度的兼容性

| 冻结制度 | 审查结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `PASS_WITH_ONE_BLOCKER` | 新增计算和登记角色保持分权；提交投影构建边界尚未完整规范化 |
| `IF-0006 Evidence Model` | `FAIL_WITH_ONE_BLOCKER` | 提交投影缺少冲突结果和已登记依赖闭包完整性，可能丢失冲突或误判来源全集 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 全部文件保持草案、不可执行、无冻结权威且不覆盖历史 |
| 五层架构边界 | `PASS_WITH_ONE_BLOCKER` | 规则保持基础层范围；唯一缺口属于提交投影接口兼容性 |

## 独立裁决矩阵

```text
Proposal Completeness: PASS
Single Purpose: PASS
R4 Scope Discipline: PASS
R4 Assigned Blocker Closure: PASS
Proof Qualification Value Compatibility: PASS
Proof Applicability Value Compatibility: PASS
Proof Conflict Preservation: PASS
Qualification Projection Scope Identity: PASS
Qualification Projection View Identity: PASS
ABORTED Proof Closure: PASS
Exemption Applicability Candidate Contract: PASS
Exemption Applicability Registration Contract: PASS
Exemption Applicability Lineage: PASS
Exemption Applicability Projection: PASS
EXEMPT Positive Proof Closure: PASS
Legality Review Canonical Temporal Fields: PASS
Legacy Review Temporal Mapping: PASS
Legality Record / Projection Key Mapping: PASS
Original R2 Five-blocker Closure: PASS
Registered Commit Resolution Semantics: PASS
Resolution Projection Normative Type: FAIL
Resolution Projection Conflict Preservation: FAIL
Resolution Projection Dependency Closure: FAIL
Resolution Projection Contract Scope Identity: FAIL
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Consolidation Readiness: FAIL
Model-level Freeze Readiness: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## R5 修订范围约束

`CR-0002-R5` 应只处理本轮唯一阻断：

```text
Normalize Decision Commit Resolution Projection Contract
```

最低范围：

1. 使用规范 `Resolution Projection` 类型；
2. 把 `Current ...` 限定为当前重述视图的显示别名；
3. 定义四值投影结果和冲突真值表；
4. 严格定义精确契约作用域与兼容域快照的字段存在性；
5. 要求终局投影消费已登记依赖闭包和 `COMPLETE` 完整性；
6. 保持投影、历史解析和决策事实分离。

`R5` 不得：

- 修改单条提交解析的三值语义；
- 重写 `ABORTED` 证明资格链；
- 修改豁免适用性契约；
- 修改合法性审查时间规范化；
- 修改派生登记权威拓扑；
- 修改组合槽位、更正投影或失败分支类型；
- 复制整个提交模型；
- 使 `CR-0003` 获得冻结制度权威；
- 修改 `IF-0001` 至 `IF-0007`；
- 创建单一候选、冻结标识或运行时权威。

## 独立决定

1. 接受 `CR-0002-R4` 对三项指定阻断的闭合；
2. 确认 `R2` 独立审查最初登记的五项阻断已经全部闭合；
3. 将完整组合审计发现的提交解析投影兼容性登记为唯一有界阻断；
4. 将本轮结果登记为 `PASS_WITH_ONE_BOUNDED_BLOCKER`；
5. 不修改 `CR-0002-R2`、`CR-0002-R3`、`CR-0002-R4` 或任何历史审查；
6. 不合并、不冻结、不执行当前组合候选；
7. 不创建 `foundation/07_Decision.md`；
8. 下一步建立 `CR-0002-R5`，只闭合提交解析投影契约；
9. `R5` 完成后执行最终组合一致性复审；
10. 最终组合复审通过后才可建立单一候选；
11. 单一候选仍须接受合并后语义差异审查和冻结依赖审计；
12. 在正式冻结以前，全部决策模型提案保持不可执行且没有制度权威。
