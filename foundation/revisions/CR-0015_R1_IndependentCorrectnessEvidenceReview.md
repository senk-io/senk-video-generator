# CR-0015-R1 测试、回放、并发与投影正确性证据独立复审

## 复审信息

```text
Review ID: CR-0015-R1-INDEPENDENT-CORRECTNESS-EVIDENCE-REVIEW
Review Type: Independent Read-only Correctness Evidence Review
Status: COMPLETED
Result: PASS_FOR_BOUNDED_CORRECTNESS_EVIDENCE_STAGE
Reviewed Execution: CR-0015-CORRECTNESS-001
Reviewed Implementation: governance-kernel/0.2.0+sha256:4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Reviewed Test Harness Digest: ff23fbb660be2280e1e285cd6cf83d773cd7b240eeb504c417eb6a184747ee3e
Reviewed Package Digest: 9e9aa60f5b62da95cbc81d21135c4b6a0460d62061b3140509292d7ec35263bc
Review Basis: CR-0015
Reviewer: Codex
Review Authority: User-delegated evidence review authority
Review Independence: CR-0015 summary assertions were ignored; source, harness, files and databases were re-evaluated read-only
Residual Correctness-stage Blocking Finding Count: 0
Institution Freeze Created: NO
Runtime Institution Authority Created: NO
Next Authorized Stage: Cross-context and migration evidence
```

> 本复审只判断 `CR-0015` 有界正确性证据阶段是否可以退出。它不把本地回放外推为跨提供方、跨项目、跨领域或迁移证据，也不执行冻结资格审查。

## 一、独立复算

### 1.1 实现与测试执行器

复核器重新读取并按路径排序复算实现来源：

```text
runtime/governance/catalog.py
runtime/governance/kernel.py
```

```text
Observed Implementation Digest: 4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Declared Implementation Digest: 4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Result: MATCH
```

随后独立复算测试执行器来源：

```text
tests/test_governance_kernel.py
tools/run_correctness_evidence.py
```

```text
Observed Test Harness Digest: ff23fbb660be2280e1e285cd6cf83d773cd7b240eeb504c417eb6a184747ee3e
Declared Test Harness Digest: ff23fbb660be2280e1e285cd6cf83d773cd7b240eeb504c417eb6a184747ee3e
Result: MATCH
```

### 1.2 证据包

独立复算 `manifest.json` 声明的 16 个文件摘要，并重新构造规范包摘要：

```text
Observed Package Digest: 9e9aa60f5b62da95cbc81d21135c4b6a0460d62061b3140509292d7ec35263bc
Declared Package Digest: 9e9aa60f5b62da95cbc81d21135c4b6a0460d62061b3140509292d7ec35263bc
Manifest Digest Mismatch Count: 0
Unexpected or Missing File Count: 0
Result: MATCH
```

### 1.3 数据库与事件链

九个数据库全部以只读不可变方式打开。复算结果：

```text
SQLite Database Count: 9
Integrity Check = ok: 9 / 9
Journal Mode = delete: 9 / 9
Unmanifested WAL / SHM Sidecar Count: 0
Event Count: 206
Broken Previous-hash Link Count: 0
Broken Event Digest Count: 0
Append-only Trigger Count: 90
Non-conformance Protected Record Count: 0
Formal Fact Creation Metadata: PROHIBITED for 9 / 9
Result: PASS
```

## 二、测试与回放复审

单元测试原始输出包含 14 项独立测试名称，结尾计数为：

```text
Ran 14 tests
OK
```

未观察到失败、错误或资源警告。

五个回放数据库不仅结构化导出摘要相同，数据库文件字节摘要也完全相同：

```text
Replay Database Count: 5
Unique Structured Export Digest Count: 1
Unique Database File Digest Count: 1
Per-replay Event Count: 22
Per-replay Protected Record Count: 18
Result: PASS_IN_FIXED_LOCAL_CONTEXT
```

这足以确认固定本地上下文下的确定性，但不证明另一个实现、提供方或项目会产生相同结果。

## 三、并发复审

复核器没有读取并发汇总作为事实，而是直接查询四个数据库中的写入尝试、保护记录和冲突记录：

| 数据库 | 观察结果 | 保护记录 | 冲突记录 | 结论 |
| --- | --- | ---: | ---: | --- |
| `thread-idempotent.db` | 1 接受 + 31 幂等 | 1 | 0 | `PASS` |
| `thread-conflict.db` | 1 接受 + 31 冲突 | 1 | 31 | `PASS` |
| `process-idempotent.db` | 1 接受 + 15 幂等 | 1 | 0 | `PASS` |
| `process-conflict.db` | 1 接受 + 15 冲突 | 1 | 15 | `PASS` |

所有请求都收敛到同一既有记录标识，异载荷竞争没有创建第二个终态记录或覆盖首次接受内容。

```text
Single-assignment Under Reviewed Concurrency: PASS
Idempotency Under Reviewed Concurrency: PASS
Conflict Preservation Under Reviewed Concurrency: PASS
Lost Conflict Evidence Observed: NO
```

## 四、投影正确性复审

复核器直接从首个回放数据库重建投影记录关系。观察到：

```text
Projection Audit Count: 2
Projection Publication Count: 2
Projection Rebuild Requirement Count: 1
Projection Deletion Record Count: 1
```

关系检查：

1. 后继发布以前一发布为前驱；
2. 后继发布只引用后继变化审计；
3. 后继审计与发布的业务载荷摘要相同；
4. 两者完整内容摘要不同，证明各自历史身份未被抹除；
5. 重建要求固定更正后的来源、闭包和前一发布；
6. 删除记录固定旧发布与重建要求；
7. 旧审计、旧发布、新审计、新发布、重建和删除记录同时存在。

负向路径重新计数得到：

```text
Non-complete + Determinate Projection Rejection: 1
Same-transition Competing Payload Conflict: 1
Publication Content-identity Mismatch Rejection: 1
Deletion without Rebuild Rejection: 1
```

```text
Correction History: PASS
Downgrade on Incomplete Closure: PASS
Transition Conflict Preservation: PASS
Audit / Publication Business Content Identity: PASS
Rebuild Requirement Pinning: PASS
Deletion Precondition: PASS
Deletion History Preservation: PASS
```

## 五、发现与边界

### 5.1 本阶段阻断

未发现能够否定本地有界正确性结论的实现、证据或封装问题。

```text
Correctness-stage Blocking Finding Count: 0
```

### 5.2 后续证据缺口

以下项目没有被本轮证据覆盖：

- 不同运行时或存储提供方的相同合同执行；
- 独立项目中的相同制度合同消费；
- 与当前视频生成领域不同的现实领域样本；
- 实现版本、数据格式、存储或制度合同迁移；
- 外部签名、时间戳或制度封印存储；
- 适用冻结权威、独立冻结审查和正式冻结决定。

这些不是本轮正确性阶段的失败，但继续阻断完整 `IF-0007` 证据和冻结资格。

## 六、终局裁决

```text
Unit and Negative-path Evidence: PASS
Deterministic Replay Evidence: PASS_IN_FIXED_LOCAL_CONTEXT
Thread Concurrency Evidence: PASS
Process Concurrency Evidence: PASS
Projection Lifecycle Evidence: PASS_FOR_REVIEWED_LIFECYCLE
Evidence Package Integrity: PASS
Residual Correctness-stage Blockers: 0
Correctness Evidence Stage Exit: PASS
Repeated Evidence: PASS_IN_FIXED_LOCAL_CONTEXT
Stable Evidence: PASS_IN_FIXED_LOCAL_CONTEXT
Cross-provider Evidence: MISSING
Cross-project Evidence: MISSING
Cross-domain Evidence: MISSING
Migration Evidence: MISSING
Full IF-0007 Evidence: NOT_COMPLETE
Freeze Review Eligibility: NO
Applicable Freeze Authority: NOT_ESTABLISHED
Institution Freeze: NOT_CREATED
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
Next Authorized Stage: CROSS_CONTEXT_AND_MIGRATION_EVIDENCE_REQUIRED
```

准确状态是：`CR-0015` 的测试、回放、并发和投影正确性证据通过独立只读复审，本阶段可以退出；总体制度冻结仍被跨提供方、跨项目、跨领域和迁移现实证据阻断。
