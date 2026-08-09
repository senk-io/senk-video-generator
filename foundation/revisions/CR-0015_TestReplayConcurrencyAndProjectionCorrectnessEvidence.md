# CR-0015 测试、回放、并发与投影正确性证据

## 执行信息

```text
Execution Review ID: CR-0015-TEST-REPLAY-CONCURRENCY-AND-PROJECTION-CORRECTNESS-EVIDENCE
Status: COMPLETED
Result: PASS_AS_NON_AUTHORITATIVE_CORRECTNESS_EVIDENCE
Runtime Mode: NON_AUTHORITATIVE_CONFORMANCE
Executable: EVIDENCE_ONLY
Model and Interface Basis: CR-0013-R1
Implementation Evidence Basis: CR-0014-R1
Evidence Execution ID: CR-0015-CORRECTNESS-001
Implementation Version: governance-kernel/0.2.0+sha256:4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Test Harness Digest: ff23fbb660be2280e1e285cd6cf83d773cd7b240eeb504c417eb6a184747ee3e
Evidence Package Digest: 9e9aa60f5b62da95cbc81d21135c4b6a0460d62061b3140509292d7ec35263bc
Evidence Algorithm: SHA-256
Formal Fact Created: NO
Institution Freeze Created: NO
Runtime Institution Authority Created: NO
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
Next Required Stage: Cross-context and migration evidence
```

> 本文件记录本地单机、固定实现版本和证据专用测试授权下的正确性观察。通过结果证明本轮有界运行合同成立，不证明跨提供方、跨项目、跨领域或迁移条件已经成立，也不创建制度冻结。

## 一、本轮证据合同

本轮将四类不同性质的证据分别执行和保存：

```text
Unit and Negative-path Tests
Deterministic Replay
Thread and Process Concurrency
Projection Correction, Downgrade, Rebuild, Publication and Deletion
```

通过门槛为：

1. 单元与负向测试必须在资源警告提升为错误的条件下全部通过；
2. 相同输入、实现版本、提案版本、时钟序列和作用域的五次全链回放必须得到完全相同的表级导出与事件链；
3. 同一终态槽的并发写入必须只有一次首次接受，同载荷其余请求幂等，异载荷其余请求进入冲突记录；
4. 来源更正导致闭包不完整时，确定性投影必须失败关闭，只允许不确定或冲突结果；
5. 发布载荷必须与已登记审计的业务载荷内容同一，同时允许发布记录携带自身前驱历史；
6. 删除必须依赖已登记重建要求，且删除记录不得删除审计、发布或更正历史；
7. 所有数据库、事件链和证据清单必须通过独立只读复算。

## 二、实现边界加固

### 2.1 业务载荷与记录内容摘要分离

运行内核现在分别保存：

```text
Payload Digest = digest(canonical business payload)
Content Digest = digest(canonical business payload + predecessor record identity)
```

这一区分使发布封套可以同时满足两项要求：

- 与变化审计保持完全相同的业务载荷摘要；
- 以不同内容摘要保存发布记录自己的前驱关系。

因此没有通过删除前驱字段来伪造内容同一，也没有把记录历史混入业务载荷同一判断。

### 2.2 投影控制记录

受保护写入目录由 11 种核心类型扩展到 13 种，新增：

```text
Registered Projection Rebuild Requirement
Registered Projection Deletion Record
```

两者分别要求精确的来源、闭包完整性、发布和重建前置。内核还验证：

- 投影审计声明的闭包完整性必须与其已登记前置一致；
- 重建触发来源、闭包和前一发布必须与前置记录逐项一致；
- 删除目标发布和重建要求必须与前置记录逐项一致；
- 非完整闭包不能支持 `COMMITTED` 或 `ABORTED` 形式的确定性投影；
- 初始投影使用规范启动标记，后继投影必须固定前一发布和前一坐标摘要。

## 三、测试证据

执行命令：

```text
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

结果：

```text
Tests Run: 14
Failures: 0
Errors: 0
Resource Warnings: 0
Result: PASS
```

除 `CR-0014` 已有的授权、作用域、前置、幂等、冲突、追加式更正、数据库不可变性和正式模式拒绝外，本轮新增验证：

- 非完整闭包拒绝确定性投影；
- 后继审计与发布保持业务载荷同一，同时保留各自历史身份；
- 投影删除只追加删除事实，不移除既有审计和发布历史。

## 四、确定性回放

固定输入执行标识：

```text
CR-0015-CORRECTNESS-001:deterministic-input
```

五次独立数据库从空状态开始，分别安装相同证据授权、执行相同九工作流链和完整投影生命周期。结果：

```text
Replay Count: 5
Attempt Count per Replay: 22
Protected Record Count per Replay: 18
Conflict Count per Replay: 1
Unique Export Signature Count: 1
Unique Database File Digest Count: 1
Event Hash-chain Failure Count: 0
Result: PASS
```

规范表级导出摘要：

```text
f091e22698c2bd2b66a0ed55f67a34b69f544ce254a28be863c1520cd7155615
```

五个数据库文件摘要均为：

```text
609b7592a77dea95970938a99f5b4fb7fb206d8ddcc83f09ba1601657ee400d7
```

因此在本地固定输入、固定版本和固定时钟边界内，重复性与稳定性成立。该结论不能外推为跨运行时提供方稳定性。

## 五、并发证据

| 并发模式 | 场景 | 请求数 | 首次接受 | 幂等 | 冲突 | 终态记录数 | 结果 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 线程 | 同键同载荷 | 32 | 1 | 31 | 0 | 1 | `PASS` |
| 线程 | 同键异载荷 | 32 | 1 | 0 | 31 | 1 | `PASS` |
| 进程 | 同键同载荷 | 16 | 1 | 15 | 0 | 1 | `PASS` |
| 进程 | 同键异载荷 | 16 | 1 | 0 | 15 | 1 | `PASS` |

四组运行均独立初始化数据库并共享同一终态槽。数据库事务和唯一约束使首次接受者取得槽位；后续同内容请求返回既有记录，后续异内容请求保存竞争载荷与原记录摘要，不覆盖原记录。

```text
Single Terminal Assignment: PASS
Same-payload Convergence: PASS
Different-payload Conflict Preservation: PASS
Broken Event Chain Count: 0
```

## 六、投影生命周期证据

本轮按以下顺序执行：

```text
Initial Complete Closure
  -> Initial COMMITTED Audit
  -> Initial Publication
  -> Source Correction
  -> Corrected Dependency Closure
  -> INCOMPLETE Closure Completeness
  -> Projection Rebuild Requirement
  -> Reject COMMITTED Projection
  -> Accept INDETERMINATE Audit
  -> Preserve Competing Transition as Conflict
  -> Publish Content-identical Successor
  -> Reject Mismatched Publication
  -> Register Deletion of Obsolete Cache Projection
  -> Reject Deletion without Rebuild Requirement
```

观察计数：

| 结果 | 数量 |
| --- | ---: |
| `ACCEPTED_EVIDENCE_ONLY` | 18 |
| `CONFLICT_RECORDED` | 1 |
| `REJECTED_INVALID_PAYLOAD` | 1 |
| `REJECTED_CONTENT_IDENTITY_MISMATCH` | 1 |
| `REJECTED_MISSING_PREREQUISITE` | 1 |

终局状态：

```text
Projection Audit Records: 2
Projection Publication Envelopes: 2
Projection Rebuild Requirements: 1
Projection Deletion Records: 1
Audit / Publication Business Payload Digest: EQUAL
Audit / Publication Full Content Digest: DISTINCT
Prior Publication Preserved: YES
Prior Audit Preserved: YES
Rebuild Requirement Preserved: YES
Deletion Record Preserved: YES
Protected Record Removed by Deletion Registration: 0
Result: PASS
```

删除记录描述已废弃缓存投影的受保护删除事实；它没有对追加式保护表执行物理删除。

## 七、证据包

证据目录：

```text
evidence/runtime/CR-0015-CORRECTNESS-001/
```

包内包含：

- 单元测试输出和结构化汇总；
- 回放、并发和投影结构化汇总；
- 五个确定性回放数据库；
- 四个线程／进程并发数据库；
- 输入清单、总体汇总和摘要清单。

所有 16 个被清单覆盖的文件在固化后设置为只读。清单自身不进入自摘要，规范包摘要为：

```text
9e9aa60f5b62da95cbc81d21135c4b6a0460d62061b3140509292d7ec35263bc
```

独立只读检查得到：

```text
Manifested File Digest Mismatch Count: 0
SQLite Database Count: 9
SQLite Integrity Failure Count: 0
SQLite Journal Mode: delete for 9 / 9
Unmanifested WAL / SHM Sidecar Count: 0
Event Count Reviewed: 206
Broken Previous-hash Link Count: 0
Broken Event Digest Count: 0
Append-only Trigger Count: 90
Non-conformance Protected Record Count: 0
```

## 八、IF-0007 边界

`IF-0007` 要求运行样本支持对以下性质的独立评估：

| 证据维度 | 本轮状态 | 边界 |
| --- | --- | --- |
| 重复 | `PASS_IN_FIXED_LOCAL_CONTEXT` | 五次从空状态全链回放 |
| 稳定 | `PASS_IN_FIXED_LOCAL_CONTEXT` | 表级导出和数据库字节均一致 |
| 跨提供方 | `MISSING` | 只有一个本地运行实现 |
| 跨项目 | `MISSING` | 未取得另一个独立项目样本 |
| 跨领域 | `MISSING` | 未取得另一个现实领域样本 |
| 迁移 | `MISSING` | 未执行版本、存储或合同迁移 |

本轮不能用进程并发冒充跨提供方，不能用九工作流类型差异冒充跨领域，也不能用空库重放冒充迁移。

## 九、当前决定

```text
Unit and Negative-path Tests: PASS
Deterministic Replay: PASS_IN_FIXED_LOCAL_CONTEXT
Thread Concurrency: PASS
Process Concurrency: PASS
Projection Correctness: PASS_FOR_REVIEWED_LIFECYCLE
Evidence Package Integrity: PASS
Residual Correctness-stage Blocking Finding Count: 0
Correctness Evidence Substage Exit: PASS
Full IF-0007 Evidence: NOT_COMPLETE
Freeze Review Eligibility: NO
Applicable Freeze Authority: NOT_ESTABLISHED
Institution Freeze: NOT_CREATED
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
Next Required Stage: CROSS_CONTEXT_AND_MIGRATION_EVIDENCE_REQUIRED
```

准确状态是：本地固定上下文内的测试、重复回放、线程／进程并发和投影正确性证据已经闭环；跨提供方、跨项目、跨领域和迁移证据尚未建立，因而还不能进入冻结权威建立或冻结审查。
