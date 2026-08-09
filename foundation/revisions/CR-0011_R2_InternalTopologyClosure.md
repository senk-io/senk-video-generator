# 依赖闭包治理有界修订 R2：内部拓扑闭合

## 修订信息

```text
Proposal ID: CR-0011-R2
Workstream: WS-08
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0011-R1 EXACT PROPAGATION FACT INTERFACE CLOSURE
Repair Basis: CR-0011-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: DCG-IM-B1 through DCG-IM-B4 only
```

### DCG-R2-01 根解析必须内容同一登记

根候选固定 C08 全部字段、类型合同、根记录登记解析、竞争边界、完整性、结果和摘要；候选、尝试、登记载荷相等。

### DCG-R2-02 根竞争边界必须完整

边界键固定根语义键、根解析注册表、证据边界、观察切口和规则；覆盖全部候选、成功、失败、空洞和谱系，并独立登记完整性。

### DCG-R2-03 根最终解析使用四值控制面

`REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`；只有登记完整边界上的唯一根解析单例可构建闭包。

### DCG-R2-04 逐边评价稳定键

```text
Required-edge Evaluation Semantic Key =
  Closure Root Resolution ID and Digest
+ Source Node ID, Version and Digest
+ Required-edge Rule ID, Version and Digest
+ Edge Type and Direction
+ Exact Temporal Coordinate Digest
+ Registry Scope Set Boundary ID and Digest
```

目标、结果和执行者不得换键。

### DCG-R2-05 逐边候选固定全部分支

固定条件、目标解析集合、纳入／排除／缺失／冲突／未解析结果、注册表边界、证据、原因码和摘要。

### DCG-R2-06 逐边评价内容同一登记

候选、尝试、记录摘要相等，并进入同键完整竞争边界和独立完整性。闭包只能消费登记评价解析单例或登记冲突聚合。

### DCG-R2-07 闭包候选固定精确逐边解析集

C20 的边集合必须同时固定逐边评价解析 ID／摘要全集、规范排序和与必需边预期集合的集合相等证明。

### DCG-R2-08 完整性原子语义键

```text
Closure Completeness Semantic Key =
  Registered Closure Resolution ID and Digest
+ Root Resolution ID and Digest
+ Required-edge Rule ID, Version and Digest
+ Registry Scope Set Boundary and Completeness Digests
+ Exact Temporal Coordinate Digest
+ Completeness Rule Version
```

结果不得换键。

### DCG-R2-09 完整性候选与登记内容同一

候选保存 C32 全部证明；尝试和登记载荷摘要相等。同键候选进入完整评价边界和独立边界完整性。

### DCG-R2-10 完整性冲突聚合使用四值内部层

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

完整集合中 `COMPLETE + INCOMPLETE` 或同键异证明为 `CONFLICTED`；聚合固定精确原子登记解析集和集合相等证明。

### DCG-R2-11 三值消费信封必须登记

```text
Internal COMPLETE -> Consumer COMPLETE
Internal INCOMPLETE -> Consumer INCOMPLETE
Internal INDETERMINATE -> Consumer INDETERMINATE
Internal CONFLICTED -> Consumer INDETERMINATE + exact Conflict References
```

候选信封、尝试和登记载荷内容同一，冲突引用不可删除。

### DCG-R2-12 重建要求稳定键

```text
Closure Rebuild Requirement Key =
  Prior Closure Semantic Key
+ Registered Trigger Fact Import Resolution ID and Digest
+ Trigger Effective Coordinate
+ Rebuild Rule Version
```

影响范围和结果不得换键。

### DCG-R2-13 重建要求内容同一登记

固定触发、影响节点／边／作用域、原／新坐标、重建模式和证据；候选、尝试、记录及竞争边界完整登记。

### DCG-R2-14 增量复用证明稳定键

固定原闭包、重建要求、受影响子图、复用子图、集合差分、成员内容同一、边界和规则。复用结果不得进入键。

### DCG-R2-15 增量复用证明完整登记

候选、尝试、记录、竞争边界、独立完整性和四值解析内容同一。非登记单例必须完整重建。

### DCG-R2-16 传播事实导入稳定键

固定提供方事实类型、正式事实键、提交键／尝试／解析和作用域；导入候选、尝试、记录及完整竞争边界内容同一。

### DCG-R2-17 传播输入边界稳定键

固定消费域、冻结传播规则、作用域、有效坐标、允许事实类型合同、证据边界和边界规则版本。

### DCG-R2-18 传播输入边界固定事实全集

覆盖全部登记事实导入、排除、冲突、失败和空洞集合，并保存集合相等证明、独立完整性和四值边界解析。

### DCG-R2-19 新边界不创建传播执行

重建、复用和传播输入登记都不能创建失效事实、传播执行、对象修改或投影发布。

### DCG-R2-20 根与规则新增授权

```text
ClosureRootCandidateConstructionAuthorityType
ClosureRootRegistrationAuthorityType
ClosureRootBoundaryConstructionAuthorityType
ClosureRootBoundaryRegistrationAuthorityType
ClosureRootBoundaryCompletenessQualificationAuthorityType
ClosureRootBoundaryCompletenessRegistrationAuthorityType
ClosureRootResolutionExecutionAuthorityType
ClosureRootResolutionRegistrationAuthorityType
RequiredEdgeRuleBoundaryCompletenessQualificationAuthorityType
RequiredEdgeRuleBoundaryCompletenessRegistrationAuthorityType
RequiredEdgeRuleResolutionExecutionAuthorityType
RequiredEdgeRuleResolutionRegistrationAuthorityType
```

### DCG-R2-21 逐边与完整性新增授权

```text
RequiredEdgeEvaluationCandidateConstructionAuthorityType
RequiredEdgeEvaluationRegistrationAuthorityType
RequiredEdgeEvaluationBoundaryConstructionAuthorityType
RequiredEdgeEvaluationBoundaryRegistrationAuthorityType
RequiredEdgeEvaluationBoundaryCompletenessQualificationAuthorityType
RequiredEdgeEvaluationBoundaryCompletenessRegistrationAuthorityType
RequiredEdgeEvaluationAggregateExecutionAuthorityType
RequiredEdgeEvaluationAggregateRegistrationAuthorityType
ClosureCompletenessAtomicRegistrationAuthorityType
ClosureCompletenessEvaluationBoundaryConstructionAuthorityType
ClosureCompletenessEvaluationBoundaryRegistrationAuthorityType
ClosureCompletenessBoundaryCompletenessQualificationAuthorityType
ClosureCompletenessBoundaryCompletenessRegistrationAuthorityType
ClosureCompletenessAggregateExecutionAuthorityType
ClosureCompletenessAggregateRegistrationAuthorityType
ClosureCompletenessConsumerEnvelopeConstructionAuthorityType
ClosureCompletenessConsumerEnvelopeRegistrationAuthorityType
```

### DCG-R2-22 重建与传播新增授权

```text
ClosureRebuildBoundaryConstructionAuthorityType
ClosureRebuildBoundaryRegistrationAuthorityType
ClosureRebuildBoundaryCompletenessQualificationAuthorityType
ClosureRebuildBoundaryCompletenessRegistrationAuthorityType
ClosureRebuildResolutionExecutionAuthorityType
ClosureRebuildResolutionRegistrationAuthorityType
IncrementalReuseProofBoundaryConstructionAuthorityType
IncrementalReuseProofBoundaryRegistrationAuthorityType
IncrementalReuseProofBoundaryCompletenessQualificationAuthorityType
IncrementalReuseProofBoundaryCompletenessRegistrationAuthorityType
IncrementalReuseProofResolutionExecutionAuthorityType
IncrementalReuseProofResolutionRegistrationAuthorityType
PropagationFactImportConstructionAuthorityType
PropagationFactImportRegistrationAuthorityType
PropagationFactImportBoundaryConstructionAuthorityType
PropagationFactImportBoundaryRegistrationAuthorityType
PropagationFactImportBoundaryCompletenessQualificationAuthorityType
PropagationFactImportBoundaryCompletenessRegistrationAuthorityType
PropagationInputBoundaryConstructionAuthorityType
PropagationInputBoundaryRegistrationAuthorityType
PropagationInputBoundaryCompletenessQualificationAuthorityType
PropagationInputBoundaryCompletenessRegistrationAuthorityType
```

### DCG-R2-23 授权完整限界且不传播

每项固定允许稳定键、注册表、规则、输入输出、证据、有效窗口、`Can Change` 和 `Cannot Change`；全部互不传播。

### DCG-R2-24 非法状态失败关闭

- 未登记根或逐边评价进入闭包；
- 按结果过滤逐边候选；
- 完整性冲突在三值信封中丢失引用；
- 同触发产生不兼容重建范围却选赢家；
- 未登记复用证明支持增量重建；
- 传播输入边界遗漏已提交事实；
- 新授权取得传播执行或发布权威。

### DCG-R2-25 候选级关闭声明

```text
DCG-IM-B1 Root and Edge Registration: CLOSED_AS_DRAFT
DCG-IM-B2 Completeness Conflict Adapter: CLOSED_AS_DRAFT
DCG-IM-B3 Rebuild and Propagation Registration: CLOSED_AS_DRAFT
DCG-IM-B4 Cumulative Authority Catalog: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0011-R2 Status: DRAFT
WS-08 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```
