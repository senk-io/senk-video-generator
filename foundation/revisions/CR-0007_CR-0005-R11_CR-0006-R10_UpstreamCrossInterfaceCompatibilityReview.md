# CR-0007 与 CR-0005-R11／CR-0006-R10 上游交叉接口兼容审查

## 审查信息

```text
Review ID: CR-0007-CR-0005-R11-CR-0006-R10-UPSTREAM-CROSS-INTERFACE-COMPATIBILITY-REVIEW
Review Type: Independent Upstream Cross-interface Compatibility Review
Status: COMPLETED
Result: BLOCKED
Reviewed Qualification Proposal: CR-0007 QUALIFICATION GOVERNANCE
Reviewed Source Composite: CR-0005 + CR-0005-R1 through CR-0005-R11
Reviewed Temporal Composite: CR-0006 + CR-0006-R1 through CR-0006-R10
Upstream Baseline Review: CR-0005-R11-CR-0006-R10-TERMINAL-CROSS-INTERFACE-REGRESSION-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: CR-0007 self-check and interface mapping declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Qualification Model Review Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Source Registry Created: NO
Temporal Registry Created: NO
Qualification Registry Created: NO
Qualification Resolution Created: NO
Runtime Authority Created: NO
Blocking Finding Count: 4
Next Authorized Stage: CR-0007 bounded repair proposal only after explicit continuation
```

> 本文件只审查 `CR-0007` 对终局来源和时间复合接口的消费兼容性。它不修改三个提案，不执行资格计算，不创建注册表、账本、查询坐标、资格结果、制度冻结或运行时权威，也不等同于 `CR-0007` 独立模型审查。

## 一、审查命题与边界

### 审查命题

本轮独立回答：

1. `CR-0007` 是否保持 `B -> T -> K -> Q -> Qualification` 单向因果；
2. 资格输入是否完整消费四值时间查询坐标主体及其登记解析；
3. 资格输入是否只能消费 `CR-0005-R4` 后的已登记来源完整性聚合解析；
4. 来源完整性语义域、必要维度和聚合元组集合是否进入稳定身份；
5. 来源排除依据是否只消费 `CR-0005-R11` 复合模型真实提供的对象和权威；
6. 来源更正消费是否引用提供方已经定义的精确对象；
7. 未登记、未知、冲突和开放世界缺失是否保持失败关闭；
8. `CR-0007` 是否反向取得来源或时间治理权威；
9. 是否可以进入 `CR-0002`／`CR-0003` 消费接口兼容审查或独立模型审查。

### 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
CR-0005 + CR-0005-R1 through CR-0005-R11
CR-0006 + CR-0006-R1 through CR-0006-R10
CR-0005-R3-CR-0006-R2-TERMINAL-CROSS-INTERFACE-REVIEW
CR-0005-R11-CR-0006-R10-TERMINAL-CROSS-INTERFACE-REGRESSION-REVIEW
CR-0007 QUALIFICATION GOVERNANCE
Local repository state at review time
```

历史通过、文件存在、版本顺序、提案自检和 `PASS_AS_DRAFT` 声明均不作为本轮通过依据。

### 审查不处理

- `CR-0007` 与 `CR-0002` 三值依据资格接口的最终兼容裁决；
- `CR-0007` 与 `CR-0003` 四值证明资格、兼容域和前向解释接口的最终兼容裁决；
- `CR-0007` 内部全部登记拓扑、并发、幂等和更正模型的独立完整性；
- `WS-05`、`WS-06` 或后续工作流模型；
- 实现、运行样本、回放或冻结准备度。

## 二、总体裁决

`CR-0007` 保持了上游主干方向，没有反向修改 `B`、`T`、`K` 或 `Q`，也没有取得来源完整性计算权或时间映射权；但其消费键没有完整固定终局上游接口要求的四值坐标主体、来源完整性聚合元组、来源排除提供方拓扑和更正对象身份。

```text
B -> T -> K -> Q Direction: PASS
Source Authority Non-propagation: PASS_WITH_BLOCKERS
Temporal Authority Non-propagation: PASS_WITH_BLOCKERS
Four-value Query Subject Consumption: BLOCKED
Source Completeness Aggregate Pinning: BLOCKED
Source Exclusion Provider Topology: BLOCKED
Source Correction Object Identity: BLOCKED
Open-world Failure Closure: NOT_DEFEATED_BUT_NOT_SUFFICIENT
Historical / Current Separation: PARTIAL
Residual Upstream Cross-interface Blockers: 4
Overall Result: BLOCKED
```

因此：

```text
Upstream Cross-interface Compatibility: FAIL
CR-0002 / CR-0003 Consumer Compatibility Review: BLOCKED_BY_UPSTREAM_REPAIR
Independent Qualification Model Review: BLOCKED_BY_UPSTREAM_REPAIR
WS-04 Model Exit: NOT_READY
Institution Freeze: NOT_INFERRED
```

## 三、已通过的接口部分

### 方向保持单向

`CR-0007` 的规范方向为：

```text
Registered Source Boundary Vector B
  -> Registered Temporal Governance Boundary Vector T
  -> Registered Knowledge Boundary Vector K
  -> Registered Temporal Query Coordinate Q
  -> Qualification Input Package
```

资格结果不能改写上游对象。规则、资格、兼容域和前向解释身份也没有进入 `B`、`T`、`K` 或 `Q` 的稳定键。

```text
Reverse Identity Dependency: NONE_FOUND
Second Temporal Query Coordinate: NOT_CREATED
Qualification Result in Upstream Identity: NOT_FOUND
```

### 时间字段和视图模式保持分离

`CR-0007` 分离有效时间、认识边界、规则生效时间、计算时间和登记时间，并只使用：

```text
HISTORICAL_AS_KNOWN
CURRENT_RESTATED
```

未发现用当前系统时间补齐历史业务时间、把单一时间戳替代认识边界或覆盖历史视图的正向授权。

### 来源完整性没有被资格计算自证

`CR-0007` 明确禁止输入数量、查询成功、摘要存在、无返回或计算完成自证完整，也禁止资格计算者创建自身最终完整性证明。这个权威边界与 `CR-0005-R4` 后的来源完整性治理方向一致。

但“禁止自证”不足以替代精确聚合元组身份；该缺口形成 `XQG-B2`。

## 四、阻断 `XQG-B1`：四值查询坐标主体和登记解析未进入资格身份

### 上游规范要求

`CR-0005-R3 + CR-0006-R2` 已将时间查询坐标消费闭合为：

```text
Temporal Query Coordinate Key Q
  -> Coordinate Registry Boundary
  -> Registered Temporal Query Coordinate Registration Resolution RR
  -> Temporal Query Coordinate Subject Reference S
```

四值主体为：

```text
REGISTERED_SINGLETON
QUALIFIED_NOT_REGISTERED
INDETERMINATE_SUBJECT
CONFLICTED_SUBJECT
```

终局上游审查继续确认规范查询主体必须保存：

```text
Temporal Query Coordinate Key
Coordinate Subject State
Registered Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Candidate Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Conflict Set Digest or NOT_APPLICABLE or NOT_ESTABLISHED
Registered Coordinate Registration Resolution ID and Digest
Subject Reference Rule Version
```

只有 `REGISTERED_SINGLETON` 可以携带唯一已登记 `Q` 并支持确定下游结论。其他三个分支必须保留失败谱系并限制下游认识上限。

### `CR-0007` 当前缺口

`QG-C-08` 的资格稳定键固定：

```text
Qualification Source Boundary Vector B
Temporal Query Coordinate Q
Correction View Reference
Input Package Digest
```

`QG-C-18` 的输入包固定：

```text
Registered Temporal Query Coordinate Q Reference and Digest
```

但没有规范固定：

```text
Temporal Query Coordinate Subject Reference and Digest
Coordinate Subject State
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Coordinate Registration Resolution Result
Registered / Candidate / Conflict Payload Set Digests
REGISTERED_SINGLETON-only Registered Q field rule
```

仅声明“已登记 `Q`”不能替代终局四值主体和登记解析。相同坐标键可能在历史认识边界拥有 `REGISTERED` 解析，在后续边界拥有 `CONFLICTED` 解析；如果资格稳定键只固定坐标引用或输入包中的裸 `Q`，就可能复用旧确定资格，绕过当前冲突。

### 反例

```text
RR0 = REGISTERED
S0 = REGISTERED_SINGLETON(Q0)
Qualification(Q0) = QUALIFIED

Later RR1 = CONFLICTED
S1 = CONFLICTED_SUBJECT

CR-0007 key without S + RR
  -> may retain or reconstruct same apparent Q0 input
  -> may reuse QUALIFIED
```

正确上限必须是：

```text
S1 = CONFLICTED_SUBJECT
  -> Qualification Result cannot be terminal
  -> INDETERMINATE or CONFLICTED according to exact qualification rule
```

### 阻断判定

```text
Finding ID: XQG-B1
Severity: BLOCKING
Type: TEMPORAL_COORDINATE_SUBJECT_IDENTITY_OMISSION
Result: OPEN
```

### 最低修复要求

`CR-0007` 的输入包、资格稳定键、候选、登记记录和确定终局前置条件必须共同固定完整 `S + RR`，并声明：

```text
REGISTERED_SINGLETON + content-identical unique Q
  -> may support QUALIFIED or DISQUALIFIED

QUALIFIED_NOT_REGISTERED
  -> INDETERMINATE

INDETERMINATE_SUBJECT
  -> INDETERMINATE

CONFLICTED_SUBJECT
  -> CONFLICTED or INDETERMINATE without selecting a coordinate
```

不得只增加证据引用而不进入稳定身份。

## 五、阻断 `XQG-B2`：来源完整性聚合解析未按必要维度形成精确元组集合

### 上游规范要求

`CR-0005-R4` 已把来源完整性收紧为四值聚合：

```text
Source Completeness Aggregate Resolution Key =
  Source Completeness Semantic Domain Key
+ Registered Evaluation Boundary ID and Digest
+ Required Evaluation Boundary Completeness Resolution IDs and Digests
+ Aggregate Resolution Rule Version
```

下游不能选择底层有利评价。`CR-0006-R4` 进一步定义必要维度映射元组：

```text
Required Source Completeness Aggregate Resolution Tuple =
  Required Dimension ID and Version
+ Source Completeness Semantic Domain Key and Digest
+ Registered Source Completeness Aggregate Resolution ID and Digest
+ Source Completeness Aggregate Result
+ Registered Source Completeness Evaluation Boundary ID and Digest
+ Required Evaluation-boundary Completeness Resolution IDs and Digests
```

每个必要维度必须与恰好一个适用元组一一对应，并形成规范排序的精确元组集合摘要。

### `CR-0007` 当前缺口

`QG-C-14` 只要求规则声明必要完整性维度，`QG-C-18` 只保存：

```text
Registered Source Completeness Aggregate References
```

当前没有固定：

```text
Exact Required Source Completeness Semantic Domain Key Set Digest
Per-dimension Registered Aggregate Resolution ID and Digest
Aggregate Result
Registered Evaluation Boundary ID and Digest
Evaluation-boundary Completeness Resolution IDs and Digests
Exact Required Aggregate Resolution Tuple Set Digest
One-to-one required-dimension coverage proof
```

泛化“聚合引用”允许实现选择旧的 `COMPLETE` 聚合、遗漏必要维度、重复映射一个有利聚合或不固定评价边界。输入包总摘要只能证明被选内容没有变化，不能证明选择集合满足上游必要维度契约。

### 反例

```text
Required Dimensions = {IDENTITY, COVERAGE}

Tuple(IDENTITY) = COMPLETE
Tuple(COVERAGE) = CONFLICTED

Generic Aggregate References = {Tuple(IDENTITY)}
Input Package Digest is stable
  -/-> Required dimensions are complete
```

### 阻断判定

```text
Finding ID: XQG-B2
Severity: BLOCKING
Type: SOURCE_COMPLETENESS_AGGREGATE_TUPLE_UNDERPINNING
Result: OPEN
```

### 最低修复要求

规则、输入包、稳定键、候选和登记记录必须固定必要语义域、逐维度精确元组、元组集合摘要及集合相等证明。只有全部必要元组为适用、已登记、内容同一且 `COMPLETE`，并且评价边界自身完整无冲突时，才可支持确定资格终局。

## 六、阻断 `XQG-B3`：来源排除依据声明了上游未提供的登记拓扑

### 上游真实接口

`CR-0005` 的 `SR-C-16` 要求任何来源排除绑定：

```text
Exclusion Basis ID and Version
Exact Registry Scope
Exact Source Type or Identity Scope
Valid Interval
Decision and Authority References
Institution Freeze Reference
Evidence References
```

该规则证明来源排除必须有制度依据，但 `CR-0005` 至 `R11` 没有为名为 `Institutional Source Exclusion Basis` 的独立对象定义：

```text
Candidate Exclusion Basis Record
Exclusion Basis Registration Attempt
Registered Institutional Source Exclusion Basis
Exclusion Basis Registration Resolution
Exclusion Basis Registration Authority Type
Canonical Exclusion Basis Payload Digest
```

### `CR-0007` 当前越界

`QG-C-05` 把 `Institutional Source Exclusion Basis` 的逻辑真源声明为 `WS-02`，`QG-C-33` 又声明其身份、作用域、决定和登记权威属于 `WS-02`；`QG-C-56` 则消费：

```text
Registered Institutional Source Exclusion Basis References
```

该“已登记对象”并不是 `CR-0005-R11` 复合模型的已定义提供方输出。消费方不能通过命名一个上游对象来补造提供方登记拓扑。

同时，`CR-0007` 规定一个通过资格消费的排除依据可以在资格计算中排除来源，但没有固定 `CR-0005` 已登记排除决定或适用性解析。资格合格不等于排除决定在当前来源边界和时间坐标上适用。

### 反例

```text
Frozen Exclusion Institution exists
+ Exclusion Basis Qualification = QUALIFIED
  -/-> Registered WS-02 Exclusion Decision exists
  -/-> Exclusion is applicable at Q
  -/-> Source may be removed from Qualification Input Set
```

### 阻断判定

```text
Finding ID: XQG-B3
Severity: BLOCKING
Type: UNDEFINED_PROVIDER_REGISTRATION_TOPOLOGY_AND_AUTHORITY_EXPANSION
Result: OPEN
```

### 最低修复要求

有且只有两种无环修复方向可供后续修订选择：

```text
PATH_A
  -> consume exact CR-0005 SR-C-16 exclusion-basis fields
  -> do not call it a registered WS-02 object
  -> require separate applicable registered source exclusion decision before exclusion

PATH_B
  -> first create an independently reviewed CR-0005 provider-side bounded revision
  -> establish exclusion-basis registration topology
  -> then let CR-0007 consume its exact registered output
```

`CR-0007` 自行创建、登记或扩张 `WS-02` 排除依据均非法。

## 七、阻断 `XQG-B4`：来源更正消费对象没有精确落到提供方类型

### 上游真实对象

`CR-0005` 明确定义：

```text
Source Correction Record
Source Registry Current View
Source Applicability and Correction Record References
```

其中：

- `Source Correction Record` 是追加式非语义更正；
- `Source Registry Current View` 是指定边界和时间坐标上的可重建读面；
- 来源适用性最小接口保存来源适用性和更正记录引用。

### `CR-0007` 当前歧义

`QG-C-18` 和 `QG-C-56` 使用：

```text
Source Correction View References
```

上游没有这个精确规范对象。该词既可能表示更正记录集合，也可能表示当前读面，还可能被实现为临时投影。三者的身份、可变性、时间坐标和权威不同。

如果历史资格消费当前读面，就可能把后续更正带入 `HISTORICAL_AS_KNOWN`；如果当前资格只消费原始更正记录而不固定聚合和视图规则，又可能选择有利更正或遗漏冲突。

### 阻断判定

```text
Finding ID: XQG-B4
Severity: BLOCKING
Type: UNDEFINED_SOURCE_CORRECTION_CONSUMER_OBJECT
Result: OPEN
```

### 最低修复要求

后续修订必须为每个资格视图模式选择并固定上游精确对象：

```text
HISTORICAL_AS_KNOWN
  -> exact registered Source Correction Record set inside B/K/Q boundary
  -> exact set digest and completeness/conflict references

CURRENT_RESTATED
  -> exact Source Registry Current View ID and digest
  -> exact construction rule, Q, source records and correction set lineage
```

不得使用未定义的通用“更正视图”别名。

## 八、阻断之间的关系

四个阻断不是重复字段问题：

```text
XQG-B1
  -> fixes whether temporal query subject itself is usable

XQG-B2
  -> fixes whether required source completeness dimensions are fully and exactly supported

XQG-B3
  -> fixes whether source exclusion is provided by a real upstream authority path

XQG-B4
  -> fixes which immutable source correction representation is consumed at each view mode
```

它们共同决定资格输入集合和坐标是否可复现。只修复其中一项不能使接口通过。

## 九、反向权威和循环检查

未发现 `CR-0007` 明示取得以下上游权威：

```text
Source Record Construction or Registration Authority
Source Boundary or Snapshot Registration Authority
Source Completeness Evaluation or Aggregate Authority
Temporal Mapping or Registration Authority
Knowledge Boundary Construction Authority
Temporal Query Coordinate Registration Authority
```

但 `XQG-B3` 通过声明一个上游未定义的已登记排除对象形成了事实上的提供方拓扑扩张，因此总体权威分离只能判为带阻断通过。

```text
Explicit Upstream Authority Capture: NONE_FOUND
Implicit Provider Topology Expansion: FOUND
Cross-interface Acyclicity: STRUCTURALLY_PRESERVED_BUT_INPUT_IDENTITY_INCOMPLETE
```

## 十、修复后的必要反例复验

后续有界修订至少必须通过：

### 坐标登记演进

```text
RR0 = REGISTERED, S0 = REGISTERED_SINGLETON
RR1 = CONFLICTED, S1 = CONFLICTED_SUBJECT

Expected:
  Qualification Key 0 != Qualification Key 1
  historical terminal remains historical
  current terminal reuse is prohibited
```

### 来源完整性不利元组

```text
Required Dimension A = COMPLETE
Required Dimension B = INCOMPLETE or CONFLICTED

Expected:
  no QUALIFIED or DISQUALIFIED terminal
  omitted B is detected by set-equality proof
```

### 排除依据无登记决定

```text
Frozen exclusion contract exists
No applicable registered source exclusion decision

Expected:
  source remains in required input set
  or qualification remains INDETERMINATE
```

### 历史更正边界

```text
Correction C1 recorded after historical K0
CURRENT_RESTATED Q1 includes C1

Expected:
  HISTORICAL_AS_KNOWN at Q0 excludes C1
  CURRENT_RESTATED at Q1 includes exact C1 lineage
  qualification identities differ
```

## 十一、审查结论与退出状态

### 阻断清单

| 发现 | 主题 | 状态 |
|---|---|---|
| `XQG-B1` | 四值时间查询坐标主体与登记解析未固定 | `OPEN` |
| `XQG-B2` | 必要来源完整性聚合元组集合未固定 | `OPEN` |
| `XQG-B3` | 来源排除依据提供方登记拓扑未定义且权威越界 | `OPEN` |
| `XQG-B4` | 来源更正消费对象未精确映射 | `OPEN` |

### 已确认保持项

```text
B -> T -> K -> Q Direction: PRESERVED
No Second Query Coordinate: PRESERVED
Temporal Field Separation: PRESERVED
Historical / Current View Names: PRESERVED
Qualification Does Not Self-certify Completeness: PRESERVED
No Institution Freeze Inference: PRESERVED
```

### 当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Blocking Findings: 4
CR-0007 Upstream Cross-interface Compatibility: FAIL
CR-0007 Proposal Status: DRAFT_UNCHANGED
CR-0007-R1 Required: YES
CR-0002 / CR-0003 Consumer Compatibility Review: NOT_READY
Independent Qualification Model Review: NOT_READY
WS-04 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只能建立 `CR-0007-R1` 有界修订，精确关闭 `XQG-B1` 至 `XQG-B4`。修订后必须重新执行本上游交叉接口兼容审查；只有阻断数为零，才能进入 `CR-0002`／`CR-0003` 消费接口兼容审查和独立资格模型审查。
