# CR-0012-R2 闭包导入前置条件修正

## 修订信息

```text
Proposal ID: CR-0012-R2
Proposal Type: Bounded Closure Import Premise Correction
Status: DRAFT
Executable: NO
Workstream: WS-09
Repair Basis: CR-0013-NINE-WORKSTREAM-OVERALL-FREEZE-READINESS-REVIEW / NFR-B2
Predecessor Composite: CR-0012 + CR-0012-R1
Directory Candidate Basis: CR-0010-R4
Institution Freeze Created: NO
Publication Authority Created: NO
Runtime Authority Created: NO
```

> 本修订只纠正 `PAG-C-30` 对 `WS-07` 导入状态的过早断言，不改变投影稳定键、审计／发布分权、转换槽竞争、重建、删除或消费者值域。

## 一、替代条款

### PAG-R2-01 候选映射不等于已登记导入

`CR-0011` 已提供闭包与完整性类型的精确候选／登记映射；`CR-0010-R4` 只把这些映射纳入后继目录候选。两者共同证明候选接口可以精确校验，但不证明类型已经冻结或登记。

```text
Provider Exact Type Candidate: PRESENT
WS-07 Successor Directory Candidate: PRESENT
Provider Institution Freeze: ABSENT
WS-07 Type Import Registration Resolution: ABSENT
Runtime Import Status: NOT_REGISTERED
```

### PAG-R2-02 替代 PAG-C-30

`PAG-C-30` 被本条完整替代：

> 投影候选模型可以依据 `CR-0011` 与 `CR-0010-R4` 校验闭包／完整性类型的精确候选映射。任何运行构建、审计或发布，只能消费在未来冻结的 `WS-07` 后继类型目录中取得 `REGISTERED_EXACT` 导入解析、且记录本身取得内容同一登记解析的 `WS-08` 闭包／完整性类型。保留槽、候选导入、待冻结类型或待登记类型一律不可发布。

### PAG-R2-03 投影治理类型同样受此约束

`PAG-C-29` 的三类候选／登记映射已经进入 `CR-0010-R4` 后继目录候选，但在提供方制度冻结和逐类型登记解析成立前，仍不得创建正式审计、重建或删除登记事实。

### PAG-R2-04 发布封套保持独立

发布封套继续由独立发布注册表治理。它不因 `CR-0010-R4` 存在而成为派生记录类型，也不取得 `WS-07` 登记权威。

## 二、失败关闭

以下任一条件出现时，投影路径必须拒绝运行消费：

```text
Missing Provider Freeze Reference
OR Missing Type Import Registration Resolution
OR Import Resolution != REGISTERED_EXACT
OR Record Registration Resolution != REGISTERED_CONTENT_IDENTICAL
OR Closure Completeness Resolution != COMPLETE
OR Import Tuple Digest Conflict
```

拒绝结果必须保留输入引用、目录版本、解析缺口、观察时间和不可变证据摘要，不能静默降级为可发布。

## 三、修复声明

```text
NFR-B2 Unsupported Imported Premise: CLOSED_AS_DRAFT
Candidate Mapping / Runtime Registration Separation: PASS
WS-07 Directory Successor Dependency: EXPLICIT
WS-08 Registered Closure Dependency: EXPLICIT
Projection / Fact Separation Changed: NO
Audit / Publication Authority Separation Changed: NO
Runtime Publication Eligibility Created: NO
WS-09 Model Exit: BLOCKED_PENDING_INTERFACE_REGRESSION
```

下一阶段必须执行九工作流联合接口回归。回归通过前，不得恢复“已经精确导入”的无条件表述。
