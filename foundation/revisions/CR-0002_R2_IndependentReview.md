# CR-0002-R2 决策模型独立一致性审查

## 审查信息

```text
Review ID: CR-0002-R2-LOCAL-REVIEW
Review Type: Independent Foundation Model Consistency Review
Status: COMPLETED
Result: PASS_WITH_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0002-R2
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, R1 review findings and dependent candidate interfaces
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是独立一致性审查记录，不是制度冻结。它不能使 `CR-0002-R2` 获得运行时权威、创建任何登记权威、批准决策事实提交或替代 `IF-0007` 的冻结程序。

## 审查命题

本轮独立回答：

1. `R2` 是否逐项处理 `CR-0002-R1-LOCAL-REVIEW` 的五项阻断；
2. 候选计算、派生记录登记和正式事实提交是否保持权威分离；
3. `ABORTED` 是否具有充分、版本化且可随认识演进的证明语义；
4. 组合要求和豁免是否拥有完整的记录与登记边界；
5. 合法性审查、失效决策和历史解释是否保持因果与时间分离；
6. 更正是否只改变表示，不借投影覆盖历史；
7. 当前候选是否具备进入冻结准备度审计的模型条件。

## 审查依据

```text
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-R1 Decision Model
CR-0002-R1 Independent Review
CR-0002-R2 Decision Model
CR-0003 Constitution Candidate R2
CR-0003 Freeze Dependency Readiness Audit
AGENTS.md
```

`CR-0003` 候选只用于检查接口兼容性和已发现的证明风险，不构成冻结制度，也不反向授权本提案。

## 总体裁决

`CR-0002-R2` 已经完成以下实质修复：

- 将决策行为尝试、候选决策、准入解析、决策事实提交和目标迁移拆成独立阶段；
- 明确 `ADMISSIBLE` 不等于 `Decision Fact`；
- 为决策事实增加受保护权威写入和唯一决策键；
- 为依据资格与权威适用性增加版本、时点、来源范围和更正视图契约；
- 将组合槽位、豁免和最终决策从裁决倾向中分离；
- 将合法性审查、失效决策和依赖传播分开；
- 将更正限制为非语义表示修正；
- 保持决策事实与目标迁移的因果分离。

因此，`R2` 的主体结构和修订方向通过审查。

但新增闭合结构仍有五项阻断：

1. 多类派生记录登记权威被引用，但没有形成完整、可审计的授权拓扑；
2. `ABORTED` 缺少未应用证明的资格、适用性和随时间演进的解析契约；
3. 组合要求和豁免缺少完整候选记录、登记记录与谱系字段；
4. 合法性审查与更正投影缺少登记内容同一性、解析谱系和双时间适用边界；
5. 准入失败与提交未知的两个分支仍存在会污染正式语义的术语歧义。

这些问题不要求推翻 `R2`，应由 `CR-0002-R3` 做第二轮有界闭合。在完成修订和复审以前，`R2` 不具备模型级冻结准备度。

## 已通过部分

### 一、决策事实成立因果通过

`R2` 已明确：

```text
Registered Admissibility Record = ADMISSIBLE
-/-> Decision Fact
```

只有受保护权威写入才能建立：

```text
Authoritative Decision Record
-> Decision Fact
```

这修复了 `R1` 中确定性准入计算可能直接获得正式事实权威的问题。

```text
Decision Fact Causality: PASS
Admissibility / Fact Separation: PASS
```

否定性提交结果仍有证明资格阻断，见阻断二。

### 二、决策尝试与提交尝试分离通过

`R2` 区分：

```text
Decision Attempt Record
Decision Fact Commit Attempt Record
```

前者记录裁决行为及其输入，后者记录进入权威写入前固定的提交输入。两者都不自动证明决策事实已经成立。

```text
Act Attempt / Commit Attempt Separation: PASS
```

### 三、外部解析消费方向通过

依据资格和权威适用性均被定义为外部、已登记、版本化输入：

```text
Registered Basis Qualification Resolution
Registered Authority Applicability Resolution
```

决策准入不得临时创建资格、恢复权威或在来源不完备时推断正向结果。这解决了 `R1` 反向扩大决策职责的核心风险。

```text
Qualification Ownership Separation: PASS
Authority Applicability Ownership Separation: PASS
Temporal Coordinate Requirement: PASS
```

来源注册表和资格治理制度是否真实存在，仍属于冻结前外部依赖，不属于本轮模型内部阻断。

### 四、决策与目标迁移分离通过

```text
Decision Fact
+ Target Transition Preconditions
+ Independent Target Commit
-> Target Formal State Transition
```

目标状态不能反推决策事实，执行失败也不能抹除已成立决策历史。

```text
Decision / Target Transition Separation: PASS
Decision / Execution Separation: PASS
```

### 五、组合决策的基本方向通过

`R2` 已将：

```text
REQUIRED | CONDITIONALLY_EXEMPTIBLE
```

和：

```text
SATISFIED | NOT_SATISFIED | EXEMPT | INDETERMINATE
```

从决策倾向中分离，并禁止把缺少记录解释为豁免。最终决策也被要求成为拥有一个主要权威的独立决策。

```text
Implicit Joint Authority Prevention: PASS
Composite Semantic Direction: PASS_WITH_BLOCKER
```

阻断来自记录与登记契约不完整，而不是组合决策方向错误。

### 六、合法性审查与失效决策分离通过

```text
Registered Legality Review Record
-> may support Invalidation Decision Request
-/-> Invalidation Decision Fact
-/-> Dependency Invalidation Propagation
```

只有新的合法失效决策及独立适用性提交才能改变当前适用状态。这修复了 `R1` 中“审查可触发传播”与“审查无状态权威”之间的冲突。

```text
Legality Review / Invalidation Separation: PASS
Invalidation / Propagation Separation: PASS
```

### 七、表示更正与语义变更分离通过

`R2` 明确更正不得改变决策行为、权威、对象、裁决倾向、迁移类型、决策时点和事实身份。语义变化必须通过新的撤销、取代或失效决策。

```text
Correction / Semantic Decision Separation: PASS
```

更正投影的时间和谱系仍需补齐，见阻断四。

## 阻断一：派生记录登记权威拓扑不完整

### 登记权威拓扑问题

`R2` 引用了以下登记权威：

```text
Admissibility Registration Authority
Decision Commit Resolution Registration Authority
Composite Resolution Registration Authority
Legality Review Registration Authority
Correction Registration Authority
```

但统一类型边界只明确列出部分执行角色和记录，没有为每一类登记权威建立完整接口，也没有统一声明：

```text
Authority Grant ID and Version
Can Change
Cannot Change
Allowed Candidate Record Types
Allowed Outcome Types
Allowed Object and Version Scope
Allowed Rule Versions
Effective Interval
Content Identity Requirement
Registration Preconditions
Failure Behavior
```

`IF-0001` 要求每项权威显式声明可以改变和不得改变的范围。仅在流程箭头中写入 `Registration Authority`，不能证明适用授权已经存在。

### 内容同一性问题

准入登记和合法性审查登记使用“确定性登记检查”，但只有部分条款明确登记者不得改变内容。组合解析、提交结果解析、合法性审查和更正登记没有统一的不变量：

```text
Registered Content Digest
= Candidate Content Digest
```

若登记者能够在登记时修改结果、原因、时点或来源，就会因拥有登记能力而取得隐式解释权。

### 必须补充的登记权威契约

`R3` 应定义通用但不隐式传播的登记权威接口：

```text
Derived Record Registration Authority Contract
```

每个具体登记类型必须拥有独立授权实例，并至少绑定：

```text
Registration Authority Grant ID
Registered Record Type
Candidate Record Type
Object Scope
Rule Version Scope
Effective Interval
Candidate Digest
Registered Digest
Registration Decision Rule
Registration Evidence
Registered At
```

通用接口只统一字段和不变量，不能让一个授权实例自动登记所有派生记录类型。

### 登记权威拓扑结论

```text
Registration Authority Completeness: FAIL
Content Identity Invariant: FAIL
Risk Level: HIGH
Required Action: CR-0002-R3
```

## 阻断二：ABORTED 证明资格与解析演进未闭合

### 未应用证明只有名称，没有资格链

`R2` 允许：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

但尚未定义：

- 谁组装候选证明；
- 谁计算证明资格；
- 谁登记资格结果；
- 证明引用哪些权威来源；
- 来源集合如何证明完备；
- 证明在哪个提交契约、对象、版本和时间坐标上适用；
- 证据更正或来源适用性变化后如何重新解释；
- 多个相反证明并存时如何失败关闭。

```text
Proof Type Name
-/-> Qualified Proof
```

`Coverage or Completeness Proof Reference` 自身也不能因为被引用就证明来源完备。它必须拥有外部资格和权威来源。

### 历史解析与当前可用认识混合

`Registered Decision Commit Resolution Record` 保存一个版本化提交解析，但没有定义：

```text
Prior Resolution Record References
Resolution Lineage ID
Resolution Relationship
Historical Resolution View
Current Projection View
Source Applicability Change Inputs
Qualification Correction Inputs
Projection Rule Version
```

当证明资格、来源适用性或解析规则随时间变化时，系统需要同时保留：

```text
Historical Resolution Record
Current Reconstructed Projection
```

当前投影可以变为 `INDETERMINATE` 或与历史结论不同，但不能覆盖原始已登记解析。

### ABORTED 使用条件未闭合

安全的 `ABORTED` 至少需要：

```text
Historical Proof Qualification = QUALIFIED
+ Current Qualification Applicability = APPLICABLE
+ Matching Commit Key and Attempt ID
+ Matching Commit Contract Version
+ Matching Temporal Coordinate
+ Complete Applicable Source Set
+ No Unresolved Contrary Source
```

任何条件不成立都必须保持 `INDETERMINATE`。

### 必须补充的最小接口

`R3` 不应复制整个提交模型，但必须选择以下一种方式：

1. 定义自足的最小未应用证明资格与投影接口；或
2. 明确消费一个兼容的受保护提交接口，并列出不可降低的不变量。

最低对象至少包括：

```text
Candidate Non-application Proof Record
Registered Proof Qualification Record
Registered Proof Applicability Resolution
Proof Qualification Projection
Resolution Lineage
Current Resolution Projection
```

这些对象都不能创建或撤销决策事实。

### ABORTED 证明结论

```text
Positive COMMITTED Attribution: PASS
ABORTED Proof Qualification: FAIL
Resolution Evolution Boundary: FAIL
Historical Record Preservation under Reinterpretation: FAIL
Risk Level: HIGH
Required Action: CR-0002-R3
```

## 阻断三：组合要求与豁免缺少完整记录契约

### 组合记录缺口

`R2` 规定组合解析应形成候选记录，再由独立登记权威保存，但没有定义：

```text
Candidate Composite Requirement Resolution Record
Registered Composite Requirement Resolution Record
```

也没有列出登记记录必须绑定的字段。

### 豁免资格缺口

`Qualified Exemption Basis` 被作为输入引用，但没有明确它必须是哪个已登记资格解析、如何绑定来源范围、更正视图和规则版本。

此外，`EXEMPT` 是否定性结论：它证明特定槽位不要求对应决策。若来源不完备，仅仅没有触发必需条件不能建立豁免。

```text
Required Condition Not Observed
-/-> EXEMPT
```

### 必须补充的组合解析记录

候选与登记记录至少需要：

```text
Composite Resolution ID
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Requirement Mode
Referenced Decision Fact IDs
Registered Exemption Basis Resolution IDs
Resolution Outcome
Outcome Reason Codes
Source Set Digest
Coverage or Completeness Proof Reference
Effective At
As Of
Resolved At
Rule and Institution Version
Candidate Digest
Registration Authority Reference
Registered Digest
Evidence References
Prior Resolution References
Resolution Lineage ID
```

`EXEMPT` 必须具有正向、合格且完备的豁免依据；否则使用 `INDETERMINATE`。

### 组合记录结论

```text
Composite Semantic Direction: PASS
Composite Record Contract: FAIL
Exemption Proof Boundary: FAIL
Risk Level: HIGH
Required Action: CR-0002-R3
```

## 阻断四：合法性审查与更正投影的谱系和时间边界不完整

### 合法性审查登记字段不完整

`DM-R2-31` 列出了审查坐标和来源，但没有强制登记记录保存：

```text
Candidate Review Record ID and Digest
Reviewer Identity
Registration Authority Reference
Registered Record Digest
Registered At
Prior Review Record References
Review Lineage ID
Review Relationship
```

因此，系统无法证明登记内容与候选内容相同，也无法表达后续审查是补充、更正、取代当前投影还是仅提供并列解释。

### 当前重建缺少稳定投影键

`CURRENT_RECONSTRUCTION` 定义了视图方向，但没有稳定键约束：

```text
Reviewed Decision Fact ID
Review Mode
Effective At
As Of
Rule Compatibility Domain
Source Set Boundary
Correction View
```

没有稳定投影键，不同来源范围和规则版本的结果可能被错误地当作同一个“当前合法性”。

### 更正时间字段存在回写歧义

更正记录使用：

```text
Effective At
As Of
Registered At
```

但没有区分：

```text
Corrected Historical Coordinate
Correction Known At
Correction Applicable From
Projection Produced At
```

如果把 `Effective At` 解释为更正从历史时点起覆盖读取，就可能制造当时系统已经知道该更正的假历史。

### 更正投影缺少解析角色与谱系

`Current Decision Read Projection` 被声明为可重建，但没有定义：

- 谁构建候选投影；
- 谁登记或发布投影；
- 投影是否只是可删除读面；
- 如何处理多项更正的先后、取代和冲突；
- 如何绑定投影规则版本和来源完备性；
- 如何保证投影不反向成为新的权威决策记录。

### 必须补充的双时间投影边界

```text
Original Record: immutable historical source
Correction Record: append-only knowledge change
Historical View: what was recorded and known at declared coordinate
Current Projection: rebuildable interpretation under declared source view
```

任何当前投影都必须绑定稳定投影键、来源集合、规则版本、谱系和产生时间。投影不得成为决策事实或修改权威记录。

### 审查与更正投影结论

```text
Legality / Invalidation Causality: PASS
Legality Review Registration Contract: FAIL
Current Review Projection Key: FAIL
Correction Bitemporal Semantics: FAIL
Correction Projection Lineage: FAIL
Risk Level: HIGH
Required Action: CR-0002-R3
```

## 阻断五：失败分支术语仍可能污染正式语义

### 准入失败分支歧义

完整路径写为：

```text
INADMISSIBLE -> Illegal or Rejected Decision Attempt Record
```

这里的 `Rejected` 容易与合法裁决倾向 `REJECT` 混淆。

一个裁决倾向为 `REJECT` 的决策完全可能通过准入并形成合法决策事实；而一个因字段或权威不合格而未通过准入的行为，只是：

```text
NON_ADMISSIBLE_DECISION_ATTEMPT
```

是否属于违法行为还可能需要独立制度分类，不能由准入枚举自动扩大为法律或责任判断。

### 提交未知分支歧义

完整路径写为：

```text
INDETERMINATE -> Decision Fact Status Unknown
```

这可能被实现为权威决策事实自身的一个状态。正确语义应是：

```text
Decision Commit Resolution = INDETERMINATE
Decision Fact Existence = unresolved at declared coordinate
```

未知属于解析认识，不属于决策事实生命周期。系统不得为了表达未知而创建或修改决策事实。

### 术语修订结论

```text
Failure Branch Type Safety: FAIL
Risk Level: MEDIUM
Required Action: CR-0002-R3
```

## R1 五项阻断闭合复核

| `R1` 阻断 | `R2` 处理 | 本轮结论 |
|---|---|---|
| 决策事实缺少受保护登记边界 | 增加候选、准入、提交尝试、受保护写入和权威记录 | `PASS_WITH_PROOF_AND_REGISTRATION_BLOCKERS` |
| 资格与权威解析输入未闭合 | 增加外部已登记解析、时间和来源边界 | `PASS` |
| 组合决策豁免与最终语义不完整 | 增加槽位、豁免和独立最终决策 | `PASS_WITH_RECORD_BLOCKER` |
| 事后合法性、失效和传播未闭合 | 增加双视图、独立登记、新失效决策和传播门槛 | `PASS_WITH_LINEAGE_BLOCKER` |
| 更正记录契约不完整 | 限定非语义更正并增加资格登记 | `PASS_WITH_BITEMPORAL_BLOCKER` |

## 权威拓扑审计矩阵

| 行为 | 执行角色 | 所需授权 | 是否可创建正式事实 | 本轮结果 |
|---|---|---|---|---|
| 行使裁决 | `Decision Maker` | 主要决策权威 | 只有成功提交后 | `PASS` |
| 计算准入 | `Admissibility Resolver` | 准入计算授权 | 否 | `PASS` |
| 登记准入 | `Admissibility Registrar` | 准入登记权威 | 否 | `INCOMPLETE_AUTHORITY_CONTRACT` |
| 提交决策事实 | `Decision Fact Committer` | 决策事实提交权威 | 是 | `PASS_WITH_PROOF_BLOCKER` |
| 解析提交结果 | `Decision Commit Resolver` | 提交解析授权 | 否 | `PASS_WITH_EVOLUTION_BLOCKER` |
| 登记提交解析 | 未完整定义 | 提交解析登记权威 | 否 | `FAIL` |
| 解析组合要求 | `Composite Resolver` | 组合解析授权 | 否 | `INCOMPLETE_RECORD_CONTRACT` |
| 登记组合解析 | 未完整定义 | 组合解析登记权威 | 否 | `FAIL` |
| 审查合法性 | `Legality Reviewer` | 合法性审查授权 | 否 | `PASS_WITH_RECORD_BLOCKER` |
| 登记合法性审查 | 未完整定义 | 审查登记权威 | 否 | `FAIL` |
| 登记表示更正 | 未完整定义 | 更正登记权威 | 否 | `FAIL` |
| 作出失效决策 | 获授权决策者 | 失效决策权威 | 成功提交后是 | `PASS` |
| 传播失效 | 外部传播执行者 | 传播权威 | 改变下游当前适用性 | `PASS_AS_EXTERNAL_INTERFACE` |

## 与冻结制度的兼容性

| 冻结制度 | 审查结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `FAIL_WITH_BLOCKERS` | 多类登记权威仍是流程引用，尚未形成完整授权对象与作用域 |
| `IF-0006 Evidence Model` | `FAIL_WITH_BLOCKERS` | 未应用证明资格、来源适用性、解析谱系及更正双时间未闭合 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、提供者独立、跨领域和历史不覆盖；没有冻结权威 |
| 五层架构边界 | `PASS_WITH_BLOCKERS` | 基础语义正确，派生记录与投影接口仍需精确化 |

## 独立裁决矩阵

```text
Proposal Completeness: PASS
Single Purpose: PASS
Decision / Authority Separation: PASS
Decision / Evidence Separation: PASS
Decision / Execution Separation: PASS
Decision / Target Transition Separation: PASS
Decision Attempt / Commit Attempt Separation: PASS
Admissibility / Decision Fact Separation: PASS
External Qualification Ownership: PASS
External Authority Applicability Ownership: PASS
Positive Decision Fact Attribution: PASS
Registration Authority Completeness: FAIL
ABORTED Proof Qualification: FAIL
Resolution Evolution Boundary: FAIL
Composite Record Contract: FAIL
Exemption Proof Boundary: FAIL
Legality Review Registration Contract: FAIL
Correction Bitemporal Semantics: FAIL
Failure Branch Type Safety: FAIL
History Preservation Direction: PASS_WITH_BLOCKERS
Provider Independence: PASS
Domain Portability: PASS
Model-level Freeze Readiness: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## R3 修订范围约束

`CR-0002-R3` 应只处理本轮五项阻断：

```text
1. Complete Derived-record Registration Authority Topology
2. Qualified Non-application Proof and Resolution Evolution Interface
3. Composite Requirement and Exemption Record Contract
4. Legality and Correction Projection Lineage with Bitemporal Semantics
5. Failure Branch Type Repair
```

`R3` 不得：

- 在决策模型中实现完整来源注册表；
- 创建全局资格类型全集；
- 复制整个提交模型；
- 定义具体领域决策类型；
- 把派生投影提升为正式事实；
- 使任何登记权威隐式传播到其他记录类型；
- 修改 `IF-0001` 至 `IF-0007`；
- 创建冻结标识或运行时权威。

## 独立决定

1. 接受 `CR-0002-R2` 的主体结构和因果方向；
2. 将本轮审查登记为 `PASS_WITH_BLOCKERS`；
3. 不冻结 `CR-0002-R2`；
4. 不修改 `CR-0002-R2` 历史正文；
5. 不创建 `foundation/07_Decision.md`；
6. 不创建冻结标识、冻结权威或冻结决定；
7. 下一步建立 `CR-0002-R3`，只修复五项有界阻断；
8. `R3` 完成后执行独立一致性复审；
9. 模型一致性通过后仍需重新审计外部依赖、运行证据和 `IF-0007` 冻结条件；
10. 在正式冻结以前，全部决策模型提案均保持不可执行且无制度权威。
