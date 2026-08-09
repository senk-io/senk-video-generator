# 派生记录登记治理有界修订 R2：内部登记与幂等闭合

## 修订信息

```text
Proposal ID: CR-0010-R2
Title: Internal Registration and Idempotency Closure
Workstream: WS-07
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0010-R1 EXACT PROVIDER TYPE IMPORT CLOSURE
Repair Basis: CR-0010-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: DRG-IM-B1 through DRG-IM-B4 only
Interface Regression Review Required: YES
Independent Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 一、类型导入登记和全集

### DRG-R2-01 导入语义键必须稳定

```text
Provider Type Import Semantic Conflict Set Key =
  Provider Workstream ID
+ Provider Proposal Composite Version
+ Provider Type Contract ID and Version
+ Exact Candidate Record Type ID and Version
+ Exact Registered Record Type ID and Version
```

schema、结果、导入者和时间不得换键。

### DRG-R2-02 导入候选固定完整提供方合同

候选固定 R1 导入元组全部字段、提供方合同成员证明、候选导入状态、规范摘要、构造授权和证据。只有提供方精确合同可支持 `REGISTERABLE_EXACT`。

### DRG-R2-03 导入必须内容同一登记

```text
Candidate Import Payload Digest
= Attempted Import Payload Digest
= Registered Import Payload Digest
```

候选、尝试、记录和登记解析不可修改提供方字段。

### DRG-R2-04 导入竞争边界必须完整

边界键固定导入语义键、导入注册表、证据边界、观察切口和规则；载荷覆盖全部候选、成功、失败、永久空洞、提供方冲突和解析谱系，并保存集合相等证明。

### DRG-R2-05 导入边界独立登记完整性

候选边界、尝试、已登记边界和四值边界解析内容同一；完整性为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。导入者和类型合同构造者不能自证完整。

### DRG-R2-06 导入最终解析分离登记和语义结果

外层登记解析为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`；内层导入状态保持 R1 五值。只有外层 `REGISTERED` 且内层 `REGISTERABLE_EXACT` 可支持类型合同候选。

### DRG-R2-07 必要提供方类型集合必须登记

```text
Required Provider Type Set Boundary Key =
  Consumer Workstream ID and Model Version
+ Provider Workstream Set Digest
+ Required Record-purpose Catalog Version
+ Governed Evidence Boundary ID and Digest
+ Required Type Set Rule Version
```

### DRG-R2-08 必要类型边界固定全集

固定预期提供方／用途／候选—登记映射集合、观察导入集合、保留槽位集合、明确不适用集合、失败和空洞集合，以及逐集合规范摘要和相等证明。

### DRG-R2-09 导入集合完整性独立登记

只有必要类型边界已登记、完整性为 `COMPLETE` 且 `Required REGISTERABLE Set = Observed Registered Exact Import Set`，才可声明本目录版本完整。保留槽位不计作可登记类型。

## 二、正式授权事实消费

### DRG-R2-10 授权引用不能创建权威

`Registration Authority Grant Fact Consumption Reference` 固定：

```text
Formal Grant Decision Fact ID, Version and Digest
Authority -> Decision -> Evidence -> Formal Fact Chain Digest
Granting Authority and Holder Identity
Candidate / Registered Type Mapping Scope
Ledger Scope
Can Change and Cannot Change
Effective Window
Historical Commitment Reference
Evidence and Institution References
Canonical Grant Fact Payload Digest
```

### DRG-R2-11 授权引用稳定键

```text
Registration Grant Reference Semantic Key =
  Formal Grant Decision Fact ID and Version
+ Holder Identity or Role
+ Candidate-to-registered Type Mapping Digest
+ Ledger ID and Namespace
```

### DRG-R2-12 授权引用必须内容同一登记

引用候选、尝试、已登记引用、完整竞争边界、独立完整性和四值引用解析均保持内容同一。同一正式授予事实异映射、异账本或异边界必须 `CONFLICTED`。

### DRG-R2-13 授权实例只消费登记引用单例

逐类型授权实例候选必须固定引用最终解析、已登记完整竞争边界及精确授予载荷。引用非 `REGISTERED` 时不得建立授权实例。

## 三、幂等规范逻辑记录

### DRG-R2-14 逻辑记录键必须稳定

```text
Canonical Logical Derived Record Key =
  Registered Type Contract ID and Version
+ Registered Record Type ID and Version
+ Ledger ID and Namespace
+ Stable Registration Key
+ Candidate Payload Digest
```

物理外壳 ID、尝试、位置、时间和登记者不得换键。

### DRG-R2-15 物理外壳集合边界必须完整

```text
Physical Envelope Set Boundary Key =
  Canonical Logical Derived Record Key
+ Registered Ledger Boundary ID and Digest
+ Exact Successful Envelope Registration Resolution Set Digest
+ Exact Failed Attempt and Permanent Hole Set Digests
+ Boundary Rule Version
```

### DRG-R2-16 重复等价证明必须逐字段成立

每个物理外壳必须固定同一类型合同、稳定键、业务载荷摘要和账本作用域；集合成员证明及规范集合摘要必须登记。外壳归因差异不改变业务等价，但永久保留。

### DRG-R2-17 规范逻辑记录解析使用四值

```text
CANONICAL_SINGLETON
IDEMPOTENT_EQUIVALENT_SET
INDETERMINATE
CONFLICTED
```

唯一物理外壳支持单例；多个业务内容同一外壳支持等价集合；集合不完整为不确定；同稳定键异业务载荷、异类型合同或异账本为冲突。

### DRG-R2-18 规范解析必须内容同一登记

候选解析固定物理外壳完整边界、独立完整性、精确成员集和等价证明；候选、尝试、登记记录及外层四值登记解析摘要相等。

### DRG-R2-19 并发首次成功不选物理赢家

多个并发内容同一成功外壳共同形成 `IDEMPOTENT_EQUIVALENT_SET`，规范逻辑记录引用整个登记集合，不按先到、最小位置或实现主键选择权威赢家。

### DRG-R2-20 运行消费固定逻辑解析

下游只消费登记的规范逻辑记录解析及其精确物理外壳集合。单一物理外壳不能绕过集合边界和并发完整性。

## 四、更正和取代登记

### DRG-R2-21 更正稳定键按原记录和请求隔离

```text
Derived Record Correction Semantic Key =
  Original Canonical Logical Derived Record Key
+ Original Logical Resolution ID and Digest
+ Correction Request ID and Version
+ Correction Effective Coordinate
+ Type-specific Correction Rule Version
```

正确表示、结果和登记者不得换键。

### DRG-R2-22 更正候选固定非语义边界

固定原记录、缺陷字段、原表示、正确表示、业务载荷不变证明、稳定键不变证明、资格、授权、坐标、证据和候选摘要。

### DRG-R2-23 取代稳定键按前驱和取代决策隔离

```text
Derived Record Supersession Semantic Key =
  Predecessor Canonical Logical Derived Record Key
+ Successor Stable Registration Key
+ Supersession Decision Fact ID and Version
+ Supersession Effective Coordinate
+ Type-specific Supersession Rule Version
```

### DRG-R2-24 取代候选固定正式变化链

固定前驱／后继逻辑解析、正式取代决策事实链、变化类型、有效坐标、授权、证据和候选摘要。取代登记不能创建取代决定。

### DRG-R2-25 更正和取代分别内容同一登记

每域拥有独立类型合同、逐类型授权、候选、尝试、登记记录、完整竞争边界、独立完整性和四值最终解析；两域不能共享通用边界。

### DRG-R2-26 更正／取代冲突必须保留

同键异正确表示、异后继、异有效坐标或异正式事实链必须 `CONFLICTED`；不得按最新、最大版本或调用者选择赢家。

## 五、新增授权目录

### DRG-R2-27 导入和必要集合授权分权

```text
ProviderTypeImportCandidateConstructionAuthorityType
ProviderTypeImportRegistrationAuthorityType
ProviderTypeImportBoundaryConstructionAuthorityType
ProviderTypeImportBoundaryRegistrationAuthorityType
ProviderTypeImportBoundaryCompletenessQualificationAuthorityType
ProviderTypeImportBoundaryCompletenessRegistrationAuthorityType
ProviderTypeImportResolutionExecutionAuthorityType
ProviderTypeImportResolutionRegistrationAuthorityType
RequiredProviderTypeSetBoundaryConstructionAuthorityType
RequiredProviderTypeSetBoundaryRegistrationAuthorityType
RequiredProviderTypeSetCompletenessQualificationAuthorityType
RequiredProviderTypeSetCompletenessRegistrationAuthorityType
```

### DRG-R2-28 授予引用和逻辑解析授权分权

```text
RegistrationGrantReferenceConstructionAuthorityType
RegistrationGrantReferenceRegistrationAuthorityType
RegistrationGrantReferenceBoundaryConstructionAuthorityType
RegistrationGrantReferenceBoundaryRegistrationAuthorityType
RegistrationGrantReferenceBoundaryCompletenessQualificationAuthorityType
RegistrationGrantReferenceBoundaryCompletenessRegistrationAuthorityType
CanonicalLogicalRecordResolutionExecutionAuthorityType
CanonicalLogicalRecordResolutionRegistrationAuthorityType
PhysicalEnvelopeSetBoundaryConstructionAuthorityType
PhysicalEnvelopeSetBoundaryRegistrationAuthorityType
PhysicalEnvelopeSetCompletenessQualificationAuthorityType
PhysicalEnvelopeSetCompletenessRegistrationAuthorityType
```

### DRG-R2-29 更正和取代授权分权

```text
DerivedRecordCorrectionCandidateConstructionAuthorityType
DerivedRecordCorrectionRegistrationAuthorityType
DerivedRecordCorrectionBoundaryConstructionAuthorityType
DerivedRecordCorrectionBoundaryRegistrationAuthorityType
DerivedRecordCorrectionBoundaryCompletenessQualificationAuthorityType
DerivedRecordCorrectionBoundaryCompletenessRegistrationAuthorityType
DerivedRecordSupersessionCandidateConstructionAuthorityType
DerivedRecordSupersessionRegistrationAuthorityType
DerivedRecordSupersessionBoundaryConstructionAuthorityType
DerivedRecordSupersessionBoundaryRegistrationAuthorityType
DerivedRecordSupersessionBoundaryCompletenessQualificationAuthorityType
DerivedRecordSupersessionBoundaryCompletenessRegistrationAuthorityType
```

### DRG-R2-30 新授权互不传播

所有新增授权使用 DRG-C-18 的完整作用域，并固定允许稳定键、注册表、边界、输入输出和证据。导入、授予引用、逻辑解析、更正、取代及业务事实权威互不传播。

## 六、非法状态和候选声明

### DRG-R2-31 以下状态必须失败关闭

- 本地状态字段直接宣称精确导入；
- 必要类型目录遗漏提供方类型；
- 授权实例创建正式授予事实；
- 未登记授予引用支持登记授权；
- 并发物理外壳按位置选权威赢家；
- 单一外壳绕过完整集合；
- 更正改变业务语义或稳定键；
- 取代登记创建取代决定；
- 更正与取代共用未分域边界；
- 新授权隐式传播。

### DRG-R2-32 已通过接口不得回归

```text
Provider Exact Type Ownership: PRESERVED
Future Unregistered Type Slots: PRESERVED
Atomic Three-value Attempt: PRESERVED
Candidate / Registered Content Identity: PRESERVED
Registration -> Business Fact: PROHIBITED
```

### DRG-R2-33 四项阻断只在候选层关闭

```text
DRG-IM-B1 Type Import Registry and Completeness: CLOSED_AS_DRAFT
DRG-IM-B2 Authority Grant Fact Consumption: CLOSED_AS_DRAFT
DRG-IM-B3 Canonical Idempotent Record Resolution: CLOSED_AS_DRAFT
DRG-IM-B4 Correction / Supersession Registration: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0010-R2 Status: DRAFT
Authority: NONE
Executable: NO
WS-07 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 R2 接口回归和独立模型复审。
