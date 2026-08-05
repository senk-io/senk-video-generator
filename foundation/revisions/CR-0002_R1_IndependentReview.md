# CR-0002-R1 决策模型独立审查

## 审查信息

```text
Review ID: CR-0002-R1-LOCAL-REVIEW
Review Type: Independent Foundation Model Review
Status: COMPLETED
Result: PASS_WITH_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0002-R1
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, proposal history and dependent candidate graph
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是独立提案审查记录，不是制度冻结。它不能使 `CR-0002-R1` 获得制度权威、创建决策事实、授权目标迁移，或替代 `IF-0007` 要求的正式冻结程序。

## 审查目标

本轮独立回答：

1. `CR-0002-R1` 是否解决原提案已经识别的八项未决问题；
2. 决策是否保持唯一目的，并与权威、证据、策略、执行和目标迁移分离；
3. 确定性准入检查是否因计算结果唯一而取得隐式事实登记权；
4. 合格依据解析和适用权威解析是否拥有外部、版本化的消费边界；
5. 组合决策是否产生隐式联合权威或未登记的豁免事实；
6. 事后合法性审查是否可能覆盖历史或自动改变目标状态；
7. 更正、撤销、取代和失效是否具有互不混淆的历史语义；
8. 当前提案是否具备进入正式冻结审查的模型准备度。

## 审查依据

本轮只采用本地可追踪材料：

```text
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002 Decision Model
CR-0002-R1 Decision Model
CR-0003 Constitution Candidate R2
CR-0003 Freeze Dependency Readiness Audit
AGENTS.md
```

历史对话标识仅作为提案来源元数据，不作为本次结论的审查权威。

## 总体裁决

`CR-0002-R1` 已经修复原提案的主要概念混合：

- 决策事实与目标状态迁移已经分离；
- 裁决倾向与请求迁移类型已经分离；
- 多权威业务要求被拆成多个独立决策；
- 合格依据类型的定义权已经归还具体决策类型制度；
- 提交时准入检查与事后合法性审查已经分离；
- `NO_ACTION`、人工创意裁决和历史追加修正的方向成立。

因此，决策模型的核心方向通过审查。

但本轮发现五项冻结前阻断：

1. `Admissible Decision Record -> Decision Fact` 缺少受保护的权威事实登记边界；
2. 合格依据与适用权威解析缺少独立、版本化、可证明完备的输入契约；
3. `Composite Decision Requirement` 中的豁免和最终成立语义未闭合；
4. 事后合法性审查、失效决策和依赖传播之间的时间与权威边界未闭合；
5. `Correction Record` 缺少独立类型、登记资格和“不改变原决策语义”的明确契约。

这些阻断不要求推翻模型，应通过 `CR-0002-R2` 做有界修订。在修订并复审以前，`CR-0002-R1` 不得进入正式冻结审查。

## 已通过部分

### 一、单一目的通过

`DM-R1-02` 把决策限定为：

> 记录有权主体针对合格依据作出的明确裁决。

并明确排除观察、证据创建、偏差解释、成功定义、自我授权、目标迁移和客观真理证明。

这使决策不再成为吸收所有治理职责的万能对象。

```text
Decision Purpose Uniqueness: PASS
```

### 二、权威与决策分离通过

```text
Authority -> who may decide
Decision -> what was decided
```

一个决策实例只引用一个主要权威，多权威要求必须拆成多个独立决策。这符合 `IF-0001` 的权威不得隐式传播和每项权威必须具有显式边界原则。

```text
Authority / Decision Separation: PASS
```

### 三、决策事实与目标迁移分离通过

```text
Decision Fact
+ Transition Preconditions
+ Successful Institutional Commit
-> Target Formal State Transition
```

发布获批不等于已经发布，选择获批不等于资产已经写入目标生命周期。提交失败也不得反向抹除决策曾经发生。

这条因果方向与 `CR-0003` 的提交模型候选兼容。

```text
Decision / Target Transition Separation: PASS
Decision / Execution Separation: PASS
```

### 四、裁决倾向与迁移类型分离通过

```text
Disposition: APPROVE | REJECT | SUSPEND | NO_ACTION
Requested Transition: CREATE | TRANSITION | SUPERSEDE | REVOKE
```

该拆分能够正确表达“批准撤销”和“拒绝撤销”，消除了原提案将价值裁决与目标迁移编码在同一枚举中的歧义。

```text
Disposition / Transition Type Separation: PASS
```

### 五、准入检查与事后审查的方向通过

`Decision Admissibility Check` 被限定为提交时的确定性规则计算；`Decision Legality Review` 被限定为事后独立检查。二者不应成为新的价值裁决。

```text
Admissibility Check != Decision
Legality Review != Original Decision Mutation
```

概念分离成立，但正式记录和时间边界仍有阻断，见阻断二与阻断四。

```text
Admissibility / Legality Concept Separation: PASS_WITH_BLOCKERS
```

### 六、历史保留方向通过

`R1` 禁止覆盖、删除和原地修改决策事实，要求撤销、取代和失效通过追加历史表达，并禁止使用当前制度追溯否定旧制度下合法决策。

```text
History Preservation Direction: PASS
```

更正和事后解释的完整契约仍需收紧，因此总体历史语义为 `PASS_WITH_BLOCKERS`。

### 七、提供者独立性与跨领域性通过

模型不依赖特定视频生成提供者，也没有把视频领域决策类型固化为基础层全集。具体决策类型、依据、权威和迁移契约由对应治理制度定义。

```text
Provider Independence: PASS
Domain Portability: PASS
```

## 阻断一：决策事实缺少受保护的权威登记边界

### 决策事实登记问题

当前主路径包含：

```text
Deterministic Admissibility Check
  -> Admissible Decision Record
  -> Decision Fact
```

这里尚未区分：

```text
Decision Attempt Record
Candidate Decision Record
Authoritative Decision Record
Decision Fact
```

也没有明确谁有资格把通过准入的候选记录登记进决策权威注册表，以及记录写入失败、重复提交、超时或结果未知时应如何处理。

确定性计算只能证明候选记录满足规则，不能因算法唯一而自动取得正式事实登记权：

```text
Deterministic Computation
-/-> Formal Fact Registration Authority
```

`Decision Act` 的主要权威可以授权裁决行为，但 `R1` 仍必须明确该授权是否同时覆盖决策事实提交、提交由谁履行、权威写入点在哪里，以及事实登记与证据引用是否在同一受保护边界成立。

否则以下失败无法被安全分类：

```text
Decision Act observed
Admissibility evaluated as ADMISSIBLE
Authoritative record write outcome unknown
```

此时不能宣布 `Decision Fact` 已成立，也不能把它降级为确定未成立。

### 决策事实登记必须补充

`CR-0002-R2` 至少需要定义：

```text
Decision Commit Contract
Decision Commit Authority
Decision Attempt Record
Candidate Decision Record
Protected Authoritative Decision Write
Authoritative Decision Record
Decision Fact Attribution
Decision Commit Outcome
```

其中必须明确：

- 准入计算无事实所有权；
- 决策者身份不自动授予注册表写入能力；
- 权威决策记录必须不可变并绑定唯一决策键；
- 重复提交不得创建第二个决策事实；
- 写入结果无法证明时保持 `INDETERMINATE`；
- 决策事实成立与目标对象提交继续保持两个独立边界。

这不是要求决策模型复制完整提交模型，而是要求它定义自己作为正式事实生产者所必须消费的最小提交接口。

### 决策事实登记结论

```text
Decision Fact Establishment: FAIL
Risk Level: HIGH
Required Action: CR-0002-R2
```

## 阻断二：资格与权威解析输入契约未闭合

### 解析输入契约问题

完整路径使用：

```text
Qualified Basis Resolution
Applicable Authority Resolution
```

但 `R1` 没有定义这些输入究竟是：

- 原始注册表记录；
- 一次读取结果；
- 候选解析；
- 已登记解析记录；
- 某一时点的制度投影。

`Decision Admissibility Check` 因而可能被迫自行判断：

- 来源集合是否完备；
- 某条依据是否仍然合格；
- 权威是否已经撤销或取代；
- 更正证据在何时开始影响当前认识；
- 应使用哪个规则版本和制度版本。

这会反向扩大决策模型的职责，使其同时承担资格治理和权威解析。

```text
Decision Admissibility
-/-> Define Basis Qualification
Decision Admissibility
-/-> Create Authority Applicability
```

### 解析输入契约必须补充

应定义最小消费契约，而不是在决策模型内创建全局资格制度：

```text
Registered Basis Qualification Resolution
Registered Authority Applicability Resolution
Resolution Source Set
Source Completeness or Qualified Coverage Proof
Object and Version Coordinate
Effective At
As Of
Resolved At
Rule Version
Institution Version
Evidence and Correction View
Resolution Outcome
```

合法结果至少必须支持：

```text
RESOLVED
INDETERMINATE
```

当来源不可用、来源集合不完备、资格冲突、权威时点不明或规则版本缺失时，准入只能保持 `INDETERMINATE` 并失败关闭。

这些解析记录必须由外部冻结制度和相应登记权威建立。决策模型只能消费，不能为自己的准入临时创造资格或适用权威。

### 解析输入契约结论

```text
External Resolution Boundary: FAIL
Temporal and Version Binding: FAIL
Risk Level: HIGH
Required Action: CR-0002-R2
```

## 阻断三：组合决策的豁免与最终成立语义不完整

### 问题一：NOT_REQUIRED 类型错位

`DM-R1-04` 示例使用：

```text
Decision C = NOT_REQUIRED
```

但 `NOT_REQUIRED` 不属于裁决倾向：

```text
APPROVE | REJECT | SUSPEND | NO_ACTION
```

它应表达某个组合要求槽位在特定条件下被制度豁免，而不是一项不存在的决策结果。

若不分离，系统可能在没有决策、依据和权威的情况下，把“没有记录”解释为“无需决策”。

```text
Decision Record Not Found
-/-> Requirement NOT_REQUIRED
```

### 问题二：Final Decision 可能形成隐式联合权威

`R1` 允许目标制度声明最终状态由：

```text
Final Decision
or
Deterministic Institutional Commit
```

但未进一步约束 `Final Decision`。如果它只是把多个子决策合成为一个结果，就可能重新产生已被本提案禁止的联合权威。

### 组合决策语义必须补充

应分离：

```text
Composite Requirement Slot
  -> REQUIRED | CONDITIONALLY_NOT_REQUIRED

Composite Requirement Resolution
  -> SATISFIED | NOT_SATISFIED | EXEMPT | INDETERMINATE
```

`EXEMPT` 必须引用：

- 允许豁免的目标制度条款；
- 适用对象和版本；
- 豁免条件及其合格证据；
- 解析时点和规则版本；
- 有资格登记豁免解析的权威来源。

若采用 `Final Decision`，它必须是独立决策类型：拥有一个主要权威、自己的合格依据、明确裁决行为和独立决策事实。它不得被解释为多个子权威的自动合并。

若采用确定性提交，则提交器只能检查已经冻结的组合契约，不能创造新的价值裁决或豁免。

### 组合决策语义结论

```text
Composite Decision Semantics: FAIL
Implicit Joint Authority Risk: HIGH
Required Action: CR-0002-R2
```

## 阻断四：事后合法性、失效和依赖传播边界未闭合

### 事后合法性与失效问题

`DM-R1-14` 规定合法性审查可以：

```text
request an invalidation decision
trigger institutional dependency invalidation propagation
```

同时又规定审查者在没有失效权威时不得改变目标状态。

“触发传播”若会让下游正式事实失效，就是状态改变；它不能由一个只负责审查的派生结论直接启动。这两条目前存在边界冲突。

此外，审查结果：

```text
COMPLIANT
NON_COMPLIANT
INDETERMINATE
```

尚未区分候选审查输出和已登记审查记录，也没有强制绑定：

```text
Decision Time
Review Effective At
Review As Of
Reviewed At
Original Rule Version
Review Rule Version
Original Evidence View
Current Evidence and Correction View
```

如果当前更正、当前资格规则或新制度被无时点地应用到历史决策，系统可能借“解释”之名追溯覆盖历史。

### 事后合法性与失效必须补充

应建立以下因果边界：

```text
Historical Decision Record
+ Versioned Source View
+ Legality Review Contract
-> Candidate Legality Review Record

Candidate Legality Review Record
+ Review Registration Authority
-> Registered Legality Review Record

Registered Legality Review Record
-> may support Invalidation Decision Request
-/-> mutate Decision Fact
-/-> propagate formal invalidation
```

只有新的合法失效决策及其成功制度提交，才能改变当前适用状态或授权依赖传播。

同时必须分开：

```text
Historical Legality at Original Coordinate
Current Usability or Applicability
Current Knowledge about Historical Legality
```

新证据可以改变当前认识，不能覆盖原始记录；新制度可以改变未来适用性，不能自动把旧制度时期的合法决策改写为从未合法。

### 事后合法性与失效结论

```text
Legality Review Authority Boundary: FAIL
Historical / Current Interpretation Separation: FAIL
Invalidation Propagation Boundary: FAIL
Risk Level: HIGH
Required Action: CR-0002-R2
```

## 阻断五：更正记录契约不完整

### 更正记录契约问题

`DM-R1-20` 对记录错误只规定：

```text
append Correction Record
preserve Original Record
```

但没有明确：

- 更正的是表示层字段、引用关系，还是决策语义；
- 谁能提出、验证和登记更正；
- 更正依据如何满足 `IF-0006`；
- 更正从何时影响当前读取；
- 更正能否改变裁决倾向、对象、依据、权威或决策时点；
- 多项互相冲突的更正如何解析。

如果 `Correction Record` 能直接改变上述语义字段，它将绕过新的决策、撤销或取代路径。

### 更正记录契约必须补充

```text
Decision Record Correction
  -> may correct representational defect
  -> must preserve original bytes and references
  -> must cite correction evidence
  -> must use independent correction qualification and registration authority
  -> must declare effective and recorded time
  -/-> change Decision Act
  -/-> change Decision Disposition
  -/-> change Primary Authority
  -/-> change Decision Object
  -/-> create or revoke Decision Fact
```

任何会改变决策语义的变化都必须进入新的撤销、取代或失效决策，而不能伪装成记录更正。

### 更正记录契约结论

```text
Correction Boundary: FAIL
Risk Level: MEDIUM
Required Action: CR-0002-R2
```

## 跨模型职责审计

### 决策模型可以定义

```text
Decision semantic invariants
Decision object purpose
Decision act and record separation
Required external resolution interfaces
Admissibility consumption contract
Decision fact establishment contract
History and correction invariants
```

### 决策模型不得定义

```text
Global basis type enumeration
Global authority type enumeration
Basis qualification lifecycle
Authority grant lifecycle
Provider-specific transaction implementation
Domain decision type全集
Dependency propagation algorithm
Objective correctness of creative judgment
```

### 判断

`R1` 已正确移除全局依据全集，但因为外部解析接口不完整，准入检查仍可能在实现时被迫承担资格、来源完备性和权威适用性判断。

因此：

```text
Declared Responsibility Boundary: PASS
Operational Responsibility Closure: FAIL_WITH_BLOCKERS
```

## 与冻结制度的兼容性

| 冻结制度 | 审查结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `FAIL_WITH_BLOCKERS` | 决策事实登记、合法性审查登记、更正登记和组合豁免存在未闭合权威 |
| `IF-0006 Evidence Model` | `FAIL_WITH_BLOCKERS` | 解析输入完备性、时间坐标、更正视图和否定性结果证据未闭合 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、跨领域、提供者独立且不覆盖冻结制度；但不具备冻结证据和正式冻结资格 |
| 五层架构边界 | `PASS_WITH_BLOCKERS` | 基础层职责方向正确；部分外部解析与提交接口仍未封闭 |

## 对原提案八项未决问题的复核

| 原未决问题 | `R1` 处理结果 | 本轮判断 |
|---|---|---|
| 合格依据由谁定义 | 交还具体决策类型制度 | `PASS_WITH_INTERFACE_BLOCKER` |
| 登记观察是否足够 | 默认不足，必须满足资格要求 | `PASS` |
| 合法性检查是否递归 | 拆成确定性准入和事后审查 | `PASS_WITH_REGISTRATION_BLOCKER` |
| 多权威如何处理 | 多个决策加组合要求 | `PASS_WITH_COMPOSITE_BLOCKER` |
| 失效由谁裁决 | 新失效决策加制度传播 | `PASS_WITH_AUTHORITY_AND_TEMPORAL_BLOCKER` |
| `NO_ACTION` 如何保存 | 建立决策事实，不迁移目标 | `PASS` |
| 人工裁决证据要求 | 要求可审计，不要求客观审美证明 | `PASS` |
| 制度冻结是否提高门槛 | 已定义更高最低门槛 | `PASS_AS_CANDIDATE` |

## 独立裁决矩阵

```text
Proposal Completeness: PASS
Single Purpose: PASS
Authority / Decision Separation: PASS
Decision / Evidence Separation: PASS
Decision / Policy Separation: PASS
Decision / Execution Separation: PASS
Decision / Target Transition Separation: PASS
Disposition / Transition Type Separation: PASS
Admissibility / Legality Concept Separation: PASS_WITH_BLOCKERS
Decision Fact Establishment: FAIL
External Resolution Boundary: FAIL
Temporal and Version Binding: FAIL
Composite Decision Semantics: FAIL
Legality Review Authority Boundary: FAIL
Historical / Current Interpretation Separation: FAIL
Correction Boundary: FAIL
History Preservation: PASS_WITH_BLOCKERS
Provider Independence: PASS
Domain Portability: PASS
Model-level Freeze Readiness: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 修订范围约束

`CR-0002-R2` 应只处理本轮五项阻断，不扩大为所有来源、资格、提交和失效实现的总模型。

建议修订顺序：

```text
1. Authoritative Decision Fact Establishment Boundary
2. Qualified Basis and Authority Resolution Consumption Contract
3. Composite Requirement and Exemption Resolution
4. Legality Review, Invalidation and Temporal Interpretation Boundary
5. Decision Record Correction Contract
6. R2 Independent Consistency Review
```

`R2` 应定义外部接口的最小必需字段和失败关闭规则，但不得替代未来独立的来源注册表、资格治理、提交模型或依赖传播制度。

## 独立决定

1. 接受 `CR-0002-R1` 的核心方向；
2. 将本轮模型审查结论登记为 `PASS_WITH_BLOCKERS`；
3. 不冻结 `CR-0002-R1`；
4. 不修改 `CR-0002-R1` 历史正文；
5. 不创建 `foundation/07_Decision.md`；
6. 不创建冻结标识、冻结权威或冻结决定；
7. 下一步建立 `CR-0002-R2`，仅闭合五项阻断；
8. `R2` 完成后执行独立一致性复审；
9. 模型复审通过后仍需重新进行依赖、证据和冻结准备度审计；
10. 在满足 `IF-0007` 前，任何决策模型候选都保持无运行时权威。
