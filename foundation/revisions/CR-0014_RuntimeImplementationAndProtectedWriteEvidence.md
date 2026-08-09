# CR-0014 九工作流运行实现与受保护写入证据

## 执行信息

```text
Execution Review ID: CR-0014-RUNTIME-IMPLEMENTATION-AND-PROTECTED-WRITE-EVIDENCE
Status: COMPLETED
Result: PASS_AS_NON_AUTHORITATIVE_IMPLEMENTATION_EVIDENCE
Runtime Mode: NON_AUTHORITATIVE_CONFORMANCE
Executable: EVIDENCE_ONLY
Model and Interface Basis: CR-0013-R1
Evidence Execution ID: CR-0014-PW-004
Superseded Preliminary Execution IDs: CR-0014-PW-001 + CR-0014-PW-002 + CR-0014-PW-003
Implementation Version: governance-kernel/0.1.0+sha256:f273f81f789b38c656749340a5d2894c7594bfc7519869248b997b384eafa8ce
Evidence Package Digest: 77d45a57a976ffdb790c8759206f541de9e21fd95c0c2fce959043776ae6846c
Evidence Algorithm: SHA-256
Formal Fact Created: NO
Institution Freeze Created: NO
Runtime Institution Authority Created: NO
Next Required Stage: Test, replay, concurrency and projection-correctness evidence package
```

> 本文件记录真实运行实现和受保护写入观察。实现只运行于非权威证据模式；它验证候选接口约束，不把未冻结提案当作现行制度，也不创建任何正式业务或制度事实。

## 一、实现边界

现有仓库在本阶段前只有制度、执行和领域文档，没有运行代码或存储设施。本轮新增：

```text
runtime/governance/catalog.py
runtime/governance/kernel.py
tools/run_protected_write_evidence.py
tests/test_governance_kernel.py
```

运行内核使用标准库和 SQLite，提供：

- 九工作流精确类型、权威类型、提案版本和提案复合摘要目录；
- 精确持有者、权威类型、记录类型和作用域授权检查；
- 跨工作流已登记前置记录检查；
- 同语义键同载荷幂等；
- 同语义键异载荷冲突保留；
- 追加式更正和前驱引用；
- 审计载荷与发布载荷内容同一检查；
- 数据表更新和删除阻断触发器；
- 每次写入尝试的连续哈希证据链；
- 运行实现版本钉死，禁止一个数据库混用不同实现版本；
- 正式运行模式硬拒绝。

## 二、受保护写入目录

| 工作流 | 核心受保护记录 | 精确登记权威 | 前置边界 |
| --- | --- | --- | --- |
| `WS-01` | `Registered Institution Registry Entry` | `InstitutionRegistryEntryRegistrationAuthorityType` | 无运行前置；仅证据模式 |
| `WS-02` | `Registered Source Record` | `SourceRecordRegistrationAuthorityType` | `WS-01` |
| `WS-03` | `Registered Temporal Mapping Record` | `TemporalMappingRegistrationAuthorityType` | `WS-01` |
| `WS-04` | `Registered Atomic Qualification Resolution` | `QualificationResolutionRegistrationAuthorityType` | `WS-02`、`WS-03` |
| `WS-05` | `Registered Authority Applicability Consumer Resolution` | `ConsumerResolutionFinalRegistrationAuthorityType` | `WS-02`、`WS-03` |
| `WS-06` | `Registered Proof Applicability Record` | `ProofApplicabilityAtomicRegistrationAuthorityType` | `WS-04`、`WS-05` |
| `WS-07` | `Registered Derived Record Envelope` | `DerivedRecordEnvelopeRegistrationAuthorityType` | `WS-01`、`WS-02`、`WS-03`、`WS-06` |
| `WS-08` | `Registered Dependency Closure Record` | `DependencyClosureRegistrationAuthorityType` | `WS-02`、`WS-03`、`WS-07` |
| `WS-08` | `Registered Closure Completeness Record` | `ClosureCompletenessRegistrationAuthorityType` | 已登记闭包 |
| `WS-09` | `Registered Projection Change Audit Record` | `ProjectionChangeAuditRegistrationAuthorityType` | `WS-03`、`WS-07`、完整 `WS-08` 闭包 |
| `WS-09` | `Projection Publication Envelope` | `ProjectionPublicationEnvelopeRegistrationAuthorityType` | 内容同一的已登记审计 |

这是首批核心受保护写入切片，不声称已实现每个模型中的全部辅助目录、边界和聚合类型。未知类型一律失败关闭。

## 三、单次写入证据合同

每个 `write_attempts` 事件实际保存：

```text
Execution ID
Implementation Version
Institution Proposal Version and Digest
Principal ID
Workflow and Record Type
Semantic Key and Payload Digest
Input References and Output Reference
Authority and Scope References
Observed At and Recorded At
Expected and Observed Behavior
Failure-closed Result
Previous Event Hash and Event Hash
Evidence Mode
```

因此 `CR-0013-R1` 要求的执行标识、实现版本、提案版本、输入输出、权威作用域、双时间、不可变证据摘要、预期／观察行为和失败关闭结果均进入真实运行记录。

## 四、证据执行

### 4.1 前三次运行

`CR-0014-PW-001` 完成首轮证据后，代码复审发现两个应在终局证据前加固的边界：

1. 已存在数据库必须拒绝混入另一个实现版本；
2. 应显式保存作用域不匹配、正式模式、未知类型和发布载荷不一致的负向证据。

原证据包未删除或覆盖；`CR-0014-PW-002` 以追加式执行明确取代它。

对 `CR-0014-PW-002` 执行只读复查时，SQLite 的日志模式生成了未进入包清单的旁路文件。数据库内容和既有清单摘要没有损坏，但“目录内所有证据文件均受清单覆盖”的封装闭包不再成立。因此该运行也被保留为历史，不能作为终局证据包。

`CR-0014-PW-003` 在固化前完成日志检查点并切换到 `DELETE` 日志模式。独立只读复查前后，目录文件集合保持完全相同。提交前差异校验随后发现源码末尾格式需要修正；该修正会改变实现复合摘要。为确保提交后的最终源码与证据声明完全一致，执行器改为支持外部运行标识，并用最终源码追加 `CR-0014-PW-004`。`PW-003` 仍保留为已经通过内容检查、但不再对应最终源码摘要的历史运行。

### 4.2 终局运行

```text
Execution ID: CR-0014-PW-004
Started At: 2026-08-09T07:54:26.217288Z
Completed At: 2026-08-09T07:54:26.277207Z
Protected Record Types Covered: 11
Workstreams Covered: 9 / 9
Write Attempts: 59
Accepted Evidence-only Records: 12
Conflicts Preserved: 11
```

实际结果计数：

| 结果 | 数量 |
| --- | ---: |
| `ACCEPTED_EVIDENCE_ONLY` | 12 |
| `IDEMPOTENT_EXISTING` | 11 |
| `CONFLICT_RECORDED` | 11 |
| `REJECTED_UNAUTHORIZED` | 12 |
| `REJECTED_MISSING_PREREQUISITE` | 10 |
| `REJECTED_CONTENT_IDENTITY_MISMATCH` | 1 |
| `REJECTED_INVALID_PAYLOAD` | 1 |
| `REJECTED_UNKNOWN_TYPE` | 1 |

## 五、强制不变量结果

```text
Unauthorized Write Rejected: PASS
Scope Mismatch Rejected: PASS
Formal Runtime Mode Rejected: PASS
Unknown Type Rejected: PASS
Missing Prerequisite Rejected: PASS
Same Key + Same Payload Idempotent: PASS
Same Key + Different Payload Conflict-preserving: PASS
Terminal Slot Overwrite Prevented: PASS
Correction and Supersession History Preserved: PASS
Projection Publication Content-identical: PASS
Projection Publication Mismatch Rejected: PASS
Append-only UPDATE Guard: PASS
Append-only DELETE Guard: PASS
Event Hash Chain: PASS
SQLite Integrity: PASS
Formal Record Count: 0
```

## 六、证据包

终局证据目录：

```text
evidence/runtime/CR-0014-PW-004/
```

| 文件 | 内容 |
| --- | --- |
| `input_manifest.json` | 执行、实现、提案摘要、作用域和非权威边界 |
| `authority_grants.jsonl` | 证据专用测试授权，不是制度授权 |
| `write_attempts.jsonl` | 59 项追加式尝试和事件哈希 |
| `protected_records.jsonl` | 12 项被接受的证据模式记录 |
| `write_conflicts.jsonl` | 11 项同键异载荷冲突 |
| `immutability_checks.json` | 更新、删除阻断观察 |
| `governance.db` | 只读 SQLite 运行状态和追加式触发器 |
| `summary.json` | 执行计数和观察摘要 |
| `manifest.json` | 文件摘要和规范包摘要 |

所有包内文件生成后被设置为只读。独立复算得到：

```text
Package Digest: 77d45a57a976ffdb790c8759206f541de9e21fd95c0c2fce959043776ae6846c
Manifest Verification: PASS
SQLite Integrity Check: PASS
SQLite Journal Mode: DELETE
File Set Stable Before / After Read-only Review: PASS
59-event Hash-chain Verification: PASS
```

只读权限和摘要用于检测变化，不等于制度封印、签名存储或正式冻结。

## 七、基础实现测试

运行命令：

```text
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

结果：

```text
Tests Run: 11
Failures: 0
Errors: 0
Resource Warnings: 0
Result: PASS
```

这些测试用于验证实现能产生可信受保护写入证据，不替代下一阶段的重复回放、并发竞争和完整投影正确性证据。

## 八、当前决定

```text
Nine-workstream Core Protected-write Substrate: IMPLEMENTED
Protected-write Evidence: PASS
Implementation Compatibility for Evidence Slice: PASS
Formal Runtime Eligibility: NO
Formal Institution Facts Created: NO
Institution Freeze: NOT_CREATED
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
Next Required Substage: TEST_REPLAY_CONCURRENCY_PROJECTION_CORRECTNESS_EVIDENCE_REQUIRED
```

本阶段证明核心受保护写入底座可以按候选接口失败关闭。它不证明高并发、跨进程回放、跨提供方、跨项目、跨领域、迁移或完整投影重建已经正确。
