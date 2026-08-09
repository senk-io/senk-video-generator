# 投影审计与发布接口有界修订 R1：转换槽身份闭合

```text
Proposal ID: CR-0012-R1
Workstream: WS-09
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0012
Repair Basis: CR-0012-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: PAG-IM-B1 only
```

### PAG-R1-01 转换槽键不含新候选摘要

```text
Projection Transition Slot Key =
  Projection Stable Key
+ Previous Published Envelope Registration Resolution ID and Digest
   or CANONICAL_BOOTSTRAP_MARKER
+ Previous Temporal Coordinate Digest or NOT_APPLICABLE
+ New Temporal Coordinate Digest
+ Projection Transition Rule Version
```

候选投影摘要、审计结果、发布者和时间不得进入槽键。

### PAG-R1-02 审计语义键绑定转换槽

`Projection Change Audit Semantic Key` 由转换槽键、审计合同版本和审计注册表组成；新候选摘要只进入审计候选载荷。

### PAG-R1-03 发布语义键绑定同一转换槽

`Projection Publication Semantic Key` 由转换槽键、登记审计解析和发布合同版本组成；候选／发布摘要只进入成员载荷。

### PAG-R1-04 同槽候选必须共同竞争

同一槽全部候选投影、候选审计、登记审计、发布尝试、成功、失败和空洞分别进入完整边界并独立证明完整。

### PAG-R1-05 审计冲突真值

同槽唯一内容身份可登记；多个内容同一候选为幂等集合；多个异投影摘要、异视图或异变化原因载荷必须 `CONFLICTED`。

### PAG-R1-06 发布冲突真值

同槽只能发布一个内容身份或内容同一幂等集合。异候选摘要、异登记审计、异视图或异闭包引用必须 `CONFLICTED`，不得先到或最后写入获胜。

### PAG-R1-07 后继必须消费登记前驱

除规范首次槽外，新转换必须固定前一发布外壳的最终登记解析。裸缓存、最大时间或最新位置不能成为前驱。

### PAG-R1-08 历史分叉永久保留

冲突槽、失败发布和未选候选永久保留。后续修复产生新槽和显式前驱关系，不覆盖冲突历史。

### PAG-R1-09 候选级关闭声明

```text
PAG-IM-B1 Transition Slot Competition Identity: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Final Model Review: REQUIRED
```

## 当前决定

```text
WS-09 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```
