# 证明与豁免适用性治理有界修订 R2：精确登记与零阶闭合

## 修订信息

```text
Proposal ID: CR-0009-R2
Title: Exact Registration and Rank-zero Closure
Workstream: WS-06
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0009-R1 INTERNAL TOPOLOGY AND WELL-FOUNDED COMPLETENESS CLOSURE
Repair Basis: CR-0009-R1-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Repair Scope: residual PEAG-IM-B2 + residual PEAG-IM-B3 + residual PEAG-IM-B4 + PEAG-R1-B1 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Interface Regression Review Required: YES
Independent Composite Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本修订不改变证明、资格、适用性、`ABORTED` 或 `EXEMPT` 的外部结果合同，只补齐零阶准入、适用性规则、适用性聚合和授权目录。

## 一、零阶证据类型与提供方合同

### PEAG-R2-01 零阶证据类型注册表必须封闭

`Rank-zero Evidence Type Record` 至少固定：

```text
Rank-zero Evidence Type Registry ID and Version
Evidence Type ID and Version
Allowed Provider Contract Types
Atomic Payload Contract
Allowed Provider Boundary Types
No-higher-rank Dependency Contract
Canonical Byte Contract and Digest Algorithm
Institution Freeze Reference
```

自由字符串、“原子”标签或实现配置不能建立零阶资格。

### PEAG-R2-02 零阶提供方合同必须独立登记

`Rank-zero Provider Boundary Contract` 至少固定：

```text
Provider Contract ID and Version
Provider Authority and Registry Scope
Exact Evidence Type Binding
Provider Boundary Stable Key Contract
Atomic Record Membership Contract
Boundary Completeness Interface Contract
Correction and Historical Replay Contract
No Recursive Completeness Applicability Input Contract
Canonical Payload Digest
Institution Freeze Reference
```

### PEAG-R2-03 零阶类型和提供方合同分别使用稳定键

```text
Rank-zero Evidence Type Semantic Key =
  Rank-zero Evidence Type Registry ID and Version
+ Evidence Type ID and Version

Rank-zero Provider Contract Semantic Key =
  Rank-zero Provider Contract Registry ID and Version
+ Provider Contract ID and Version
+ Evidence Type ID and Version
```

载荷、结果、登记者和登记时间不得换键。

### PEAG-R2-04 零阶类型与合同必须先冻结后登记

候选、精确制度冻结、登记尝试和已登记记录的规范摘要必须相等。每类记录拥有独立注册表、完整竞争边界、独立边界完整性和四值登记解析。

### PEAG-R2-05 零阶资格拥有稳定语义键

```text
Rank-zero Eligibility Semantic Conflict Set Key =
  Registered Rank-zero Evidence Type Resolution ID and Digest
+ Registered Provider Contract Resolution ID and Digest
+ Atomic Evidence Record ID, Version and Payload Digest
+ Provider Boundary ID and Digest
+ Provider Boundary Completeness Resolution ID and Digest
+ No-higher-rank Dependency Proof Digest
+ Rank-zero Eligibility Rule Version
```

资格结果、执行者和时间不得换键。

### PEAG-R2-06 零阶候选必须证明无高阶依赖

候选至少保存：

```text
Exact Atomic Evidence Payload and Digest
Registered Type and Provider Contract References
Provider Boundary Membership Proof
Provider Boundary Completeness Resolution
Exact Dependency Edge Set = EMPTY_SET
Dependency Edge Set Equality Proof
No Completeness-proof Applicability Input Proof
Eligibility Result and Reason Codes
Candidate Payload Digest
Eligibility Authority Reference
```

### PEAG-R2-07 零阶结果使用四值

```text
ELIGIBLE | NOT_ELIGIBLE | INDETERMINATE | CONFLICTED
```

登记类型／合同单例、原子载荷匹配、完整提供方边界及登记空依赖集合支持 `ELIGIBLE`；确定违反原子或空依赖合同支持 `NOT_ELIGIBLE`；未知为 `INDETERMINATE`；同键异载荷、异依赖集合或异结果为 `CONFLICTED`。

### PEAG-R2-08 零阶资格必须内容同一登记

候选、尝试和已登记资格摘要相等，并进入同键完整竞争边界。边界覆盖全部候选、成功、失败、永久空洞和解析谱系，由独立权威登记完整性。

### PEAG-R2-09 零阶叶消费门

完整性依赖图只有在零阶资格最终登记解析为 `REGISTERED` 且语义结果为 `ELIGIBLE` 时，才可把对象作为零阶叶。其他登记或语义结果全部失败关闭。

### PEAG-R2-10 零阶边界完整性不是完整性证明适用性

零阶类型、合同和资格注册表的边界完整性只证明注册表竞争集合读取完整，不判断业务证明内容完整，且不得依赖 `Completeness Proof Applicability`。因此不形成自举循环。

## 二、适用性规则精确登记

### PEAG-R2-11 证明和豁免规则稳定键必须分域

```text
Proof Applicability Rule Semantic Conflict Set Key =
  Proof Applicability Rule Registry ID and Version
+ Proof Type ID and Version
+ Rule ID and Version
+ Applicability Semantic Domain

Exemption Applicability Rule Semantic Conflict Set Key =
  Exemption Applicability Rule Registry ID and Version
+ Exemption Type ID and Version
+ Rule ID and Version
+ Applicability Semantic Domain
```

两域不能共享语义键或注册表边界。

### PEAG-R2-12 规则候选必须固定精确载荷

分别固定允许类型、资格输入、坐标、来源适用性要求、完整性阶合同、相反来源合同、四值真值表、失效、更正、前向解释、规范字节合同、候选摘要、制定授权和证据。

### PEAG-R2-13 规则必须内容同一冻结登记

```text
Candidate Rule Payload Digest
= Frozen Rule Content Digest
= Attempted Rule Payload Digest
= Registered Rule Payload Digest
```

登记不能创建或替代制度冻结。

### PEAG-R2-14 规则竞争边界按域完整

```text
Rule Competition Boundary Key =
  Type-specific Rule Semantic Conflict Set Key
+ Type-specific Rule Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Rule Boundary Version
```

载荷覆盖全部候选、成功、失败、永久空洞、冻结引用解析和既有解析谱系，并保存逐集合相等证明。

### PEAG-R2-15 规则边界和完整性分别登记

候选边界、尝试、已登记边界和四值边界解析保持内容同一；独立边界完整性为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。

### PEAG-R2-16 规则最终解析使用封闭真值表

登记完整边界内唯一冻结内容单例为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；同键异载荷、异冻结内容或矛盾解析为 `CONFLICTED`；其他为 `INDETERMINATE`。

### PEAG-R2-17 适用性计算只消费规则登记单例

计算键和候选必须固定规则最终解析、已登记完整竞争边界、边界完整性和精确竞争集合摘要。任何非 `REGISTERED` 分支不得计算确定适用性。

## 三、证明适用性聚合精确登记

### PEAG-R2-18 证明聚合使用稳定语义键

```text
Proof Applicability Aggregate Semantic Key =
  Proof Applicability Semantic Conflict Set Key
+ Registered Proof Applicability Evaluation Boundary ID and Digest
+ Evaluation Boundary Registration Resolution ID and Digest
+ Evaluation Boundary Completeness Resolution ID and Digest
+ Exact Atomic Applicability Registration Resolution Set Digest
+ Proof Applicability Aggregate Rule Version
```

结果、聚合者和登记时间不得换键。

### PEAG-R2-19 证明聚合候选固定完整原子集合

候选固定聚合键、全部原子登记解析、原子载荷摘要集合、集合相等证明、相反终局引用、逐成员比较、四值结果、原因码、执行授权、证据和候选摘要。

### PEAG-R2-20 证明聚合候选与登记内容同一

候选、登记尝试和已登记聚合记录摘要必须相等。聚合登记解析使用 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### PEAG-R2-21 证明聚合竞争边界必须完整

边界键固定聚合语义键、聚合注册表、证据边界、观察切口和边界规则；载荷覆盖聚合候选、成功、失败、空洞、解析谱系和集合相等证明。

### PEAG-R2-22 证明聚合边界完整性独立登记

边界构造者、原子计算者、聚合者、登记者和投影构造者不能自证聚合竞争边界完整。只有登记边界且完整性为 `COMPLETE` 可支持确定聚合登记解析。

### PEAG-R2-23 证明聚合真值表封闭

完整集合只有 `APPLICABLE` 支持 `APPLICABLE`；只有 `INAPPLICABLE` 支持 `INAPPLICABLE`；两者并存或同键异载荷为 `CONFLICTED`；存在未知或不完整输入为 `INDETERMINATE`。

## 四、豁免适用性聚合精确登记

### PEAG-R2-24 豁免聚合使用稳定语义键

```text
Exemption Applicability Aggregate Semantic Key =
  Exemption Applicability Semantic Conflict Set Key
+ Registered Exemption Applicability Evaluation Boundary ID and Digest
+ Evaluation Boundary Registration Resolution ID and Digest
+ Evaluation Boundary Completeness Resolution ID and Digest
+ Exact Atomic Applicability Registration Resolution Set Digest
+ Exemption Applicability Aggregate Rule Version
```

### PEAG-R2-25 豁免聚合拥有独立完整登记链

豁免聚合分别拥有候选载荷、登记尝试、已登记记录、竞争边界、边界登记解析、独立完整性和聚合登记解析；字段合同与证明聚合同构但注册表、类型和稳定键隔离。

### PEAG-R2-26 豁免聚合真值表封闭

使用与证明聚合相同的四值比较规则。`Requirement Mode = REQUIRED` 的确定原子结果只能参与 `INAPPLICABLE` 一侧，不能被其他候选提升为 `APPLICABLE`。

### PEAG-R2-27 投影信封只消费登记聚合单例

证明或豁免投影输入必须固定各自聚合登记解析、聚合竞争边界、独立完整性、精确原子集合、资格冲突、适用性冲突和底层证据。非登记单例不得支持确定投影。

## 五、显式授权类型目录

### PEAG-R2-28 零阶类型和合同授权

```text
RankZeroEvidenceTypeCandidateConstructionAuthorityType
RankZeroEvidenceTypeRegistrationAuthorityType
RankZeroEvidenceTypeBoundaryConstructionAuthorityType
RankZeroEvidenceTypeBoundaryRegistrationAuthorityType
RankZeroEvidenceTypeBoundaryCompletenessQualificationAuthorityType
RankZeroEvidenceTypeBoundaryCompletenessRegistrationAuthorityType
RankZeroEvidenceTypeResolutionExecutionAuthorityType
RankZeroEvidenceTypeResolutionRegistrationAuthorityType
RankZeroProviderContractCandidateConstructionAuthorityType
RankZeroProviderContractRegistrationAuthorityType
RankZeroProviderContractBoundaryConstructionAuthorityType
RankZeroProviderContractBoundaryRegistrationAuthorityType
RankZeroProviderContractBoundaryCompletenessQualificationAuthorityType
RankZeroProviderContractBoundaryCompletenessRegistrationAuthorityType
RankZeroProviderContractResolutionExecutionAuthorityType
RankZeroProviderContractResolutionRegistrationAuthorityType
```

### PEAG-R2-29 零阶资格和依赖图授权

```text
RankZeroEligibilityExecutionAuthorityType
RankZeroEligibilityRegistrationAuthorityType
RankZeroEligibilityBoundaryConstructionAuthorityType
RankZeroEligibilityBoundaryRegistrationAuthorityType
RankZeroEligibilityBoundaryCompletenessQualificationAuthorityType
RankZeroEligibilityBoundaryCompletenessRegistrationAuthorityType
CompletenessDependencyGraphConstructionAuthorityType
CompletenessDependencyGraphRegistrationAuthorityType
CompletenessDependencyGraphBoundaryConstructionAuthorityType
CompletenessDependencyGraphBoundaryRegistrationAuthorityType
CompletenessDependencyGraphBoundaryCompletenessQualificationAuthorityType
CompletenessDependencyGraphBoundaryCompletenessRegistrationAuthorityType
AcyclicityQualificationExecutionAuthorityType
AcyclicityQualificationRegistrationAuthorityType
```

### PEAG-R2-30 证明规则与适用性授权

```text
ProofApplicabilityRuleCandidateConstructionAuthorityType
ProofApplicabilityRuleRegistrationAuthorityType
ProofApplicabilityRuleBoundaryConstructionAuthorityType
ProofApplicabilityRuleBoundaryRegistrationAuthorityType
ProofApplicabilityRuleBoundaryCompletenessQualificationAuthorityType
ProofApplicabilityRuleBoundaryCompletenessRegistrationAuthorityType
ProofApplicabilityRuleResolutionExecutionAuthorityType
ProofApplicabilityRuleResolutionRegistrationAuthorityType
ProofApplicabilityComputationAuthorityType
ProofApplicabilityAtomicRegistrationAuthorityType
ProofApplicabilityEvaluationBoundaryConstructionAuthorityType
ProofApplicabilityEvaluationBoundaryRegistrationAuthorityType
ProofApplicabilityBoundaryCompletenessQualificationAuthorityType
ProofApplicabilityBoundaryCompletenessRegistrationAuthorityType
ProofApplicabilityAggregateExecutionAuthorityType
ProofApplicabilityAggregateRegistrationAuthorityType
ProofApplicabilityAggregateBoundaryConstructionAuthorityType
ProofApplicabilityAggregateBoundaryRegistrationAuthorityType
ProofApplicabilityAggregateBoundaryCompletenessQualificationAuthorityType
ProofApplicabilityAggregateBoundaryCompletenessRegistrationAuthorityType
ProofApplicabilityAggregateResolutionExecutionAuthorityType
ProofApplicabilityAggregateResolutionRegistrationAuthorityType
ProofProjectionInputEnvelopeConstructionAuthorityType
ProofProjectionInputEnvelopeRegistrationAuthorityType
```

### PEAG-R2-31 豁免规则与适用性授权

```text
ExemptionApplicabilityRuleCandidateConstructionAuthorityType
ExemptionApplicabilityRuleRegistrationAuthorityType
ExemptionApplicabilityRuleBoundaryConstructionAuthorityType
ExemptionApplicabilityRuleBoundaryRegistrationAuthorityType
ExemptionApplicabilityRuleBoundaryCompletenessQualificationAuthorityType
ExemptionApplicabilityRuleBoundaryCompletenessRegistrationAuthorityType
ExemptionApplicabilityRuleResolutionExecutionAuthorityType
ExemptionApplicabilityRuleResolutionRegistrationAuthorityType
ExemptionApplicabilityComputationAuthorityType
ExemptionApplicabilityAtomicRegistrationAuthorityType
ExemptionApplicabilityEvaluationBoundaryConstructionAuthorityType
ExemptionApplicabilityEvaluationBoundaryRegistrationAuthorityType
ExemptionApplicabilityBoundaryCompletenessQualificationAuthorityType
ExemptionApplicabilityBoundaryCompletenessRegistrationAuthorityType
ExemptionApplicabilityAggregateExecutionAuthorityType
ExemptionApplicabilityAggregateRegistrationAuthorityType
ExemptionApplicabilityAggregateBoundaryConstructionAuthorityType
ExemptionApplicabilityAggregateBoundaryRegistrationAuthorityType
ExemptionApplicabilityAggregateBoundaryCompletenessQualificationAuthorityType
ExemptionApplicabilityAggregateBoundaryCompletenessRegistrationAuthorityType
ExemptionApplicabilityAggregateResolutionExecutionAuthorityType
ExemptionApplicabilityAggregateResolutionRegistrationAuthorityType
ExemptionProjectionInputEnvelopeConstructionAuthorityType
ExemptionProjectionInputEnvelopeRegistrationAuthorityType
```

### PEAG-R2-32 既有类型和完整性授权也必须使用稳定名称

R1 中斜线简称由本修订和以下逐项类型覆盖：

```text
ProofTypeCandidateConstructionAuthorityType
ProofTypeRegistrationAuthorityType
ProofTypeBoundaryConstructionAuthorityType
ProofTypeBoundaryRegistrationAuthorityType
ProofTypeBoundaryCompletenessQualificationAuthorityType
ProofTypeBoundaryCompletenessRegistrationAuthorityType
ProofTypeResolutionExecutionAuthorityType
ProofTypeResolutionRegistrationAuthorityType
ExemptionTypeCandidateConstructionAuthorityType
ExemptionTypeRegistrationAuthorityType
ExemptionTypeBoundaryConstructionAuthorityType
ExemptionTypeBoundaryRegistrationAuthorityType
ExemptionTypeBoundaryCompletenessQualificationAuthorityType
ExemptionTypeBoundaryCompletenessRegistrationAuthorityType
ExemptionTypeResolutionExecutionAuthorityType
ExemptionTypeResolutionRegistrationAuthorityType
CompletenessProofQualificationExecutionAuthorityType
CompletenessProofQualificationRegistrationAuthorityType
CompletenessProofApplicabilityExecutionAuthorityType
CompletenessProofApplicabilityRegistrationAuthorityType
CompletenessEvaluationExecutionAuthorityType
CompletenessEvaluationRegistrationAuthorityType
ProofQualificationProjectionConstructionAuthorityType
ExemptionApplicabilityProjectionConstructionAuthorityType
```

投影发布权威仍属于 `WS-09`，不由本模型创建。

### PEAG-R2-33 所有授权使用完整作用域且互不传播

每个授权实例固定允许域、类型、规则、稳定键、注册表、边界、输入输出、阶数、证据、有效窗口、`Can Change`、`Cannot Change` 和授予事实。构造、登记、边界、完整性、解析、聚合、信封与投影权威互不传播。

## 六、并发、历史和非法状态

### PEAG-R2-34 并发同键事实必须共同竞争

相同零阶、规则或聚合语义键下的并发候选、成功、失败和空洞进入同一边界；先到、最后写入、最大版本或调用者选择不能决定结果。

### PEAG-R2-35 更正和演进必须追加

非语义更正追加记录；类型、合同、规则、原子集合、证据边界或投影输入变化产生新身份。历史零阶资格、规则、聚合、失败、空洞和冲突永久保留。

### PEAG-R2-36 以下状态必须失败关闭

- 调用方自行声明零阶或不可再分；
- 零阶资格依赖完整性证明适用性；
- 未登记类型／合同支持零阶叶；
- 证明与豁免规则共用竞争边界；
- 聚合选择原子评价边界的有利子集；
- 聚合候选直接成为投影输入；
- 不完整聚合边界支持确定结果；
- 人类可读简称替代稳定授权类型；
- 证明授权在豁免域使用或反向使用；
- 新规则或聚合覆盖历史。

## 七、回归与候选声明

### PEAG-R2-37 已通过边界不得回归

```text
Type Registry Topology: PRESERVED
Natural-number Rank and Strict Descent: PRESERVED
WS-04 / WS-05 Compatibility: PRESERVED
CR-0002 / CR-0003 Compatibility: PRESERVED
ABORTED / EXEMPT Positive Chains: PRESERVED
```

### PEAG-R2-38 四项残余阻断只在候选层关闭

```text
PEAG-IM-B2 Rank-zero Eligibility: CLOSED_AS_DRAFT
PEAG-IM-B3 Applicability Aggregate Identity: CLOSED_AS_DRAFT
PEAG-IM-B4 Explicit Authority Type Catalog: CLOSED_AS_DRAFT
PEAG-R1-B1 Applicability Rule Registration: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0009-R2 Status: DRAFT
Authority: NONE
Executable: NO
WS-06 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 R2 接口回归和独立复合模型复审；R2 自检不能证明 WS-06 闭合。
