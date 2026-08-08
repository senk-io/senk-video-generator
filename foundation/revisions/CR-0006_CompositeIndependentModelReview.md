# CR-0006 时间映射治理复合模型独立审查

## 审查信息

```text
Review ID: CR-0006-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Review
Status: COMPLETED
Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 + CR-0006-R2
Cross-interface Baseline: CR-0005-R3-CR-0006-R2-TERMINAL-CROSS-INTERFACE-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-checks and cross-interface pass do not establish internal model completeness
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只审查时间映射治理复合模型自身是否完整、确定、双时间可重放且失败关闭。它不重新审查 `CR-0005` 来源模型，不修改被审提案，也不创建时间字段、映射、账本、坐标、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 规范时间字段、映射规则、最低矩阵和查询规则是否拥有可验证制度登记根；
2. 规范时间值是否具有稳定身份、候选—登记链和冲突边界；
3. 映射输入、规则和不同证据是否进入同一语义竞争域；
4. 旧字段映射是否真正确定且不能通过换规则或换证据逃避冲突；
5. 时间更正和迁移是否具有决定独立的竞争键及完整登记解析；
6. 时间派生账本、认识边界和双视图是否可重放；
7. 查询坐标注册表边界是否具有稳定身份而不是只拥有描述；
8. 原始断言和来源边界接口是否发生回归；
9. `WS-01` 引用兼容和终局交叉接口结论是否仍成立；
10. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 KNOWLEDGE BOUNDARY AND TEMPORAL LEDGER CLOSURE
CR-0006-R2 DERIVED EVALUATION AND COORDINATE REGISTRATION CLOSURE
All CR-0005 / CR-0006 cross-interface review records
Local repository state at review time
```

提案自检、文件存在、作者身份、交叉接口通过和规则数量均不作为内部模型通过依据。

## 总体裁决

复合模型成功建立：

```text
Registered Raw Temporal Assertion
  -> immutable Mapping Input
  -> Candidate / Registered Mapping Record
  -> append-only Temporal Derived Ledger Boundary
  -> Temporal Governance Boundary Vector T
  -> Knowledge Boundary Vector K
  -> Temporal Query Coordinate Q
  -> four-value Coordinate Registration Resolution
```

以下模型方向通过：

```text
Single-purpose Boundary: PASS
Canonical Temporal Field Separation: PASS
Valid / Observed / Recorded / Reviewed Separation: PASS
Precision and Uncertainty Preservation: PASS
System-clock Non-substitution: PASS
Raw Assertion Provider Identity: PASS
Open-world Exact-known-set Safety: PASS
Query-specific Minimum Completeness Matrix: PASS
Temporal-ledger Append-only Boundary: PASS
Temporal-ledger Completeness Non-self-proof: PASS
Knowledge Boundary Stable Key: PASS
Historical / Current View Separation: PASS
Four-stage Acyclicity: PASS
Coordinate Registration Four-value Direction: PASS
Cross-interface Compatibility: PASS
WS-01 Reference Direction: PASS_AS_DRAFT
```

但五项内部对象与竞争域尚未闭合：

1. 规范字段、映射规则、最低矩阵和查询规则缺少完整制度注册根；
2. 规范时间值只有字段列表，没有稳定值键和登记解析；
3. 映射键包含证据和规则，不同证据或规则产生的不兼容值可以逃离共同竞争集合；
4. 更正和迁移键包含请求或决定 ID，跨决定冲突没有聚合解析；
5. 查询坐标注册表边界有对象和权威，却没有稳定边界键与内容同一登记身份。

因此：

```text
Canonical Time Separation: PASS
Bitemporal Append-only Direction: PASS
Temporal Governance Contract Registration: FAIL_WITH_BOUNDED_BLOCKER
Canonical Temporal Value Identity: FAIL_WITH_BOUNDED_BLOCKER
Legacy Mapping Determinism: FAIL_WITH_BOUNDED_BLOCKER
Correction / Migration Conflict Aggregation: FAIL_WITH_BOUNDED_BLOCKER
Historical Knowledge Boundary: PASS
Coordinate Registry Boundary Identity: FAIL_WITH_BOUNDED_BLOCKER
WS-01 Reference Compatibility: PASS_AS_DRAFT
Cross-interface Gate: PASS
Independent Model Review: FAIL
CR-0006-R3 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
```

## 一、已通过：规范时间分离和不确定性

最低字段保持不可互换：

```text
VALID_AT / VALID_FROM / VALID_UNTIL
OBSERVED_AT
RECORDED_AT
REVIEWED_AT
DECIDED_AT
COMMITTED_AT
MAPPED_AT
CORRECTED_AT
SYSTEM_CLOCK_READING_AT
```

字段定义固定语义类别、主体、来源、值形态、时钟、时区、精度、不确定性、区间和映射资格。相同字面时间戳不证明字段等价。

```text
Canonical Field Semantic Separation: PASS
Valid / Transaction-time Separation: PASS
Review / Decision / Commit-time Separation: PASS
Bare Timestamp Prohibition: PASS
Default-time Substitution Prohibition: PASS
```

规范时间值保存字段身份、主体、时钟、时区、精度、不确定区间、来源断言和映射引用。区间默认半开，未知终点不能用当前时间或最大值补齐。

```text
Precision Preservation: PASS
Uncertainty Non-upgrade: PASS
Interval Boundary Explicitness: PASS
System Clock as Evidence Only: PASS
```

这些语义通过项不等于值对象登记身份已经闭合。

## 二、已通过：时间账本、认识边界与双视图

R1 建立无环阶段：

```text
Stage 1: Registered Base Source Boundary Vector B
Stage 2: Registered Temporal Records whose inputs reference B
Stage 3: Registered Temporal Governance Boundary Vector T
Stage 4: Registered Knowledge Boundary Vector K referencing B + T
```

映射、更正和迁移记录进入独立追加账本位置与边界；完整性由独立权威按载体、位置、读取和冲突子域评价。

R2 补充治理证据边界、时间账本完整性稳定键和四值登记解析。

```text
Temporal Ledger Position Non-reuse: PASS
Temporal Ledger Boundary Stable Key: PASS
Completeness Evidence Boundary: PASS
Completeness Four-value Resolution: PASS
Temporal Governance Vector Identity: PASS
```

`Known At` 收敛为认识边界向量；历史视图同时固定 `B` 与 `T`，当前重述必须使用新的 `B`、`T`、`K` 和查询身份。

```text
Knowledge-time Type Closure: PASS
Historical Knowledge Boundary: PASS
Current Restatement Non-overwrite: PASS
Four-stage Identity Cycle: NONE_FOUND
```

## 三、阻断 TM-M1：时间治理制度注册根不完整

模型定义了：

```text
Canonical Temporal Field Key
Temporal Mapping Rule Key
Registered Minimum Matrix Contract ID and Digest
Temporal Query Rule Version
```

也声明字段与映射规则的定义、登记权威，但没有为这些制度对象建立一致的根登记模型。

缺少：

```text
Temporal Field Registry ID Allocation and non-reuse resolution
Canonical Field Candidate / Registration Attempt / Registered Resolution
Field Registry Boundary and Completeness
Mapping Rule Candidate / Registration Attempt / Registered Resolution
Mapping Rule Registry Boundary and Completeness
Minimum Matrix Contract Key and Registration Resolution
Temporal Query Rule Key and Registration Resolution
```

### 反例

同一 `Temporal Field ID + Version` 被两个登记包定义为不同语义类别，或同一 `Mapping Rule ID + Version` 对时区和不确定性采用不同转换算法。当前只有稳定键和权威方向，没有完整登记边界与四值解析证明哪一个制度载荷可消费。

R2 的要求集合资格又依赖 `Registered Minimum Matrix Contract`，但该合同本身没有在复合模型中定义稳定候选—登记链。

```text
Expected: registered CONFLICTED governance-contract resolution
Current: contract references without complete registry roots
Result: TM-M1 reproduced
```

### 关闭条件

`CR-0006-R3` 必须建立统一但逐类型分权的制度注册契约，至少覆盖规范字段、映射规则、最低矩阵和查询规则：

1. 稳定键和永久版本身份；
2. 候选、登记尝试、内容同一和四值登记解析；
3. 逐类型注册表边界、必要完整性和冲突子域；
4. 合格 `NOT_REGISTERED`，缺失与读取失败只能 `INDETERMINATE`；
5. 只有已登记 `REGISTERED` 制度对象可以进入映射、要求资格和查询坐标。

```text
TM-M1 Governance Contract Registry Roots: BLOCKED
```

## 四、阻断 TM-M2：规范时间值缺少稳定登记身份

模型列出 `Canonical Temporal Value` 的字段：

```text
Canonical Temporal Value ID
Canonical Temporal Field ID and Version
Subject ID and Version
Instant or Interval
Clock / Timezone / Precision / Uncertainty
Source Assertion References
Mapping Record Reference or NATIVE_CANONICAL
Value Digest
```

但没有定义：

```text
Canonical Temporal Value Key
Candidate Canonical Temporal Value
Value Registration Attempt
Registered Canonical Temporal Value Resolution
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

也没有明确原生规范值与映射产生值是否进入同一目标字段、主体和查询域的冲突集合。

### 反例

同一主体、同一规范字段和同一来源边界产生两个相同 ID 但不同区间，或两个不同 ID 但语义上竞争的不兼容规范值。映射记录可以分别内容同一登记，但下游查询坐标只引用某个值 ID 和摘要，缺少值注册表完整竞争解析。

```text
Expected: registered CONFLICTED canonical-value resolution
Current: value shape without registration model
Result: TM-M2 reproduced
```

### 关闭条件

R3 必须定义：

1. 值 ID 与稳定键一对一、不复用；
2. 规范值候选—登记—四值解析及内容同一；
3. 目标字段、主体、语义域、来源边界和规则版本的值竞争集合；
4. 原生规范值与映射值的同域冲突聚合；
5. 查询坐标只能消费已登记 `REGISTERED` 的唯一规范值或显式失败解析。

```text
TM-M2 Canonical Temporal Value Identity: BLOCKED
```

## 五、阻断 TM-M3：映射可以通过证据或规则换键逃离冲突

映射输入键包含：

```text
Registered Raw Temporal Assertion ID and Digest
Base Source Boundary Vector ID and Digest
Source / Target Field IDs and Versions
Subject ID and Version
Temporal Mapping Rule ID and Version
Supporting Evidence Set Digest
```

映射解析键又绑定完整输入记录、规则和目标字段。不同规则或不同证据集合天然产生不同映射解析键。

### 反例

同一原始断言和目标规范字段：

```text
Rule R1 + Evidence E1 -> MAPPED(value A)
Rule R2 + Evidence E2 -> MAPPED(value B)
A incompatible with B
```

两个结果分别在自己的映射键内唯一且内容同一。`TM-C-32` 要求“多个可比较不兼容值、规则或登记载荷”为 `CONFLICTED`，但模型没有证据与规则独立的映射语义竞争键、完整映射集合边界或聚合登记解析来实施该要求。

置信度禁止选赢家的方向正确，但没有共同竞争身份时无法保证所有竞争项都被比较。

### 关闭条件

R3 必须建立：

```text
Temporal Mapping Semantic Conflict Set Key =
  Raw Assertion semantic identity
+ Subject ID and Version
+ Target Canonical Field ID and Version
+ Base Source Boundary Vector
+ Mapping Semantic Domain
+ Conflict Set Rule Version
```

该键必须排除映射记录 ID、映射时间、执行者、证据集合 ID 和单一映射规则 ID。不同规则与证据评价进入完整竞争集合，再形成四值聚合映射解析。

只有已登记聚合 `MAPPED` 可以产生唯一规范值；不兼容值或规则为 `CONFLICTED`，集合或规则注册边界不完整为 `INDETERMINATE`。

```text
TM-M3 Mapping Semantic Conflict Aggregation: BLOCKED
```

## 六、阻断 TM-M4：更正和迁移可以按请求或决定换键

当前键分别包含：

```text
Temporal Correction Key
  -> Correction Request ID

Temporal Migration Key
  -> Migration Decision ID
```

这使针对同一原始时间记录、相同字段集合或相同迁移作用域的不兼容请求与决定天然拥有不同键。

更正虽声明资格、候选、登记和内容同一方向，迁移虽声明版本化与不覆盖，但两者都没有决定 ID 独立的语义竞争集合、完整候选边界和四值聚合登记解析。

### 反例

```text
Correction C1 -> timezone UTC
Correction C2 -> timezone UTC+09

Migration M1 -> target contract V2
Migration M2 -> incompatible target contract V3
```

不同请求或决定 ID 使各自记录不必同键冲突。历史视图可以固定不同时间账本边界，但在同一完整边界内仍需要规范聚合决定冲突，而不是由查询者选择一个更正或迁移。

### 关闭条件

R3 必须分别建立：

```text
Temporal Correction Semantic Conflict Set Key
Temporal Migration Semantic Conflict Set Key
```

语义键必须排除请求 ID、决定 ID、记录 ID、登记时间和执行者；候选记录仍保存这些谱系字段。完整竞争集合必须形成候选—登记四值聚合解析，同键不兼容为 `CONFLICTED`，未知边界为 `INDETERMINATE`。

当前重述只能消费新的已登记聚合解析，不能覆盖历史更正或迁移。

```text
TM-M4 Correction / Migration Conflict Domains: BLOCKED
```

## 七、阻断 TM-M5：查询坐标注册表边界缺少稳定键

R2 新增：

```text
Temporal Query Coordinate Registry Boundary
Temporal Query Coordinate Registry Completeness Resolution
```

并要求边界固定候选、登记尝试、已登记坐标、规范摘要、空洞与冲突子域，形成候选—登记链。边界完整性复用时间派生账本完整性契约。

但 R2 没有定义：

```text
Temporal Query Coordinate Registry Boundary Key
Candidate Boundary Payload Digest
Registered Boundary Payload Digest
same-key incompatible boundary behavior
```

### 反例

两个边界 ID 对同一坐标注册表、相同位置范围或精确记录集合声明不同空洞或冲突子域。登记解析键绑定边界 ID 和摘要，因此它们形成不同解析键，而不是先得到一个边界冲突结果。

```text
Expected: stable boundary key with registered CONFLICTED resolution
Current: boundary description without normative key
Result: TM-M5 reproduced
```

### 关闭条件

R3 必须为坐标注册表边界建立稳定键，至少固定：

```text
Coordinate Registry ID and Version
Boundary Shape
Position Range or Exact Coordinate Record Set Digest
Registry Scope Digest
Boundary Rule Version
```

并建立候选—登记内容同一、同键异载荷冲突、边界四值登记解析和必要完整性。坐标登记解析只能消费已登记 `REGISTERED` 的唯一边界或显式 `CONFLICTED` 边界解析。

```text
TM-M5 Coordinate Registry Boundary Identity: BLOCKED
```

## 八、已通过：旧字段安全方向与接口边界

旧字段逐目标字段独立映射，`Review As Of` 不能替代认识边界，`Reviewed At` 只有审查行为证据时才能映射 `REVIEWED_AT`。系统创建、更新时间和文件修改时间不能默认映射现实时间。

```text
Legacy Field One-target-per-mapping: PASS
Review As Of Non-substitution: PASS
Reviewed At Evidence Requirement: PASS
System-time Non-substitution: PASS
Forward Precision Non-upgrade: PASS
```

这些方向通过，但由于 TM-M1 至 TM-M3，`Legacy Mapping Determinism` 仍不能最终通过。

来源侧接口继续只消费已登记原始断言和来源边界，时间治理不能反向创建或修改来源事实。

```text
Raw Assertion Content Identity: PASS
Source Boundary Non-mutation: PASS
Terminal Cross-interface Result: REMAINS_PASS
```

## 九、R3 修订边界

下一阶段应建立单一 `CR-0006-R3`，只关闭五项内部模型阻断。

允许修改：

- 时间治理制度对象的注册根；
- 规范时间值稳定身份和登记解析；
- 映射语义竞争集合及聚合解析；
- 更正与迁移语义竞争集合及聚合解析；
- 查询坐标注册表边界稳定键和登记解析；
- 相应权威类型、非法状态、自检和当前状态。

不得修改：

- 规范时间字段不可互换与精度、不确定性规则；
- 来源断言交接；
- 开放世界最低完整性矩阵；
- 时间派生账本、认识边界和双视图；
- 终局交叉接口通过记录；
- `CR-0005` 来源模型；
- 任何实际注册表、账本、制度冻结或运行时权威。

## 十、退出门复核

```text
Canonical Time Separation: PASS
Bitemporal Append-only Direction: PASS
Legacy Mapping Safety Direction: PASS
Legacy Mapping Determinism: FAIL
Historical Knowledge Boundary: PASS
WS-01 Reference Compatibility: PASS_AS_DRAFT
Cross-interface Compatibility: PASS
Independent Model Review: FAIL
Internal Model Blockers: TM-M1 + TM-M2 + TM-M3 + TM-M4 + TM-M5
WS-03 Model Exit: BLOCKED
Institution Freeze Readiness: NOT_ESTABLISHED
```

## 当前决定

```text
CR-0006 Composite Independent Model Review: COMPLETED
Review Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
Bounded Blockers: TM-M1 + TM-M2 + TM-M3 + TM-M4 + TM-M5
CR-0006-R3 Required: YES
Cross-interface Gate: REMAINS_PASS
WS-03 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段应建立 `CR-0006-R3`，只关闭上述五项内部模型阻断；完成后执行 `CR-0006` 复合模型独立复审。
