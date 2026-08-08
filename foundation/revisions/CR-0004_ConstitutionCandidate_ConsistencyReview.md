# CR-0004 宪制候选独立一致性审查

## 审查信息

```text
Review ID: CR-0004-CONSTITUTION-CANDIDATE-CONSISTENCY-REVIEW
Review Type: Independent Single Candidate Consistency Review
Status: COMPLETED
Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
Executable: NO
Reviewed Candidate: CR-0004-CONSTITUTION-CANDIDATE
Review Basis: CR-0004-R5-FINAL-CLOSURE-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Candidate self-check ignored; source mappings independently re-evaluated
External Approval Required: NO
Candidate Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只审查单一候选是否完整、无歧义地保存 CR-0004 基础稿及 R1 至 R5 的最终规范语义。它不修改候选，不创建制度冻结、注册表、账本、启动模式或运行时权威。

## 审查命题

本轮独立回答：

1. 六份规范来源是否全部具有可追踪去向；
2. 显式覆盖关系是否正确移除旧直接模式投影；
3. 最终候选使用的每个稳定身份是否在候选内部完整定义；
4. 生命周期竞争、跨域合成和更正是否仍可确定解析；
5. 三种冻结引用模式是否保存精确来源、双时间和非追溯边界；
6. 启动清单、外部锚、窗口、证据、封印、终局、存在和模式是否保持单向因果；
7. 四值、五值、冲突优先级和合格否定是否保持闭合；
8. 候选是否还存在模型级阻断；
9. `WS-01` 是否可以退出；
10. 当前是否具备制度冻结资格。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-CONSTITUTION-CANDIDATE
CR-0003-CONSTITUTION-CANDIDATE-R2
CR-0004
CR-0004-LOCAL-REVIEW
CR-0004-R1
CR-0004-R1-LOCAL-REVIEW
CR-0004-R2
CR-0004-R2-LOCAL-REVIEW
CR-0004-R3
CR-0004-R3-LOCAL-REVIEW
CR-0004-R4
CR-0004-R4-LOCAL-REVIEW
CR-0004-R5
CR-0004-R5-FINAL-CLOSURE-REVIEW
CR-0004-CONSTITUTION-CANDIDATE
Local repository state at review time
```

候选自检、作者身份、历史讨论和文件顺序均不作为通过依据。

## 总体裁决

候选成功建立单一规则编号和显式来源谱系，并保持了分权、追加历史、合格否定、封印状态、终局存在及五值模式仲裁主干。

```text
Single Candidate Structure: PASS
Source Rule Citation Coverage: PASS
Explicit Overlay Precedence: PASS
Authority Non-propagation: PASS
Freeze ID Allocation Model: PASS
Protected Normal Commit Model: PASS
Bootstrap Seal / Terminal / Presence / Mode Chain: PASS
Post-terminal Conflict Dominance: PASS
History and Non-authority Boundary: PASS
```

但来源“被引用”不等于来源语义已经完整进入候选。审查发现四组有界合并阻断：

1. 生命周期、更正和复合适用性丢失稳定身份及完整合成真值表；
2. 冻结引用解析丢失规范解析键、视图枚举、三模式精确来源和前瞻非追溯边界；
3. 启动控制对象丢失清单解析、外部锚、解析核心及原始封印稳定身份；
4. 规范启动因果路径把已登记窗口放在其所属保护提交之前。

因此：

```text
Source Citation Completeness: PASS
Semantic Payload Retention: FAIL_WITH_BOUNDED_BLOCKERS
Standalone Candidate Completeness: FAIL_WITH_BOUNDED_BLOCKERS
Candidate Consistency Review: FAIL
Candidate Revision Required: YES
WS-01 Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
```

`CR-0004-R5-FINAL-CLOSURE-REVIEW` 的模型闭合结论仍然有效；本轮阻断来自后续单一候选的合并压缩，不是对 R5 历史审查的改写。

## 一、已通过：单一结构与来源谱系

候选只保留：

```text
IR-CC-001 through IR-CC-058
```

检查结果：

```text
Final Rule Count: 58
Unique Rule IDs: 58
Contiguous Rule IDs: PASS
Source IR-C Rules Cited: 58 / 58
Source IR-R1 Rules Cited: 55 / 55
Source IR-R2 Rules Cited: 34 / 34
Source IR-R3 Rules Cited: 37 / 37
Source IR-R4 Rules Cited: 25 / 25
Source IR-R5 Rules Cited: 30 / 30
Uncited Source Rules: 0
Final Rules with Provenance Range: 58 / 58
```

基础稿与五份修订继续作为历史来源保存；候选没有创建第二套并行规范编号。

```text
Single Consolidated Rule Set: PASS
Historical Source Preservation: PASS
Provenance Coverage: PASS
```

## 二、已通过：显式覆盖与最终模式链

候选正确应用：

```text
Bootstrap Closed Record
  -> LEGACY_NON_NORMATIVE_BOOTSTRAP_CLOSURE_ASSERTION

raw seal fact
  -> SEALED_COMPLETE only

NOT_SEALED / INDETERMINATE / CONFLICTED
  -> registered Seal State Resolution

nonterminal unknown
  -> Closure Progress Ledger

terminal result
  -> COMMITTED | ABORTED | CONFLICTED

terminal existence
  -> PRESENT | ABSENT | INDETERMINATE | CONFLICTED

current mode
  -> ACTIVE_CLOSED
   | ABORTED_CLOSED
   | COMMIT_UNRESOLVED
   | CONFLICTED
   | INDETERMINATE
```

只有已登记模式解析及完整模式账本边界可以产生 `Bootstrap Mode`，且只有 `ACTIVE_CLOSED` 可以开放 `NATIVE`。

迟到冲突进入新的来源向量和模式解析；历史成功仍保留在历史认识视图，不能覆盖当前冲突。

```text
Legacy Direct Mode Projection Removed: PASS
Raw Seal / Seal State Separation: PASS
Progress / Terminal Separation: PASS
Qualified Terminal ABSENT: PASS
Registered Five-value Mode: PASS
Conflict-first Arbitration: PASS
Historical / Current Separation: PASS
```

## 三、已通过：正常冻结与分配提交

候选保持：

```text
Allocation Attempt
  -> Allocation Record
  -> Registered Four-value Allocation Resolution
  -> Freeze Decision
  -> Fixed Candidate Write Set and Authority Bundle
  -> Commit Attempt
  -> Protected Content-identical Write
  -> Registered Four-value Commit Resolution
```

冻结标识命名空间唯一、永久不可复用；退役只追加历史。正常提交仍要求冻结账本、注册表和归因记录在同一保护边界内分别内容同一。

```text
Allocation Fact / Resolution Separation: PASS
Dual Completeness for ALLOCATED: PASS
Freeze ID Non-reuse: PASS
Coordination / Registration Separation: PASS
Protected Write Attribution: PASS
ABORTED Qualified-proof Requirement: PASS
```

## 四、阻断 B1：生命周期、更正和复合适用性身份不完整

### 问题一：候选消费未定义竞争集合键

候选的 `Lifecycle Effect Resolution Key` 直接引用：

```text
Lifecycle Applicability Conflict Set Key
```

但单一候选没有定义该键的字段、目标规范化规则或禁止字段。R2 来源要求它至少绑定：

```text
Source Institution ID and Version
Target Institution ID and Version or NOT_APPLICABLE
Query Effective Scope Digest
Applicability Valid At Coordinate
Lifecycle Semantic Domain
Conflict Set Rule Version
```

并禁止使用决定事实、记录标识、记录时间、插入顺序或写入者来隔离竞争。

缺少该定义时，同一语义竞争可以按决定事实或记录身份换键逃逸。

### 问题二：继任聚合和复合适用性没有稳定解析键

候选定义了 `Successor Selection Conflict Set Key`，但没有定义：

```text
Successor Selection Aggregate Resolution Key
Composite Lifecycle Applicability Resolution Key
```

候选也没有完整恢复复合候选—登记链的共同字段和载荷同一要求。它要求冻结引用消费“已登记复合适用性”，却没有在单一候选内给该记录一个可复现身份。

### 问题三：跨域真值表被压缩为不足以判定冲突的摘要

候选只说明“撤销产生不适用、替代与唯一继任产生不适用”，没有保留下列必须为冲突的组合：

```text
REVOKES + UNIQUE_SUCCESSOR -> CONFLICTED
NOT_EFFECTIVE source applicability + UNIQUE_SUCCESSOR -> CONFLICTED
SUPERSEDES + successor not UNIQUE_SUCCESSOR -> CONFLICTED
incompatible registered composite results for same key -> CONFLICTED
```

这会允许实现者对同一跨域来源产生不同确定结果。

### 问题四：更正链没有稳定键

候选保留更正候选—登记链和字段白名单，却没有保留：

```text
Institution Registry Correction Key =
  Original Record ID and Digest
+ Corrected Field Set Digest
+ Correction Request ID
+ Effective At
```

因此无法从单一候选判断同一更正是幂等重申还是冲突载荷。

### 风险

```text
Conflict-set Escape: POSSIBLE
Composite Resolution Identity: INCOMPLETE
Cross-domain Determinism: INCOMPLETE
Correction Idempotency: INCOMPLETE
Freeze Reference Applicability Determinism: FAIL_WITH_BLOCKER
```

### 有界修复要求

`CR-0004-CONSTITUTION-CANDIDATE-R1` 必须：

1. 恢复生命周期竞争集合完整稳定键及禁止字段；
2. 恢复继任聚合和复合适用性解析键；
3. 恢复候选—登记链、共同字段、内容同一和同键冲突规则；
4. 恢复 R3 跨域合成的完整优先级和冲突真值表；
5. 恢复注册表更正稳定键。

## 五、阻断 B2：冻结引用解析身份和三模式契约不完整

### 问题一：规范解析键没有进入候选

候选要求解析记录“绑定稳定键”，但没有定义来源中的：

```text
Freeze Reference Resolution Key =
  Institution Freeze Reference Key
+ Valid At
+ Known At
+ Institution Resolution Boundary Vector Digest
+ View Mode
+ Freeze Reference Resolution Rule Version
```

因此无法确定边界、认识时间、视图或规则变化何时必须形成新的解析身份。

### 问题二：View Mode 没有封闭值域

候选多次使用 `View Mode`，但没有在规范枚举中固定：

```text
HISTORICAL_AS_KNOWN
CURRENT_RESTATED
```

虽然文字描述了历史认识和当前重述，未封闭的协议值仍允许实现侧出现第三种未审查模式。

### 问题三：三模式必需来源被压缩为“各自全部来源”

候选保留三个合法组合，但没有分别枚举 `NATIVE`、`PRESERVED` 和 `PROSPECTIVE` 的精确必需来源。由此丢失了以下不可替换约束：

- `NATIVE` 必须绑定正常提案、审查、冻结决定、提交归因和已登记 `COMMITTED`；
- `PRESERVED` 必须同时验证完整旧冻结链和启动登记链，启动决定不得替换旧决定、权威、证据或提交；
- `PROSPECTIVE` 必须绑定新分配标识、独立启动审查和启动识别决定；
- 每个来源必须拥有独立 `COMPLETE` 边界。

### 问题四：前瞻识别的非追溯边界丢失

来源要求：

```text
Validity Start no earlier than Bootstrap COMMITTED At
```

并要求旧声明标识和时间只作历史字段，不得成为新冻结引用的标识或有效起点。候选没有保留这两条确定约束。

### 风险

```text
Resolution Key Collision: POSSIBLE
Unreviewed View Mode: POSSIBLE
Under-proven Mode-specific Reference: POSSIBLE
Prospective Retroactivity: NOT_EXPLICITLY_PROHIBITED
Freeze Reference Determinism: FAIL_WITH_BLOCKER
```

### 有界修复要求

R1 必须：

1. 恢复完整 `Freeze Reference Resolution Key`；
2. 固定两个 `View Mode` 值及各自时间消费规则；
3. 分别恢复三种模式的精确必需来源清单；
4. 明确 `PROSPECTIVE` 有效起点不得早于已登记启动 `COMMITTED`；
5. 明确历史声明标识和时间不得冒充新冻结引用字段。

## 六、阻断 B3：启动控制对象稳定身份不完整

### 问题一：清单登记解析只有值域，没有稳定键

候选保留：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

但没有恢复 `Bootstrap Manifest Registration Resolution Key` 及完整真值表。因此清单载体边界或规则变化是否产生新解析身份、何时可以形成合格 `NOT_REGISTERED`，在单一候选内不确定。

### 问题二：外部锚缺少两个稳定键和解析真值表

候选只说外部锚拥有“独立四值提交解析”，没有定义：

```text
External Bootstrap Anchor Commitment Key
External Anchor Commitment Resolution Key
```

也没有保留内容同一锚、完整外部边界、合格无写入证明、不同清单摘要和不兼容锚记录的确定分支。

这使内部窗口虽然引用“已登记外部锚”，却无法从候选判断该锚是否是同键内容同一的 `COMMITTED`。

### 问题三：证据解析消费未定义核心键

候选的 `Bootstrap Commit Evidence Resolution Key` 引用：

```text
Bootstrap Commit Resolution Core Key
```

但候选没有定义该核心键。来源要求它绑定唯一清单、已登记清单解析、已登记外部锚解析、窗口键、允许尝试和规则版本，并禁止窗口与最终解析摘要互相包含。

### 问题四：原始封印声明“同键”但没有定义键

候选要求原始封印同键同载荷幂等、同键不同载荷冲突，却没有恢复：

```text
Bootstrap Commit Evidence Boundary Seal Key =
  Bootstrap Commit Resolution Conflict Set Key
+ COMMIT_EVIDENCE_SET
```

因此原始封印的受保护单赋值域没有完整身份。

### 风险

```text
Manifest Resolution Identity: INCOMPLETE
External Anchor Identity: INCOMPLETE
Bootstrap Core Identity: UNDEFINED_BUT_CONSUMED
Raw Seal Single-assignment Key: INCOMPLETE
Bootstrap Control-chain Reproducibility: FAIL_WITH_BLOCKER
```

### 有界修复要求

R1 必须恢复：

1. 清单登记解析键、候选—登记链和四值真值表；
2. 外部锚承诺键、解析键、候选—登记链和四值真值表；
3. `Bootstrap Commit Resolution Core Key` 的完整字段及无环禁止项；
4. 原始封印单赋值键；
5. 所有相关候选和已登记载荷内容同一要求。

## 七、阻断 B4：启动窗口登记因果顺序反转

### 问题

候选的规范因果路径写为：

```text
Registered Genesis Manifest
  -> Registered External Anchor
  -> Registered Bootstrap Window
  -> Protected Internal Bootstrap Commit
```

但 R2 最终语义要求：

1. 在清单登记和外部锚提交后构造 `Candidate Bootstrap Window Definition Record`；
2. 内部启动尝试只能消费该精确候选；
3. 窗口登记者只能在内部保护边界中登记内容相同候选；
4. `Registered Bootstrap Window Definition Record` 与内部锚、首批注册表集合、识别账本集合和归因记录在同一保护提交中成立。

候选当前顺序把已登记窗口放在保护边界之前，产生两种错误解释：

```text
Interpretation A:
  window registered outside protected internal commit

Interpretation B:
  protected commit requires a registered record that only it may create
```

前者破坏原子归因；后者形成循环前置条件。

### 风险

```text
Window Registration Outside Protected Boundary: POSSIBLE
Bootstrap Commit Precondition Cycle: POSSIBLE
Atomic First-entry Attribution: FAIL_WITH_BLOCKER
```

### 有界修复要求

规范路径必须改为：

```text
Registered Genesis Manifest
  -> Registered External Anchor COMMITTED Resolution
  -> Candidate Bootstrap Window Definition
  -> Bootstrap Commit Attempt binding exact candidate
  -> Protected Internal Bootstrap Commit
       -> Registered Bootstrap Window Definition
       + Bootstrap Anchor Record
       + First Institution Registry Entry Set
       + Freeze Ledger Recognition Entry Set
       + Bootstrap Commit Attribution Record
  -> Bootstrap Commit Evidence Resolution
```

候选窗口与已登记窗口必须内容同一；窗口登记不得提前证明提交或关闭。

## 八、无环和攻击场景审查

| 场景 | 预期 | 结果 |
|---|---|---|
| 分配账本边界不完整 | `INDETERMINATE` | PASS |
| 同冻结标识不同内容 | `CONFLICTED` 且不得复用 | PASS |
| 生命周期决定按记录 ID 分隔竞争 | 必须同集合冲突 | FAIL，竞争集合键未定义 |
| 撤销与唯一继任同时成立 | `CONFLICTED` | FAIL，完整跨域表缺失 |
| 同更正请求产生不同载荷 | `CONFLICTED` | FAIL，更正键缺失 |
| 同引用不同 Known At | 新解析身份 | FAIL，解析键缺失 |
| 前瞻冻结有效时间早于启动提交 | 拒绝 | FAIL，非追溯约束缺失 |
| 不同清单摘要写入同一外部锚域 | `CONFLICTED` | FAIL，锚键缺失 |
| 已登记窗口先于内部保护提交 | 禁止 | FAIL，规范路径反转 |
| 空查询推断终局 ABSENT | 禁止 | PASS |
| 封印后迟到证据 | 当前 `CONFLICTED`，历史保留 | PASS |
| 候选模式开放 NATIVE | 禁止 | PASS |
| 模式账本边界不完整 | 外层失败关闭 | PASS |

已审查的 R4/R5 末端图没有发现新的自引用：

```text
Seal-state Self-reference: ABSENT
Progress / Terminal Key Collision: ABSENT
Terminal-presence Self-reference: ABSENT
Mode-resolution Self-reference: ABSENT
```

阻断集中在合并时遗漏的上游身份和一条因果路径，不要求重写已通过的末端模式仲裁。

## 九、阻断矩阵

| 阻断 | 范围 | 严重度 | 修订目标 |
|---|---|---|---|
| B1 生命周期、更正与复合适用性身份 | `IR-CC-019..024` | HIGH | 恢复稳定键、登记链和完整合成表 |
| B2 冻结引用解析与三模式契约 | `IR-CC-025..029` | HIGH | 恢复解析键、视图枚举、逐模式来源和非追溯边界 |
| B3 启动控制对象身份 | `IR-CC-032..039` | HIGH | 恢复清单、外部锚、核心和封印键 |
| B4 启动窗口提交因果 | `IR-CC-034`、`IR-CC-053` | HIGH | 候选窗口先于尝试，登记窗口位于保护提交内 |

四项阻断均可在单一候选 R1 内有界修复，不需要修改基础稿、R1 至 R5 或任何历史审查。

## 十、非阻断观察

以下仍未完成，但不是本轮四项合并阻断的修复内容：

```text
IF-0007 authoritative institution freeze
WS-02 through WS-09 external governance closure
Provider-source reality-bound evidence
Runtime carrier implementation and migration
Independent external approval where required
```

候选即使完成 R1 修复并通过复审，也只能成为内部一致候选，不能自动取得冻结资格。

## 十一、阶段决定

```text
CR-0004 Constitution Candidate Review: COMPLETED
Review Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
Candidate Structure: PASS
Source Citation Coverage: PASS
Standalone Semantic Completeness: FAIL
Open Candidate Blockers: 4
Candidate Revision Required: YES
Authorized Next Artifact: CR-0004-CONSTITUTION-CANDIDATE-R1
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只能建立 `CR-0004-CONSTITUTION-CANDIDATE-R1`，有界恢复上述身份、真值表和窗口提交因果。R1 必须保留本候选、全部历史修订和审查文件不变，并在完成后接受独立一致性复审。
