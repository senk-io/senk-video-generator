# CR-0016-R1 运行证据数据库迁移独立复审

## 复审信息

```text
Review ID: CR-0016-R1-INDEPENDENT-MIGRATION-EVIDENCE-REVIEW
Review Type: Independent Read-only Migration Evidence Review
Status: COMPLETED
Result: PASS_FOR_REVIEWED_MIGRATION_PATH
Reviewed Execution: CR-0016-MIGRATION-001
Reviewed Source: CR-0014-PW-004
Reviewed Target Implementation: governance-kernel/0.2.0+sha256:4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Reviewed Migration Harness Digest: 46488fce8b7d578711a24dae3d52e11e5100dcf93cf863be90e646120c203f2d
Reviewed Package Digest: ee015cda57a52ed82a7fc67eab09e9f0611925d6249cc9c89c063324485020a2
Reviewer: Codex
Review Authority: User-delegated migration evidence review authority
Review Independence: CR-0016 summaries were ignored; source, migration result and relationships were reconstructed read-only
Residual Reviewed-path Blocking Finding Count: 0
Institution Freeze Created: NO
Next Authorized Stage: External cross-context evidence acquisition
```

> 本复审确认一个精确迁移路径，不确认任意未来版本、任意数据格式或任意提供方存储都可迁移。

## 一、源码与包摘要复算

当前运行实现摘要独立复算结果：

```text
Observed: 4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Declared: 4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Result: MATCH
```

迁移执行器复合摘要覆盖：

```text
runtime/governance/migration.py
migration_tests/test_v01_to_v02_migration.py
tools/run_migration_evidence.py
```

```text
Observed: 46488fce8b7d578711a24dae3d52e11e5100dcf93cf863be90e646120c203f2d
Declared: 46488fce8b7d578711a24dae3d52e11e5100dcf93cf863be90e646120c203f2d
Result: MATCH
```

七个清单文件和规范包摘要重新计算：

```text
Observed Package Digest: ee015cda57a52ed82a7fc67eab09e9f0611925d6249cc9c89c063324485020a2
Declared Package Digest: ee015cda57a52ed82a7fc67eab09e9f0611925d6249cc9c89c063324485020a2
Unexpected or Missing File Count: 0
Digest Mismatch Count: 0
Result: MATCH
```

## 二、源证据复核

复核器直接读取 `CR-0014-PW-004` 的清单和数据库：

```text
Source Package Digest: 77d45a57a976ffdb790c8759206f541de9e21fd95c0c2fce959043776ae6846c
Source Database Digest: 9e64da1355af98a939ae0c4cece065ca1b0d67d90afc7ae0d4c9c97865032f42
Migration Lineage Source Digest: 9e64da1355af98a939ae0c4cece065ca1b0d67d90afc7ae0d4c9c97865032f42
Result: MATCH
```

源证据数据库没有被迁移器原地修改。

## 三、历史逐行保留复核

复核器使用源数据库原列集合，从迁移数据库按旧主键集合抽取历史行，逐行比较：

```text
runtime_metadata: PASS_WITH_EXPECTED_VERSION_AND_MIGRATION_METADATA_CHANGE
authority_grants: PASS
protected_records: PASS
write_attempts: PASS
write_conflicts: PASS
```

源 59 个事件摘要与迁移数据库前 59 个事件摘要完全相同：

```text
Legacy Event Prefix Length: 59
Changed Legacy Event Hash Count: 0
Final Mixed-version Event Count: 68
Broken Link Count: 0
Broken Digest Count: 0
```

## 四、摘要可恢复性复核

复核器从旧记录原始载荷和前驱身份重新计算 12 个内容摘要，全部匹配。迁移分类表计数为：

| 对象 | 可推导 | 不可推导 |
| --- | ---: | ---: |
| 保护记录 | 12 | 0 |
| 写入尝试 | 23 | 36 |
| 冲突既有侧 | 11 | 0 |
| 冲突竞争侧 | 0 | 11 |

```text
Explicit Legacy Unknown Count: 47
Fabricated Replacement Digest Count: 0
```

保持未知是正确的失败关闭结果。若把载荷摘要复制到内容摘要列，会虚假声称已知前驱关系；本迁移没有这样做。

## 五、旧载荷与后继复核

旧记录现行载荷评估重新计数：

```text
CURRENT_PAYLOAD_CONFORMANT: 9
LEGACY_RETAINED_NOT_CURRENTLY_CONFORMANT: 3
```

复核器直接调用当前载荷验证合同检查七条迁移后记录：

```text
Post-migration Current Payload Record Count: 7
Invalid Current Payload Count: 0
```

关系重建确认：

- 新来源、闭包、完整性、审计和发布均保留精确旧前驱；
- 重建要求固定更正来源、完整性和旧发布；
- 新发布与新审计业务载荷摘要相同；
- 删除记录固定旧发布和重建要求；
- 旧发布与旧审计仍然存在。

## 六、迁移数据库复核

```text
Authority Grant Count: 13
Protected Record Count: 19
Write Attempt Count: 68
Write Conflict Count: 11
SQLite Integrity Check: ok
Foreign-key Failure Count: 0
SQLite User Version: 2
SQLite Journal Mode: delete
Append-only Trigger Count: 16
Unmanifested WAL / SHM Sidecar Count: 0
```

## 七、终局裁决

```text
Reviewed Migration Source Pinning: PASS
Source Immutability: PASS
Legacy Row Preservation: PASS
Legacy Event-chain Preservation: PASS
Unknown Digest Non-fabrication: PASS
Current Successor Validation: PASS
Post-migration Runtime Compatibility: PASS
Migration Evidence: PASS_FOR_REVIEWED_0_1_TO_0_2_PATH
Residual Reviewed-path Blockers: 0
Cross-provider Evidence: MISSING
Cross-project Evidence: MISSING
Cross-domain Evidence: MISSING
Full IF-0007 Evidence: NOT_COMPLETE
Freeze Review Eligibility: NO
Applicable Freeze Authority: NOT_ESTABLISHED
Institution Freeze: NOT_CREATED
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
Next Authorized Stage: EXTERNAL_CROSS_CONTEXT_EVIDENCE_REQUIRED
```

准确状态是：迁移证据维度已对精确版本路径成立，剩余冻结阻断缩减为跨提供方、跨项目和跨领域现实证据。
