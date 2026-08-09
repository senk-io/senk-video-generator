# 派生记录登记治理有界修订 R3：幂等冲突键闭合

## 修订信息

```text
Proposal ID: CR-0010-R3
Title: Idempotency Conflict-key Closure
Workstream: WS-07
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0010-R2 INTERNAL REGISTRATION AND IDEMPOTENCY CLOSURE
Repair Basis: CR-0010-R2-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Repair Scope: DRG-R2-B1 only
Institution Freeze Created: NO
Runtime Authority Created: NO
```

### DRG-R3-01 逻辑语义键不得包含载荷摘要

R2 的逻辑键由本规则覆盖为：

```text
Canonical Logical Derived Record Semantic Key =
  Registered Type Contract ID and Version
+ Registered Record Type ID and Version
+ Ledger ID and Namespace
+ Stable Registration Key
```

候选载荷摘要、外壳、尝试、位置、时间和登记者不得进入该键。

### DRG-R3-02 载荷内容身份只属于竞争成员

```text
Derived Record Content Identity =
  Canonical Logical Derived Record Semantic Key
+ Candidate Payload Digest
+ Candidate Payload Canonical Byte Contract Digest
```

### DRG-R3-03 完整竞争边界先按语义键收集

边界必须覆盖同一逻辑语义键下全部候选载荷摘要、尝试、成功外壳、失败、永久空洞和解析谱系，不能先按摘要过滤。

### DRG-R3-04 内容分组必须可重放

```text
Exact Content Identity Group Set =
  group all complete-boundary members by
  Candidate Payload Digest + Canonical Byte Contract Digest
```

固定分组集合摘要、逐组成员摘要、规范排序和从完整成员集到分组集的集合相等证明。

### DRG-R3-05 幂等只在单一内容组内成立

```text
one Content Identity Group
+ one physical envelope
  -> CANONICAL_SINGLETON

one Content Identity Group
+ multiple content-identical physical envelopes
  -> IDEMPOTENT_EQUIVALENT_SET
```

### DRG-R3-06 多内容组必须冲突

```text
same Canonical Logical Derived Record Semantic Key
+ more than one Content Identity Group
  -> CONFLICTED
```

组内物理数量、最早位置、最新位置、授权持有人和最大版本不能选赢家。

### DRG-R3-07 不完整边界不能推断幂等或冲突消失

边界或分组集合不完整时为 `INDETERMINATE`。已观察到异内容可以支持冲突，但未观察到异内容不能在不完整边界上证明单一内容组。

### DRG-R3-08 规范解析登记固定完整分组

候选规范解析必须固定逻辑语义键、登记完整竞争边界、独立完整性、完整成员集、内容分组集和集合相等证明；候选、尝试和登记载荷摘要相等。

### DRG-R3-09 更正与取代引用新逻辑语义键

R2 更正／取代键中的 `Canonical Logical Derived Record Key` 统一解释为本修订不含载荷摘要的语义键，并另行固定被更正或取代的精确内容身份和规范解析。

### DRG-R3-10 以下状态必须失败关闭

- 载荷摘要重新进入逻辑语义键或竞争边界键；
- 在收集完整集合前按载荷摘要过滤；
- 多个内容组按物理顺序选赢家；
- 不完整边界支持幂等单例；
- 更正只引用语义键而不固定精确内容身份。

### DRG-R3-11 候选级关闭声明

```text
DRG-R2-B1 Idempotency Conflict-key Identity: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Final Model Review: REQUIRED
```

## 当前决定

```text
CR-0010-R3 Status: DRAFT
Authority: NONE
Executable: NO
WS-07 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行接口回归和终局独立模型复审。
