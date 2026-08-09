# CR-0010-R4 下游类型目录后继候选

## 修订信息

```text
Proposal ID: CR-0010-R4
Proposal Type: Bounded Downstream Type Directory Successor Candidate
Status: DRAFT
Executable: NO
Workstream: WS-07
Repair Basis: CR-0013-NINE-WORKSTREAM-OVERALL-FREEZE-READINESS-REVIEW / NFR-B1
Predecessor Composite: CR-0010 + CR-0010-R1 + CR-0010-R2 + CR-0010-R3
Provider Candidates: CR-0011 composite + CR-0012 composite
Institution Freeze Created: NO
Type Registration Created: NO
Runtime Authority Created: NO
```

> 本修订只建立承接 `WS-08`、`WS-09` 精确类型合同的后继目录候选。它不把候选类型变成已登记类型，不激活保留槽，不创建制度冻结或运行时登记权威。

## 一、修订边界

### DRG-R4-01 不原地修改保留槽

`CR-0010-R1` 中的四个保留槽保持原始历史状态：

```text
RESERVED_UNREGISTERED_TYPE_SLOT
```

本修订建立新的目录后继候选；不得把旧目录中的槽位改写为已登记或可运行。

### DRG-R4-02 后继关系

```text
Predecessor Type Directory Version
  -> Candidate Successor Type Directory Version
  -> Future Frozen Type Directory Version
  -> Future Type Import Registration Resolutions
```

候选后继身份由以下字段决定：

```text
Predecessor Directory Version ID and Digest
+ Ordered Provider Import Tuple Digests
+ Directory Scope
+ Knowledge Boundary Vector K
+ Candidate Observed At
+ Candidate Recorded At
```

同一身份出现不同导入清单或不同载荷摘要时必须进入冲突集合，不得覆盖。

## 二、WS-08 精确候选导入

### DRG-R4-03 闭包类型映射

```text
Candidate Dependency Closure Record
  -> Registered Dependency Closure Record

Candidate Closure Completeness Record
  -> Registered Closure Completeness Record

Candidate Closure Rebuild Requirement
  -> Registered Closure Rebuild Requirement
```

每个导入元组必须逐项固定：

```text
Provider Proposal ID and Composite Version
Provider Candidate Type ID and Version
Provider Registered Type ID and Version
Provider Schema Contract Reference
Provider Stable Semantic Key Contract Reference
Provider Ledger Scope Contract Reference
Provider Correction and Supersession Contract Reference
Provider Candidate-construction Authority Type
Provider Registration Authority Type
Consumer Directory Slot ID
Import Tuple Payload Digest and Digest Algorithm
Provider Institution Freeze Reference
Import Registration Resolution Reference
```

当前最后两项不存在，故状态只能是：

```text
EXACT_IMPORT_CANDIDATE_PENDING_PROVIDER_FREEZE_AND_REGISTRATION
```

### DRG-R4-04 闭包消费前置条件

任何消费者只有在下列条件全部成立后才能把闭包类型视为已导入：

```text
Provider Contract Frozen
AND Successor Directory Frozen
AND Per-type Import Registration Resolution = REGISTERED_EXACT
AND Referenced Record Registration Resolution = REGISTERED_CONTENT_IDENTICAL
AND Closure Completeness Resolution = COMPLETE
```

候选目录、接口通过或名称匹配均不能替代这些事实。

## 三、WS-09 精确候选导入

### DRG-R4-05 投影治理类型映射

```text
Candidate Projection Change Audit Record
  -> Registered Projection Change Audit Record

Candidate Projection Rebuild Requirement
  -> Registered Projection Rebuild Requirement

Candidate Projection Deletion Record
  -> Registered Projection Deletion Record
```

这些映射使用与 `DRG-R4-03` 相同的完整导入元组。当前状态为：

```text
EXACT_IMPORT_CANDIDATE_PENDING_PROVIDER_FREEZE_AND_REGISTRATION
```

### DRG-R4-06 发布封套不进入派生记录类型目录

`Projection Publication Envelope` 由独立发布注册表治理，不是派生业务事实，不进入 `WS-07` 类型登记目录。旧保留槽中的发布输入／封套名称只保留历史，不得据此创建派生记录登记权威。

## 四、冲突、幂等与权威

### DRG-R4-07 内容同一与冲突

```text
Same Provider Type Identity + Same Import Tuple Digest
  -> IDEMPOTENT_CANDIDATE

Same Provider Type Identity + Different Import Tuple Digest
  -> CONFLICTED_IMPORT_CANDIDATE
```

冲突候选不能进入目录冻结或类型登记。

### DRG-R4-08 权威不传播

目录候选构造、验证或未来登记权威都不能取得：

- `WS-08` 闭包计算、完整性判定或传播权威；
- `WS-09` 投影构建、审计内容生成、发布、删除或重建权威；
- `CR-0002` 决策或 `CR-0003` 提交权威。

### DRG-R4-09 失败关闭

缺失冻结引用、缺失登记解析、导入冲突、摘要算法不匹配、稳定键或 schema 不同一时，导入状态必须保持待定或冲突；不得默认登记、默认兼容或允许受保护写入。

## 五、修复声明

```text
NFR-B1 Successor Directory Candidate: CLOSED_AS_DRAFT
WS-08 Exact Candidate Import Tuples: PRESENT
WS-09 Exact Candidate Import Tuples: PRESENT
Legacy Reserved Slots Mutated: NO
Provider Institution Freeze References: ABSENT
Type Import Registration Resolutions: ABSENT
Runtime Type Eligibility Created: NO
WS-07 Model Exit: BLOCKED_PENDING_INTERFACE_REGRESSION
```

下一阶段必须把本修订与 `CR-0011`、`CR-0012` 及 `CR-0002`、`CR-0003` 一并执行联合接口回归。回归通过也不等于类型已经冻结或登记。
