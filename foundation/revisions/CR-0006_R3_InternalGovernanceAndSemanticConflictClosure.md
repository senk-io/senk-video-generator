# 时间映射治理有界修订 R3

## 修订信息

```text
Proposal ID: CR-0006-R3
Title: Internal Governance and Semantic Conflict Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R2 DERIVED EVALUATION AND COORDINATE REGISTRATION CLOSURE
Repair Basis: CR-0006-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-M1 + TM-M2 + TM-M3 + TM-M4 + TM-M5 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Independent Model Re-review Required: YES
Cross-interface Regression Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0005-R4
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `CR-0006` 复合模型独立审查的五项内部阻断。它不覆盖基础稿、R1、R2 或审查记录的历史文本，不创建规范字段、映射规则、时间值、账本、查询坐标、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R3-01 R3 只覆盖五项内部模型阻断

```text
TM-M1 Governance Contract Registry Roots
TM-M2 Canonical Temporal Value Identity
TM-M3 Mapping Semantic Conflict Aggregation
TM-M4 Correction / Migration Conflict Domains
TM-M5 Coordinate Registry Boundary Identity
```

未被本修订显式覆盖的 `CR-0006 + R1 + R2` 规则继续作为合并候选语义。终局来源—时间接口、认识边界和四值查询主体不得改变。

### TM-R3-02 时间制度对象不得自授权或自证完整

```text
Temporal Governance Contract
  -/-> grant its own definition or registration authority

Mapping Rule
  -/-> prove its own registry completeness

Canonical Temporal Value
  -/-> prove its own uniqueness

Aggregate Mapping Resolution
  -/-> prove its competing-record boundary
```

根授权和制度冻结引用必须来自 `IF-0007` 兼容外部边界。

## 二、TM-M1：统一时间治理制度注册根

### TM-R3-03 制度对象类型必须封闭且逐类型分权

```text
CANONICAL_TEMPORAL_FIELD_DEFINITION
TEMPORAL_MAPPING_RULE
COMPLETENESS_MINIMUM_MATRIX
TEMPORAL_QUERY_RULE
```

统一注册框架不合并权威。每种类型仍拥有独立定义、登记、边界、完整性和解析权威。

### TM-R3-04 时间治理注册表标识必须先分配

```text
Temporal Governance Registry ID Allocation Key =
  Governance Namespace ID and Version
+ Governance Contract Type
+ Candidate Registry ID
+ Intended Registry Scope Digest
+ Allocation Rule Version
```

候选、分配尝试、分配记录和登记解析必须内容同一，使用：

```text
ALLOCATED | NOT_ALLOCATED | INDETERMINATE | CONFLICTED
```

ID 在类型命名空间内永久不可复用；退役只追加历史。

### TM-R3-05 每个制度合同必须拥有稳定键

```text
Temporal Governance Contract Key =
  Governance Contract Type
+ Allocated Registry ID and Version
+ Contract ID and Version
+ Semantic Domain
+ Contract Rule Version
```

类型专用载荷分别覆盖：

- 规范字段的语义、主体、来源、值形态、时钟、精度和映射资格；
- 映射规则的输入、目标、算法、证据、时区、不确定性、失败与禁止推断；
- 最低矩阵的查询目的、边界形态、必要维度与不可削减规则；
- 查询规则的有效时间、认识边界、视图继承、坐标规范化与失败语义。

### TM-R3-06 制度合同必须形成内容同一登记链

```text
Registered ALLOCATED Governance Registry ID
+ Complete Governance Contract Payload
  -> Candidate Temporal Governance Contract
  -> Governance Contract Registration Attempt
  -> Registered Governance Contract Record
```

```text
Candidate Contract Payload Digest
= Registered Contract Payload Digest
```

同键异载荷必须冲突，不能按类型、登记时间或使用次数选赢家。

### TM-R3-07 制度注册表边界必须拥有稳定身份

```text
Temporal Governance Contract Registry Boundary Key =
  Governance Contract Type
+ Governance Registry ID and Version
+ First and Last Position or Exact Contract Record Set Digest
+ Registry Scope Digest
+ Boundary Rule Version
```

边界形成候选—登记链，保存空洞和冲突子域。载体、位置、读取和冲突子域完整性由不能定义或登记合同的独立权威评价。

### TM-R3-08 制度合同登记解析必须四值化

```text
Temporal Governance Contract Registration Resolution Key =
  Temporal Governance Contract Key
+ Registered Contract Registry Boundary ID and Digest
+ Required Registry Completeness Resolution IDs and Digests
+ Contract Resolution Rule Version
```

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有唯一内容同一合同、完整边界和无冲突支持 `REGISTERED`。合格完整空集支持 `NOT_REGISTERED`；缺失、读取或边界未知支持 `INDETERMINATE`；同键异载荷支持 `CONFLICTED`。

### TM-R3-09 所有时间治理消费者必须固定合同解析

规范字段、映射输入、要求集合资格和查询坐标必须分别绑定精确 `REGISTERED` 合同解析 ID 和摘要。只引用字段版本、规则版本或最低矩阵版本不能替代登记解析。

任何合同解析变化必须形成新的映射、要求评价或查询坐标身份；历史对象继续引用旧解析。

## 三、TM-M2：规范时间值稳定身份

### TM-R3-10 规范时间值 ID 必须一对一且不可复用

```text
Canonical Temporal Value ID Allocation Key =
  Registered Canonical Field Definition ID and Digest
+ Subject ID and Version
+ Temporal Value Semantic Slot ID and Version
+ Candidate Value ID
+ Allocation Rule Version
```

分配形成候选—尝试—登记四值解析。相同 ID 不能绑定不同字段、主体、语义槽或值载荷；退役不能复用。

### TM-R3-11 规范时间值语义槽必须排除值包字段

```text
Canonical Temporal Value Semantic Conflict Set Key =
  Registered Canonical Field Definition ID and Digest
+ Subject ID and Version
+ Temporal Value Semantic Slot ID and Version
+ Base Source Boundary Vector ID and Digest
+ Temporal Value Purpose
+ Conflict Set Rule Version
```

该键禁止包含值 ID、字面时间、映射记录 ID、映射时间、执行者和证据集合 ID。语义槽必须由来源断言角色或查询契约固定，查询者不能临时创建槽来隔离冲突。

### TM-R3-12 规范值必须形成候选—登记链

```text
Registered ALLOCATED Canonical Value ID
+ Registered Canonical Field Contract
+ Complete Canonical Value Payload
  -> Candidate Canonical Temporal Value
  -> Canonical Value Registration Attempt
  -> Registered Canonical Temporal Value Record
```

载荷必须包含基础稿规定的时点或区间、时钟、时区、精度、不确定性、来源断言、映射或 `NATIVE_CANONICAL` 引用及规范摘要。候选和登记载荷必须内容同一。

### TM-R3-13 规范值竞争边界必须覆盖原生值和映射值

```text
Canonical Temporal Value Competing Record Boundary Key =
  Canonical Temporal Value Semantic Conflict Set Key
+ Canonical Value Registry Boundary ID and Digest
+ Exact Competing Value Record Set Digest
+ Required Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

原生规范断言和映射产生值必须进入同一语义槽竞争边界，不能按来源模式分开消除冲突。

### TM-R3-14 规范值聚合解析必须四值化

```text
Canonical Temporal Value Aggregate Resolution Key =
  Canonical Temporal Value Semantic Conflict Set Key
+ Registered Competing Value Boundary ID and Digest
+ Required Boundary Completeness Resolution IDs and Digests
+ Aggregate Rule Version
```

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

唯一规范载荷或内容同一重申支持 `REGISTERED`；完整空集支持 `NOT_REGISTERED`；集合、字段、来源或证据未知支持 `INDETERMINATE`；不兼容时点、区间、精度、不确定性、来源模式或载荷支持 `CONFLICTED`。

查询坐标只可消费 `REGISTERED` 唯一值；其他结果必须失败关闭。

## 四、TM-M3：映射语义竞争和聚合解析

### TM-R3-15 映射语义冲突键必须排除规则和证据包

```text
Temporal Mapping Semantic Conflict Set Key =
  Registered Raw Temporal Assertion ID and Payload Digest
+ Subject ID and Version
+ Target Canonical Field Definition ID and Digest
+ Base Source Boundary Vector ID and Digest
+ Mapping Semantic Domain
+ Canonical Value Semantic Slot ID and Version
+ Conflict Set Rule Version
```

禁止包含映射记录 ID、单一映射规则 ID、证据集合 ID、映射时间、执行者和置信度。

### TM-R3-16 单一规则映射记录继续保留完整谱系

现有映射输入键和候选—登记链继续保存精确规则、证据、算法、精度和不确定性。它们是竞争集合成员身份，不是最终语义冲突键。

只有使用已登记 `REGISTERED` 映射规则合同的记录可以成为合格成员；规则冲突或未登记使成员资格失败关闭。

### TM-R3-17 映射竞争边界必须覆盖全部可比较成员

```text
Temporal Mapping Competing Record Boundary Key =
  Temporal Mapping Semantic Conflict Set Key
+ Mapping Ledger Boundary ID and Digest
+ Exact Eligible Mapping Record Set Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

不同规则和证据集合的映射必须进入同一完整边界。边界不能由映射执行者、规则制定者或聚合者自证完整。

### TM-R3-18 映射聚合解析必须使用四值

```text
Temporal Mapping Aggregate Resolution Key =
  Temporal Mapping Semantic Conflict Set Key
+ Registered Competing Mapping Boundary ID and Digest
+ Registered Mapping Rule Registry Boundary ID and Digest
+ Required Completeness Resolution IDs and Digests
+ Aggregate Rule Version
```

```text
MAPPED(Canonical Temporal Value Candidate Payload Digest)
NOT_MAPPABLE(Qualified Reason)
INDETERMINATE
CONFLICTED
```

全部合格成员唯一支持同一规范值解析时可 `MAPPED`；完整集合和合格不可映射证据支持 `NOT_MAPPABLE`；集合、规则、证据或来源未知支持 `INDETERMINATE`；不兼容值、规则、精度、区间或载荷支持 `CONFLICTED`。

### TM-R3-19 映射聚合不得按置信度或时间选赢家

置信度、映射时间、登记位置、规则版本较新或使用次数都不能选择冲突赢家。新规则产生新成员和新完整边界；历史聚合解析保留，当前重述使用新的聚合身份。

只有已登记聚合 `MAPPED` 可以产生内容同一的规范时间值候选；该候选仍必须经过规范值登记和聚合解析。下游确定查询必须同时验证映射聚合为 `MAPPED` 且规范值聚合为 `REGISTERED`，不能由任一方自证另一方。

## 五、TM-M4：时间更正竞争域

### TM-R3-20 更正语义键必须排除请求 ID

```text
Temporal Correction Semantic Conflict Set Key =
  Original Temporal Record ID and Digest
+ Correctable Field Semantic Set Digest
+ Correction Effective Temporal Coordinate
+ Correction Semantic Domain
+ Conflict Set Rule Version
```

请求 ID、记录 ID、登记时间、执行者和证据集合 ID 不得进入语义冲突键。

### TM-R3-21 更正必须形成完整竞争边界和聚合解析

```text
Temporal Correction Competing Record Boundary
  -> covers all qualified candidate and registered corrections

Temporal Correction Aggregate Resolution =
  APPLIED | NOT_APPLIED | INDETERMINATE | CONFLICTED
```

唯一内容同一非语义更正支持 `APPLIED`；完整合格未应用证明支持 `NOT_APPLIED`；边界或资格未知支持 `INDETERMINATE`；不兼容时区、格式、精度或载荷支持 `CONFLICTED`。

当前重述只能消费已登记聚合 `APPLIED`；历史记录和旧视图不得覆盖。

## 六、TM-M4：时间迁移竞争域

### TM-R3-22 迁移语义键必须排除决定 ID

```text
Temporal Migration Semantic Conflict Set Key =
  Source Temporal Contract ID and Version
+ Migration Scope Digest
+ Migration Semantic Domain
+ Migration Effective Coordinate
+ Conflict Set Rule Version
```

迁移决定 ID、记录 ID、登记时间、执行者和目标合同 ID 不得用于隔离竞争；目标合同保留在成员载荷中。

### TM-R3-23 迁移必须形成完整竞争边界和聚合解析

```text
Temporal Migration Competing Record Boundary
  -> covers all qualified candidate and registered migrations

Temporal Migration Aggregate Resolution =
  MIGRATED | NOT_MIGRATED | INDETERMINATE | CONFLICTED
```

唯一目标合同和内容同一迁移支持 `MIGRATED`；完整合格未迁移证明支持 `NOT_MIGRATED`；边界、合同或决定资格未知支持 `INDETERMINATE`；不同目标合同、不兼容作用域或载荷支持 `CONFLICTED`。

迁移不能覆盖旧映射或更正；新聚合解析只进入新的时间治理边界和当前重述。

### TM-R3-24 更正和迁移聚合必须逐操作分权

更正与迁移分别拥有竞争边界构造、边界登记、聚合执行和聚合登记权威。更正权不能创建迁移，迁移权不能更正原始断言，两者都不能修改历史时间账本边界。

## 七、TM-M5：查询坐标注册表边界稳定身份

### TM-R3-25 坐标注册表必须拥有稳定根身份

```text
Temporal Query Coordinate Registry ID and Version
Coordinate Registry Scope Digest
Coordinate Registry Contract Registration Resolution ID and Digest
```

该注册表合同属于 `TEMPORAL_QUERY_RULE` 兼容治理域，但其身份分配、合同登记和边界权威仍独立。

### TM-R3-26 坐标注册表边界必须拥有稳定键

```text
Temporal Query Coordinate Registry Boundary Key =
  Coordinate Registry ID and Version
+ Boundary Shape
+ First and Last Position or Exact Coordinate Record Set Digest
+ Coordinate Registry Scope Digest
+ Boundary Rule Version
```

边界键不得包含边界记录 ID、构造者、登记时间或登记解析结果。

### TM-R3-27 坐标边界必须形成内容同一登记链

```text
Candidate Coordinate Registry Boundary
  -> Coordinate Boundary Registration Attempt
  -> Registered Coordinate Registry Boundary Record
```

候选和登记载荷必须共同固定坐标候选、登记尝试、已登记坐标、规范摘要、空洞、冲突子域、边界形态和规则，并保持摘要内容同一。

### TM-R3-28 坐标边界登记解析必须四值化

```text
Coordinate Registry Boundary Registration Resolution Key =
  Temporal Query Coordinate Registry Boundary Key
+ Coordinate Boundary Registry Boundary ID and Digest
+ Required Boundary-registry Completeness Resolution IDs and Digests
+ Boundary Resolution Rule Version
```

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同键异载荷、不同空洞或冲突子域必须 `CONFLICTED`；边界注册表不完整必须 `INDETERMINATE`。

### TM-R3-29 查询坐标登记解析只能消费已解析边界

以本规则收紧 R2 的坐标登记解析键：

```text
Temporal Query Coordinate Registration Resolution Key =
  Temporal Query Coordinate Key
+ Registered Coordinate Registry Boundary Registration Resolution ID and Digest
+ Required Coordinate Registry Completeness Resolution IDs and Digests
+ Coordinate Registration Resolution Rule Version
```

边界解析必须为 `REGISTERED`，并内容同一指向精确坐标边界。原有四值坐标登记解析、规范载荷集合和来源适用性消费接口保持不变。

## 八、权威、回归和非法状态

### TM-R3-30 新增角色必须逐类型逐操作分权

制度注册、值分配与登记、映射聚合、更正聚合、迁移聚合、坐标边界登记及其完整性权威不得互相传播。每个授权实例必须限定合同类型、字段、主体、来源边界、语义域、账本、输出和规则版本。

### TM-R3-31 新增非法状态必须失败关闭

- 未登记治理合同被映射或查询消费；
- 规范值 ID 复用或值记录绕过聚合解析；
- 规则 ID、证据集合或置信度隔离映射冲突；
- 更正请求 ID 或迁移决定 ID 隔离语义冲突；
- 当前重述覆盖历史映射、更正或迁移；
- 坐标边界记录 ID 隔离同键边界冲突；
- 未取得 `REGISTERED` 边界解析的坐标边界进入坐标登记解析；
- 内部修订改变 `Known At` 类型、来源断言接口或四阶段无环链；
- 候选、自检或文件存在替代已登记解析。

### TM-R3-32 已通过主干不得回归

```text
Canonical Field Separation: PRESERVED
Precision and Uncertainty: PRESERVED
Raw Assertion Provider Identity: PRESERVED
Open-world Minimum Matrix: PRESERVED
Temporal-ledger Bitemporal Boundary: PRESERVED
Knowledge Boundary Type Closure: PRESERVED
Historical / Current View Separation: PRESERVED
Coordinate Four-value Resolution: PRESERVED
Cross-interface Acyclicity: PRESERVED
WS-01 Reference Direction: PRESERVED
```

## 九、候选级闭合声明

### TM-R3-33 R3 只声明五项内部阻断候选闭合

```text
TM-M1 Governance Contract Registry Roots: CLOSED_AS_DRAFT
TM-M2 Canonical Temporal Value Identity: CLOSED_AS_DRAFT
TM-M3 Mapping Semantic Conflict Aggregation: CLOSED_AS_DRAFT
TM-M4 Correction / Migration Conflict Domains: CLOSED_AS_DRAFT
TM-M5 Coordinate Registry Boundary Identity: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R3 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-M1 + TM-M2 + TM-M3 + TM-M4 + TM-M5 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 `CR-0006` 复合模型独立复审，并与 `CR-0005-R4` 共同执行终局接口回归检查。自检不能独立证明五项阻断关闭。
