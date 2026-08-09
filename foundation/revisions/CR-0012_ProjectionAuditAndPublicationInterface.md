# 投影审计与发布接口治理提案

## 提案信息

```text
Proposal ID: CR-0012
Title: Projection Audit and Publication Interface
Workstream: WS-09
Status: DRAFT
Authority: NONE
Executable: NO
Depends On: CR-0006-R10 TEMPORAL MAPPING GOVERNANCE COMPOSITE
Depends On: CR-0010-R3 DERIVED RECORD REGISTRATION GOVERNANCE COMPOSITE
Depends On: CR-0011-R2 DEPENDENCY CLOSURE GOVERNANCE COMPOSITE
Consumer Interface: CR-0002-CONSTITUTION-CANDIDATE
Consumer Interface: CR-0003-CONSTITUTION-CANDIDATE-R2
Cross-interface Reviews Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本提案治理候选投影、变化审计登记和内容同一发布。投影是可删除重建的认识读面，不创建决策、提交、解析、失效或行动事实。

## 一、边界和对象

### PAG-C-01 单一目的

```text
Registered Projection Contract
+ Exact Projection Stable Key
+ Registered COMPLETE Dependency Closure Reference
+ Candidate Projection Snapshot
+ Registered Content-identical Change Audit
+ Projection Publication Authority
  -> Projection Publication Envelope
```

### PAG-C-02 投影与事实严格分离

投影结果不创建或修改正式事实、历史解析、目标状态、重试、取消、失效或来源选择。

### PAG-C-03 对象家族

```text
Projection Type Contract
Candidate Projection Snapshot
Candidate Projection Change Audit Record
Registered Projection Change Audit Record
Projection Publication Envelope
Projection Rebuild Requirement
Projection Deletion Record
Projection Correction Awareness Record
```

## 二、类型和稳定键

### PAG-C-04 投影类型合同必须冻结登记

合同固定类型、结果代数、输入类型、闭包要求、视图、稳定键、构建、审计、发布、删除、重建和更正语义；候选、冻结、尝试和登记摘要相等，并进入完整竞争边界。

### PAG-C-05 首批投影类型

```text
COMMIT_RESOLUTION_PROJECTION
PROOF_QUALIFICATION_PROJECTION
EXEMPTION_APPLICABILITY_PROJECTION
TARGET_STATE_PROJECTION
COMPOSITE_REQUIREMENT_PROJECTION
```

自由字符串或未登记类型不得发布。

### PAG-C-06 视图模式封闭

```text
HISTORICAL
CURRENT_RESTATED
```

历史视图固定原坐标和原闭包；当前重述使用新坐标、新闭包和新审计，不能覆盖历史发布。

### PAG-C-07 投影稳定键

```text
Projection Stable Key =
  Registered Projection Type Contract ID and Version
+ Projection Consumer Scope
+ Root Resolution ID and Digest
+ Exact Contract Scope or Compatibility Domain Snapshot
+ Validity As Of
+ K / Q / S / RR
+ Projection View Mode
+ Projection Rule ID, Version and Payload Digest
```

结果、载荷摘要、构建者、发布时间和缓存位置不得换键。

## 三、输入闭包与候选投影

### PAG-C-08 只消费登记完整闭包

候选必须固定 `CR-0011` 的闭包引用、底层节点／边／排除／冲突集合和三值完整性信封。只有登记 `COMPLETE` 支持确定终局投影。

### PAG-C-09 非完整闭包失败关闭

`INCOMPLETE`、`INDETERMINATE`、内部冲突、开放世界缺失或只有摘要时，候选投影只能为 `INDETERMINATE` 并保存原因与冲突引用。

### PAG-C-10 候选投影最低载荷

固定稳定键、结果、纳入／排除解析、制度排除、谱系、冲突集、闭包、来源快照、更正、兼容性、证据、构建授权、规则、生成时间和候选摘要。

### PAG-C-11 投影真值表由类型合同定义

提交投影保持 `COMMITTED | ABORTED | INDETERMINATE | CONFLICTED`；资格、豁免和目标状态使用各自冻结代数。投影器不能自行增加或选择终局。

### PAG-C-12 构建者只有计算权

构建者不能创建解析、闭包、排除规则、兼容关系、决策、提交、失效、审计登记、发布或策略授权。

## 四、变化审计

### PAG-C-13 审计稳定键

```text
Projection Change Audit Semantic Key =
  Projection Stable Key
+ Previous Published Envelope ID and Digest or NOT_APPLICABLE
+ Candidate Projection Digest
+ Previous and New Temporal Coordinate Digests
+ Audit Rule Version
```

### PAG-C-14 候选审计最低载荷

固定投影类型／作用域／视图、前后摘要与坐标、规则、增加／删除来源、适用性变化、闭包、原因码、生成时间、投影执行授权、证据和候选摘要。

### PAG-C-15 首次投影显式使用无前驱

首次投影前一外壳和摘要使用 `NOT_APPLICABLE`；不得伪造空历史或把缓存缺失解释为首次发布。

### PAG-C-16 审计必须内容同一登记

```text
Candidate Audit Payload Digest
= Attempted Audit Payload Digest
= Registered Audit Business Payload Digest
```

登记消费 WS-07 精确类型合同、逐类型授权、不可变尝试、完整竞争边界和幂等解析。

### PAG-C-17 审计登记不证明投影为事实

候选或登记审计只记录认识读面变化，不成为投影真值、决策事实、提交结果或发布授权。

## 五、内容同一发布

### PAG-C-18 发布外壳稳定键

```text
Projection Publication Semantic Key =
  Projection Stable Key
+ Candidate Projection Digest
+ Registered Change Audit Record ID and Digest
+ Publication Contract Version
```

### PAG-C-19 发布前四方内容同一

```text
Candidate Projection View Mode
= Registered Audit View Mode
= Publication Envelope View Mode

Candidate Projection Digest
= Registered Audit New Projection Digest
= Published Payload Digest
```

### PAG-C-20 发布者不得修改载荷

发布者只能验证闭包、审计、授权和内容同一并追加外壳；不得重新计算、规范化、压缩语义、删冲突或改变视图。

### PAG-C-21 发布外壳最低载荷

固定投影稳定键、候选摘要、完整闭包引用、登记审计、发布授权、发布契约、视图、已发布摘要、位置、时间、前驱外壳和证据。

### PAG-C-22 发布必须形成完整竞争解析

同一发布语义键的候选、尝试、成功、失败、空洞和谱系进入完整边界并独立证明完整。同键异载荷或异审计必须 `CONFLICTED`。

## 六、更正、失效、删除和重建

### PAG-C-23 更正和适用性变化只触发重建

登记更正、适用性变化、闭包变化、规则或兼容变化产生新 `Projection Rebuild Requirement`，不修改历史候选、审计或发布外壳。

### PAG-C-24 合法恢复路径封闭

```text
PATH_A_NEW_SUPPORT
PATH_B_AUTHORIZED_EXCLUSION_OR_INVALIDATION
PATH_C_COMPATIBILITY_OR_LEGALITY_RESOLUTION
```

每条路径固定新的登记输入、完整闭包、权威、证据和重建；投影器不能自行裁决冲突。

### PAG-C-25 重建要求内容同一登记

固定原外壳、触发事实、路径、影响范围、原／新坐标、必要闭包和证据；候选、尝试和登记摘要相等，并进入完整竞争边界。

### PAG-C-26 删除只作用于可重建读面

可删除候选缓存和当前发布缓存，但不得删除登记审计、发布历史外壳、底层事实、解析、闭包、证据、更正或尝试。

### PAG-C-27 删除必须登记

删除记录固定精确缓存对象、原因、授权、重建前置、时间和证据。缓存不存在不证明历史发布不存在。

### PAG-C-28 降级合法且不改写历史

新认识可使终局投影降级为 `INDETERMINATE` 或 `CONFLICTED`，但必须新建候选、审计和发布外壳。

## 七、WS-07 类型导入

### PAG-C-29 精确候选／登记映射

```text
Candidate Projection Change Audit Record
  -> Registered Projection Change Audit Record
Candidate Projection Rebuild Requirement
  -> Registered Projection Rebuild Requirement
Candidate Projection Deletion Record
  -> Registered Projection Deletion Record
```

分别提供精确 schema、稳定键、账本、更正合同和导入元组；发布外壳使用独立发布注册表，不冒充派生业务事实。

### PAG-C-30 WS-08 闭包类型槽位精确激活

投影类型合同只消费 CR-0011 已闭合并经 WS-07 精确导入的闭包／完整性类型；保留槽位或待导入类型不可发布。

## 八、权威目录

### PAG-C-31 类型、构建和审计分权

```text
ProjectionTypeContractCandidateConstructionAuthorityType
ProjectionTypeContractRegistrationAuthorityType
ProjectionBuildExecutionAuthorityType
ProjectionChangeAuditCandidateConstructionAuthorityType
ProjectionChangeAuditRegistrationAuthorityType
ProjectionAuditBoundaryConstructionAuthorityType
ProjectionAuditBoundaryRegistrationAuthorityType
ProjectionAuditBoundaryCompletenessQualificationAuthorityType
ProjectionAuditBoundaryCompletenessRegistrationAuthorityType
```

### PAG-C-32 发布、重建和删除分权

```text
ProjectionPublicationAuthorityType
ProjectionPublicationEnvelopeRegistrationAuthorityType
ProjectionPublicationBoundaryConstructionAuthorityType
ProjectionPublicationBoundaryRegistrationAuthorityType
ProjectionPublicationBoundaryCompletenessQualificationAuthorityType
ProjectionPublicationBoundaryCompletenessRegistrationAuthorityType
ProjectionRebuildRequirementConstructionAuthorityType
ProjectionRebuildRequirementRegistrationAuthorityType
ProjectionDeletionExecutionAuthorityType
ProjectionDeletionRecordRegistrationAuthorityType
```

### PAG-C-33 授权不传播

类型、构建、审计、发布、重建、删除和边界完整性权威互不传播，也不取得事实、解析、闭包、失效决定、行动或制度冻结权威。

## 九、非法状态与退出门槛

### PAG-C-34 以下状态失败关闭

- 非 `COMPLETE` 闭包支持终局投影；
- 候选投影直接发布；
- 审计登记者修改候选审计或投影；
- 发布者修改已审计载荷、视图或冲突；
- 前后摘要、坐标或视图不一致；
- 缓存缺失被解释为首次发布或事实不存在；
- 更正、失效或重建覆盖历史外壳；
- 删除登记审计、事实、闭包或证据；
- 投影结果授权重试、取消、选择来源或失效；
- 构建、审计或发布权威隐式传播。

### PAG-C-35 模型退出门槛

```text
Projection / Fact Separation: REQUIRED_PASS
Audit / Publication Authority Separation: REQUIRED_PASS
Content-identical Publication: REQUIRED_PASS
Closure Completeness Consumption: REQUIRED_PASS
Correction-aware Rebuild: REQUIRED_PASS
WS-03 / WS-07 / WS-08 Compatibility: REQUIRED_PASS
CR-0002 / CR-0003 Compatibility: REQUIRED_PASS
Independent Model Review: REQUIRED_PASS
Residual Internal and Interface Blockers: REQUIRED_0
```

## 当前决定

```text
CR-0012 Status: DRAFT
Authority: NONE
Executable: NO
WS-09 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Implementation Evidence: NOT_CREATED
Protected-write Evidence: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段执行接口兼容审查和独立模型审查。
