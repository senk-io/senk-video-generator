# 派生记录登记治理有界修订 R1：精确提供方类型导入闭合

## 修订信息

```text
Proposal ID: CR-0010-R1
Title: Exact Provider Type Import Closure
Workstream: WS-07
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0010 DERIVED RECORD REGISTRATION GOVERNANCE
Repair Basis: CR-0010-PROVIDER-AND-CONSUMER-INTERFACE-COMPATIBILITY-REVIEW
Repair Scope: XDR-B1 + XDR-B2 only
Institution Freeze Created: NO
Runtime Authority Created: NO
```

### DRG-R1-01 类型导入元组是只读引用

```text
Derived Record Provider Type Import Tuple =
  Provider Workstream and Proposal Composite Version
+ Provider Type Contract Reference and Digest
+ Exact Candidate Record Type ID and Version
+ Exact Registered Record Type ID and Version
+ Exact Candidate Payload Schema Digest
+ Exact Registered Business Payload Schema Digest
+ Stable Registration Key Contract Digest
+ Ledger Scope Contract Digest
+ Correction / Supersession Contract Digest
+ Provider Institution Freeze Reference
+ Import Tuple Digest
```

导入不创建、重命名或修改提供方类型。

### DRG-R1-02 导入状态必须封闭

```text
REGISTERABLE_EXACT
IMPORT_PENDING
RESERVED_UNREGISTERED_TYPE_SLOT
INDETERMINATE
CONFLICTED
```

只有 `REGISTERABLE_EXACT` 可以进入类型合同候选。

### DRG-R1-03 精确导入必须内容同一

类型合同中的候选／登记类型、业务 schema、稳定键、账本、更正和取代合同必须与提供方导入元组逐字段内容同一。任何本地补字段、别名或默认值使导入 `CONFLICTED`。

### DRG-R1-04 未命名 WS-06 类型保持待导入

以下 CR-0010 本地别名立即废止：

```text
Registered Proof Applicability Record
Registered Exemption Applicability Record
Registered Completeness Evaluation Record
```

在 WS-06 没有提供精确同名合同前，其导入状态为 `IMPORT_PENDING`，不得注册。

### DRG-R1-05 既有精确消费类型可以导入

```text
CR-0003 Registered Proof Qualification Record
CR-0003 Registered Qualification Applicability Record
CR-0002 Registered Exemption Basis Applicability Resolution Record
```

仍须固定各自提供方版本和完整导入元组；名称出现本身不等于 `REGISTERABLE_EXACT`。

### DRG-R1-06 WS-04／WS-05／WS-06 新内部类型按提供方合同导入

原子资格、资格聚合、权威适用性、规则、边界、完整性和聚合记录只有在提供方明确给出候选／登记类型映射及业务载荷合同时才能导入。CR-0010 不合并其内部角色。

### DRG-R1-07 未来类型必须是未登记槽位

```text
WS-08 Dependency Closure Type Slot
WS-08 Closure Completeness Type Slot
WS-09 Projection Audit Type Slot
WS-09 Publication Input / Envelope Type Slot
```

初始状态全部为 `RESERVED_UNREGISTERED_TYPE_SLOT`。

### DRG-R1-08 保留槽位没有运行资格

保留槽位不能产生类型合同候选、类型登记解析、逐类型授权实例、登记尝试或已登记派生记录。槽位只证明未来命名空间被预留，不证明 schema 或语义。

### DRG-R1-09 槽位转为精确导入必须新建目录版本

提供方模型闭合并完成接口审查后，必须形成新的类型导入元组、类型目录版本、类型合同候选、制度冻结和登记解析；不能原地补全槽位。

### DRG-R1-10 类型导入竞争必须保留

相同提供方类型身份出现不兼容 schema、稳定键、账本或更正合同，必须进入同一导入冲突集合并为 `CONFLICTED`，不得由 CR-0010 选择赢家。

### DRG-R1-11 导入解析不能传播提供方权威

导入构造、验证和登记权威不能取得提供方类型定义、业务计算、派生记录登记、闭包或投影发布权威。

### DRG-R1-12 基础目录条款累计覆盖

`DRG-C-12` 至 `C-14` 的名称清单只作为待核对发现清单；能否登记完全由本修订的导入状态决定。`DRG-C-13` 的未来三类记录不得视为首批可登记合同。

### DRG-R1-13 候选级关闭声明

```text
XDR-B1 Provider-owned Exact Type Identity: CLOSED_AS_DRAFT
XDR-B2 Future Type Reservation Boundary: CLOSED_AS_DRAFT
Interface Re-review: REQUIRED
Independent Model Review: BLOCKED_PENDING_INTERFACE
```

## 当前决定

```text
CR-0010-R1 Status: DRAFT
Authority: NONE
Executable: NO
WS-07 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须复审提供方类型导入接口，再执行独立模型审查。
