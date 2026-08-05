# 第一原则

## 制度冻结信息

```text
Freeze ID: IF-0001
Constitution: AI Native Engineering Constitution
Chapter: Authority Model
Status: FROZEN
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: b86a4839-ae44-4ea0-b71c-7e597e09c8f1
```

本章定义 AI 原生工程中的权威模型。这里的“权威”不是执行能力，而是改变正式现实的合法资格。

> 现实定义世界是什么；权威定义谁有资格改变世界。

本章中的“必须”“不得”和“只能”均为规范性要求。下层治理、执行、验证、领域和知识文档不得与本章冲突。

## A-01 权威先于执行

> 任何执行，都必须存在对应的权威。

AI 可以拥有执行能力，但不天然拥有改变正式事实的权力。生成、选择、批准、拒绝、发布、归档和覆盖都属于需要授权的行为。

以下状态非法：

```text
AI 生成
  -> 自动采用
```

原因是：

```text
Generation Authority != Selection Authority
```

任何正式事实必须具有完整的成立链：

```text
Authority
  -> Decision
  -> Evidence
  -> Formal Fact
```

缺少权威、决策或证据中的任意一项，结果都不得成为正式事实。

## A-02 权威不得隐式传播

权威必须逐层、显式授予，不能继承、猜测或因上游权限自动获得。

```text
Brief Authority
  != Script Authority
  != Shot Authority
  != Selection Authority
  != Publication Authority
```

拥有提示词处理权，不代表拥有叙事修改权；拥有脚本修改权，不代表拥有镜头批准权。

每项授权必须明确建立和结束。超出授权范围的行为不得通过“任务需要继续”获得合法性。

## A-03 每项权威必须具有显式边界

每个权威主体必须同时声明：

```text
Can Change
Cannot Change
```

最低边界如下：

| 主体 | 可以改变 | 不得改变 |
|---|---|---|
| Prompt Compiler | 提示词、提供者格式、提示语法 | 镜头意图、叙事、预期 |
| Generator | 生成候选项 | 批准候选项、删除候选项、修改预期 |
| Verifier | 比较、测量、报告偏差 | 修复、重试、降低标准 |
| Diagnosis Engine | 解释失败原因 | 改写验证事实 |
| Policy Engine | 重试、升级、替换提供者、请求人工 | 修改观察、验证或证据 |
| Timeline Composer | 绑定已接受资产 | 绑定候选资产、创建接受事实 |
| Publisher | 发布已验证时间线 | 发布未验证时间线 |

任何新增 Agent、组件或人工角色，在获得执行资格前都必须补充同样的边界声明。

## A-04 权威拥有完整生命周期

权威不仅拥有一次决策，还拥有该决策领域内允许发生的生命周期。

选择权威负责：

```text
Candidate
  -> Selected
  -> Rejected
  -> Revoked
```

时间线权威负责：

```text
Draft
  -> Assembled
  -> Verified
  -> Frozen
```

状态不得跨越。任何迁移必须由负责该生命周期的权威作出，并保留决策和证据。

一个权威不得借用其他权威的状态迁移来扩大自身权限。

## A-05 权威拥有不变量

每项权威必须声明其持续成立的不变量。

最低不变量包括：

```text
Selection Invariant:
One Candidate -> One Selection Decision

Timeline Invariant:
Only Accepted Asset

Publication Invariant:
Only Verified Timeline
```

任何不变量被破坏时，系统必须立即失败关闭。不得通过补写历史、降低标准或默认推断让非法状态继续流动。

## A-06 权威不得验证自己

> 任何权威都不能为自己的行为提供最终有效性证明。

生成者不能宣称自己的结果合格；选择者不能仅凭自身选择证明选择正确；策略引擎不能修改验证结论来证明自身策略有效。

验证必须来自独立权威。若执行者与验证者由同一模型或同一 Agent 承担，仍必须使用不同的任务契约、输入边界、证据记录和裁决身份，不能把一次自我反思冒充独立验证。

没有独立验证，系统只有自证，不构成工程验收。

## A-07 权威迁移产生历史

历史来自正式的权威状态迁移，而不是来自文件存在、时间线出现或最终导出。

```text
Candidate
  -> Selected
```

只有选择权威作出的正式迁移，才能产生“候选项曾被选择”的历史事实。

时间线和导出物可以投影历史，但不能创造或反推历史。

每次权威迁移必须至少记录：

- 迁移前状态；
- 迁移后状态；
- 权威主体；
- 决策对象及版本；
- 决策依据；
- 证据；
- 发生时间。

## A-08 历史承诺后的权威事实不可变

权威一旦作出正式裁决，该裁决就成为历史承诺，不得覆盖、删除或静默替换。

后续变化只能追加新的状态：

```text
Revoked
Superseded
Deprecated
```

新裁决必须引用被撤销、取代或弃用的旧裁决，并说明原因。当前状态可以改变，历史事实不能消失。

## 非法状态总表

以下情况一律非法：

- 没有授权的执行改变正式事实；
- 上游权威自动继承下游权威；
- Agent 超出 `Can Change` 边界；
- 生命周期跨越中间状态；
- 不变量破坏后继续执行；
- 执行者自行完成最终验证；
- 根据时间线或导出物反推选择合法；
- 覆盖、删除或静默替换历史裁决。

发现非法状态时，系统必须失败关闭并保存证据。

## 体系主轴

AI Native Engineering 的顺序不是“先让 AI 执行，再补制度”，而是：

```text
Reality
  -> Authority
  -> Execution
  -> Verification
  -> Diagnosis
  -> Policy
  -> Knowledge
```

首先确认现实，其次确认谁有资格改变现实，然后才允许执行。执行结果必须经过独立验证，偏差进入诊断，诊断驱动策略，经过重复证据支持的模式才可能进入知识。

预期的资格、分类、冻结和成功定义已由 `IF-0002` 建立，见 [`../execution/Expectation.md`](../execution/Expectation.md)。

偏差作为一等事实的语义及其合法演化路径已由 `IF-0003` 建立，见 [`../execution/Gap.md`](../execution/Gap.md)。

诊断作为对偏差的受治理解释，其证据、不确定性、版本和因果边界已由 `IF-0004` 建立，见 [`../execution/Diagnosis.md`](../execution/Diagnosis.md)。

策略作为未来执行的唯一合法控制者，其行动空间、选择、授权、预算和责任边界已由 `IF-0005` 建立，见 [`../execution/Policy.md`](../execution/Policy.md)。

证据作为正式事实的信任根，其不可变性、版本绑定、充分性和审计边界已由 `IF-0006` 建立，见 [`05_Evidence.md`](./05_Evidence.md)。

制度的资格、审查、冻结、演化和最高治理边界已由 `IF-0007` 建立，见 [`06_Institution.md`](./06_Institution.md)。
