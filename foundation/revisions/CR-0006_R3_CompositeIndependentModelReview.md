# CR-0006-R3 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 + CR-0006-R2 + CR-0006-R3
Repair Basis: CR-0006-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R3 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0006-R3` 对五项既有内部阻断的修复是否完整。它不修改被审提案，不重新裁决来源模型，也不创建时间制度对象、账本、查询坐标、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 时间治理制度合同注册根是否完整；
2. 规范时间值是否拥有稳定身份和共同冲突域；
3. 映射结果是否跨规则与证据聚合冲突；
4. 更正和迁移是否拥有决定独立的语义键、完整竞争边界和可登记聚合身份；
5. 查询坐标注册表边界是否拥有稳定身份与登记解析；
6. 时间账本、认识边界、历史视图和来源接口是否回归；
7. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 KNOWLEDGE BOUNDARY AND TEMPORAL LEDGER CLOSURE
CR-0006-R2 DERIVED EVALUATION AND COORDINATE REGISTRATION CLOSURE
CR-0006-R3 INTERNAL GOVERNANCE AND SEMANTIC CONFLICT CLOSURE
CR-0006-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

提案自检、规则数量、文件存在和作者声明均不作为通过依据。

## 总体裁决

R3 已实质关闭五项原阻断中的四项，并关闭更正、迁移决定 ID 的语义逃逸；但更正和迁移的竞争边界与聚合解析仍只有名称和结果枚举，没有稳定键及登记身份。

```text
TM-M1 Governance Contract Registry Roots: CLOSED
TM-M2 Canonical Temporal Value Identity: CLOSED
TM-M3 Mapping Semantic Conflict Aggregation: CLOSED
TM-M4 Correction / Migration Conflict Domains: CLOSED_WITH_ONE_RESIDUAL_BLOCKER
TM-M5 Coordinate Registry Boundary Identity: CLOSED
```

已通过方向：

```text
Governance Contract Stable Keys: PASS
Governance Contract Registration Roots: PASS
Canonical Temporal Value Allocation: PASS
Canonical Value Semantic Conflict Set: PASS
Canonical Value Aggregate Resolution: PASS
Mapping Semantic Conflict Set: PASS
Mapping Competing-record Boundary: PASS
Mapping Aggregate Resolution: PASS
Correction / Migration Semantic Keys: PASS
Coordinate Registry Root Identity: PASS
Coordinate Boundary Stable Key: PASS
Coordinate Boundary Registration Resolution: PASS
Previously Passed Temporal-model Backbone: PASS
```

因此：

```text
Independent Model Re-review: FAIL
CR-0006-R4 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、TM-M1 复验：时间治理制度注册根闭合

R3 建立封闭制度类型集合，并为规范字段、映射规则、最低完整性矩阵和查询规则定义统一但逐类型分权的注册框架。

```text
Temporal Governance Registry ID Allocation Key
Temporal Governance Contract Key
Temporal Governance Contract Registry Boundary Key
Temporal Governance Contract Registration Resolution Key
```

分配、候选、尝试、登记、边界、独立完整性和四值解析链完整。消费者必须固定精确 `REGISTERED` 合同解析；只引用版本号不能替代登记解析。

```text
Registry Root Bootstrap: PASS
Contract Type Closure: PASS
Content-identical Registration: PASS
Qualified NOT_REGISTERED: PASS
TM-M1 Result: CLOSED
```

## 二、TM-M2 复验：规范时间值身份闭合

规范时间值 ID 分配固定字段、主体、语义槽与候选值 ID，并禁止复用。规范值语义冲突键排除值 ID、字面时间、映射记录、执行者和证据集合。

原生规范值和映射产生值进入同一竞争边界，聚合解析保持：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

查询坐标只能消费唯一 `REGISTERED` 值。

```text
Stable Value Identity: PASS
Native / Mapped Common Conflict Domain: PASS
Value-package Key Escape: CLOSED
TM-M2 Result: CLOSED
```

## 三、TM-M3 复验：映射语义竞争闭合

映射语义冲突键固定原始断言、主体、目标字段、基础来源边界、语义域和规范值槽，并明确排除规则、证据集合、映射时间、执行者和置信度。

竞争边界覆盖不同规则和证据产生的全部可比较成员。聚合解析绑定已登记竞争边界、规则注册表边界和必要完整性，并禁止按置信度、时间、位置或较新规则选赢家。

```text
Rule / Evidence Key Escape: CLOSED
Cross-rule Competing Boundary: PASS
MAPPED / NOT_MAPPABLE / INDETERMINATE / CONFLICTED: PASS
TM-M3 Result: CLOSED
```

## 四、TM-M4 主体复验：决定独立语义域闭合

更正语义键排除请求 ID、记录 ID、登记时间、执行者和证据集合。迁移语义键排除决定 ID、记录 ID、登记时间、执行者和目标合同 ID。

这已经关闭原审查中“换请求或决定即可逃离冲突域”的主体问题。

```text
Correction Request-ID Escape: CLOSED
Migration Decision-ID Escape: CLOSED
Conflict-first Result Sets: PRESENT
Historical Non-overwrite: PASS
```

## 五、有界阻断 TM-R3-B1：更正与迁移边界及聚合解析缺少稳定身份

`TM-R3-21` 只声明：

```text
Temporal Correction Competing Record Boundary
Temporal Correction Aggregate Resolution
```

`TM-R3-23` 只声明：

```text
Temporal Migration Competing Record Boundary
Temporal Migration Aggregate Resolution
```

两处都没有定义稳定边界键、精确成员集合摘要、必要完整性、候选—登记链和聚合解析键。结果枚举不能代替对象身份。

至少缺少：

```text
Temporal Correction Competing Record Boundary Key
Temporal Correction Aggregate Resolution Key
Temporal Migration Competing Record Boundary Key
Temporal Migration Aggregate Resolution Key
```

### 反例

同一更正语义域存在两条不兼容更正。边界甲只纳入第一条并给出 `APPLIED`，边界乙纳入两条并给出 `CONFLICTED`。当前没有边界键和完整成员集合证明哪一个边界内容同一，也没有聚合解析键迫使同域异载荷发生冲突。

迁移具有同构反例：同一迁移语义域的两个目标合同被不同表面边界分别解析为 `MIGRATED`。

```text
Expected: exact complete competing set + registered aggregate identity
Current: named objects and result enums without stable keys
Result: TM-R3-B1 reproduced
```

### 关闭条件

`CR-0006-R4` 必须分别为更正和迁移：

1. 定义竞争记录边界稳定键；
2. 固定语义冲突键、账本边界、精确合格成员集合摘要和必要完整性；
3. 建立候选边界、登记尝试、内容同一登记记录和四值边界解析；
4. 定义聚合解析稳定键并固定已登记边界解析 ID 与摘要；
5. 同键异成员、异目标、异区间或异结果载荷必须 `CONFLICTED`；
6. 当前重述只能消费已登记、内容同一的聚合解析。

```text
TM-R3-B1 Correction / Migration Boundary and Aggregate Identity: BLOCKED
```

## 六、TM-M5 复验：坐标注册表边界身份闭合

R3 为坐标注册表建立稳定根身份、边界键、候选—登记链和边界登记四值解析。查询坐标登记解析进一步固定已登记坐标边界解析 ID 与摘要。

```text
Coordinate Registry Root Identity: PASS
Boundary Record-ID Escape: CLOSED
Boundary Content Identity: PASS
Resolved-boundary Consumption: PASS
TM-M5 Result: CLOSED
```

## 七、回归与退出判定

未发现 R3 对以下既有时间模型主干造成内部回归：

```text
Canonical Field Separation: PASS
Precision and Uncertainty Preservation: PASS
Raw Assertion Provider Identity: PASS
Temporal-ledger Append-only Boundary: PASS
Knowledge Boundary Type Closure: PASS
Historical / Current View Separation: PASS
Coordinate Four-value Resolution: PASS
Four-stage Acyclicity: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0006-R3 Independent Model Re-review: COMPLETED
Original Five Blockers: FOUR_CLOSED + ONE_CLOSED_WITH_RESIDUAL
Residual Bounded Blockers: 1
CR-0006-R4 Required: YES
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```
