# CR-0004 独立模型与启动闭环审查

## 审查信息

```text
Review ID: CR-0004-LOCAL-REVIEW
Review Type: Independent Model and Bootstrap Closure Review
Status: COMPLETED
Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0004
Reviewed Workstream: WS-01
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Separate review task contract and immutable review record; not an external freeze review
External Approval Required: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只审查 `CR-0004` 的模型完整性、权威拓扑、引用解析和启动闭环，不是制度冻结审查。审查通过结构不等于提案可以执行、登记或冻结。

## 审查命题

本轮独立回答：

1. 提案是否保持制度注册表与冻结引用支持的单一目的；
2. 制度身份、版本、摘要、冻结决定、提交、注册和解析是否因果闭合；
3. 冻结标识和每类权威是否拥有唯一、显式且不传播的来源；
4. 三种合法登记／冻结依据组合是否可以确定性解析；
5. 生命周期和更正记录是否能在不伪造历史的前提下改变引用适用性；
6. `CR-0004` 注册表外冻结是否拥有可验证成功契约；
7. 外部启动锚是否真正终止自证循环且没有跨载体原子性缺口；
8. 启动识别是否保留原始历史并阻止旧标识拼接新链；
9. 当前提案是否已经满足 `WS-01` 的独立审查退出门槛。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-CONSTITUTION-CANDIDATE
CR-0003-CONSTITUTION-CANDIDATE-R2
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
CR-0004
Local repository state at review time
```

历史讨论、作者身份和自检结论只作为定位信息，不作为通过依据。

## 总体结论

`CR-0004` 已经建立可继续修订的完整主体结构：

```text
Single Purpose: PASS
Institution / Version / Content Separation: PASS
Registry / Freeze Ledger Separation: PASS
Proposal / Review / Freeze / Commit Separation: PASS
Freeze Reference Minimum Fields: COMPLETE
Registration and Freeze Basis Modes: PASS
History Non-retroactivity: PASS
Provider Independence: PASS
Cross-domain Portability: PASS
```

但四个因果边界仍未闭合：

```text
B1 Freeze ID and Protected Registration Authority Topology: BLOCKED
B2 Lifecycle and Correction Registration Causality: BLOCKED
B3 Pre-registry Commit and External Bootstrap Anchor Protocol: BLOCKED
B4 Mode-specific Freeze Reference Resolution Contract: BLOCKED
```

因此：

```text
Proposal Structure: PASS
Proposal Completeness: PASS_WITH_BLOCKERS
Bootstrap Closure: FAIL
Independent Model Review: PASS_WITH_FOUR_BOUNDED_BLOCKERS
WS-01 Exit Eligibility: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
```

四项阻断均可在一个有界 `CR-0004-R1` 中修复，不要求推翻提案的单一目的、历史模式或八字段冻结引用兼容面。

## 一、通过项

### 单一目的

提案只负责制度版本注册、冻结账本、冻结引用和启动支持，没有吸收业务资格、业务权威适用性、决策、通用闭包或业务投影职责。

```text
Single Purpose: PASS
Adjacent Authority Absorption: NOT_OBSERVED
```

### 身份、内容和历史

提案明确分离：

```text
Institution ID
Institution Version ID
Institution Content Artifact
Frozen Content Digest
Freeze ID
```

同一版本不同摘要和同一冻结标识不同冻结事实均要求保留冲突。内容位置与内容身份分离，新版本、生命周期关系和表示更正均采用追加语义。

```text
Identity Separation: PASS
Digest / Legitimacy Separation: PASS
Historical Immutability: PASS
```

### 冻结链分层

提案正确区分制度审查决定、冻结决定、提交尝试、受保护写入、注册条目和冻结引用。`FREEZE_AUTHORIZED` 不直接创建冻结事实，完成观察也不能替代权威记录。

```text
Review / Freeze Decision Separation: PASS
Decision / Commit Separation: PASS
Observation / Formal Fact Separation: PASS
```

### 注册表与冻结账本

制度身份、版本和生命周期由制度注册表持有；冻结行为、权威、决定和证据谱系由冻结账本持有。引用必须绑定两个来源，单一账本边界不能证明另一账本完整。

```text
Registry / Freeze Ledger Separation: PASS
Single-boundary Overreach Prevention: PASS
```

### 启动历史保护

提案正确区分：

```text
NATIVE + NATIVE_FREEZE
BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

旧链完整时保留精确旧链；旧链不完整时只能使用新冻结标识建立向未来生效的启动识别冻结。启动观察摘要不得冒充原始冻结摘要。

```text
Legacy Freeze ID Reuse Prevention: PASS
Prospective Recognition Boundary: PASS
Historical Non-retroactivity: PASS
```

## 二、阻断 B1：冻结标识与受保护登记权威拓扑未闭合

### 本地事实

`IR-C-09` 定义了制度身份分配、冻结决定、提交执行、冻结账本登记和制度注册表登记权威，但没有定义：

```text
Freeze ID Allocation Authority Type
Freeze ID Allocation Record
Freeze ID Uniqueness Scope
Freeze ID Collision Resolution
```

`IR-C-21` 允许在提交尝试中预分配 `Freeze ID`，却没有说明谁有权分配、分配依据、全局或局部唯一边界、失败后保留状态以及冲突时的权威记录。

`IR-C-50` 又让 `Bootstrap Freeze Recognition Decision Maker` 分配新的启动冻结标识，导致冻结决定权威隐式取得标识分配权。

### 原子登记缺口

正常提交尝试只绑定：

```text
Freeze Decision Reference
Freeze Authority Reference
Declared Registry ID
Declared Freeze Ledger ID
Declared Write-set Digest
```

它没有绑定：

```text
Freeze ID Allocation Record
Freeze Ledger Registration Authority Grant
Institution Registry Entry Registration Authority Grant
Institution Commit Attribution Write Authority Grant
Candidate Freeze Ledger Entry Digest
Candidate Institution Registry Entry Digest
Candidate Attribution Record Digest
```

`IR-C-23` 要求三个记录在同一保护边界成立，但没有定义保护协调者如何同时消费三个独立授权而不传播权威，也没有证明三个最终载荷与提交前固定载荷内容同一。

### 风险

当前模型允许以下未被类型系统明确禁止的路径：

```text
Freeze Decision Maker
  -> self-allocates Freeze ID

Commit Execution Authority
  -> implicitly acquires two registration authorities

Declared Write-set Digest
  -> final payloads not independently content-identity checked
```

这会破坏 `IF-0001` 的权威先于执行、权威不传播和权威不得自证。

### 有界修复要求

`CR-0004-R1` 必须补充：

1. 独立 `Freeze ID Allocation Authority Type`；
2. 不可变 `Freeze ID Allocation Attempt` 和 `Freeze ID Allocation Record`；
3. 唯一性作用域、碰撞、预分配、保留、弃用和不可复用规则；
4. 正常及启动提交尝试对全部写入授权实例的精确引用；
5. 三个候选权威记录的稳定身份和提交前摘要；
6. 保护协调者只能消费独立授权，不能继承或创建这些授权；
7. 最终三个记录分别通过内容同一校验；
8. 启动冻结识别决定只能引用已分配冻结标识，不能自行分配。

```text
Finding B1: BLOCKING
Repair Scope: authority types, allocation records and protected write payload contract only
```

## 三、阻断 B2：生命周期与更正登记因果未闭合

### 本地事实

`IR-C-42` 声明 `SUPERSEDES`、`REVOKES`、`DEPRECATES` 由新生命周期决定建立，但只要求有效时间、作用域、依据和证据。

当前没有定义：

```text
Institution Lifecycle Decision Act
Institution Lifecycle Decision Attempt
Candidate Lifecycle Relation Record
Lifecycle Relation Registration Authority Grant
Registered Lifecycle Relation Record
Lifecycle Stable Key and Payload Digest
Lifecycle Commit or Registration Result
```

`IR-C-43` 对更正只定义原记录、更正字段、原值、新值、理由、证据和时间，没有定义更正资格、候选记录、登记尝试、内容同一和稳定身份。

### 为什么是模型级阻断

冻结引用解析直接消费：

```text
Correction Boundary
Lifecycle Boundary
```

并让这些记录影响：

```text
Reference Applicability
Reference Usability
Institution Current View
```

因此生命周期和更正不是可推迟的显示细节。若其成立链不完整，任何主体都可能通过追加一个未授权关系或“更正”改变制度引用的当前可用性。

### 有界修复要求

`CR-0004-R1` 必须补充：

1. 生命周期决定的行为、尝试、候选、登记和权威记录链；
2. 每个生命周期关系只引用一个主要生命周期决定权威；
3. 稳定键至少绑定源版本、目标版本、关系类型、作用域和有效时间；
4. 生命周期关系的内容同一、幂等、冲突和更正规则；
5. 更正资格计算与更正登记分权；
6. 更正候选、登记尝试、内容同一摘要和已登记更正记录；
7. 明确禁止更正改变内容摘要、制度语义、冻结决定或历史有效区间；
8. 只有已登记且在查询边界内的生命周期和更正记录可以影响引用解析。

```text
Finding B2: BLOCKING
Repair Scope: lifecycle and correction record causality only
```

## 四、阻断 B3：注册表外提交与外部启动锚协议未闭合

### 注册表外提交缺口

`IR-C-46` 要求 `CR-0004` 先完成 `Successful Pre-registry Institution Commit`，并列出内容、审查、权威、决定、证据、作用域、归因和不可变历史引用。

但该对象没有：

```text
Stable Identity
Commit Attempt Identity
Protected Write-set
Commit Authority Contract
Success / Abort / Unknown Resolution
Independent Resolution Authority
Content-identity Registration
Conflict Behavior
```

“普通文件写入或仓库提交本身不能证明成功”是正确禁止边界，但提案没有定义什么确定性正向记录能够证明注册表外提交成功。

### 外部启动锚缺口

`Bootstrap Anchor Record` 引用 `External Immutable Anchor Commitment Reference`，但没有定义：

```text
External Anchor Commitment Object
External Anchor Commitment Authority
External Anchor Candidate and Stable Key
External Anchor Payload Digest
Creation and Registration Times
Verification Authority and Result
Failure and Conflict Behavior
```

启动锚内部保存外部锚引用，而外部锚又必须定位启动锚、首批集合和提交证据。当前没有规定预分配标识、候选清单或两阶段内容身份协议，因而可能形成摘要自引用或不明确的跨载体原子性要求。

### 启动关闭缺口

`Bootstrap Closed Record` 与首批条目同批写入，但没有独立启动提交解析。若外部锚成功而注册表写入未知，或注册表写入可见而外部锚不可验证，当前只有笼统 `INDETERMINATE`，没有稳定尝试、解析键和冲突保留路径。

### 风险

```text
Pre-registry file history
  -> may be mistaken for successful institution commit

Internal Bootstrap Anchor
  -> may attempt to validate its own external commitment

Partial cross-carrier write
  -> bootstrap window may close without a deterministically verified first set
```

### 有界修复要求

`CR-0004-R1` 必须补充专用启动提交契约：

1. `Pre-registry Institution Commit Attempt`、权威记录和稳定提交引用；
2. 注册表外保护载体、候选写集摘要、内容同一和独立提交解析；
3. `External Bootstrap Anchor Commitment` 对象、权威、稳定键和不可变载荷；
4. 在写入前固定全部首批条目标识、摘要和 `Bootstrap Manifest Digest`，避免摘要自引用；
5. 外部锚承诺与内部首批提交的明确先后和关联键；
6. `Bootstrap Commit Resolution` 的 `COMMITTED | ABORTED | INDETERMINATE | CONFLICTED` 值域；
7. 只有独立解析为 `COMMITTED` 才能使 `Bootstrap Closed Record` 取得当前有效地位；
8. 任一部分未知或冲突时保留全部部分写入，不重开窗口、不换键绕过。

该修复只需要闭合一次性启动提交，不要求在 `CR-0004` 中复制通用 `CR-0003` 提交模型。

```text
Finding B3: BLOCKING
Repair Scope: pre-registry and bootstrap commit protocol only
```

## 五、阻断 B4：三种引用模式缺少确定性解析契约

### 本地事实

`IR-C-36` 定义冻结链资格四值，`IR-C-38` 定义资格与适用性的可用性投影，方向正确。

但当前没有分别定义以下模式的必需来源集合和终局条件：

```text
NATIVE + NATIVE_FREEZE
BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

尤其缺少：

- 哪些精确记录全部匹配才是 `VERIFIED`；
- 哪种正向否定证据才可以产生 `REJECTED`；
- 同标识不同摘要、决定、权威、作用域或提交引用如何进入 `CONFLICTED`；
- 原始旧链和启动链各自需要哪些完整性边界；
- 更正和生命周期边界如何影响历史视图与当前视图；
- 每个注册表和账本边界由什么已登记完整性记录证明完整。

### 解析身份缺口

`Institution Freeze Reference Key` 唯一标识被解析引用，但没有定义独立 `Freeze Reference Resolution Key`。

解析结果依赖：

```text
Valid At
Known At
Registry Boundary
Freeze Ledger Boundary
Correction Boundary
Lifecycle Boundary
Rule Version
View Mode
```

这些坐标变化会产生不同解析现实，不能只用引用键或自由 `Resolution ID` 区分。

### 风险

不同实现可以对同一输入作出不同终局，或者在边界不完整时把未找到记录解释为 `REJECTED`。启动模式还可能只验证启动锚而漏验精确旧链或向未来识别冻结链。

### 有界修复要求

`CR-0004-R1` 必须补充：

1. 三种合法模式各自的必需来源集合；
2. 每种模式的 `VERIFIED`、`REJECTED`、`INDETERMINATE`、`CONFLICTED` 真值表；
3. 已登记边界完整性记录及其独立权威；
4. `Freeze Reference Resolution Key`，绑定引用键、双时间、边界向量、视图模式和规则版本；
5. 历史认识视图与当前重述视图分离；
6. 原始链、更正链、生命周期链和启动链冲突全部保留；
7. 缺失、读取失败、边界不完整和外部锚不可验证只能产生 `INDETERMINATE`；
8. 解析候选和登记记录的完整内容同一契约。

```text
Finding B4: BLOCKING
Repair Scope: resolution key, completeness and three mode-specific truth tables only
```

## 六、阻断间关系

四个阻断存在明确顺序：

```text
B1 Freeze ID and Protected Registration Authority
  -> B2 Lifecycle and Correction Registration Causality
  -> B3 Pre-registry and Bootstrap Commit Protocol
  -> B4 Mode-specific Freeze Reference Resolution
```

原因：

- 没有稳定冻结标识和写入权威，启动提交无法固定对象；
- 生命周期和更正成立链不闭合，引用适用性输入不可信；
- 注册表外提交和启动锚不闭合，启动模式没有可信终点；
- 前三项闭合后，才能定义三种模式的确定性解析真值表。

四项可以在同一 R1 中设计，但必须按该顺序审查。

## 七、非阻断外部依赖

以下仍然属于后续冻结或实现依赖，不是本轮新增模型阻断：

- 摘要算法和规范字节契约尚未独立审查；
- 通用资格和派生登记治理尚未冻结；
- 制度注册表、冻结账本和保护提交尚无实现证据；
- 没有重复、稳定、跨提供者、跨项目和跨领域证据；
- 没有适用注册表外冻结权威；
- 没有正式冻结决定或成功制度提交。

这些条件不能通过修复 R1 自动成立。

## 八、审查矩阵

```text
Single Purpose: PASS
Object Type Separation: PASS
Institution Identity / Version / Digest: PASS
Proposal / Review / Freeze / Commit Separation: PASS
Registry / Freeze Ledger Separation: PASS
Freeze Reference Eight-field Compatibility: PASS
Registration / Freeze Basis Mode Separation: PASS
History Non-retroactivity: PASS
Provider Independence: PASS
Cross-domain Portability: PASS
Freeze ID Allocation Authority: FAIL
Protected Registration Authority Topology: FAIL
Lifecycle Decision Registration Causality: FAIL
Correction Registration Causality: FAIL
Pre-registry Commit Success Contract: FAIL
External Bootstrap Anchor Protocol: FAIL
Bootstrap Commit Resolution: FAIL
Mode-specific Resolution Truth Tables: FAIL
Freeze Reference Resolution Stable Key: FAIL
Boundary Completeness Qualification: FAIL
Known Model-level Blockers: FOUR_BOUNDED_BLOCKERS
Proposal Completeness: PASS_WITH_BLOCKERS
Bootstrap Closure: FAIL
Independent Model Review: PASS_WITH_FOUR_BOUNDED_BLOCKERS
WS-01 Exit Eligibility: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
```

## 独立决定

1. 接受 `CR-0004` 的主体结构、单一目的和历史保护模型；
2. 不接受当前提案为模型闭合的 `WS-01` 候选；
3. 将结果登记为 `PASS_WITH_FOUR_BOUNDED_BLOCKERS`；
4. 下一阶段建立 `CR-0004-R1`，只修复 B1 至 B4；
5. R1 不得扩张到 `WS-02`、通用资格、业务决策或通用提交治理；
6. 保留 `CR-0004` 原文和本审查作为不可覆盖历史；
7. R1 完成后必须另行执行独立模型与启动闭环复审；
8. 复审通过前不进入实现、经验性证据采集或冻结准备；
9. 本轮不创建注册表、冻结账本、冻结标识、运行时权威或制度冻结。
