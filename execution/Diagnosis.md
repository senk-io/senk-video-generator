# 诊断模型

## 制度冻结信息

```text
Freeze ID: IF-0004
Constitution: AI Native Engineering Constitution
Chapter: Diagnosis Model
Status: FROZEN
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: 646434d9-8c03-4277-ac61-33b852c995ab
Depends On: IF-0001 Authority Model
Depends On: IF-0002 Expectation Model
Depends On: IF-0003 Gap Model
```

本章定义 AI 原生工程中的诊断模型。诊断不是事实、策略或知识，而是基于当前证据对偏差作出的受治理解释。

> 现实已经发生，偏差已经成立；诊断只回答为什么会产生这个偏差。

本章中的“必须”“不得”和“只能”均为规范性要求。诊断不得修改现实、观察或偏差，也不得决定下一步行动。

## D-01 诊断不是现实

诊断永远不是事实，只是对偏差的解释。

```text
Reality: 已经发生
Gap: 已经成立
Diagnosis: 对 Gap 的解释
```

诊断不得修改现实，也不得修改偏差。

对于同一历史时点，现实事实和特定偏差事实保持唯一；针对同一偏差可以存在多个诊断。

## D-02 诊断始终引用偏差

诊断不能直接解释观察。

非法推导：

```text
Observation
  -> Diagnosis
```

合法推导：

```text
Expectation
  -> Observation
  -> Gap
  -> Diagnosis
```

绕过偏差会使诊断脱离冻结预期，进而开始重新定义现实。

## D-03 一个偏差可以拥有多个诊断

例如，“角色漂移”偏差可能同时具有以下候选解释：

```text
Prompt Constraint Missing
Model Limitation
Reference Image Inconsistent
```

多个诊断可以并存，也可能分别得到不同证据支持。诊断不是唯一真相，而是受治理的假设。

系统不得为了形成单一叙事而静默删除竞争诊断。

## D-04 诊断必须声明置信度

诊断不得使用无证据的确定性表述。每项诊断必须同时声明：

```text
Confidence
Evidence
Unknowns
```

置信度表达当前证据对该解释的支持程度，不把解释升级为事实。

诊断必须显式记录未知项，包括无法观察的提供者内部行为、缺失上下文或尚未验证的假设。

## D-05 诊断不得创造证据

诊断只能引用已经存在且可追踪的证据，不得把自身推断写成证据。

没有证据支持“提示词写得不好”时，合法结论只能是：

```text
Insufficient Evidence
```

需要新证据时，诊断可以声明证据缺口，但不能自行补造观察、实验结果或历史事实。

## D-06 诊断必须归入原因分类

诊断不得只使用无法聚合的自由描述，必须归入统一原因分类。

### 预期原因

```text
Expectation Incomplete
Expectation Ambiguous
Expectation Conflict
```

### 执行原因

```text
Execution Interrupted
Execution Timeout
Execution Skipped
```

### 提供者原因

```text
Provider Limitation
Provider Instability
Provider Regression
```

### 知识原因

```text
Pattern Missing
Knowledge Outdated
```

### 人工原因

```text
Manual Override
Manual Selection
Manual Modification
```

自由文本可以补充解释，但不能替代原因分类。

## D-07 诊断不得决定策略

诊断回答“为什么”，策略回答“怎么办”。

例如，诊断可以是：

```text
Prompt Constraint Missing
```

但诊断不得直接声明：

```text
Retry
Repair
Escalate
Replace Provider
Human Review
```

这些行动属于策略权威。把行动写入诊断会破坏解释与决策的分离。

## D-08 诊断必须保留不确定性

无法确认唯一原因时，系统必须保留多个候选诊断及各自置信度，不能为了让流程继续而强行选择一个。

```text
Candidate A: 0.61
Candidate B: 0.27
Candidate C: 0.12
```

候选诊断的置信度可以不构成完整概率分布，但其尺度和含义必须一致且可解释。

## D-09 诊断必须版本化

诊断会随着证据增加而修订，但不得覆盖历史解释。

```text
Diagnosis V1: Provider Issue
  -> More Evidence
Diagnosis V2: Expectation Ambiguous
```

新版本必须引用被修订的旧版本、新增证据和修订原因。旧诊断仍是“当时根据当时证据作出的解释”这一历史事实。

## D-10 诊断不得自动成为知识

单次诊断只是一次解释，不能直接进入知识库或基础制度。

唯一合法升级路径是：

```text
Diagnosis
  -> Repeated
  -> Pattern
  -> Knowledge
  -> Institution
```

缺少模式评审时，诊断必须保持为个案解释。

## D-11 诊断必须可复审

新的证据可以支持、削弱或推翻现有诊断。

```text
Diagnosis V1
  -> More Evidence
  -> Diagnosis V2
```

复审只改变解释，不改变原始现实、观察和偏差。被推翻的诊断不得从历史中消失。

## D-12 诊断止于因果解释

诊断回答为什么，不回答怎么办，也不负责决定谁应承担责任。

```text
Diagnosis ends at: Root Cause
Policy starts at: Next Action
```

责任归属如果需要正式裁决，必须由独立权威和制度处理，不能由因果解释自动产生。

## D-13 诊断拥有可解释性职责

诊断存在的唯一目的，是让后来者能够回答：

> 为什么当时作出了这个解释？

每项诊断必须让读者沿引用关系找到偏差、证据、未知项、原因分类、置信度及版本历史。

“AI 当时觉得这样”不构成可解释诊断。

## D-14 诊断永远不是最终真相

诊断只是截至当前证据最合理的解释，允许修正、追加和并存。

```text
Diagnosis: revisable
Reality: not revisable by Diagnosis
Gap: not revisable by Diagnosis
```

置信度很高也不能把诊断升级为现实事实。诊断的确定性永远受现有证据边界约束。

## 诊断成立条件

诊断只有同时满足以下条件才能正式成立：

- 引用一个已经成立且不可变的偏差；
- 明确声明原因分类；
- 引用已有证据，不自行创造证据；
- 声明置信度及其尺度；
- 声明已知未知项；
- 不修改现实、观察或偏差；
- 不包含策略行动或责任裁决；
- 可与其他候选诊断并存；
- 可以被后续证据复审；
- 具有可追踪版本和历史关系。

## 非法状态总表

以下情况一律非法：

- 把诊断声明为现实事实或最终真相；
- 诊断直接解释观察而不引用偏差；
- 为同一偏差强行保留唯一解释；
- 使用确定性语言却不声明置信度；
- 把推断、猜测或模型自述当作证据；
- 不进入统一原因分类；
- 在诊断中写入重试、修复、升级或人工评审行动；
- 为了推进流程而删除不确定性或竞争诊断；
- 覆盖旧诊断而不保留版本历史；
- 让单次诊断自动进入知识库或制度；
- 因诊断变化而修改原始偏差；
- 用诊断直接决定责任归属。

发现非法状态时，系统必须失败关闭并保存证据。

## 受治理的闭环

完整因果链为：

```text
Reality
  -> Expectation
  -> Observation
  -> Gap
  -> Diagnosis
  -> Policy
  -> Execution
  -> Learning
  -> Knowledge
  -> Institution
```

其中执行出现两次：第一次执行产生观察，策略之后的下一次执行尝试缩小偏差。

```text
Expectation
  -> Execution
  -> Observation
  -> Gap
  -> Diagnosis
  -> Policy
  -> Next Execution
```

这不是一次性生成流程，而是受治理的执行闭环。

## 本章边界

本章定义诊断如何解释偏差，不定义下一步行动。谁拥有策略权威，以及重试、修复、重新规划、升级和人工评审的制度边界，已由 `IF-0005` 建立，见 [`Policy.md`](./Policy.md)。
