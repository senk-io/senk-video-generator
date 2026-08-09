# 依赖闭包治理提案

## 提案信息

```text
Proposal ID: CR-0011
Title: Dependency Closure Governance
Workstream: WS-08
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: NORMATIVE_MODEL_CANDIDATE
Depends On: CR-0005-R11 SOURCE REGISTRY INTERFACE COMPOSITE
Depends On: CR-0006-R10 TEMPORAL MAPPING GOVERNANCE COMPOSITE
Depends On: CR-0010-R3 DERIVED RECORD REGISTRATION GOVERNANCE COMPOSITE
Consumer Interface: CR-0002-CONSTITUTION-CANDIDATE
Consumer Interface: CR-0003-CONSTITUTION-CANDIDATE-R2
Future Consumer: WS-09 PROJECTION AUDIT AND PUBLICATION INTERFACE
Cross-interface Reviews Required: YES
Independent Composite Model Review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本提案建立指定根、坐标、必需边规则和注册表作用域上的可重放依赖闭包及独立完整性。它不创建根业务事实、不决定适用性、不构建终局投影，也不传播候选或未提交失效。

## 一、单一目的与边界

### DCG-C-01 单一目的

```text
Registered Closure Root Resolution
+ Registered Required-edge Rule
+ Registered Complete Registry Scope Set
+ Exact Temporal Coordinate
  -> Candidate Dependency Closure
  -> Registered Dependency Closure
  -> Independent Registered Closure Completeness
  -> Dependency Closure Reference
```

### DCG-C-02 闭包构建不等于完整性

```text
Closure Computation Authority != Closure Completeness Authority
Closure Registration Authority != Completeness Registration Authority
```

### DCG-C-03 闭包不创建业务事实

闭包不能创建或改写决策、提交、资格、适用性、来源、时间、失效、豁免或目标状态事实。

### DCG-C-04 摘要不证明完整

闭包摘要只证明已给节点／边集合的内容身份；没有独立注册表边界和完整性登记时不得推断全集完整。

## 二、规范对象

### DCG-C-05 对象家族必须封闭

```text
Closure Root Resolution
Required-edge Rule
Registry Scope Contract
Registered Registry Scope Set Boundary
Candidate Dependency Closure Record
Registered Dependency Closure Record
Candidate Closure Completeness Record
Registered Closure Completeness Record
Dependency Closure Reference
Closure Rebuild Requirement
Closure Invalidation Input
Propagation Input Boundary
Closure Correction Record
```

### DCG-C-06 WS-07 精确类型合同

本模型向 WS-07 提供：

```text
Candidate Dependency Closure Record
  -> Registered Dependency Closure Record

Candidate Closure Completeness Record
  -> Registered Closure Completeness Record

Candidate Closure Rebuild Requirement
  -> Registered Closure Rebuild Requirement
```

每个映射拥有精确 schema、稳定键、账本作用域、更正合同和逐类型授权导入元组。

## 三、闭包根与坐标

### DCG-C-07 根类型必须登记

允许根至少包括已登记决策解析、提交解析、资格投影输入、适用性解析、组合要求解析及提供方明确登记的新根类型。自由类型或裸 ID 不可作根。

### DCG-C-08 根解析稳定键

```text
Closure Root Resolution Semantic Key =
  Root Type Contract ID and Version
+ Root Record ID, Version and Payload Digest
+ Root Registry ID and Scope
+ Validity As Of
+ Knowledge Boundary Vector K
+ Temporal Query Coordinate Q
+ Coordinate Subject S and RR
+ Projection View Mode
+ Root Resolution Rule Version
```

### DCG-C-09 根必须是登记单例

根解析固定根记录登记解析、完整竞争边界及独立完整性。未登记、冲突或身份未知的根不能支持确定闭包。

### DCG-C-10 坐标不得默认当前值

有效时点、认识向量、查询主体、视图模式或根版本缺失时为 `INDETERMINATE`；构建者不得取系统时间、最新位置或当前投影补足。

## 四、必需边规则

### DCG-C-11 必需边规则稳定键

```text
Required-edge Rule Semantic Key =
  Required-edge Rule Registry ID and Version
+ Root Type
+ Closure Semantic Domain
+ Rule ID and Version
```

结果、构建者和登记时间不得换键。

### DCG-C-12 规则载荷必须精确

至少固定：

```text
Allowed Node and Edge Types
Per-node Required Edge Types
Edge Direction and Multiplicity
Conditional Edge Predicates
Terminal Node Contract
Institutional Exclusion Contract
Registry Scope Derivation Contract
Open-world / Closed-world Semantics
Traversal and Cycle Contract
Missing and Conflict Behavior
Canonical Ordering and Digest Contract
```

### DCG-C-13 规则先冻结后登记

候选、精确制度冻结、登记尝试和已登记规则摘要必须相等，并进入完整竞争边界和独立完整性。只有四值登记解析 `REGISTERED` 单例可用。

### DCG-C-14 规则版本变化产生新闭包身份

新边类型、条件、终止、排除或世界语义不能重解释历史闭包，必须形成新规则版本和新闭包。

## 五、注册表作用域集合

### DCG-C-15 每个注册表作用域必须独立

来源、证据、更正、资格、适用性、决策、提交、兼容、排除、闭包及其他账本分别声明注册表 ID、命名空间、边界和完整性接口。一个水位不能覆盖另一个注册表。

### DCG-C-16 作用域集合稳定键

```text
Registry Scope Set Semantic Key =
  Root Resolution ID and Digest
+ Required-edge Rule ID, Version and Payload Digest
+ Exact Temporal Coordinate Digest
+ Registry Scope Derivation Rule Version
```

### DCG-C-17 候选作用域集合固定预期与观察全集

固定预期注册表类型／ID／作用域集合、观察集合、明确不适用集合、缺失集合、冲突集合、逐集合摘要和相等证明。

### DCG-C-18 作用域集合必须内容同一登记

候选、尝试和已登记作用域集合边界摘要相等；独立完整性为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。只有登记且 `COMPLETE` 可支持确定闭包。

## 六、闭包构建

### DCG-C-19 闭包稳定键

```text
Dependency Closure Semantic Key =
  Root Resolution ID and Digest
+ Required-edge Rule ID, Version and Payload Digest
+ Registered Registry Scope Set Boundary ID and Digest
+ Registry Scope Set Completeness Resolution ID and Digest
+ Exact Temporal Coordinate Digest
+ Closed-world / Open-world Semantics
+ Traversal Rule Version
```

节点、边、结果、构建者和生成时间不得换键。

### DCG-C-20 候选闭包必须保存完整遍历状态

```text
Exact Root Set and Digest
Exact Visited Node Set and Digest
Exact Evaluated Required-edge Set and Digest
Exact Included Edge Set and Digest
Exact Institutionally Excluded Edge Set and Digest
Exact Missing Edge Set and Digest
Exact Conflicted Edge Set and Digest
Exact Unresolved Frontier Set and Digest
Per-registry Boundary and Completeness References
Cycle and Strongly-connected-component References
Traversal Trace Digest
Canonical Closure Digest
```

### DCG-C-21 必需边评价逐边登记

每条必需边保存来源节点、边类型、条件结果、目标解析、注册表、坐标、纳入／排除／缺失／冲突结果、证据和规则。构建者不能从摘要反推逐边事实。

### DCG-C-22 制度排除必须正向证明

排除边必须固定冻结排除规则、适用权威、精确节点／边／坐标、证据和登记解析。未找到目标、类型不认识或读取失败不能作为制度排除。

### DCG-C-23 开放世界缺失保持未解析

```text
Open-world + edge not found -> UNRESOLVED_FRONTIER
```

不能推断目标不存在、不适用或制度排除。

### DCG-C-24 封闭世界否定要求权威枚举边界

只有注册表边界登记完整、枚举合同冻结且集合相等证明成立时，缺失边可登记为确定缺失；否则保持未解析。

### DCG-C-25 环不能被静默截断

闭包保存环和强连通分量。规则允许的内容同一环可作为完整分量处理；禁止环、未知环或不完整分量必须保留为冲突或未解析前沿。

## 七、闭包登记

### DCG-C-26 候选和登记业务载荷必须内容同一

```text
Candidate Closure Payload Digest
= Attempted Registered Payload Digest
= Registered Closure Business Payload Digest
```

登记不能改变节点、边、排除、缺失、冲突、前沿、坐标或摘要。

### DCG-C-27 闭包登记使用 WS-07 精确合同

登记尝试、类型合同、逐类型授权、幂等逻辑记录、同键异载荷冲突、更正和取代均消费 `CR-0010-R3`。

### DCG-C-28 闭包竞争边界必须完整

同一闭包语义键下全部候选、尝试、登记记录、失败、永久空洞和解析谱系进入一个竞争边界；只有登记完整边界上的唯一内容身份可消费。

## 八、闭包完整性

### DCG-C-29 完整性严格三值

```text
COMPLETE
INCOMPLETE
INDETERMINATE
```

冲突作为独立控制面和证据保留，并安全适配为消费结果 `INDETERMINATE`。

### DCG-C-30 `COMPLETE` 要求全部正向条件

```text
All roots visited
All required edges evaluated
All discovered nodes included or institutionally excluded
No unresolved frontier
No unresolved edge or node conflict
All registry scope boundaries registered and COMPLETE
All boundaries match K / Q / S / RR
Causal closure satisfied
Closure candidate registered content-identically
```

### DCG-C-31 `INCOMPLETE` 只允许确定缺口

登记完整来源下存在未访问根、未评价必需边、确定缺失边、非法排除或因果闭包违反可支持 `INCOMPLETE`。未知读取或开放世界缺失不能支持确定否定。

### DCG-C-32 完整性候选固定逐项证明

固定闭包登记解析、根覆盖、必需边覆盖、节点／排除覆盖、前沿空集证明、冲突空集证明、逐注册表边界、坐标匹配、因果闭包、结果、原因码、证据和候选摘要。

### DCG-C-33 完整性计算与登记独立

闭包构建者、闭包登记者、边评价者和投影构建者不能计算或登记最终完整性。完整性计算和登记也彼此分离。

### DCG-C-34 完整性登记使用 WS-07 精确合同

候选与登记载荷内容同一，同键异结果进入竞争边界；最终消费者只接受登记解析单例。摘要不能替代完整性记录。

## 九、闭包引用

### DCG-C-35 闭包引用最低合同

```text
Registered Dependency Closure Record ID and Digest
Registered Closure Completeness Record ID and Digest
Closure and Completeness Registration Resolution IDs and Digests
Projection Key or Consumer Scope
Root Resolution ID and Digest
Required-edge Rule ID, Version and Digest
Registered Registry Scope Set Boundary ID and Digest
Temporal Query Coordinate Q
Knowledge Boundary Vector K
Coordinate Subject S and RR
Projection View Mode
Closure Digest
Underlying Node / Edge / Exclusion / Conflict Set Digests
Evidence References
```

### DCG-C-36 只有登记 `COMPLETE` 支持终局消费者

`INCOMPLETE`、`INDETERMINATE`、登记冲突、开放世界缺失或只有闭包摘要时，终局投影必须保持 `INDETERMINATE`。

## 十、重建、失效与传播输入

### DCG-C-37 变化只创建重建要求

来源适用性、证据更正、资格／适用性、规则、注册表边界或根版本变化产生 `Closure Rebuild Requirement`，不修改历史闭包。

### DCG-C-38 重建要求稳定键

固定原闭包、触发事实、变化类型、受影响节点／边／作用域、原／新坐标、规则、证据和重建原因。相同触发不得产生不兼容范围。

### DCG-C-39 增量重建必须证明未受影响部分可复用

复用子图必须固定原闭包成员、影响边界、内容同一证明和集合差分证明。无法证明时执行完整重建，不能假定缓存有效。

### DCG-C-40 失效不删除历史

新闭包和完整性追加登记；旧闭包仍可在历史坐标重放。更正或失效不能覆盖原节点、边、排除或完整性。

### DCG-C-41 传播只消费已提交事实

`Propagation Input Boundary` 只允许：

```text
Committed Applicability Change Fact
Committed Invalidation Decision Fact
Registered Correction with applicable change resolution
Frozen Dependency Propagation Rule
Propagation Authority
```

候选、审查、怀疑、缺失或未登记适用性不能触发正式传播。

### DCG-C-42 闭包不执行正式传播

本模型只登记传播输入边界和重建要求，不创建失效决策、修改依赖对象、发布投影或授权行动。

## 十一、权威目录

### DCG-C-43 根、规则和作用域分权

```text
ClosureRootResolutionExecutionAuthorityType
ClosureRootResolutionRegistrationAuthorityType
RequiredEdgeRuleCandidateConstructionAuthorityType
RequiredEdgeRuleRegistrationAuthorityType
RequiredEdgeRuleBoundaryConstructionAuthorityType
RequiredEdgeRuleBoundaryRegistrationAuthorityType
RegistryScopeSetConstructionAuthorityType
RegistryScopeSetRegistrationAuthorityType
RegistryScopeSetCompletenessQualificationAuthorityType
RegistryScopeSetCompletenessRegistrationAuthorityType
```

### DCG-C-44 闭包和完整性分权

```text
RequiredEdgeEvaluationAuthorityType
RequiredEdgeEvaluationRegistrationAuthorityType
DependencyClosureBuildExecutionAuthorityType
DependencyClosureRegistrationAuthorityType
DependencyClosureBoundaryConstructionAuthorityType
DependencyClosureBoundaryRegistrationAuthorityType
DependencyClosureBoundaryCompletenessQualificationAuthorityType
DependencyClosureBoundaryCompletenessRegistrationAuthorityType
ClosureCompletenessQualificationExecutionAuthorityType
ClosureCompletenessRegistrationAuthorityType
```

### DCG-C-45 重建和传播输入分权

```text
ClosureRebuildRequirementConstructionAuthorityType
ClosureRebuildRequirementRegistrationAuthorityType
IncrementalReuseProofConstructionAuthorityType
IncrementalReuseProofRegistrationAuthorityType
PropagationInputBoundaryConstructionAuthorityType
PropagationInputBoundaryRegistrationAuthorityType
```

### DCG-C-46 所有授权互不传播

根、规则、作用域、边评价、闭包、完整性、重建、复用证明和传播输入授权互不传播，也不取得来源、适用性、失效决策、传播执行、投影发布或制度冻结权威。

## 十二、非法状态与退出门槛

### DCG-C-47 以下状态必须失败关闭

- 闭包构建者或登记者自证完整；
- 闭包摘要替代节点、边或完整性登记；
- 一个注册表边界证明另一个注册表完整；
- 开放世界缺失被解释为不存在或排除；
- 未登记排除规则删除必需边；
- 环被截断但不保留分量和冲突；
- 未解析前沿仍登记 `COMPLETE`；
- 候选闭包直接成为投影输入；
- 增量重建无复用证明；
- 候选审查、怀疑或来源缺失触发正式传播；
- 重建覆盖历史闭包；
- 闭包创建决策、提交、失效、发布或行动权威。

### DCG-C-48 模型退出门槛

```text
Computation / Completeness Separation: REQUIRED_PASS
Root and Required-edge Determinism: REQUIRED_PASS
Registry Scope Completeness: REQUIRED_PASS
Missing and Conflict Preservation: REQUIRED_PASS
Rebuild and Invalidation: REQUIRED_PASS
WS-02 / WS-03 / WS-07 Compatibility: REQUIRED_PASS
CR-0002 / CR-0003 Consumer Compatibility: REQUIRED_PASS
Independent Model Review: REQUIRED_PASS
Residual Internal and Interface Blockers: REQUIRED_0
```

## 当前决定

```text
CR-0011 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Created: YES
Cross-interface Reviews: REQUIRED
Independent Composite Model Review: REQUIRED
WS-08 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Implementation Evidence: NOT_CREATED
Protected-write Evidence: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 WS-02／WS-03／WS-07 提供方与 CR-0002／CR-0003 消费接口审查，再执行独立模型审查。
