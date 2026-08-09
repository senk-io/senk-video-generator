# CR-0010-R2 复合独立模型复审

## 复审信息

```text
Review ID: CR-0010-R2-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Status: COMPLETED
Result: BLOCKED
Reviewed Composite: CR-0010 + CR-0010-R1 + CR-0010-R2
Initial Review Basis: CR-0010-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Interface Basis: CR-0010-R2-INTERFACE-REGRESSION-REVIEW
Reviewer: Codex
Review Independence: CR-0010-R2 self-check declarations were ignored
Closed Original Finding Count: 4
New Blocking Finding Count: 1
Residual Blocking Finding Count: 1
Next Authorized Stage: CR-0010-R3 idempotency conflict-key repair
```

## 一、总体裁决

类型导入全集、正式授予事实引用、更正／取代登记和物理外壳集合均已建立，但规范逻辑记录键错误包含候选载荷摘要，导致同一稳定键异载荷被分到不同逻辑身份，无法形成要求的冲突。

```text
DRG-IM-B1 Type Import Registry and Completeness: CLOSED
DRG-IM-B2 Authority Grant Fact Consumption: CLOSED
DRG-IM-B3 Canonical Idempotent Record Resolution: BLOCKED
DRG-IM-B4 Correction / Supersession Registration: CLOSED
Residual Internal Blockers: 1
Overall Result: BLOCKED
```

## 二、已关闭发现

```text
Finding ID: DRG-IM-B1
Result: CLOSED

Finding ID: DRG-IM-B2
Result: CLOSED

Finding ID: DRG-IM-B4
Result: CLOSED
```

类型导入拥有语义键、内容同一登记、竞争边界和必要类型全集；逐类型授权固定正式授予事实链；更正与取代拥有分域稳定键、正式变化链和独立登记边界。

## 三、`DRG-R2-B1`：载荷摘要错误进入逻辑冲突键

R2 定义：

```text
Canonical Logical Derived Record Key =
  Type Contract
+ Registered Record Type
+ Ledger Scope
+ Stable Registration Key
+ Candidate Payload Digest
```

这与基础稿的冲突规则矛盾：

```text
same Stable Registration Key
+ different Candidate Payload Digest
  -> CONFLICTED registration set
```

因为不同摘要生成不同逻辑键和不同物理外壳集合边界，两个载荷永远不会在同一竞争集合中相遇。

```text
Finding ID: DRG-R2-B1
Severity: BLOCKING
Result: OPEN
```

最低修复：从逻辑语义键和竞争边界键删除载荷摘要；载荷摘要只进入成员内容身份。完整边界先按稳定登记键收集全部载荷，再将同摘要成员归为幂等组；存在多个摘要组时必须 `CONFLICTED`。

## 四、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Residual Blocking Findings: DRG-R2-B1
CR-0010-R3 Required: YES
Interface Regression after R3: REQUIRED
Independent Final Model Review after R3: REQUIRED
WS-07 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只修复幂等逻辑键和同键异载荷冲突聚合。
