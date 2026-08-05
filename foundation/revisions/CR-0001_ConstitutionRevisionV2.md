# 宪法修订提案第二版

## 提案状态

```text
Proposal ID: CR-0001
Status: DRAFT
Authority: NONE
Executable: NO
Review Status: PASS_WITH_BLOCKERS
Latest Review: CR-0001-R2
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: 4d543a1d-968e-40e6-a0dd-4fe5b16fee06
Triggered By: Constitution Consistency Review
Affected Freeze: IF-0001 through IF-0007
```

> 本文件只保存待审查提案，不是冻结制度，不得作为运行时规则、验收标准或状态迁移依据。

第二轮对象一致性审查见 [`CR-0001_ObjectGraphReview_R2.md`](./CR-0001_ObjectGraphReview_R2.md)。审查确认提案结构可以继续，但对象图与权威边界尚未达到冻结条件。

## 提案目标

消除基础制度内部的逻辑矛盾，并为“符合预期”和“偏离预期”建立对称、可审计的合法路径。

本提案不直接修改任何既有冻结章节。所有变更必须经过独立制度审查并形成新的冻结版本或正式取代关系。

## P0：比较对象

拟引入 `Comparison`，用于对冻结预期与可追踪观察进行纯比较。

```text
Expectation
  + Observation
  -> Comparison
```

`Comparison` 不解释原因、不选择行动、不作业务裁决，也不修改预期或观察。

### 未决问题

纯比较计算可以没有决策权威，但其结果要成为正式事实，仍必须满足：

```text
Authority + Evidence + Decision = Formal Fact
```

后续冻结必须明确“执行比较”与“登记比较结果为正式事实”分别由谁负责。

## P0：符合对象

拟引入 `Conformance Record`，为没有偏差的执行建立正式记录。

比较结果不得只有两个状态。为满足证据不足时失败关闭，候选状态至少包括：

```text
MATCHED
NOT_MATCHED
UNKNOWN
```

候选分支为：

```text
Validated Observation
  -> Comparison
       -> MATCHED -> Conformance Record
       -> NOT_MATCHED -> Gap
       -> UNKNOWN -> Evidence Required
```

`Conformance Record` 证明某项观察在指定预期、容差、对象和版本下符合要求，但不自动产生选择、批准或发布决定。

## P0：验证职责

拟把验证明确拆成两个职责：

```text
Evidence Validation
Comparison
```

候选顺序为：

```text
Observation
  -> Evidence
  -> Evidence Validation
  -> Comparison
  -> Conformance Record | Gap | UNKNOWN
```

验证不得定义成功、修改预期、解释原因或选择策略。

### 未决问题

必须冻结验证记录、比较记录、符合记录和裁决之间的权威边界，避免把技术验证重新扩大为最终验收。

## P0：正式事实分类

正式事实应按类型分类，不得被误写成必然依次发生的线性生命周期。

候选分类包括：

```text
Candidate Fact
Comparison Fact
Conformance Fact
Gap Fact
Decision Fact
Assembly Fact
Publication Fact
```

不同事实之间的合法引用关系、前置条件和互斥关系必须由后续冻结明确声明。

## P1：四类关系模型

基础层不再使用含义不明的“唯一主轴”。拟分别建立：

1. `Reality Model`：对象和事实如何存在。
2. `Execution Model`：AI 如何在授权下工作。
3. `Trust Model`：系统依据什么信任正式事实。
4. `Evolution Model`：经验如何经过治理成长为制度。

四类模型必须分别标注边类型，不得用一张箭头图同时表达时间、信任、因果和制度升级。

## P1：失败定义

拟正式确认：

```text
Gap != Failure
```

`Gap` 属于现实差异；`Failure` 属于执行无法合法继续的状态。

候选区分：

```text
Missing Authority -> Failure
Budget Exhausted -> Failure
Human Decision Required -> Suspended
```

硬预期偏离只能产生具有阻断语义的偏差，不得由比较器或偏差对象自动宣布失败。

## P1：裁决模型

拟引入独立的 `Decision Model`，统一表示：

```text
Selection Decision
Acceptance Decision
Publication Decision
Override Decision
```

决策不等于权威：权威回答谁有资格决定，决策记录该主体实际决定了什么。

决策不等于策略：策略授权未来运行时行动，决策可以改变正式对象的生命周期状态。

### 无偏差成功路径候选

```text
Conformance Record
  + Acceptance Authority
  + Acceptance Decision
  + Evidence
  -> Accepted Formal Fact
```

该路径仍需独立冻结，当前不得执行。

## P2：知识成熟度

拟把经验成熟过程细分为：

```text
Pattern
  -> Practice
  -> Knowledge
  -> Institution Proposal
```

每一级的准入证据、审查权威和取代关系尚待定义。

## 必须进入正式修订的既有冲突

后续冻结不得只新增对象，还必须显式处理：

1. `E-05` 中“硬预期偏离立即失败”与 `G-02`、`G-08` 的冲突；
2. `P-01` 及策略准入条件导致无偏差结果无法继续的冲突；
3. `A-03` 中策略授权与执行能力混写的问题；
4. 策略运行时边界与制度治理边界的冲突；
5. 基础层的视频领域和具体提供者依赖；
6. 选择生命周期被错误表达为线性状态的问题；
7. 迟到证据与非法回填之间的边界；
8. 术语重复定义和空白术语表造成的漂移。

## 审查准入条件

本提案只有在以下问题都有明确答案后，才能进入制度审查：

- 比较由谁执行，比较事实由谁登记；
- `UNKNOWN` 如何阻断后续裁决；
- 软预期容差如何影响 `MATCHED`；
- 创意预期何时必须进入人工裁决；
- 符合事实与验收决定如何分离；
- 有偏差和无偏差路径如何汇合到生命周期裁决；
- 策略与普通生命周期决策如何分离；
- 哪些旧原则被取代，哪些只需澄清；
- 旧版本历史如何保持合法；
- 四类关系模型是否仍存在循环或反向权威。

## 建议冻结顺序

本顺序只是提案，不预先分配冻结编号：

```text
Comparison and Conformance
  -> Decision Model
  -> Verification Boundary
  -> Expectation and Failure Amendment
  -> Policy Scope Amendment
  -> Authority Matrix Amendment
  -> Foundation Portability Revision
  -> Glossary Alignment
  -> Constitution Consistency Review
```

## 禁止事项

在本提案正式冻结以前：

- 不得据此修改 `IF-0001` 至 `IF-0007` 的历史正文；
- 不得把 `MATCHED` 自动解释为接受或发布；
- 不得把 `NOT_MATCHED` 自动解释为失败；
- 不得让纯比较绕过权威和证据成为正式事实；
- 不得让策略控制制度提案、审查或冻结；
- 不得把本文件加入现行制度优先级。
