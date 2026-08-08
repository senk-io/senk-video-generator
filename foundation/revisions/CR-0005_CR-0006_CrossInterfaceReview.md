# CR-0005 / CR-0006 独立交叉接口一致性审查

## 审查信息

```text
Review ID: CR-0005-CR-0006-CROSS-INTERFACE-REVIEW
Review Type: Independent Cross-interface Consistency Review
Status: COMPLETED
Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0005 SOURCE REGISTRY INTERFACE
Reviewed Proposal: CR-0006 TEMPORAL MAPPING GOVERNANCE
Planning Basis: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Interface Baseline: CR-0004-CONSTITUTION-CANDIDATE-R1
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-checks ignored; interface ownership, keys and failure cases independently re-evaluated
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只审查 `CR-0005` 与 `CR-0006` 是否形成完整、无循环且可重放的来源—时间接口。它不修改两份被审草案，不创建来源注册表、时间注册表、制度冻结、账本或运行时权威。

## 审查命题

本轮独立回答：

1. 来源身份、边界、快照和完整性是否在时间解释之前稳定成立；
2. 时间映射是否只能消费而不能反向创建或修改来源事实；
3. 来源记录是否向时间映射提供完整且稳定的原始时间断言身份；
4. `OPEN_WORLD` 与认识边界确定性门槛是否相容；
5. `Known At`、`Knowledge Boundary Vector` 和规范时间值是否具有唯一类型关系；
6. 历史认识视图是否同时固定来源账本与时间映射账本的认识边界；
7. 来源适用性解析是否绑定内容同一的时间查询坐标；
8. 两份提案是否可以进入各自独立模型审查；
9. 当前是否产生任何冻结或运行时资格。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-CONSTITUTION-CANDIDATE
CR-0003-CONSTITUTION-CANDIDATE-R2
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0004-CONSTITUTION-CANDIDATE-R1-CONSISTENCY-REVIEW
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
CR-0005 SOURCE REGISTRY INTERFACE
CR-0006 TEMPORAL MAPPING GOVERNANCE
Local repository state at review time
```

提案自检、作者身份、文件顺序和历史讨论均不作为通过依据。

## 总体裁决

两份提案已经建立正确的主干所有权与单向依赖：

```text
Registered Source Records
  -> Registered Source Boundary and Snapshot
  -> Independent Source Completeness Records
  -> Registered Multi-registry Source Boundary Vector
  -> Temporal Mapping and Knowledge Boundary Construction
  -> Temporal Query Coordinate
  -> Source Applicability Resolution
```

时间治理不能创建、修改或删除来源记录、边界、快照与完整性；来源治理不能解释旧时间字段、构造规范时间值或自行建立认识边界。候选—登记分离、追加历史、冲突保留、权威不传播及双视图方向均兼容。

```text
Object Ownership Separation: PASS
Source-before-temporal Causality: PASS
Cross-interface Acyclicity: PASS
Authority Non-propagation: PASS
Append-only History: PASS
Conflict Preservation Direction: PASS
WS-01 Reference Direction: PASS_AS_DRAFT
```

但结构无环不等于接口已经闭合。审查发现五项有界阻断：

1. 来源记录没有向映射输入提供稳定的原始时间断言身份和摘要；
2. 时间治理把所有完整性维度一律要求为 `COMPLETE`，与开放世界成员完整性规则冲突；
3. `Known At Reference`、`Canonical Known At Value` 和 `Knowledge Boundary Vector` 之间缺少封闭类型契约；
4. 历史认识边界没有固定时间映射、更正和迁移账本自身的登记边界与完整性；
5. 时间查询坐标、认识边界视图和来源适用性解析之间缺少内容同一约束。

因此：

```text
Structural Cross-interface Compatibility: PASS
Semantic Interface Closure: FAIL_WITH_BOUNDED_BLOCKERS
Historical Reproducibility: FAIL_WITH_BOUNDED_BLOCKERS
Cross-interface Review: FAIL
CR-0005 Revision Required: YES
CR-0006 Revision Required: YES
Independent Model Review Entry: BLOCKED
WS-02 Exit: BLOCKED
WS-03 Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
```

## 一、已通过：对象所有权与无环因果

`CR-0005` 的来源边界和快照身份不依赖时间映射结果：

```text
Source Registry Boundary Key
  -/-> Temporal Mapping Result

Source Registry Snapshot Key
  -/-> Knowledge Boundary Vector
```

`CR-0006` 只能消费已登记的多注册表来源边界向量：

```text
Registered Multi-registry Source Boundary Vector
  -> Candidate Knowledge Boundary Vector
  -> Knowledge Boundary Registration Attempt
  -> Registered Knowledge Boundary Vector
```

返回的规范时间值、映射记录和认识边界引用不能反向改变来源事实。

```text
Source Object Ownership: PASS
Temporal Object Ownership: PASS
Reverse Mutation Prohibition: PASS
Identity Cycle: NONE_FOUND
```

## 二、已通过：分权、追加历史和冲突保留

两份提案分别声明逐操作权威，并禁止构造、登记、完整性、解析、更正和迁移权威隐式传播。两侧候选与登记载荷均要求内容同一；冲突记录不能按时间、优先级或置信度静默消除。

```text
Construction / Registration Separation: PASS
Completeness / Source Registration Separation: PASS
Mapping Rule / Execution / Registration Separation: PASS
Correction Append-only Boundary: PASS
Cross-registry Conflict Preservation: PASS
Temporal Mapping Conflict Preservation: PASS
```

## 三、阻断 B1：原始时间断言交接身份不完整

`CR-0005` 的 `Source Record` 只显式绑定：

```text
Observed Temporal Field Reference
Recorded Temporal Field Reference
```

它说明这些字段引用保持不透明，但没有要求共同绑定：

```text
Raw Temporal Assertion ID
Raw Temporal Assertion Digest
Raw Temporal Value or Interval Digest
Source Temporal Field ID and Version
Subject ID and Version
Assertion Evidence References
```

`CR-0006` 的 `Temporal Mapping Input Record` 却以 `Raw Temporal Assertion ID and Digest` 为必需输入。字段定义引用只能说明“这个字段是什么意思”，不能稳定标识“这一次原始断言的值和证据是什么”。

如果依赖规范载荷内部的隐式字段，实现者可能对相同来源记录抽取不同断言，或在不改变映射输入表面键的情况下改变原始值。

### 关闭条件

`CR-0005-R1` 必须为每个可映射时间断言定义稳定身份、载荷摘要、字段身份、主体、原始值形态和证据引用，并纳入来源记录及快照摘要；`CR-0006-R1` 必须只消费该已登记断言引用，不允许重新抽取未登记断言。

```text
B1 Raw Assertion Handoff: BLOCKED
```

## 四、阻断 B2：开放世界完整性与时间确定性门槛冲突

`CR-0005` 正确规定：

```text
OPEN_WORLD
  -> MEMBERSHIP_COMPLETENESS cannot be exhaustive COMPLETE
  -> exact registered members may still be readable and reproducible
```

但 `CR-0006` 的 `TM-C-23` 规定：

```text
any boundary completeness != COMPLETE
  -> no determinate Knowledge Boundary result
```

这会使任何包含开放世界注册表的认识边界永久无法形成确定结果，即使查询只要求重放精确已登记成员，并不需要证明世界中不存在其他成员。

接口必须区分：

```text
Required Completeness Dimensions for exact-known-set replay
Required Completeness Dimensions for exhaustive absence claim
Required Completeness Dimensions for query-specific scope
```

开放世界可以支持精确已知集合重放，但不能支持穷尽否定。只有查询确实要求穷尽成员资格时，`MEMBERSHIP_COMPLETENESS` 才能成为确定性前置门。

### 关闭条件

`CR-0006-R1` 必须把“一律全部完整”改为按查询目的、世界模式和精确作用域登记的必要维度集合；该集合及其规则版本必须进入认识边界条目身份。不得降低 `CR-0005` 对开放世界缺失的失败关闭要求。

```text
B2 Open-world Completeness Compatibility: BLOCKED
```

## 五、阻断 B3：认识时间类型契约未封闭

当前接口同时出现：

```text
CR-0005: Known At Reference
CR-0005: Knowledge Boundary Vector Reference
CR-0006: Canonical Known At Value
CR-0006: Knowledge Boundary Vector
```

`CR-0006` 已明确单一时间戳不能替代认识边界，但最低规范字段集合没有定义 `KNOWN_AT` 字段，且没有说明 `Canonical Known At Value` 是：

- 查询标签；
- 每注册表截点的公共上限；
- 规范时间字段值；
- 还是认识边界向量的派生显示值。

`CR-0005` 的来源适用性解析又同时使用 `Known At Reference` 和 `Knowledge Boundary Vector Reference`，没有禁止前者被实现为裸时间戳。

### 关闭条件

两份 R1 必须建立封闭类型关系：

```text
Knowledge Boundary Vector Reference
  -> required normative knowledge coordinate

Canonical Known-at Label or Upper-bound Value
  -> optional subordinate field with explicit identity
  -/-> substitute Knowledge Boundary Vector
```

如果保留 `Known At Reference`，必须明确其唯一合法目标及内容身份；如果它只是向量别名，应统一名称并删除第二种可解释路径。

```text
B3 Knowledge-time Type Closure: BLOCKED
```

## 六、阻断 B4：时间治理账本缺少自身认识边界

历史查询不仅依赖来源记录何时已知，也依赖映射、更正和迁移记录当时是否已经登记。当前认识边界固定了 `WS-02` 来源注册表向量，却没有固定：

```text
Temporal Mapping Ledger Boundary and Digest
Temporal Mapping Registration Completeness
Temporal Correction Ledger Boundary and Digest
Temporal Migration Ledger Boundary and Digest
Temporal Conflict Subdomain Boundary
```

仅用映射记录的 `RECORDED_AT <= Known At` 过滤不足以证明没有被遗漏的同键映射或冲突；“没有读到另一条映射”不能证明它当时不存在。

如果把时间映射账本未经分层地塞回其输入来源向量，又会形成：

```text
Source Vector
  -> Mapping Record
  -> same Source Vector identity
```

因此必须显式建立阶段边界，而不能靠实现约定消除循环。

### 关闭条件

`CR-0006-R1` 必须定义时间派生账本的稳定登记边界、快照或等价不可变截点、独立必要完整性和冲突子域；认识边界构造必须采用无环阶段：

```text
Registered Base Source Vector
  -> Registered Temporal Mapping / Correction Boundary
  -> Registered Knowledge Boundary Vector
```

后续时间记录只能形成新的时间账本边界和新的认识边界，不能改变旧向量。

```text
B4 Temporal-ledger Historical Boundary: BLOCKED
```

## 七、阻断 B5：查询坐标与来源适用性缺少内容同一

`CR-0006` 的 `Knowledge Boundary Vector` 已包含 `Temporal View Mode`，而 `Temporal Query Coordinate` 又单独包含同一视图。当前没有要求二者必须相等。

`CR-0005` 的 `Source Applicability Resolution Key` 分别绑定：

```text
Valid At Reference
Known At Reference
View Mode Reference
```

但最小输出接口改为：

```text
Applicability Valid At Reference
Knowledge Boundary Vector Reference
```

它没有要求引用完整的 `Temporal Query Coordinate ID and Digest`，也没有声明分散字段必须与一个已登记查询坐标内容同一。这允许混合：

```text
Valid At from coordinate A
Knowledge Boundary from coordinate B
View Mode from coordinate C
```

从而产生任何单一合法时间查询都无法重放的来源适用性结果。

### 关闭条件

两份 R1 必须选择一个唯一规范接口：来源适用性解析绑定已登记 `Temporal Query Coordinate ID and Digest`；如果保留展开字段，它们必须与该坐标内容同一，并明确：

```text
Query View Mode = Knowledge Boundary View Mode
Query Valid At = Applicability Valid At
Query Knowledge Boundary = Applicability Knowledge Boundary
```

同键不兼容坐标或载荷必须 `CONFLICTED`，未知或未登记坐标必须 `INDETERMINATE`。

```text
B5 Coordinate Content Identity: BLOCKED
```

## 八、反例验证

### 反例一：同字段引用、不同原始值

两个来源记录拥有相同 `Recorded Temporal Field Reference`，但规范载荷中的原始值不同。由于没有已登记断言身份，映射输入可能在不改变显式交接字段的情况下变化。

```text
Expected: distinct registered Raw Temporal Assertion identities
Current: interface identity incomplete
Result: B1 reproduced
```

### 反例二：开放世界精确快照

一个 `OPEN_WORLD` 注册表的载体、位置、读取和冲突子域均完整，查询只重放精确快照成员。成员穷尽仍按规则不能为 `COMPLETE`，时间治理因“任一维度非完整”拒绝确定认识边界。

```text
Expected: determinate exact-known-set boundary without qualified absence
Current: forced indeterminate
Result: B2 reproduced
```

### 反例三：裸 Known At 替代向量

来源适用性解析把 `Known At Reference` 实现为单一时间戳，同时输出另一个认识向量引用。两者不一致时没有类型或同一规则决定失败值。

```text
Expected: one normative Knowledge Boundary identity
Current: two independently interpretable paths
Result: B3 reproduced
```

### 反例四：迟到发现的旧映射冲突

历史查询第一次只读取映射 A，后来发现同键映射 B 在当时已经登记。没有时间映射账本边界和完整性记录时，旧查询无法证明它当时读取了完整映射集合。

```text
Expected: immutable temporal-ledger boundary reveals omission or conflict
Current: historical completeness not reproducible
Result: B4 reproduced
```

### 反例五：混合时间坐标

解析使用坐标 A 的有效时间、坐标 B 的认识边界和坐标 C 的视图模式。所有引用分别存在，但组合从未作为一个查询坐标登记。

```text
Expected: INDETERMINATE or CONFLICTED
Current: no mandatory content-identity check
Result: B5 reproduced
```

## 九、修订边界

下一阶段只能建立有界修订：

```text
CR-0005-R1
  -> close B1, B3 and B5 provider/consumer fields

CR-0006-R1
  -> close B1, B2, B3, B4 and B5 temporal contracts
```

允许修改：

- 原始时间断言对象、来源记录交接字段与快照摘要覆盖；
- 查询所需完整性维度集合及开放世界分支；
- 认识时间类型、向量条目和可选显示时间值；
- 时间映射、更正、迁移账本的无环历史边界；
- 时间查询坐标与来源适用性解析的内容同一字段；
- 相应非法状态、自检、状态和谱系说明。

不得修改：

- `CR-0005` 的来源身份、位置、边界、快照和完整性所有权；
- `CR-0006` 的规范时间字段分离及双视图原则；
- 两侧候选—登记分离、追加历史和冲突优先规则；
- `CR-0004-R1` 已通过的 `WS-01` 模型；
- 历史草案或本审查记录；
- 任何制度冻结、注册表实例或运行时权威。

## 十、退出门复核

```text
Cross-interface Structure: PASS
Cross-interface Acyclicity: PASS
Raw Temporal Assertion Handoff: FAIL
Open-world Completeness Compatibility: FAIL
Knowledge-time Type Closure: FAIL
Temporal-ledger Historical Boundary: FAIL
Coordinate Content Identity: FAIL
CR-0005 Independent Model Review Entry: BLOCKED
CR-0006 Independent Model Review Entry: BLOCKED
WS-02 Model Exit: BLOCKED
WS-03 Model Exit: BLOCKED
Institution Freeze Readiness: NOT_ESTABLISHED
```

## 当前决定

```text
CR-0005 / CR-0006 Cross-interface Review: COMPLETED
Review Result: PASS_WITH_FIVE_BOUNDED_BLOCKERS
Bounded Blockers: B1 + B2 + B3 + B4 + B5
CR-0005-R1 Required: YES
CR-0006-R1 Required: YES
Independent Model Reviews: NOT_STARTED
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Temporal Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段应建立 `CR-0005-R1` 与 `CR-0006-R1`，只关闭上述五项阻断；随后先复审交叉接口，再分别执行独立模型审查。
