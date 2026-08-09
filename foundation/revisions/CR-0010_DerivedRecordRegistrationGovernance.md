# 派生记录登记治理提案

## 提案信息

```text
Proposal ID: CR-0010
Title: Derived Record Registration Governance
Workstream: WS-07
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: NORMATIVE_MODEL_CANDIDATE
Depends On: CR-0004-R5 INSTITUTION REGISTRY AND FREEZE REFERENCE SUPPORT COMPOSITE
Depends On: CR-0005-R11 SOURCE REGISTRY INTERFACE COMPOSITE
Depends On: CR-0006-R10 TEMPORAL MAPPING GOVERNANCE COMPOSITE
Depends On: CR-0009-R2 PROOF AND EXEMPTION APPLICABILITY GOVERNANCE COMPOSITE
Consumer Interface: CR-0002-CONSTITUTION-CANDIDATE
Consumer Interface: CR-0003-CONSTITUTION-CANDIDATE-R2
Future Consumer: WS-08 DEPENDENCY CLOSURE GOVERNANCE
Future Consumer: WS-09 PROJECTION AUDIT AND PUBLICATION INTERFACE
Cross-interface Reviews Required: YES
Independent Composite Model Review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本提案只治理派生记录从不可变候选到内容同一登记外壳的过程。它不计算业务结果，不创建决策、提交、闭包或投影事实，也不把通用登记能力传播为具体记录类型权威。

## 一、单一目的和边界

### DRG-C-01 单一目的

```text
Registered Derived Record Type Contract
+ Registered Per-type Registration Authority Instance
+ Immutable Candidate Derived Record
+ Registration Preconditions
  -> Immutable Registration Attempt
  -> Content-identical Registered Derived Record Envelope or failure
```

### DRG-C-02 登记不是业务计算

```text
Registration -/-> compute Qualification
Registration -/-> compute Applicability
Registration -/-> compute Admissibility
Registration -/-> compute Commit or Composite Resolution
Registration -/-> compute Closure Completeness
Registration -/-> create Projection Result
```

### DRG-C-03 登记不是正式事实提交

登记派生记录不能创建决策事实、目标迁移、权威写入成功、`COMMITTED`、`ABORTED`、`EXEMPT` 或发布事实。

### DRG-C-04 通用接口不传播具体权威

一个登记实现可以支持多个类型合同，但每次登记必须消费一个精确逐类型授权实例。实现能力、代码复用或接口可达性不构成授权。

## 二、规范对象

### DRG-C-05 对象家族必须封闭

```text
Derived Record Type Contract
Derived Record Type Registration Attempt
Registered Derived Record Type Contract
Derived Record Type Registration Resolution
Per-type Registration Authority Instance
Authority Instance Registration Attempt
Registered Per-type Registration Authority Instance
Authority Instance Registration Resolution
Candidate Derived Record Envelope
Derived Record Registration Attempt Record
Registered Derived Record Envelope
Derived Record Registration Resolution
Derived Record Competition Boundary
Derived Record Boundary Completeness Resolution
Derived Record Correction Record
Derived Record Supersession Record
```

### DRG-C-06 候选记录与登记外壳必须分层

候选载荷由业务计算权威产生；登记外壳只增加登记归因、账本位置、尝试和规范摘要，不改变候选业务载荷。

## 三、派生记录类型注册表

### DRG-C-07 类型合同稳定键

```text
Derived Record Type Contract Semantic Key =
  Derived Record Type Registry ID and Version
+ Candidate Record Type ID and Version
+ Registered Record Type ID and Version
+ Ledger Scope Type
```

合同载荷、授权、结果、登记时间和实现版本不得换键。

### DRG-C-08 类型合同最低载荷

```text
Candidate Record Type and Schema Contract
Registered Record Type and Schema Contract
Allowed Ledger ID / Namespace Contract
Stable Registration Key Contract
Candidate Payload Canonicalization Contract
Candidate Payload Digest Contract
Registered Envelope Contract
Idempotency and Duplicate Contract
Conflict Contract
Correction and Supersession Contract
Allowed Outcome Algebra
Required Rule and Institution Versions
Registration Preconditions
Failure Behavior
Canonical Byte Contract and Digest Algorithm
Institution Freeze Reference
```

### DRG-C-09 类型合同必须先冻结后登记

```text
Candidate Type Contract
  -> exact-payload Institution Freeze
  -> Type Contract Registration Attempt
  -> Registered Type Contract
```

候选、冻结、尝试和登记载荷摘要必须相等。

### DRG-C-10 类型合同竞争边界必须完整

边界键固定类型语义键、类型注册表、证据边界、观察切口和规则版本；载荷覆盖全部候选、成功、失败、永久空洞、冻结引用解析和既有解析谱系，并保存集合相等证明。

### DRG-C-11 类型合同解析使用四值控制面

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有登记完整边界上的唯一冻结内容单例可被消费；同键异模式、异键合同、异幂等或异更正语义必须 `CONFLICTED`。

## 四、首批逐类型合同目录

### DRG-C-12 决策模型记录必须分别登记合同

```text
Registered Admissibility Record
Registered Decision Commit Resolution Record
Registered Composite Requirement Resolution Record
Registered Exemption Basis Applicability Resolution Record
Registered Legality Review Record
Registered Legality Review Temporal Normalization Record
Registered Decision Correction Record
```

### DRG-C-13 提交模型记录必须分别登记合同

```text
Registered Proof Qualification Record
Registered Qualification Applicability Record
Registered Commit Resolution Record
Registered Target State Resolution Record
Registered Dependency Closure Record
Registered Closure Completeness Record
Registered Projection Change Audit Record
```

其中闭包、完整性和投影审计的最终载荷合同分别等待 `WS-08/WS-09` 新类型版本补齐；本提案不预判其业务字段。

### DRG-C-14 WS-04 至 WS-06 记录必须分别登记合同

```text
Registered Qualification Resolution
Registered Qualification Interpretation Record
Qualification Correction Record
Registered Atomic Authority Applicability Record
Registered Authority Applicability Consumer Resolution
Authority Applicability Correction Record
Registered Proof Applicability Record
Registered Exemption Applicability Record
Registered Completeness Evaluation Record
```

### DRG-C-15 类型目录扩展只能追加版本

新增候选／登记类型映射、账本作用域或模式必须产生新类型合同和注册表版本。通配符、父类型授权或“所有派生记录”合同非法。

## 五、逐类型登记授权实例

### DRG-C-16 授权实例只允许一个精确映射

```text
One Candidate Record Type
-> One Registered Record Type
-> One Ledger ID and Namespace
-> One Type Contract Version
```

### DRG-C-17 授权实例稳定键

```text
Per-type Registration Authority Semantic Key =
  Registration Authority Registry ID and Version
+ Authority Grant ID and Version
+ Registered Type Contract ID and Version
+ Candidate-to-registered Type Mapping Digest
+ Ledger ID and Namespace
```

授权持有人、时间和结果不得换键。

### DRG-C-18 授权实例最低载荷

```text
Registration Authority Grant ID and Version
Authority Holder Identity or Role
Candidate Record Type
Registered Record Type
Type Contract ID, Version and Payload Digest
Allowed Ledger ID and Namespace
Allowed Object Types and Version Scope
Allowed Stable Registration Key Domains
Allowed Outcome Types
Allowed Rule and Institution Versions
Effective From and Until
Can Change
Cannot Change
Registration Preconditions
Registration Decision Rule ID and Version
Failure Behavior
Grant Evidence References
Grant Institution Reference
Authority Payload Digest
```

### DRG-C-19 `Can Change` 和 `Cannot Change` 必须明确

`Can Change` 只允许追加内容同一登记外壳、登记归因和账本位置。`Cannot Change` 至少包括候选载荷、结果、理由、来源、时间、正式事实、其他账本和类型合同。

### DRG-C-20 授权实例必须内容同一登记

候选授权引用、登记尝试和已登记授权实例摘要相等，并进入完整竞争边界和独立完整性；最终解析为四值控制面。

### DRG-C-21 授权有效性必须按尝试坐标判断

登记尝试固定授权有效窗口、尝试时间、目标对象版本、规则／制度版本和账本坐标。系统当前时间不能追溯改变历史授权有效性。

## 六、候选派生记录信封

### DRG-C-22 候选信封必须内容寻址

```text
Candidate Record ID
Candidate Record Type and Version
Registered Target Record Type and Version
Registered Type Contract ID, Version and Digest
Stable Registration Key
Exact Business Payload
Business Payload Canonical Byte Contract
Candidate Payload Digest
Candidate Construction Authority Reference
Candidate Produced At
Rule and Institution Versions
Source / Evidence / Coordinate References
Prior Lineage References
```

### DRG-C-23 稳定登记键必须由类型合同定义

稳定键只包含业务语义身份和允许的作用域。候选 ID、载荷摘要、结果、写入者、登记时间、账本位置和重试次数不得用于换键。

### DRG-C-24 候选不可由登记者规范化

登记者不得清洗、补默认值、排序业务集合、改变枚举、重算业务结果或迁移模式。任何规范化必须由候选构造阶段按冻结类型合同完成。

## 七、登记尝试

### DRG-C-25 每次调用先形成不可变尝试

`Derived Record Registration Attempt Record` 至少绑定：

```text
Registration Attempt ID
Candidate Record ID, Type, Version and Payload Digest
Stable Registration Key
Registered Type Contract Resolution ID and Digest
Per-type Authority Instance Resolution ID and Digest
Target Registered Record Type
Target Ledger ID and Namespace
Expected Ledger Version or Boundary
Registration Decision Rule ID and Version
Attempted Registered Payload Digest
Idempotency Token and Replay Reference
Evidence References
Attempted At
Attempt Digest
Failure Evidence or NOT_APPLICABLE
```

### DRG-C-26 原子尝试结果严格三值

```text
REGISTERED
DECLINED
INDETERMINATE
```

未找到登记记录不能证明 `DECLINED`；同键竞争冲突由独立登记解析层表达，不写入单次尝试结果。

### DRG-C-27 所有尝试永久保留

成功、拒绝、未知、重复、并发失败和永久空洞都必须追加保存。后续成功不能删除或改写先前尝试。

## 八、内容同一登记

### DRG-C-28 业务载荷摘要必须相等

```text
Candidate Payload Digest
= Attempted Registered Payload Digest
= Registered Business Payload Digest
```

任一不等必须拒绝登记并保留证据。

### DRG-C-29 登记外壳只增加非业务归因

至少保存候选、类型合同、授权实例、尝试、稳定键、业务载荷摘要、登记账本位置、登记时间、账本版本、外壳摘要和证据。

### DRG-C-30 登记不能升级语义

候选资格、适用性、准入、解析或完整性结果保持原值；登记不能把候选、未知或冲突升级为正式决策、提交或确定投影。

## 九、幂等、重复和并发

### DRG-C-31 幂等身份由稳定键和载荷摘要共同判断

```text
same Stable Registration Key
+ same Candidate Payload Digest
+ same Type Contract Version
+ same Ledger Scope
  -> IDEMPOTENT_REPLAY
```

重复调用必须引用既有内容同一登记记录；可以追加尝试，不得创建第二个逻辑记录。

### DRG-C-32 同键异载荷必须冲突

```text
same Stable Registration Key
+ different Candidate Payload Digest
  -> CONFLICTED registration set
```

不得最后写入获胜、首次写入获胜、按版本号获胜或静默覆盖。

### DRG-C-33 异键同载荷不得默认合并

不同稳定键即为不同语义身份，除非冻结类型合同明确声明等价关系且登记了解析。摘要相同不能自行消除身份差异。

### DRG-C-34 并发尝试进入同一竞争边界

同一类型合同、账本作用域和稳定键下的全部候选、尝试、成功、失败和空洞进入一个竞争边界。并发顺序不改变语义解析。

### DRG-C-35 账本版本冲突不等于业务拒绝

乐观并发或预期账本版本不匹配可以使尝试 `INDETERMINATE` 或按合同重试，但不能推断候选业务结果无效或 `DECLINED`。

## 十、登记解析和完整边界

### DRG-C-36 登记语义冲突键

```text
Derived Record Registration Semantic Conflict Set Key =
  Registered Type Contract ID and Version
+ Registered Record Type ID and Version
+ Ledger ID and Namespace
+ Stable Registration Key
```

载荷、尝试、结果、登记者和时间不得换键。

### DRG-C-37 竞争边界必须覆盖完整集合

边界键固定语义冲突键、账本边界、证据边界、观察切口和规则版本；载荷覆盖全部候选、尝试、成功记录、永久空洞、重复引用和解析谱系，并保存逐集合相等证明。

### DRG-C-38 边界必须内容同一登记并独立证明完整

候选边界、尝试和已登记边界摘要相等；边界登记解析为四值控制面，独立完整性为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。登记者和对象解析者不能自证完整。

### DRG-C-39 最终登记解析使用四值

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

登记完整边界内唯一内容同一成功或其幂等副本支持 `REGISTERED`；完整零成功支持 `NOT_REGISTERED`；同键异载荷或矛盾记录支持 `CONFLICTED`；其他为 `INDETERMINATE`。

### DRG-C-40 运行消费只允许登记单例

只有最终解析 `REGISTERED` 且唯一逻辑内容身份可作为已登记派生记录消费。原子尝试 `REGISTERED` 不能绕过完整竞争边界。

## 十一、更正和取代

### DRG-C-41 非语义更正必须追加

更正记录固定原登记记录、缺陷、正确表示、证据、资格、授权、有效坐标和摘要。更正不得修改原业务载荷或稳定键。

### DRG-C-42 语义变化必须新建业务身份

结果、理由、来源、坐标、规则、对象版本或业务语义变化必须产生新候选和按类型合同确定的新稳定键，并通过取代记录连接历史。

### DRG-C-43 取代不删除历史

取代记录固定前驱、后继、取代类型、有效坐标、权威和证据。旧记录、尝试、冲突、更正和账本位置永久保留。

### DRG-C-44 更正和取代自身必须拥有类型合同

通用更正接口不能登记任意记录类型的更正。每类更正／取代记录必须拥有独立候选到登记类型映射和逐类型授权实例。

## 十二、权威目录

### DRG-C-45 类型合同操作分权

```text
DerivedRecordTypeContractCandidateConstructionAuthorityType
DerivedRecordTypeContractRegistrationAuthorityType
DerivedRecordTypeContractBoundaryConstructionAuthorityType
DerivedRecordTypeContractBoundaryRegistrationAuthorityType
DerivedRecordTypeContractBoundaryCompletenessQualificationAuthorityType
DerivedRecordTypeContractBoundaryCompletenessRegistrationAuthorityType
DerivedRecordTypeContractResolutionExecutionAuthorityType
DerivedRecordTypeContractResolutionRegistrationAuthorityType
```

### DRG-C-46 授权实例操作分权

```text
PerTypeRegistrationAuthorityCandidateConstructionAuthorityType
PerTypeRegistrationAuthorityRegistrationAuthorityType
PerTypeRegistrationAuthorityBoundaryConstructionAuthorityType
PerTypeRegistrationAuthorityBoundaryRegistrationAuthorityType
PerTypeRegistrationAuthorityBoundaryCompletenessQualificationAuthorityType
PerTypeRegistrationAuthorityBoundaryCompletenessRegistrationAuthorityType
PerTypeRegistrationAuthorityResolutionExecutionAuthorityType
PerTypeRegistrationAuthorityResolutionRegistrationAuthorityType
```

### DRG-C-47 派生记录登记操作分权

```text
DerivedRecordRegistrationAttemptConstructionAuthorityType
DerivedRecordEnvelopeRegistrationAuthorityType
DerivedRecordCompetitionBoundaryConstructionAuthorityType
DerivedRecordCompetitionBoundaryRegistrationAuthorityType
DerivedRecordBoundaryCompletenessQualificationAuthorityType
DerivedRecordBoundaryCompletenessRegistrationAuthorityType
DerivedRecordRegistrationResolutionExecutionAuthorityType
DerivedRecordRegistrationResolutionRegistrationAuthorityType
DerivedRecordCorrectionQualificationAuthorityType
DerivedRecordCorrectionRegistrationAuthorityType
DerivedRecordSupersessionQualificationAuthorityType
DerivedRecordSupersessionRegistrationAuthorityType
```

### DRG-C-48 授权不得传播

类型合同、授权实例、尝试、登记、边界、完整性、解析、更正和取代权威互不传播；业务计算权威不自动取得登记权威，登记权威不取得业务计算、决策、提交、闭包、投影发布或制度冻结权威。

## 十三、接口兼容

### DRG-C-49 WS-01 只提供冻结引用和制度注册支持

类型合同和授权实例消费有效制度冻结引用；本模型不创建冻结、分配冻结 ID 或修改制度注册表。

### DRG-C-50 WS-02／WS-03 只提供来源和时间引用

候选与登记外壳可以保存来源、证据和时间坐标引用，但不得创建、修改或重新解析来源／时间事实。

### DRG-C-51 WS-06 提供首批闭合类型

证明／豁免类型、资格、适用性、完整性及其登记载荷由 `WS-06` 定义；本模型只注册内容同一候选，不重算结果。

### DRG-C-52 WS-08／WS-09 通过新类型版本接入

闭包、闭包完整性、投影审计和发布输入类型必须在其模型闭合后登记精确类型合同和逐类型授权。本模型不提前定义业务载荷或发布资格。

## 十四、非法状态和退出门槛

### DRG-C-53 以下状态必须失败关闭

- 一个授权实例登记多个候选或登记类型；
- 通配符、父类型或“所有派生记录”授权；
- 登记者规范化或修改候选载荷；
- 没有尝试记录却宣称登记成功或拒绝；
- 候选与登记业务摘要不等；
- 同键异载荷最后写入获胜；
- 异键同摘要被默认合并；
- 账本版本冲突被解释为业务拒绝；
- 原子成功绕过完整竞争边界；
- 更正或取代覆盖原记录；
- 登记创建业务结果、决策、提交、闭包、发布或冻结事实；
- 候选、自检或文件存在替代已登记解析。

### DRG-C-54 模型退出门槛

```text
Per-type Authority Topology: REQUIRED_PASS
Registration Attempt Preservation: REQUIRED_PASS
Content Identity: REQUIRED_PASS
Idempotency and Concurrency: REQUIRED_PASS
Correction History: REQUIRED_PASS
WS-01 / WS-02 / WS-03 / WS-06 Compatibility: REQUIRED_PASS
CR-0002 / CR-0003 Consumer Compatibility: REQUIRED_PASS
Independent Model Review: REQUIRED_PASS
Residual Internal and Interface Blockers: REQUIRED_0
```

## 当前决定

```text
CR-0010 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Created: YES
Cross-interface Reviews: REQUIRED
Independent Composite Model Review: REQUIRED
WS-07 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Implementation Evidence: NOT_CREATED
Protected-write Evidence: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先执行 `WS-01/WS-02/WS-03/WS-06` 提供方及 `CR-0002/CR-0003` 消费接口审查，再执行独立模型审查。
