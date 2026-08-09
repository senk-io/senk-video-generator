# 证明与豁免适用性治理提案

## 提案信息

```text
Proposal ID: CR-0009
Title: Proof and Exemption Applicability Governance
Workstream: WS-06
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: NORMATIVE_MODEL_CANDIDATE
Depends On: CR-0007-R5 QUALIFICATION GOVERNANCE COMPOSITE
Depends On: CR-0008-R4 AUTHORITY APPLICABILITY GOVERNANCE COMPOSITE
Consumes: CR-0005-R11 SOURCE REGISTRY INTERFACE COMPOSITE
Consumes: CR-0006-R10 TEMPORAL MAPPING GOVERNANCE COMPOSITE
Consumer Interface: CR-0002-CONSTITUTION-CANDIDATE
Consumer Interface: CR-0003-CONSTITUTION-CANDIDATE-R2
Cross-interface Reviews Required: YES
Independent Composite Model Review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本提案闭合未应用证明和豁免依据的类型、资格、适用性、完整性、冲突、失效及演进。它不创建提交结果、组合豁免结果、决策事实、提交事实或目标迁移。

## 一、单一目的和边界

### PEAG-C-01 单一目的

```text
Registered Proof or Exemption Type
+ Candidate Proof or Exemption Basis
+ Registered Qualification from WS-04
+ Registered Source / Authority Applicability Inputs
+ Registered Completeness Qualification and Applicability
+ Frozen Applicability Rule
  -> Registered Proof or Exemption Applicability
  -> Rebuildable Projection
```

### PEAG-C-02 类型名称不能证明资格

```text
Proof Type Name -/-> QUALIFIED
Exemption Type Name -/-> QUALIFIED
Registered Type -/-> Applicable
```

### PEAG-C-03 资格和适用性必须分离

```text
Historical Registered Qualification = QUALIFIED
  -/-> Current Applicability = APPLICABLE
```

资格由 `WS-04` 计算和登记；本模型不得重新实现资格真值或改写历史资格。

### PEAG-C-04 本模型不创建终局结果

```text
Proof Applicability -/-> ABORTED
Exemption Applicability -/-> EXEMPT
Applicability -/-> COMMITTED
Applicability -/-> Decision Fact
Applicability -/-> Retry Authority
```

## 二、类型注册表

### PEAG-C-05 证明类型注册表初始封闭

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

新增类型必须产生新类型注册表版本并完成独立冻结，不能用任意字符串扩展。

### PEAG-C-06 豁免类型必须登记而非自由命名

每个豁免类型至少固定类型 ID 和版本、允许要求契约、槽位、对象／迁移类型、依据类型、资格规则绑定、适用性规则绑定、完整性合同、失效合同、冻结引用和规范摘要。

### PEAG-C-07 类型记录必须内容同一登记

```text
Candidate Type Record
  -> exact-payload Institution Freeze
  -> Type Registration Attempt
  -> Registered Type Record
  -> Complete Type Competition Boundary
  -> Four-value Type Registration Resolution
```

只有登记完整边界上的唯一冻结单例可被消费。

### PEAG-C-08 类型冲突必须保留

同一类型 ID 和版本下异语义、异规则绑定、异完整性或异冻结内容必须 `CONFLICTED`，不得按时间或版本号选赢家。

## 三、未应用证明候选

### PEAG-C-09 候选证明必须固定精确作用域

至少绑定：

```text
Candidate Proof ID and Payload Digest
Registered Proof Type and Resolution
Commit Key and Commit Attempt ID
Decision Key
Commit Contract ID and Version
Target Object ID and Version
Target Decision Registry ID and Expected Registry Version
Declared Write-set Digest
Claimed Closed Boundary or Version Range
Validity As Of and Knowledge Boundary Vector
Authoritative Source References
Source Registry Snapshot References and Source Set Digest
Coverage or Completeness Proof Candidate Reference
Contrary Source References
Evidence References
Assembler Identity and Authority
Assembly Rule Version
```

### PEAG-C-10 缺失不是未应用证明

未找到记录、缓存未命中、异步日志缺失、读取失败、超时和投影空值都不能建立未应用证明或确定性不适用。

### PEAG-C-11 组装者不拥有下游权威

证明组装权威不取得资格计算、资格登记、适用性、完整性、提交解析或 `ABORTED` 权威。

## 四、证明资格消费

### PEAG-C-12 历史原子证明资格严格三值

```text
QUALIFIED | DISQUALIFIED | INDETERMINATE
```

证明资格必须消费 `CR-0007` 的原子资格登记，不得把 `CR-0002` 旧四值文字解释为原子 `CONFLICTED`。

### PEAG-C-13 四值冲突只属于聚合或投影

```text
QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED
```

相反原子资格在登记完整评价边界上聚合为 `CONFLICTED`；历史原子记录保持不可变。

### PEAG-C-14 证明资格规则是 WS-04 专用配置

`Proof Qualification Rule` 必须作为 `WS-04` 已冻结且已登记规则或消费者配置绑定，不在本模型创建第二资格注册表。

### PEAG-C-15 资格作用域模式严格二选一

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

精确模式固定一个提交契约；兼容域模式固定不可变域快照及全部成员契约和逐成员资格规则绑定。

## 五、证明适用性

### PEAG-C-16 证明适用性坐标必须完整

```text
Registered Proof Qualification Record ID and Digest
Candidate Proof ID and Payload Digest
Commit Key and Commit Attempt ID
Decision Key
Qualification Scope Mode and Contract Scope
Validity As Of
Knowledge Boundary Vector
Temporal Query Coordinate Subject S and RR
Projection View Mode
Source Applicability Package Set Digest
Correction Representation Digest
Proof Applicability Rule ID, Version and Payload Digest
```

### PEAG-C-17 证明适用性结果为四值

```text
APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
```

### PEAG-C-18 `APPLICABLE` 需要完整正向链

历史资格为 `QUALIFIED`、类型登记单例、精确身份匹配、所有必要来源适用、完整性合格且适用、无相反来源、时间主体登记单例和规则登记单例，才可支持 `APPLICABLE`。

### PEAG-C-19 `INAPPLICABLE` 只允许确定性否定

完整来源下，资格确定失效、证明超出有效坐标、合同／写集合／尝试不匹配或必要来源确定不适用可支持 `INAPPLICABLE`。开放世界缺失不能支持该结果。

### PEAG-C-20 冲突不能被适用性执行者消解

资格聚合、来源、类型、规则、完整性或相反证据存在不可比较冲突时必须 `CONFLICTED` 或 `INDETERMINATE`，不得选择有利记录。

## 六、豁免资格与适用性

### PEAG-C-21 豁免资格继续由 WS-04 提供

`Exemption Qualification Rule` 是 `WS-04` 已冻结规则配置；原子资格三值、冲突聚合四值和内容同一登记边界与证明资格相同。

### PEAG-C-22 豁免适用性稳定坐标

至少固定：

```text
Registered Exemption Qualification Resolution ID and Digest
Exemption Basis ID and Version
Registered Exemption Type and Resolution
Requirement Contract ID and Version
Requirement Mode and Slot ID
Target Object ID and Version
Target Transition Type
Frozen Exemption Rule ID, Version and Payload Digest
Validity As Of and Knowledge Boundary Vector
S / RR / Q / K Coordinate
Projection View Mode
Source Applicability Package Set Digest
Correction View Digest
Exemption Applicability Rule ID, Version and Payload Digest
```

### PEAG-C-23 豁免适用性结果为四值

```text
APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
```

### PEAG-C-24 豁免适用要求条件模式

只有 `Requirement Mode = CONDITIONALLY_EXEMPTIBLE`、槽位／对象／版本／迁移内容同一且冻结豁免规则适用时，才可能得到 `APPLICABLE`。`REQUIRED` 模式确定支持 `INAPPLICABLE`。

### PEAG-C-25 豁免缺失不能证明适用

缺少决策记录、未观察到条件、来源缺失、资格未知或完整性未知只能产生 `INDETERMINATE`，不能建立 `APPLICABLE` 或 `EXEMPT`。

## 七、完整性资格和适用性

### PEAG-C-26 完整性证明必须独立

证明或豁免内容构造者、资格计算者、适用性计算者和终局消费者不得构造或登记自己的最终完整性证明。

### PEAG-C-27 完整性也必须资格与适用性分离

```text
Registered Completeness Proof Qualification
+ Registered Completeness Proof Applicability
  -> may support COMPLETE
```

类型名称、文件存在、摘要存在或执行成功不能替代该链。

### PEAG-C-28 完整性边界必须覆盖必要全集

固定必要来源类型和目的、预期与观察集合摘要、集合相等证明、失败尝试、永久空洞、相反来源、证据边界和独立边界完整性解析。

### PEAG-C-29 完整性结果为四值

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

只有合格且适用的完整性证明可支持 `COMPLETE`；相反完整性结论必须共同竞争。

## 八、规则登记

### PEAG-C-30 四类规则必须分别登记

```text
Proof Qualification Rule Binding
Proof Applicability Rule
Exemption Qualification Rule Binding
Exemption Applicability Rule
```

资格规则绑定只引用 `WS-04`；适用性规则由本模型候选、冻结和登记。

### PEAG-C-31 适用性规则必须内容同一冻结登记

候选、精确制度冻结、登记尝试和已登记规则摘要必须相等，并进入同键完整竞争边界和独立完整性解析。

### PEAG-C-32 规则演进不重解释历史

新规则版本、兼容关系或适用域变化产生新计算和投影身份。历史资格与适用性记录继续固定原规则。

## 九、候选、登记与冲突边界

### PEAG-C-33 适用性候选必须可重放

证明与豁免候选分别固定稳定坐标、所有资格／来源／完整性输入、逐谓词结果、四值结果、原因码、执行授权、证据和规范摘要。

### PEAG-C-34 候选与登记必须内容同一

```text
Candidate Applicability Payload Digest
= Attempted Registered Payload Digest
= Registered Applicability Payload Digest
```

登记者不能修改结果、作用域、来源、冲突或完整性。

### PEAG-C-35 同键竞争边界必须完整

证明适用性与豁免适用性分别拥有语义冲突键、候选／成功／失败／空洞／谱系全集、内容同一边界登记、独立完整性和四值登记解析。

### PEAG-C-36 运行消费只允许登记单例或登记聚合

原子登记单例可表达一个历史适用性结论；同键多记录必须在登记完整边界上聚合。未登记、不完整或冲突边界不能支持确定投影。

## 十、投影和正向终局链

### PEAG-C-37 证明资格投影键必须精确

固定候选证明、提交键、尝试、决策键、作用域模式、精确契约或兼容域快照、有效时点、认识向量、视图、资格规则域、来源边界、更正表示和投影规则。

### PEAG-C-38 证明投影分别保存两层冲突

投影必须分别保存资格结果／冲突和适用性结果／冲突，不能用单一 `CONFLICTED` 隐藏冲突来源。

### PEAG-C-39 `ABORTED` 接口只提供正向输入

```text
Historical Qualification = QUALIFIED
+ Projected Qualification = QUALIFIED
+ Aggregate Proof Applicability = APPLICABLE
+ Exact Proof / Attempt / Decision Key / Contract Scope
+ Matching Write-set and Temporal Coordinate
+ Registered Closure Completeness = COMPLETE
+ Complete Applicable Source Set
+ No Qualification or Applicability Conflict
+ No Unresolved Contrary Source
  -> may support Candidate Commit Resolution = ABORTED
```

本模型不创建候选提交解析。

### PEAG-C-40 豁免投影键必须精确

固定资格解析、豁免依据、要求契约、对象版本、迁移、槽位、冻结规则、有效时点、认识向量、视图、来源边界、更正表示和适用性规则。

### PEAG-C-41 `EXEMPT` 接口只提供正向输入

```text
Requirement Mode = CONDITIONALLY_EXEMPTIBLE
+ Registered Exemption Qualification = QUALIFIED
+ Exemption Applicability Projection = APPLICABLE
+ Exact Slot / Object / Version / Transition / Temporal Coordinate
+ Complete Applicable Source Set
+ Qualified and Applicable Completeness Proof
+ No Qualification or Applicability Conflict
+ No Unresolved Contrary Source
  -> may support Composite Resolution = EXEMPT
```

本模型不创建组合解析。

## 十一、权威目录

### PEAG-C-42 操作授权逐项分离

类型构造／登记／边界／完整性／解析，证明组装，资格消费组装，证明适用性计算／登记／边界／完整性／聚合，豁免适用性对应操作，完整性证明资格／适用性／登记，以及投影构建／发布授权必须分别登记。

### PEAG-C-43 授权作用域必须完整且不传播

每项授权固定允许类型、稳定键、注册表、规则、输入输出、来源／证据边界、有效窗口、`Can Change`、`Cannot Change` 和授予证据。任何授权不得传播到相邻操作、`ABORTED`、`EXEMPT`、决策、提交或冻结。

## 十二、失效、更正和前向解释

### PEAG-C-44 失效只追加新适用性

来源生命周期、更正、撤销、到期、规则或知识边界变化产生新适用性身份和投影重建要求，不修改历史证明、资格或适用性。

### PEAG-C-45 前向解释不得放大确定性

历史 `INDETERMINATE` 或 `CONFLICTED` 不得仅靠兼容声明变为确定结果；历史确定结果只有登记的定向兼容合同可保持，否则要求重新资格、重新适用和投影重建。

## 十三、非法状态与退出门槛

### PEAG-C-46 以下状态必须失败关闭

- 类型名称直接证明资格或适用性；
- 缺失来源被解释为未应用、`ABORTED` 或 `EXEMPT`；
- 原子资格产生 `CONFLICTED`；
- 资格计算者同时自证完整性；
- 未登记规则、类型、资格或适用性参与投影；
- 证明与豁免适用性共用未分域竞争边界；
- 冲突记录按时间、版本或调用者偏好选赢家；
- 投影摘要替代底层记录和闭包；
- 适用性变化覆盖历史；
- `ABORTED` 自动授权重试；
- 本模型创建提交、组合、决策或冻结事实。

### PEAG-C-47 模型退出门槛

```text
Qualification / Applicability Separation: REQUIRED_PASS
Proof / Completeness Authority Separation: REQUIRED_PASS
ABORTED Positive Chain: REQUIRED_PASS
EXEMPT Positive Chain: REQUIRED_PASS
Conflict and Evolution Contract: REQUIRED_PASS
WS-04 / WS-05 Compatibility: REQUIRED_PASS
CR-0002 / CR-0003 Consumer Compatibility: REQUIRED_PASS
Independent Model Review: REQUIRED_PASS
Residual Internal and Interface Blockers: REQUIRED_0
```

## 当前决定

```text
CR-0009 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Created: YES
Cross-interface Reviews: REQUIRED
Independent Composite Model Review: REQUIRED
WS-06 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Implementation Evidence: NOT_CREATED
Protected-write Evidence: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先执行 `WS-04/WS-05` 提供方接口审查，再核验 `CR-0002/CR-0003` 的 `ABORTED` 与 `EXEMPT` 正向消费链，最后进行独立模型审查。
