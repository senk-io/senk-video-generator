# 权威适用性治理提案

## 提案信息

```text
Proposal ID: CR-0008
Title: Authority Applicability Governance
Workstream: WS-05
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: NORMATIVE_MODEL_CANDIDATE
Depends On: CR-0005-R11 SOURCE REGISTRY INTERFACE COMPOSITE
Depends On: CR-0006-R10 TEMPORAL MAPPING GOVERNANCE COMPOSITE
Consumes: IF-0001 Authority Model
Consumes: IF-0006 Evidence Model
Consumes: IF-0007 Institution Model
Upstream Cross-interface Review Required: YES
CR-0002 Consumer Interface Review Required: YES
Independent Composite Model Review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本提案只判断一个已存在、已登记的权威授予在精确主体、对象、行为、作用域和时间坐标上是否适用。它不创建授予，不扩张作用域，不判断依据资格，也不创建决策或提交事实。

## 一、单一目的与边界

### AAG-C-01 单一目的

```text
Registered Authority Grant Reference
+ Exact Authority Applicability Coordinate
+ Registered Source Applicability Inputs
+ Registered Temporal Subject
+ Registered Applicability Rule
  -> Registered Authority Applicability Resolution
```

### AAG-C-02 适用性不等于权威授予

```text
Authority Grant Fact -> may be evaluated
Applicability Resolution -/-> create Authority Grant Fact
Applicability Resolution -/-> expand Authority Scope
Applicability Resolution -/-> delegate Authority
Applicability Resolution -/-> cure invalid Grant
```

### AAG-C-03 适用性不等于资格或决策

```text
Qualification -/-> Authority Applicability
Authority Applicability -/-> Qualification
Authority Applicability -/-> Decision Fact
Authority Applicability -/-> Commit Fact
Authority Applicability -/-> Target Transition
```

### AAG-C-04 历史解析不可变

已登记解析保存当时授予版本、规则、来源、时间主体、认识边界和更正表示。撤销、到期、来源生命周期变化或新知识产生新解析身份，不覆盖历史记录。

## 二、规范对象

### AAG-C-05 对象家族必须封闭

```text
Authority Grant Consumption Reference
Authority Applicability Coordinate
Authority Applicability Rule
Authority Applicability Input Package
Candidate Atomic Authority Applicability Record
Atomic Authority Applicability Registration Attempt
Registered Atomic Authority Applicability Record
Atomic Authority Applicability Registration Resolution
Atomic Authority Applicability Evaluation Boundary
Atomic Boundary Completeness Resolution
Authority Applicability Conflict Aggregate
Authority Applicability Consumer Resolution
Authority Applicability Correction Record
```

### AAG-C-06 授予消费引用只引用已有权威事实

`Authority Grant Consumption Reference` 至少绑定：

```text
Authority Grant ID and Version
Granting Authority Identity and Grant Fact Reference
Authority Holder Identity or Role
Authority Type
Granted Object Types and Scope
Allowed Decision Types
Allowed Dispositions
Allowed Transition Types
Delegation and Non-delegation Constraints
Effective At and Expires At
Revocation and Supersession Contract
Grant Registry ID and Version
Grant Registration Resolution ID and Digest
Exact Grant Payload Digest
Institution Version and Freeze Reference
Evidence References
```

### AAG-C-07 授予登记解析使用四值控制面

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有内容同一、已冻结且唯一登记单例可以进入适用性计算。控制面四值不得冒充适用性结果。

### AAG-C-08 授予消费引用不能修补授予

引用构造者不得改变授予主体、作用域、期限、允许行为、撤销状态或冻结内容。任何不一致必须失败关闭并保存证据。

## 三、精确适用性坐标

### AAG-C-09 坐标必须完整

```text
Authority Applicability Coordinate =
  Authority Holder Identity or Role
+ Decision Type
+ Decision Object ID and Version
+ Decision Object Type
+ Decision Time
+ Requested Disposition
+ Requested Transition Type
+ Correction or Read Projection
+ Validity As Of
+ Knowledge Boundary Vector K
+ Registered Temporal Query Coordinate Q
+ Registered Temporal Query Coordinate Subject Reference S
+ Coordinate Registration Resolution RR
```

### AAG-C-10 坐标字段不得隐式默认

未知对象版本、决定时间、请求迁移、表示模式或时间主体不能由执行者取“当前”“最新”或默认值补足，只能产生 `INDETERMINATE`。

### AAG-C-11 四值时间主体必须整体消费

```text
REGISTERED_SINGLETON
QUALIFIED_NOT_REGISTERED
INDETERMINATE_SUBJECT
CONFLICTED_SUBJECT
```

只有 `REGISTERED_SINGLETON` 且坐标登记解析为 `REGISTERED` 可支持确定适用性；其余分支失败关闭。

### AAG-C-12 坐标对齐必须内容同一

授予作用域、来源适用性输入、适用性规则、候选记录和消费解析必须固定同一决策坐标。只比较时间戳或对象 ID 不构成对齐。

## 四、来源适用性输入

### AAG-C-13 来源适用性必须消费 WS-02 终局接口

`Registered Source Applicability Consumption Tuple` 至少固定：

```text
Registered Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
Source Applicability Change Conflict Set Key
Registered Source Applicability Change Set Boundary ID and Digest
Registered Temporal Query Coordinate Subject Reference ID and Digest
Registered Post-query Lifecycle View Evaluation Subject Resolution ID and Digest
Selected Target Lifecycle Registry Boundary ID and Digest
Boundary-context Eligibility Resolution ID and Digest
Registered Source Applicability Aggregate Resolution ID and Digest
Registered Lifecycle Record-type Catalog Aggregate Resolution Set Digest
Exact Source Registry and Correction References
Canonical Payload Digest
```

### AAG-C-14 来源适用性内部结果保持四值

```text
APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
```

`CONFLICTED` 不得被调用方选择有利来源、边界或当前视图消除。

### AAG-C-15 必要来源集合必须由规则声明

适用性规则必须声明每个适用性语义域所需来源类型、目的、作用域和完整性维度。执行者不得临时减少必要来源集合。

### AAG-C-16 来源消费包必须证明集合相等

```text
Required Source Applicability Tuple Set Digest
Observed Source Applicability Tuple Set Digest
Canonical Ordering Contract
Required-to-observed Set Equality Proof ID and Digest
Independent Completeness Authority Reference
```

缺少集合相等证明时不能建立确定结果。

### AAG-C-17 来源生命周期只改变后续适用性身份

同一授予和决策坐标下，来源生命周期边界推进使用相同 `Q` 但新的查询后视图评价和来源适用性聚合，必须产生新的适用性输入及解析身份。

### AAG-C-18 历史和当前重述必须分离

```text
HISTORICAL -> exact historical lifecycle boundary and evaluation
CURRENT_RESTATED -> exact selected successor evaluation and current knowledge boundary
```

当前重述不能覆盖历史解析；历史视图不能支持当前选择。

## 五、适用性规则治理

### AAG-C-19 规则必须拥有稳定语义键

```text
Authority Applicability Rule Semantic Conflict Set Key =
  Applicability Governance Registry ID and Version
+ Applicability Semantic Domain
+ Authority Type
+ Decision Type
+ Rule ID and Version
```

规则载荷、登记者、登记时间和结果不得用于换键。

### AAG-C-20 规则载荷必须冻结精确语义

至少固定：

```text
Allowed Grant Types and Scope Matching Contract
Holder and Role Matching Contract
Object and Version Matching Contract
Decision / Disposition / Transition Matching Contract
Effective / Expiry / Revocation Evaluation Contract
Required Source Applicability Contract
Temporal and Knowledge Coordinate Contract
Result and Failure-closure Algebra
Completeness Requirements
Canonical Byte Contract and Digest Algorithm
```

### AAG-C-21 规则必须先冻结后登记

```text
Candidate Rule
  -> independent institutional review
  -> exact-payload Institution Freeze
  -> Registration Attempt
  -> Registered Rule
  -> Four-value Rule Registration Resolution
```

候选、冻结和登记载荷摘要必须相同。

### AAG-C-22 规则竞争必须保留

同一规则语义键下异载荷、异结果代数、异来源要求或异冻结内容必须进入同一完整竞争边界并解析为 `CONFLICTED`，不得按版本号或登记时间选赢家。

### AAG-C-23 计算只能消费规则登记单例

规则登记解析必须绑定已登记完整竞争边界、独立边界完整性和精确竞争集合摘要。非 `REGISTERED` 结果一律禁止适用性计算。

## 六、输入和稳定身份

### AAG-C-24 输入包必须内容寻址

`Authority Applicability Input Package` 至少绑定：

```text
Authority Grant Consumption Reference and Digest
Exact Authority Applicability Coordinate and Digest
Registered Applicability Rule and Resolution
Exact Registered Source Applicability Tuple Set and Digest
Source Tuple Set Equality Proof
Required Source Completeness Resolutions
Temporal Subject and Coordinate Registration Resolution
Correction Representation
Construction Authority Reference
Canonical Byte Contract and Input Package Digest
```

### AAG-C-25 原子适用性语义键必须排除结果事实

```text
Atomic Authority Applicability Semantic Key =
  Authority Grant ID and Version
+ Authority Grant Payload Digest
+ Authority Holder Identity or Role
+ Exact Authority Applicability Coordinate Digest
+ Applicability Rule ID and Version and Payload Digest
+ Source Applicability Tuple Set Digest
+ Source Tuple Set Equality Proof Digest
+ Correction Representation Digest
+ Atomic Result Algebra Version
```

候选 ID、记录 ID、结果、执行者、登记位置和登记时间不得用于换键。

### AAG-C-26 输入变化必须产生新身份

授予版本、对象版本、请求行为、规则、时间主体、认识边界、来源生命周期评价、更正表示或完整性引用任一变化，都必须产生新的原子适用性语义身份。

## 七、计算和结果代数

### AAG-C-27 原子适用性结果严格三值

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

单次计算不得产生 `CONFLICTED`。

### AAG-C-28 `APPLICABLE` 要求完整正向链

至少同时证明：

```text
Grant Registration Resolution = REGISTERED
Rule Registration Resolution = REGISTERED
Holder or Role matches content-identically
Object, Decision, Disposition and Transition are within exact scope
Decision Time is inside effective non-expired interval
No applicable registered revocation or supersession disables the grant
All required Source Applicability Outcomes = APPLICABLE
Temporal Subject = REGISTERED_SINGLETON
Coordinate Registration Resolution = REGISTERED
All required completeness resolutions are COMPLETE
```

### AAG-C-29 `NOT_APPLICABLE` 只允许确定性否定

来源完整且无冲突时，以下任一可支持 `NOT_APPLICABLE`：

```text
Holder or Role outside exact grant scope
Object or Version outside exact grant scope
Decision / Disposition / Transition outside allowed scope
Decision Time before effective interval or after expiry
Valid registered revocation or supersession effective at coordinate
Required Source Applicability Outcome = INAPPLICABLE
```

### AAG-C-30 开放世界缺失必须不确定

授予缺失、撤销集合不完整、来源集合不完整、时间或作用域未知、规则冲突、来源冲突以及边界未知都只能支持 `INDETERMINATE`，不能从“未找到”推断 `NOT_APPLICABLE`。

### AAG-C-31 来源冲突必须保留

任一必要来源输入为 `CONFLICTED` 时，原子结果只能为 `INDETERMINATE` 并携带冲突引用。适用性执行者不得把来源冲突改写为不适用或适用。

### AAG-C-32 候选计算必须保存完整可重放证明

候选记录至少保存输入包、规则、逐谓词结果、必要来源集合、完整性、失败原因、结果、计算权威、规范摘要和证据引用。

## 八、原子登记和冲突聚合

### AAG-C-33 原子候选与登记载荷必须内容同一

```text
Candidate Atomic Payload Digest
= Attempted Registered Payload Digest
= Registered Atomic Payload Digest
```

登记不能修改结果、坐标、规则、来源集合或证据边界。

### AAG-C-34 原子登记解析使用四值控制面

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

失败尝试和永久空洞必须保留。只有登记单例可进入冲突聚合或消费解析。

### AAG-C-35 原子评价边界必须覆盖完整竞争集合

```text
Atomic Authority Applicability Evaluation Boundary Key =
  Atomic Authority Applicability Semantic Key
+ Atomic Registry ID and Version
+ Registry Evidence Boundary ID and Digest
+ Exact Atomic Registration Resolution Set Digest
+ Failed Attempt and Permanent Hole Set Digests
+ Required Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

### AAG-C-36 边界必须登记且独立证明完整

候选边界、登记尝试、已登记边界和四值边界登记解析必须内容同一。独立边界完整性解析为：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

计算者、登记者和聚合者不能自证完整。

### AAG-C-37 冲突聚合结果使用四值

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
CONFLICTED
```

只有登记完整边界可以支持确定聚合。完整集合同时存在 `APPLICABLE` 与 `NOT_APPLICABLE` 时必须 `CONFLICTED`。

### AAG-C-38 聚合不得选择有利子集

聚合键必须固定已登记评价边界、边界登记解析、独立完整性解析、精确原子登记解析集合和聚合规则版本。任何子集聚合均为非法。

## 九、三值消费解析

### AAG-C-39 决策消费接口严格三值

`Registered Authority Applicability Resolution` 的规范结果只能是：

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

这与 `CR-0002 DM-C-07` 内容同一。

### AAG-C-40 四值聚合必须显式适配为三值

```text
Aggregate APPLICABLE -> Consumer APPLICABLE
Aggregate NOT_APPLICABLE -> Consumer NOT_APPLICABLE
Aggregate INDETERMINATE -> Consumer INDETERMINATE
Aggregate CONFLICTED -> Consumer INDETERMINATE + mandatory Conflict References
```

适配不得删除冲突引用或放大确定性。

### AAG-C-41 消费解析必须固定最小合同

除 `DM-C-07` 字段外，至少补充：

```text
Authority Applicability Coordinate ID and Digest
Temporal Subject and Coordinate Registration Resolution IDs and Digests
Registered Applicability Rule ID, Version and Payload Digest
Exact Source Applicability Tuple Set Digest
Source Tuple Set Equality Proof ID and Digest
Atomic Record or Aggregate Source Kind
Atomic Registration Resolution or Aggregate Resolution ID and Digest
Registered Evaluation Boundary and Completeness IDs and Digests
Consumer Adaptation Rule Version
Conflict References or NOT_APPLICABLE
Consumer Payload Digest
```

### AAG-C-42 原子和聚合来源必须互斥

消费解析只能引用一个内容同一原子登记单例，或一个登记完整边界上的冲突聚合；不能同时引用两类来源拼接结果。

### AAG-C-43 只有适用结果支持决策准入

```text
APPLICABLE -> may support admissibility
NOT_APPLICABLE -> deterministic negative only when completeness is proven
INDETERMINATE -> fail closed
```

消费解析本身不创建 `ADMISSIBLE`、`INADMISSIBLE` 或决策事实。

## 十、撤销、到期、变更和更正

### AAG-C-44 撤销必须是已登记外部权威事实

适用性治理只消费已登记撤销、暂停、取代或终止事实及其完整竞争解析，不能自行撤销授予。

### AAG-C-45 到期由精确坐标计算

到期判断固定授予有效区间、规范时间映射、决策时间和查询主体。系统墙钟或执行时间不能替代决策坐标。

### AAG-C-46 作用域变化必须产生新授予版本

扩大、缩小或重新解释权威作用域必须由权威授予治理产生新版本或追加变化事实；适用性规则不能静默变更旧授予载荷。

### AAG-C-47 更正必须追加

非语义表示缺陷以 `Authority Applicability Correction Record` 追加；规则、输入、结果或作用域语义变化必须产生新身份和新解析。历史记录、失败尝试、空洞和冲突永久保留。

### AAG-C-48 当前重述必须可追溯

当前重述固定被重述历史解析、所有新增授予变化、来源生命周期评价、规则和知识边界。当前重述不能宣称旧解析当时错误，除非存在独立登记更正事实。

## 十一、权威目录

### AAG-C-49 操作授权必须逐项登记

```text
Grant Consumption Reference Construction Authority Type
Applicability Rule Definition Authority Type
Applicability Rule Registration Authority Type
Applicability Input Assembly Authority Type
Source Tuple Set Equality Proof Construction Authority Type
Source Tuple Set Equality Proof Registration Authority Type
Atomic Applicability Computation Authority Type
Atomic Applicability Registration Authority Type
Atomic Evaluation Boundary Construction Authority Type
Atomic Evaluation Boundary Registration Authority Type
Atomic Boundary Completeness Qualification Authority Type
Atomic Boundary Completeness Registration Authority Type
Applicability Conflict Aggregate Execution Authority Type
Applicability Conflict Aggregate Registration Authority Type
Consumer Resolution Construction Authority Type
Consumer Resolution Registration Authority Type
Applicability Correction Authority Type
```

### AAG-C-50 授权作用域必须完整

每项授权至少固定允许的注册表、权威类型、语义域、规则、稳定键、输入输出类型、上游引用、规范摘要合同、有效窗口、可变字段、不可变字段、授予权威和证据。

### AAG-C-51 权威不得传播

授予权威、规则权威、输入组装、计算、登记、边界、完整性、聚合、消费解析、更正、决策和制度冻结权威互不传播。

## 十二、并发、失败与非法状态

### AAG-C-52 并发同键记录必须共同竞争

同一原子语义键下的并发候选、尝试和记录必须进入同一完整评价边界。先到、最后写入、重试次数和登记者身份不能选赢家。

### AAG-C-53 失败尝试和永久空洞必须保留

计算失败、登记失败、边界失败、完整性未知和永久空洞均进入追加历史及相应边界，不能由后续成功删除。

### AAG-C-54 以下状态必须失败关闭

- 从适用性解析创建或扩张权威授予；
- 未登记、冲突或未冻结的授予或规则参与计算；
- 决策坐标字段缺失却取当前值；
- 时间主体非登记单例却产生确定结果；
- 来源适用性集合缺少集合相等证明；
- 来源冲突被选择、忽略或改写为确定结果；
- 从未找到授予、撤销或来源事实推断 `NOT_APPLICABLE`；
- 原子候选直接产生 `CONFLICTED`；
- 聚合选择完整评价边界的有利子集；
- 四值冲突在三值消费适配中丢失引用；
- 到期使用系统墙钟替代决策时间；
- 新规则、来源视图或更正覆盖历史解析；
- 计算、登记或聚合权威创建决策、提交或冻结事实。

### AAG-C-55 失败行为必须可重放

每个失败关闭结果必须保存精确输入身份、失败阶段、责任权威、证据边界、缺失或冲突引用及规范原因码。异常消息不能替代登记失败记录。

## 十三、演进与兼容

### AAG-C-56 规则演进不得重解释历史

新规则版本只作用于新计算身份。历史解析继续固定原规则及其冻结引用。

### AAG-C-57 兼容解释不得放大确定性

```text
Historical APPLICABLE -> APPLICABLE only with registered directional compatibility
Historical NOT_APPLICABLE -> NOT_APPLICABLE only with registered directional compatibility
Historical INDETERMINATE -> cannot become determinate without new computation
Conflict references -> cannot be dropped
```

### AAG-C-58 重新解析必须追加

授予、规则、对象版本、来源生命周期、时间映射、知识边界或更正变化要求新输入包、新候选、新登记和新消费解析；不能就地改写。

## 十四、接口与退出条件

### AAG-C-59 上游只读接口

```text
WS-02 Source and Lifecycle Truth -> read-only consumption
WS-03 Temporal Subject and Coordinates -> read-only consumption
WS-05 -> upstream mutation: PROHIBITED
WS-05 -> second temporal query coordinate: PROHIBITED
```

### AAG-C-60 下游消费接口

```text
WS-05 Registered Authority Applicability Resolution
  -> CR-0002 Decision Admissibility consumer
  -> WS-06 Proof and Exemption Applicability consumer where expressly scoped
```

下游不能反向要求本模型放宽三值接口、授予作用域或来源冲突。

### AAG-C-61 WS-04 与 WS-05 保持分权

资格解析可以成为后续准入的独立输入，但不是权威适用性谓词。权威适用性不得通过“依据已合格”推断授予适用。

### AAG-C-62 模型退出门槛

```text
Grant / Applicability Separation: REQUIRED_PASS
Authority Non-propagation: REQUIRED_PASS
Coordinate Completeness: REQUIRED_PASS
Source Applicability Interface Compatibility: REQUIRED_PASS
Conflict Preservation: REQUIRED_PASS
CR-0002 Three-value Consumer Compatibility: REQUIRED_PASS
Independent Model Review: REQUIRED_PASS
Residual Internal and Interface Blockers: REQUIRED_0
```

## 当前决定

```text
CR-0008 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Created: YES
Upstream Cross-interface Review: REQUIRED
CR-0002 Consumer Interface Review: REQUIRED
Independent Composite Model Review: REQUIRED
WS-05 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Implementation Evidence: NOT_CREATED
Protected-write Evidence: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先对 `CR-0008` 与 `CR-0005-R11`／`CR-0006-R10` 执行上游交叉接口审查，再与 `CR-0002` 执行三值消费接口审查，最后进行独立模型审查。
