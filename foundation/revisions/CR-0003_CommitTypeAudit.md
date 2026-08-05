# 提交边界类型审计

## 审计信息

```text
Review ID: CR-0003-TYPE-AUDIT
Review Type: Object / Process / Record Boundary Audit
Status: COMPLETED
Result: PASS_WITH_CONSTRAINTS
Executable: NO
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: 3ca24e43-5b46-473a-b6f3-6d63de3fb0a6
Reviews: Commit as a proposed Foundation Object
Depends On: CR-0002-R1 Decision Model
```

> 本文件是类型审计记录，不是冻结制度。它只确定 `Commit` 的建模边界，不能授权运行时提交或改变任何正式事实。

## 审计问题

本轮只回答以下问题：

1. `Commit` 是对象、过程、角色、记录、结果还是技术事务？
2. `Decision Fact` 是否属于 `Formal Institutional Fact`？
3. 谁拥有提交规则、提交记录和目标正式事实？
4. 提交能否在不产生第二次裁决的情况下建立目标正式事实？
5. 失败、不确定和部分提交如何保存历史而不污染目标事实？

## 总体结论

`Commit` 适合进入基础层成为独立模型，但不适合被压缩成单一“基础对象”。

```text
Commit Model = Foundation Model
Commit = Governed Process
Committer = Execution Role
Commit Contract = Value Object owned by Target Governing Institution
Commit Attempt = Governed Runtime Process Instance
Commit Record = Immutable Runtime Record
Commit Result = Value
Transaction = Implementation Mechanism
```

原因是：基础层需要定义“治理裁决何时可以合法投影为目标正式状态”的跨领域不变量；实际提交行为仍是一次受权威约束的运行时过程。把模型所在层级与其中每个节点的对象类型混为一谈，会让 `Commit` 同时承担规则、执行和事实三种职责。

## 类型裁决

| 节点 | 类型 | 唯一目的 | 结论 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义正式状态投影的不变量 | `PASS` |
| `Commit Contract` | 值对象 | 声明一次目标迁移允许采用的提交语义 | `PASS` |
| `Committer` | 执行角色 | 执行提交协议 | `PASS` |
| `Commit Attempt` | 受治理的运行时过程实例 | 尝试原子建立声明的目标写集 | `PASS` |
| `Commit Record` | 不可变运行时记录 | 保存一次提交尝试及其结果 | `PASS` |
| `Commit Result` | 值 | 表达 `COMMITTED`、`ABORTED` 或 `INDETERMINATE` | `PASS` |
| `Commit Evidence` | 证据引用集合 | 支持提交行为、前置检查和结果 | `PASS` |
| `Transaction` | 技术实现机制 | 提供隔离、原子性或持久化能力 | `PASS`，但不得成为制度事实来源 |
| `Commit` 单一基础对象 | 混合类型 | 同时承担规则、过程、记录和结果 | `FAIL` |

## 正式事实分类

`Decision Fact` 是正式制度事实，不是等待提交后才取得资格的候选记录。

```text
Formal Institutional Fact
  -> Governance Fact
       -> Decision Fact
       -> Authority Grant Fact
       -> Institution Freeze Fact
  -> Domain Fact
       -> Asset Selection Fact
       -> Timeline Publication Fact
       -> Domain Lifecycle Fact
```

分类依据是事实描述的对象，不是事实合法性的等级。两类事实都必须满足当时适用的权威、决策和证据要求。

`Institution Proposal` 本身是提案对象，不应直接列为治理事实；“提案已提交”“提案已批准”才是治理事实。对象存在与关于对象已经发生的正式状态不能互相替代。

## 提交的唯一职责

提交只回答一个问题：

> 一项已经成立且仍适用的决策事实，是否在满足目标制度前置条件后，被完整、唯一且可审计地投影成了声明的目标正式状态？

提交不得：

- 创建、修改或取代决策事实；
- 补充缺失的权威、依据或证据；
- 解释为什么应当作出某项裁决；
- 改写目标制度的迁移前置条件；
- 把技术写入成功直接等同于制度提交成功；
- 用补偿删除已经发生的历史。

## 所有权拆分

不存在一个同时拥有全部提交语义的单一注册表。

| 内容 | 唯一逻辑所有者 |
|---|---|
| 提交不变量 | 冻结制度 |
| 具体迁移的 `Commit Contract` | 目标类型治理制度 |
| `Commit Record` | 提交账本 |
| 目标正式事实及当前状态 | 目标对象注册表 |
| 提交证据 | 证据账本 |
| 决策事实 | 决策账本 |

这是职责分离，不是多重真源。每一类事实仍只有一个逻辑所有者。

## 权威边界

提交者不因能够写入目标注册表而获得裁决权。

```text
Decision Authority
  -> establishes Decision Fact

Commit Execution Authority
  -> permits Committer to attempt declared write set

Target Registry Authority
  -> owns authoritative target state
```

每次提交尝试必须引用一个适用的主要提交执行授权。该授权只允许执行已经由目标制度和决策事实限定的迁移，不能扩大裁决内容或改变目标写集。

## 提交与技术事务

```text
Commit != Database Commit
Commit != File Write
Commit != API Success
Commit != Event Published
```

技术事务可以实现提交所需的原子性和隔离性，但不能独自证明制度提交成立。制度提交还必须证明：

- 输入决策事实存在且在提交时仍适用；
- 目标对象和预期源版本唯一；
- 迁移前置条件在提交点成立；
- 写集完整且没有越界字段；
- 提交结果已经进入目标权威注册表；
- 提交记录和证据可以重新定位。

## 原子性与多个正式事实

一个提交可以建立多个目标正式事实，但必须同时满足：

- 它们属于同一个声明写集；
- 它们受同一个原子提交边界保护；
- 每个事实都有明确的目标逻辑所有者；
- 所有适用决策和组合前置条件已经齐备；
- 任何一项不能提交时，整个写集都不得宣称 `COMMITTED`。

如果基础设施不能证明跨注册表原子性，就不得把多个本地事务包装成一个全局原子提交。此时必须拆成多个提交，并由独立的组合流程记录中间状态、失败和后续恢复。

```text
Atomicity not provable
  -> Multiple Commit Records
  -> Explicit Composite Progress
  -> No Global COMMITTED Claim
```

## 失败与不确定

提交结果只允许：

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：声明写集已经完整成为目标权威状态；
- `ABORTED`：目标权威状态没有发生本次声明迁移；
- `INDETERMINATE`：当前证据无法证明已提交或未提交，必须失败关闭并进入确定性对账。

`FAILED` 不作为基础结果，因为它无法区分“已确认没有写入”和“结果未知”。

提交失败或不确定不会撤销、覆盖或降级原 `Decision Fact`。它只意味着该决策尚未成功投影为本次目标状态。

## 幂等与并发

每次提交必须具有稳定的提交键，并至少绑定：

```text
Decision Fact ID
Target Object ID
Expected Source Version
Requested Transition Type
Declared Write Set
Commit Contract Version
```

相同提交键的重放不得产生第二次状态迁移。源版本冲突必须 `ABORTED` 或 `INDETERMINATE`，不得静默覆盖较新的目标状态。

## 历史边界

- 每次尝试都产生新的不可变 `Commit Record`；
- 重试必须引用先前尝试，不能覆盖先前结果；
- 补偿是新的受治理迁移，不是删除旧提交；
- 对账可以追加结果确认记录，不能改写原始观察与证据；
- 目标当前状态可以改变，曾经发生的提交历史不能消失。

## 非递归检查

提交不需要另一项决策来“批准这次提交动作”，前提是：

1. 目标迁移已经由适用 `Decision Fact` 授权；
2. `Committer` 具有提交执行权威；
3. 提交只执行确定性的冻结契约；
4. 提交不扩张裁决语义。

若提交过程中出现新的价值判断、范围选择或冲突裁决，必须停止提交并请求新的决策，不能把判断藏在提交器内部。

## 最终审计结论

```text
Foundation Relevance: PASS
Single Object Classification: FAIL
Model-level Separation: PASS
Decision Independence: PASS
Execution Separation: PASS
Formal Fact Classification: PASS_WITH_CLARIFICATION
Authority Separation: PASS_WITH_CONSTRAINTS
History Preservation: PASS
Cross-domain Portability: PASS
Drafting Readiness: PASS
```

建议动作：建立独立的 `CR-0003 Commit Model` 草案；草案必须采用“基础层制度模型 + 运行时提交过程 + 不可变提交记录”的结构，不得把 `Commit` 写成同时拥有权威、决策、执行和目标事实的万能对象。
