# 来源注册表接口有界修订 R1

## 修订信息

```text
Proposal ID: CR-0005-R1
Title: Raw Temporal Assertion and Coordinate Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005 SOURCE REGISTRY INTERFACE
Repair Basis: CR-0005-CR-0006-CROSS-INTERFACE-REVIEW
Repair Scope: B1 + B3 + B5 provider-side fields only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Parallel Revision Target: CR-0006-R1
Cross-interface Re-review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复交叉接口审查中分配给来源侧的 B1、B3 和 B5。它不覆盖 `CR-0005` 或审查记录的历史文本，不创建实际来源记录、注册表、时间坐标、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R1-01 R1 只覆盖三个来源侧接口阻断

本修订只覆盖 `CR-0005` 的 `SR-C-04`、`SR-C-11`、`SR-C-19`、`SR-C-29`、`SR-C-30`、`SR-C-39`、`SR-C-40`、`SR-C-42`、`SR-C-43` 及相应自检和当前状态中与下列事项冲突的部分：

```text
B1 Registered Raw Temporal Assertion Handoff
B3 Knowledge-time Reference Type Closure
B5 Temporal Query Coordinate Content Identity
```

未被本修订显式覆盖的 `CR-0005` 规则继续作为合并候选语义。`CR-0006-R1` 负责 B2、B4 以及 B1、B3、B5 的时间侧契约。

### SR-R1-02 R1 不改变来源与时间的所有权边界

`WS-02` 只登记来源提供方给出的原始时间断言及其载荷，不解释断言，不生成规范时间值，不选择映射规则，也不构造认识边界或时间查询坐标。

```text
Registered Raw Temporal Assertion
  -> source fact owned by WS-02
  -> may be consumed by WS-03
  -/-> Canonical Temporal Value
```

## 二、B1：原始时间断言的稳定交接

### SR-R1-03 原始时间断言必须成为显式来源子对象

向 `CR-0005` 的来源对象表新增：

| 对象 | 类型 | 唯一目的 | 逻辑真源 |
|---|---|---|---|
| `Raw Temporal Assertion` | 不可变来源子记录 | 保存来源提供方给出的一个原始时间值或区间及其字段身份 | 来源记录登记边界 |

原始断言可以是原生规范时间声明，也可以是尚未映射的旧字段声明。对象存在只证明来源提供方登记了该断言，不证明其语义正确、可映射或适用于任何查询。

### SR-R1-04 每个原始时间断言必须拥有稳定身份和载荷

```text
Raw Temporal Assertion Key =
  Source Registry ID and Version
+ Source Registry Domain
+ Preallocated Source Record ID
+ Assertion Local ID
+ Source Temporal Field ID and Version
+ Subject ID and Version
```

断言载荷至少绑定：

```text
Raw Temporal Assertion ID
Raw Temporal Assertion Key
Raw Value Shape
Raw Value or Interval
Raw Value Digest
Declared Clock Scale and Timezone, when present
Declared Precision and Uncertainty, when present
Origin Reference
Assertion Evidence References
Candidate Assertion Payload Digest
Registered Assertion Payload Digest
```

`Raw Temporal Assertion ID` 必须由其分配权威与一个 `Raw Temporal Assertion Key` 一对一绑定；标识不得复用，也不能通过改变父记录、字段、主体或局部标识继续沿用。

```text
Raw Temporal Assertion Identity Allocation Authority Type
Raw Temporal Assertion Construction Authority Type
```

断言身份分配者、断言构造者与父来源记录登记者不得互相继承权威。断言随父记录登记只能由授权实例同时允许 `Source Record` 和 `Raw Temporal Assertion` 输出的 `Source Record Registration Authority Type` 执行；缺少任一精确输出授权时必须失败关闭。

字段身份、主体、原始值、区间边界、精度、不确定性、来源或证据变化必须形成不同载荷。同键不同载荷必须 `CONFLICTED`，不得按记录顺序选赢家。

### SR-R1-05 原始断言必须与来源记录原子登记

```text
Candidate Source Record
+ Candidate Raw Temporal Assertions
  -> Source Record Registration Attempt
  -> Registered Source Record
   + Registered Raw Temporal Assertions
```

`Preallocated Source Record ID` 只为候选及其子断言提供稳定父身份，不证明登记成功。只有来源记录登记尝试把父记录和全部声明子断言内容同一写入时，断言才成为已登记来源事实。

```text
Candidate Assertion Payload Digest
= Registered Assertion Payload Digest
```

断言不得脱离父来源记录单独变为已登记状态；部分写入、父子摘要不一致或同一局部标识对应多个载荷必须失败关闭并保留尝试历史。

### SR-R1-06 来源记录接口必须显式列出断言集合

以本规则覆盖 `SR-C-11` 中仅提供字段引用的时间交接部分。候选和已登记来源记录必须共同绑定：

```text
Registered Raw Temporal Assertion IDs and Payload Digests
Raw Temporal Assertion Set Digest
Observed Temporal Assertion Reference, when present
Recorded Temporal Assertion Reference, when present
Other Typed Temporal Assertion References, when present
```

`Observed Temporal Field Reference` 和 `Recorded Temporal Field Reference` 只能作为断言内部字段定义引用，不能替代断言身份、原始值摘要或证据引用。

### SR-R1-07 边界与快照摘要必须覆盖原始断言

任何来源边界或快照包含一个来源记录时，其规范摘要必须同时覆盖该记录的：

```text
Raw Temporal Assertion Set Digest
Ordered Raw Temporal Assertion IDs and Payload Digests
Parent-child Binding Digest
Temporal Assertion Conflict References
```

未纳入摘要的断言不能被声明位于该边界内。旧断言只能通过新的来源记录、适用性变化或允许的非语义更正追加演进，不能原地替换。

### SR-R1-08 时间映射只能消费已登记断言引用

```text
Registered Source Record
+ Registered Raw Temporal Assertion ID and Payload Digest
+ Registered Source Boundary and Snapshot
  -> eligible WS-03 mapping input
```

`WS-03` 不得从规范载荷、文本、文件元数据或未登记字段重新抽取另一条时间断言。不存在已登记断言引用时只能产生 `INDETERMINATE` 或合格 `NOT_MAPPABLE`，不能推断默认时间值。

## 三、B3：认识时间引用类型封闭

### SR-R1-09 来源侧唯一规范认识坐标是认识边界向量

在所有来源适用性和消费接口中：

```text
Known At Reference
  := Registered Knowledge Boundary Vector ID and Digest
```

该名称只是兼容别名，不是第二种对象类型。裸时间戳、规范时间标签、每注册表截点、系统当前时间或显示字段都不能成为独立 `Known At Reference`，也不能替代认识边界向量。

如果接口展开显示 `Known At` 标签，它必须是认识边界向量的非规范派生字段；标签变化不能改变向量身份，标签也不能证明来源集合完整。

### SR-R1-10 来源适用性必须消费已登记时间查询坐标

以本规则覆盖 `SR-C-29` 的分散时间字段键。修订后的稳定键为：

```text
Source Applicability Resolution Key =
  Source Identity and Version
+ Exact Registered Change Set Digest
+ Source Lifecycle Boundary ID and Digest
+ Registered Boundary Completeness Record IDs and Digests
+ Registered Temporal Query Coordinate ID and Digest
+ Applicability Rule Version
```

已登记时间查询坐标必须提供：

```text
Canonical Valid At Value ID and Digest
Registered Knowledge Boundary Vector ID and Digest
Temporal View Mode inherited from the Knowledge Boundary
Temporal Query Rule Version
```

来源适用性解析不能自行构造、修正或拼接这些字段。

## 四、B5：查询坐标内容同一

### SR-R1-11 分散时间字段只能作为坐标的内容同一展开

如果来源适用性记录为了审计而重复保存展开字段，必须满足：

```text
Applicability Valid At
= Temporal Query Coordinate.Valid At

Applicability Knowledge Boundary
= Temporal Query Coordinate.Knowledge Boundary

Applicability View Mode
= Temporal Query Coordinate.Knowledge Boundary.View Mode
```

展开字段不参与创建第二套坐标。任一不相等、引用未登记或摘要不匹配时，不得产生确定适用性结果。

### SR-R1-12 最小消费接口必须携带完整坐标身份

以本规则覆盖 `SR-C-30` 的时间字段部分。`Source Applicability Input` 至少绑定：

```text
Source Identity and Version
Applicability Result
Registered Temporal Query Coordinate ID and Digest
Canonical Valid At Value ID and Digest
Registered Knowledge Boundary Vector ID and Digest
Temporal View Mode
Source Registry Snapshot References
Source Boundary Completeness References
Source Applicability and Correction Record References
Applicability Rule Version
Registered Resolution ID and Digest
Evidence References
```

展开的有效时间、认识边界和视图必须与已登记查询坐标内容同一。下游只能消费，不能通过修改展开字段重新解释来源适用性。

### SR-R1-13 坐标异常必须进入封闭失败结果

```text
Registered content-identical coordinate and complete required inputs
  -> may support APPLICABLE or INAPPLICABLE

Missing, unregistered or non-identical coordinate
  -> INDETERMINATE

Same resolution key with incompatible coordinate or payload
  -> CONFLICTED
```

合格 `INAPPLICABLE` 仍必须来自精确撤销、退役、替代或暂停证据；坐标缺失、映射失败、视图不一致或摘要错误不能产生 `INAPPLICABLE`。

### SR-R1-14 时间治理返回值必须被整体消费

以本规则收紧 `SR-C-39`、`SR-C-40` 和 `SR-C-42`：

```text
Registered Temporal Query Coordinate
  = Canonical Valid At Value Reference
  + Registered Knowledge Boundary Vector Reference
  + inherited Temporal View Mode
  + Query Rule Version
  + Coordinate Digest
```

来源适用性只能引用整体坐标；规范时间值、映射记录或显示标签可以作为证据展开，但不能绕过坐标登记链。时间治理仍不得修改来源记录、断言、边界、快照或完整性。

## 五、非法状态与闭合声明

### SR-R1-15 新增非法状态必须失败关闭

- 字段定义引用替代原始时间断言身份；
- 从已登记来源载荷重新抽取未登记时间断言；
- 原始断言未进入来源记录或快照摘要即被映射；
- 父来源记录失败而子断言被标记为已登记；
- 裸时间戳或显示标签被当作 `Known At Reference`；
- 分散有效时间、认识边界和视图字段来自不同查询坐标；
- 未登记查询坐标产生确定来源适用性；
- 下游修改坐标展开字段重新解释已登记解析。

### SR-R1-16 本修订只声明候选级阻断关闭

```text
B1 Provider-side Raw Assertion Identity: CLOSED_AS_DRAFT
B3 Provider-side Knowledge-time Type: CLOSED_AS_DRAFT
B5 Provider-side Coordinate Identity: CLOSED_AS_DRAFT
Source / Temporal Ownership Regression: NONE_FOUND
Cross-interface Re-review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R1 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: B1 + B3 + B5 provider-side only
Cross-interface Re-review with CR-0006-R1: REQUIRED
Independent Model Review: BLOCKED_PENDING_CROSS_REVIEW
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须与 `CR-0006-R1` 一起接受交叉接口复审。自检和文件存在不能作为阻断已关闭或工作流退出的独立证明。
