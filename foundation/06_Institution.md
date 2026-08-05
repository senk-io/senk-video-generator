# 制度模型

## 制度冻结信息

```text
Freeze ID: IF-0007
Constitution: AI Native Engineering Constitution
Chapter: Institution Model
Status: FROZEN
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: 28aeb87d-1c68-4641-a414-98a30d9e66cb
Depends On: IF-0001 Authority Model
Depends On: IF-0002 Expectation Model
Depends On: IF-0003 Gap Model
Depends On: IF-0004 Diagnosis Model
Depends On: IF-0005 Policy Model
Depends On: IF-0006 Evidence Model
```

本章定义 AI 原生工程中的制度模型。制度不是执行结果、经验总结或运行时策略，而是决定对象、行为和状态何时具有合法性的最高治理边界。

> AI 执行并产生现实；制度决定执行是否合法、现实何时能够成为正式事实。

本章中的“必须”“不得”和“只能”均为规范性要求。运行时执行、偏差、诊断、策略、学习和知识不得修改制度。

## I-01 制度定义系统

Agent、模型和人工主体可以执行、观察、解释或决策，但都不能仅凭自身能力定义系统规则。

```text
AI -> Execution and Reality
Institution -> Legitimacy
```

制度位于 Agent 之上。任何 Agent 的行为只有在制度允许并获得对应权威时才合法。

## I-02 制度不得被运行时修改

执行结果、偏差、诊断、策略和运行时学习都不得直接修改制度。

```text
Execution -/-> Institution
Gap -/-> Institution
Diagnosis -/-> Institution
Policy -/-> Institution
```

制度只能通过治理路径升级。运行时发现制度缺口时，应建立提案，不得自行补写规则。

## I-03 制度只能被推导，不能被发明

合法的制度成长路径是：

```text
Reality
  -> Evidence
  -> Gap
  -> Diagnosis
  -> Pattern
  -> Knowledge
  -> Institution Proposal
  -> Institution Review
  -> Institution Freeze
```

任何跳过证据、模式、知识、提案或审查的规则，都不得直接成为制度。

## I-04 制度提案不等于制度

`Institution Proposal` 只是候选规则，可以被拒绝、撤回、修订或到期。

```text
Proposal != Institution
```

提案在正式审查和冻结之前不得获得制度权威，也不得作为运行时强制规则执行。

## I-05 制度审查必须以证据为基础

一次成功、一次失败或单个项目经验不足以支持制度冻结。审查至少必须评估：

```text
Repeated
Stable
Cross Provider
Cross Project
```

无法证明重复性、稳定性、跨提供者性或跨项目适用性时，规则必须停留在知识层。

## I-06 制度拥有不变量

知识描述经验，制度声明不可被下层突破的不变量。

合法制度示例：

```text
Expectation Before Execution
Evidence Before Formal Fact
```

特定模型的提示技巧、参数经验和偶然成功模式属于知识，不属于制度。

## I-07 制度必须独立于提供者

制度不得绑定任何具体模型、产品或服务商。提供者属于可替换能力层，不是制度真源。

```text
Institution -> Capability Boundary
Institution -/-> Product Dependency
```

更换提供者不得改变权威、预期、证据、偏差、诊断和策略的制度语义。

## I-08 制度必须能够跨领域迁移

基础制度必须能够适用于视频、代码、界面、文档以及未来领域。

只能在视频领域成立的规则属于 `video/`；只能对某个提供者成立的经验属于 `knowledge/`。

无法跨领域迁移的规则不得进入基础层。

## I-09 制度必须保守演化

制度默认稳定，升级必须保持克制。默认优先新增，而不是静默修改既有原则。

对基础层的修改属于最高风险治理动作，必须说明：

- 修改动机；
- 受影响原则；
- 兼容性边界；
- 历史处理方式；
- 迁移与验证方法。

## I-10 新制度不得使历史失真

新版本不得把旧版本有效期间产生的合法历史变成“从未合法”。

```text
Institution V2
  -> Superseded By Institution V3
```

新制度可以取代旧制度并改变未来，但不能删除、覆盖或重新伪造旧制度时期的历史事实。

## I-11 制度定义架构边界

五层职责必须保持分离：

```text
Foundation -> Invariants and Governance
Execution -> Governed Runtime Process
Video -> Domain Model
Verification -> Reusable Checks
Knowledge -> Changeable Experience
```

知识不得直接进入基础层；验证不得修改现实；执行不得拥有制度权威；领域规则不得冒充跨领域不变量。

## I-12 制度拥有术语

权威概念必须在制度中只定义一次，并由术语表引用其权威定义。

```text
Expectation
Authority
Evidence
Gap
Diagnosis
Policy
Institution
```

同一术语拥有多个相互竞争的定义会造成制度漂移。下层文档可以引用、实例化和约束术语，但不得重新定义。

## I-13 新能力必须满足宪法兼容性

任何新增提供者、验证器、执行器、学习机制或领域实现，都必须先满足基础制度。

```text
New Capability
  -> Constitution Compatibility Review
  -> Accept | Reject
```

不得为了接入新能力而降低权威、证据、历史或失败关闭要求。

## I-14 制度是项目内最高治理权威

在项目制度边界内，最高治理权威不是 AI、人工主体、Agent 或提供者，而是已经合法冻结的制度。

人工主体可以依据制度拥有决策权，Agent 可以依据制度拥有执行权，但任何主体都不得越过制度。

当运行时指令与冻结制度冲突时，必须停止相关状态迁移、保存证据并进入治理处理。

## 制度成立条件

一项规则只有同时满足以下条件才能成为冻结制度：

- 来自可追踪现实和证据；
- 经过重复模式与知识审查；
- 已建立独立制度提案；
- 已声明提案者、审查者和冻结权威；
- 已通过提供者独立性检查；
- 已通过跨项目和跨领域适用性检查；
- 已说明与现有制度的兼容关系；
- 不覆盖或伪造历史；
- 已完成正式制度审查；
- 具有唯一冻结标识和版本边界。

## 非法状态总表

以下情况一律非法：

- 运行时执行、偏差、诊断或策略直接修改制度；
- 把单次经验、模型建议或人工直觉直接冻结为制度；
- 把制度提案当作现行制度执行；
- 没有重复性、稳定性和迁移证据就升级知识；
- 在基础制度中绑定具体提供者；
- 把领域规则提升为跨领域不变量；
- 静默修改冻结原则；
- 用新制度覆盖或否定旧制度时期的历史；
- 让知识、验证或执行越过其架构边界；
- 在多个文件中建立相互竞争的术语定义；
- 为接入新能力而降低宪法要求；
- 让任何主体凭身份、能力或结果越过制度。

发现非法状态时，系统必须失败关闭、保存证据，并通过制度提案和审查路径处理。

## 制度演化模型

```text
Reality
  -> Evidence
  -> Expectation
  -> Gap
  -> Diagnosis
  -> Policy
  -> Execution
  -> Pattern
  -> Knowledge
  -> Institution Proposal
  -> Institution Review
  -> Institution
```

本图描述制度如何成长，不替代执行时序、现实模型或信任模型。不同关系模型必须分别命名，不得再用含义不明的“唯一主轴”混合表达。

## 本章边界

本章定义制度的资格、审查、冻结、演化和最高治理边界，不直接冻结比较、符合、裁决或学习的详细模型。尚未冻结的制度提案不得作为现行规则执行。
