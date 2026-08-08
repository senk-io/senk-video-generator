# CR-0006-R7 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 through CR-0006-R7
Repair Basis: CR-0006-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R7 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0006-R7` 对声明级证明聚合和 `T` 范围覆盖的修复。它不修改被审提案，不审查 `CR-0005-R8`，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 相同映射声明的有利与不利证明是否进入同一完整竞争域；
2. 映射竞争成员是否只能消费已登记声明级证明聚合；
3. `T` 范围是否枚举全部映射候选、声明级证明和合格成员；
4. 被消费聚合是否与 `T` 范围合格集合执行内容同一比较；
5. 覆盖结果是否作为评价子对象且不反向改变 `T`；
6. 新增证明记录类型是否获得既有封闭时间记录类型目录许可；
7. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 through CR-0006-R6
CR-0006-R7 CLAIM PROOF AND T-SCOPED COVERAGE CLOSURE
CR-0006-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级闭合声明均不作为通过依据。

## 总体裁决

R7 已关闭原两项残余语义逃逸：

```text
Claim-level Semantic Conflict Domain: PASS
Proof Payload Exclusion from Claim Key: PASS
Adverse Proof Common Competition: PASS
Claim Proof Candidate Registration: PASS
Claim Proof Boundary and Aggregate: PASS
Mapping Member Claim-proof Pinning: PASS
Exact All Mapping Candidates within T: PASS
Exact All Claim Proofs within T: PASS
Exact T-scoped Eligible Member Set: PASS
Aggregate / T-scoped Set Equality: PASS
Coverage Result Closure: PASS
M0 through M7 Acyclicity: PASS
```

但 R5 把 `Temporal Record Type -> Temporal Ledger Type` 映射明确封闭为七种记录。R6 与 R7 随后新增六种证明记录类型并写入 `Temporal Mapping Ledger`，却没有演进该封闭目录或固定新的已登记类型映射解析。因此声明级证明链虽有稳定业务键，仍没有合法时间记录类型资格。

因此：

```text
TM-R6-B1 Mapping Claim-level Proof Qualification Aggregation: CLOSED
TM-R6-B2 T-scoped Mapping Aggregate Coverage: CLOSED
Temporal Mapping Record Type Catalog Evolution: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R8 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：声明级不利证明共同竞争

R7 的映射声明语义键固定映射语义域、目标来源完整性域和适用区间，并明确排除候选键、候选载荷摘要、所有证明摘要、证据边界、结果、位置和登记时间。

全部同声明证明由统一候选、完整竞争边界和聚合解析处理：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
CONFLICTED
```

`QUALIFIED` 与 `NOT_QUALIFIED` 并存必须 `CONFLICTED`；候选级合格结果不再能绕过声明级聚合进入确定映射成员。

```text
Proof-payload-partitioned Semantic Domain: CLOSED
Adverse Candidate Filtering: PROHIBITED
Incomplete Claim Proof Boundary: INDETERMINATE
TM-R6-B1 Subject Repair: CLOSED
```

## 二、已通过：T 范围全域覆盖

R7 为每个 `T` 固定：

```text
Exact All Mapping Candidate Registration Resolution Set
Exact All Claim Proof Qualification Set
Exact T-scoped Eligible Mapping Member Set
Selected Aggregate Competing Boundary Eligible Member Set
Eligible-member Set Equality Proof
T Mapping-ledger Membership and Completeness Proof
```

覆盖资格要求集合相等，而不只要求旧聚合成员位于 `T` 内。历史 `T1` 可重放其完整聚合；当前 `T2` 新增同域候选或不利证明后必须重新计算覆盖、时间资格、评价和认识边界身份。

覆盖对象作为评价候选的内容同一子对象登记，不进入所验证的映射账本或 `T`，阶段保持单向。

```text
Old Subset Aggregate under Expanded T: COVERAGE_NOT_MATCHED
Membership-only Eligibility: PROHIBITED
Coverage Unknown: INDETERMINATE
Same Coverage Key / Incompatible Payload: CONFLICTED
TM-R6-B2 Subject Repair: CLOSED
```

## 三、有界阻断 TM-R7-B1：时间映射记录类型目录未演进

R5 的 `TM-R5-04` 明确规定记录类型映射“封闭为”七种类型，其中映射账本只允许：

```text
REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_CANDIDATE
REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_COMPETING_BOUNDARY
REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_AGGREGATE_RESOLUTION
  -> Temporal Ledger Type = MAPPING
```

R6 后续新增：

```text
REQUIRED_DIMENSION_MAPPING_PROOF_QUALIFICATION
REQUIRED_DIMENSION_MAPPING_PROOF_BOUNDARY
REQUIRED_DIMENSION_MAPPING_PROOF_AGGREGATE
```

R7 再新增：

```text
MAPPING_CLAIM_PROOF_QUALIFICATION
MAPPING_CLAIM_PROOF_BOUNDARY
MAPPING_CLAIM_PROOF_AGGREGATE
```

六种记录都被声明进入现有 `Temporal Mapping Ledger` 全局位置域，但 R6/R7 没有覆盖 `TM-R5-04`、没有建立已登记记录类型目录合同，也没有让位置、边界和完整性解析固定某个已登记目录版本。

### 反例

系统按 R5 封闭目录验证一个 R7 声明级证明候选：

```text
Temporal Record Type = MAPPING_CLAIM_PROOF_QUALIFICATION
Requested Temporal Ledger Type = MAPPING
```

该类型不在 R5 封闭映射中。若拒绝它，R7 声明级证明登记链无法完成；若直接接收它，则绕过了封闭目录约束，并使历史位置边界的类型解释依赖未登记的文本覆盖。

```text
Expected: every ledger record type has a governed catalog resolution
Current: proof record types rely on undeclared catalog expansion
Result: TM-R7-B1 reproduced
```

### 关闭条件

`CR-0006-R8` 必须二选一并保持历史边界可重放：

1. 定义时间记录类型目录合同的稳定 ID、版本和规范载荷；
2. 把 R5、R6、R7 的全部记录类型精确映射到既有账本类型和同一全局位置模型；
3. 形成目录候选、登记尝试、完整竞争边界和四值聚合解析；
4. 每个时间记录登记、账本边界和完整性解析固定已登记目录解析 ID 与摘要；
5. 旧目录继续解释旧边界，新目录只对新边界生效，禁止静默重解释历史位置；
6. 类型未分配、重复分配、同键异账本类型或目录完整性未知时必须失败关闭；
7. 或者明确把证明和覆盖对象降为既有合法记录载荷中的非账本子对象，不再声称独立时间记录。

```text
TM-R7-B1 Temporal Mapping Record Type Catalog Evolution: BLOCKED
Closure Owner: CR-0006-R8
```

## 四、回归与退出判定

未发现 R7 对以下既有方向造成其他内部回归：

```text
Global Temporal Position Model: PASS
Mapping Candidate / Boundary / Aggregate Identity: PASS
Required Dimension / Source-domain Alignment: PASS
Registered Source Completeness Aggregate Consumption: PASS
Correction / Migration Aggregate Identity: PASS
Temporal Governance Boundary Vector T: PASS
Knowledge Boundary Type Closure: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0006-R7 Independent Model Re-review: COMPLETED
Original Two Residual Blockers: CLOSED
New Residual Bounded Blockers: 1
CR-0006-R8 Required: YES
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
