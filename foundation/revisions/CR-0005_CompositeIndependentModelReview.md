# CR-0005 来源注册表复合模型独立审查

## 审查信息

```text
Review ID: CR-0005-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Review
Status: COMPLETED
Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 + CR-0005-R2 + CR-0005-R3
Cross-interface Baseline: CR-0005-R3-CR-0006-R2-TERMINAL-CROSS-INTERFACE-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-checks and cross-interface pass do not establish internal model completeness
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只审查来源注册表复合模型自身是否完整、稳定、可重放且失败关闭。它不重新审查 `CR-0006` 时间模型，不修改被审提案，也不创建来源注册表、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 来源注册表根身份与契约是否拥有可启动、可登记且无自授权的稳定链；
2. 来源身份、版本、记录和位置是否具有不可逃逸的冲突域；
3. 来源边界与快照是否可重放且不自证完整；
4. 完整性记录是否能跨不同证据集合聚合冲突；
5. 开放世界和关闭世界是否保持合格否定边界；
6. 来源适用性变化是否能跨不同决定事实进入同一语义竞争集合；
7. 更正、多注册表向量和当前读面是否保持追加与非权威；
8. 原始时间断言与时间查询坐标消费是否发生回归；
9. `WS-01` 引用兼容和终局交叉接口结论是否仍成立；
10. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 RAW TEMPORAL ASSERTION AND COORDINATE CLOSURE
CR-0005-R2 COORDINATE REGISTRATION RESOLUTION PINNING
CR-0005-R3 FOUR-VALUE COORDINATE SUBJECT CLOSURE
All CR-0005 / CR-0006 cross-interface review records
Local repository state at review time
```

提案自检、文件存在、作者身份、交叉接口通过和规则数量均不作为内部模型通过依据。

## 总体裁决

复合模型已经建立可靠的来源边界主干：

```text
Source Record + Raw Temporal Assertions
  -> atomic append position
  -> Registered Source Boundary
  -> Registered Source Snapshot
  -> independent dimensional completeness
  -> Registered Multi-registry Source Boundary Vector
  -> time-coordinate consumption
  -> Registered Source Applicability Resolution
```

以下模型方向通过：

```text
Single-purpose Boundary: PASS
Authority Non-propagation Direction: PASS
Source Record Candidate / Registration Identity: PASS
Append-only Position Direction: PASS
Boundary Stable Key: PASS
Snapshot Stable Key and Reproducibility: PASS
Snapshot Digest Non-self-proof: PASS
Open-world Absence Safety: PASS
Closed-world Independent Closure Evidence: PASS
Multi-registry Conflict Preservation: PASS
Raw Temporal Assertion Atomic Handoff: PASS
Temporal Query Coordinate Consumption: PASS
Cross-interface Compatibility: PASS
WS-01 Reference Direction: PASS_AS_DRAFT
```

但四个内部语义竞争域尚未闭合：

1. 注册表根身份与契约缺少分配、登记及完整否定解析；
2. 来源身份、版本和记录可以通过新记录 ID 或位置逃离同一语义冲突集合；
3. 完整性键包含证据集合摘要，不同证据集合的矛盾结论不会自动竞争；
4. 来源适用性变化键包含决定事实 ID，不同决定可以逃离同一生命周期竞争集合。

因此：

```text
Authoritative Provider-side Contract: FAIL_WITH_BOUNDED_BLOCKER
Source Identity and Stable Position: FAIL_WITH_BOUNDED_BLOCKER
Snapshot Reproducibility: PASS
Completeness Non-self-proof Direction: PASS
Completeness Conflict Aggregation: FAIL_WITH_BOUNDED_BLOCKER
Open-world / Closed-world Boundary: PASS
Multi-registry Conflict Preservation: PASS
Source Applicability Conflict Aggregation: FAIL_WITH_BOUNDED_BLOCKER
WS-01 Reference Compatibility: PASS_AS_DRAFT
Cross-interface Gate: PASS
Independent Model Review: FAIL
CR-0005-R4 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
```

## 一、已通过：来源边界、快照和世界模式

来源边界键固定：

```text
Source Registry ID and Version
Source Registry Domain
Registry Scope Digest
World Boundary Mode
Position Range or Exact Record Set Digest
Boundary Rule Version
```

快照键在精确已登记边界之上固定规范化与摘要规则版本，摘要覆盖成员、版本、记录摘要、位置或精确集合、作用域、世界模式、空洞和冲突引用。

快照摘要明确不能自证完整；来源边界本身也不包含完整性、快照或下游解析结果。

```text
Boundary / Snapshot Separation: PASS
Boundary Candidate / Registration Chain: PASS
Snapshot Candidate / Registration Chain: PASS
Canonical Digest Coverage: PASS
Position-hole Preservation: PASS
Conflict-reference Coverage: PASS
```

世界模式封闭为：

```text
OPEN_WORLD
CLOSED_WORLD
PARTITIONED_CLOSED_WORLD
```

开放世界缺失不能证明不存在；关闭世界必须拥有精确作用域、关闭权威、关闭决定、迟到写禁止、冲突子域和独立证据。

```text
Open-world Exhaustive-negative Prohibition: PASS
Closed-world Closure Contract: PASS
Late-write Conflict Preservation: PASS
```

## 二、已通过：原始时间断言和时间消费

R1 已使原始时间断言成为来源记录的显式不可变子对象：

```text
Raw Temporal Assertion Key
Raw Temporal Assertion ID <-> one key
Parent Source Record Atomic Registration
Raw Assertion Set Digest
Snapshot-covered Assertion IDs and Payload Digests
```

R3 使来源适用性使用四值共有查询主体，并固定坐标登记解析 ID 和摘要。四个坐标分支不再伪造对象状态。

```text
Raw Assertion Stable Identity: PASS
Parent-child Atomicity: PASS
Time-model Ownership Boundary: PASS
Known At Type Closure: PASS
Coordinate Four-value Subject Totality: PASS
Historical / Current Applicability Separation: PASS
```

终局交叉接口审查的通过结论没有发现回归。

## 三、阻断 SR-M1：注册表根身份和契约登记链不完整

模型声明：

```text
Source Registry Identity Allocation Authority Type
Source Registry Contract Registration Authority Type
Source Registry Contract Key
```

但没有定义：

```text
Source Registry ID Allocation Attempt
Source Registry ID Allocation Record
Source Registry ID Allocation Resolution Key
ALLOCATED | NOT_ALLOCATED | INDETERMINATE | CONFLICTED
Source Registry Contract Candidate
Contract Registration Attempt
Registered Contract Resolution
Contract Registry Boundary and Completeness
```

来源记录、位置、边界和快照全部依赖注册表 ID、版本与契约。仅声明权威类型和契约键不能证明该 ID 已被唯一分配、该版本已内容同一登记，或同键不存在另一不兼容契约。

### 反例

两个持有不同授权实例的执行者分别声称同一 `Source Registry ID + Version + Domain` 对应不同作用域或摘要规则。当前模型没有共同登记解析或完整注册表契约边界，可以让两份契约都成为后续来源记录的表面前置。

```text
Expected: registered CONFLICTED contract resolution
Current: no contract registration resolution
Result: SR-M1 reproduced
```

### 关闭条件

`CR-0005-R4` 必须建立：

1. 注册表 ID 分配候选、尝试、记录、不可复用和四值解析；
2. 注册表契约候选、登记尝试、内容同一和四值登记解析；
3. 契约注册表边界、必要完整性及合格 `NOT_REGISTERED`；
4. 只有 `ALLOCATED + REGISTERED` 可以产生下游注册表契约引用。

```text
SR-M1 Registry Root Bootstrap: BLOCKED
```

## 四、阻断 SR-M2：来源身份、版本和记录缺少共同冲突域

模型定义：

```text
Source Identity Key
Source Version Key
Candidate Source Record -> Registration Attempt -> Registered Source Record
```

并声明同一来源版本不同载荷必须 `CONFLICTED`。但模型没有定义来源身份分配记录和解析，也没有定义把不同 `Source Record ID`、位置或登记尝试聚合到同一来源版本语义竞争域的稳定键。

缺少：

```text
Source Identity Allocation Resolution Key
Source Identity non-reuse record
Source Version Semantic Conflict Set Key
Source Record Registration Aggregate Resolution Key
complete competing-record boundary
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

### 反例

同一 `Source Identity + Source Version ID` 分别产生载荷 A 和 B：

```text
Record RA at Position 10 -> Payload A
Record RB at Position 11 -> Payload B
```

两者拥有不同记录 ID 和位置。规则要求冲突，但没有证据独立的共同冲突键与完整竞争边界，消费者可能只读取 RA 所在精确记录集合并将其视为唯一版本。

```text
Expected: registered CONFLICTED source-version resolution
Current: conflict direction without aggregate identity
Result: SR-M2 reproduced
```

### 关闭条件

R4 必须建立：

1. 来源身份分配与永久不复用解析；
2. 排除记录 ID、位置、记录时间和写入者的来源版本语义冲突键；
3. 完整竞争记录边界和聚合四值登记解析；
4. 位置分配结果与来源记录登记内容同一，空洞保留但不能换键；
5. 边界和快照只能消费已登记 `REGISTERED` 或显式 `CONFLICTED` 聚合结果。

```text
SR-M2 Source Identity / Version Conflict Domain: BLOCKED
```

## 五、阻断 SR-M3：完整性结论可以按证据集合换键

当前完整性键为：

```text
Source Boundary Completeness Key =
  Source Registry Boundary Key
+ Completeness Dimension
+ Completeness Rule Version
+ Evidence Set Digest
```

证据集合摘要进入语义键，使同一边界、同一维度和同一规则使用不同证据集合时产生不同键。

### 反例

```text
Evidence Set E1 -> READ_COMPLETENESS = COMPLETE
Evidence Set E2 -> READ_COMPLETENESS = INCOMPLETE
```

因为 `E1 != E2`，两个结论不必进入同一键。多注册表向量或时间完整性评价可能只引用 E1 记录，而不是得到一个权威 `CONFLICTED` 聚合结果。

`CONFLICT_SUBDOMAIN_COMPLETENESS` 可以证明相关冲突子域被读取，但当前模型没有定义“完整性记录自身”的证据独立竞争域和聚合解析，不能单靠该维度补齐身份。

### 关闭条件

R4 必须区分：

```text
Completeness Semantic Domain Key
  = boundary + dimension + semantic scope + rule version

Completeness Evidence Evaluation Key
  = semantic domain + governed evidence boundary

Completeness Aggregate Resolution Key
  = semantic domain + complete evaluation boundary + resolution rule
```

同一语义域不同证据评价必须进入完整聚合集合；不兼容确定结论为 `CONFLICTED`，缺失或评价边界不完整为 `INDETERMINATE`。向量和下游只能消费已登记聚合解析。

```text
SR-M3 Completeness Conflict Aggregation: BLOCKED
```

## 六、阻断 SR-M4：来源适用性变化可以按决定事实换键

当前变化键为：

```text
Source Applicability Change Key =
  Source Identity and Version
+ Applicability Change Domain
+ Effective Scope Digest
+ Valid From
+ Change Decision Fact ID
```

`Change Decision Fact ID` 进入键，会使两个针对同一来源、相同语义域、相同作用域和相同有效坐标的不兼容决定天然拥有不同键。

### 反例

```text
Decision D1 -> ACTIVATES source S at scope X
Decision D2 -> REVOKES source S at scope X
```

由于 `D1 != D2`，两个变化记录不是同键异载荷。来源适用性解析虽然消费精确变化集合并要求冲突变化失败关闭，但没有定义决策 ID 独立的竞争集合键、变化集合完整性和组合真值表。

查询者若只构造包含 D1 的“精确变化集合”，可能得到 `APPLICABLE`；包含 D1+D2 时得到 `CONFLICTED`，但模型没有证明前一集合为何是完整历史边界。

### 关闭条件

R4 必须建立：

```text
Source Applicability Change Conflict Set Key =
  Source Identity and Version
+ Applicability Semantic Domain
+ Effective Scope Digest
+ Canonical Valid Coordinate
+ Conflict Set Rule Version
```

该键必须排除决定事实 ID、记录 ID、登记时间、位置和写入者。还必须建立完整变化集合边界、候选—登记聚合解析及至少覆盖激活、暂停、退役、替代和撤销组合的冲突优先真值表。

来源适用性解析只能消费已登记、完整且内容同一的变化聚合解析。

```text
SR-M4 Applicability Change Conflict Domain: BLOCKED
```

## 七、已通过：多注册表、更正和读面方向

多注册表向量：

```text
Ordered Registry Boundary Entry Digests
+ Vector Scope Digest
+ Vector Rule Version
```

成员顺序由规则确定，不按读取完成顺序；跨注册表不兼容来源、现实绑定、适用性和更正必须保留，优先级或“最新”不能静默消除冲突。

```text
Multi-registry Stable Identity: PASS
Cross-registry Conflict Preservation: PASS
Vector Completeness Non-self-proof: PASS
```

更正只允许表示缺陷，追加双时间历史；当前读面只能从已登记来源、变化、更正、边界和时间坐标重建，删除读面不能反向修改来源事实。

```text
Semantic Correction Prohibition: PASS
Append-only Correction Direction: PASS
Rebuildable Current View: PASS
Projection Non-authority: PASS
```

这些通过项不关闭 SR-M1 至 SR-M4。

## 八、R4 修订边界

下一阶段应建立单一 `CR-0005-R4`，只关闭四项内部模型阻断。

允许修改：

- 注册表 ID 分配和契约登记解析；
- 来源身份分配、版本竞争域和记录聚合解析；
- 完整性语义域、证据评价和聚合解析；
- 来源适用性变化竞争域、完整历史边界和组合真值表；
- 相应权威类型、非法状态、自检和当前状态。

不得修改：

- 已通过的来源边界、快照、开放世界和关闭世界方向；
- 原始时间断言原子交接；
- 四值查询主体和坐标登记解析固定；
- 多注册表冲突保留；
- 终局交叉接口通过记录；
- `CR-0006` 时间模型；
- 任何实际注册表、账本、制度冻结或运行时权威。

## 九、退出门复核

```text
Authoritative Provider-side Contract: FAIL
Completeness Non-self-proof Direction: PASS
Completeness Conflict Aggregation: FAIL
Snapshot Reproducibility: PASS
Multi-registry Conflict Preservation: PASS
WS-01 Reference Compatibility: PASS_AS_DRAFT
Cross-interface Compatibility: PASS
Independent Model Review: FAIL
Internal Model Blockers: SR-M1 + SR-M2 + SR-M3 + SR-M4
WS-02 Model Exit: BLOCKED
Institution Freeze Readiness: NOT_ESTABLISHED
```

## 当前决定

```text
CR-0005 Composite Independent Model Review: COMPLETED
Review Result: PASS_WITH_FOUR_BOUNDED_BLOCKERS
Bounded Blockers: SR-M1 + SR-M2 + SR-M3 + SR-M4
CR-0005-R4 Required: YES
Cross-interface Gate: REMAINS_PASS
WS-02 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段应建立 `CR-0005-R4`，只关闭上述四项内部模型阻断；完成后执行 `CR-0005` 复合模型独立复审。
