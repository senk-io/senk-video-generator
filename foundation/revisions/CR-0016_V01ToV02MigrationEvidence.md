# CR-0016 运行证据数据库 0.1 到 0.2 迁移证据

## 执行信息

```text
Execution Review ID: CR-0016-V01-TO-V02-MIGRATION-EVIDENCE
Status: COMPLETED
Result: PASS_AS_NON_AUTHORITATIVE_MIGRATION_EVIDENCE
Source Execution: CR-0014-PW-004
Source Implementation: governance-kernel/0.1.0+sha256:f273f81f789b38c656749340a5d2894c7594bfc7519869248b997b384eafa8ce
Target Implementation: governance-kernel/0.2.0+sha256:4bd160d6ad9a64acbb66698b342396d8b33e7a763e127dc89298d42bdbbfb5cf
Migration Execution: CR-0016-MIGRATION-001
Migration Contract: governance-schema-migration/0.1-to-0.2
Migration Harness Digest: 46488fce8b7d578711a24dae3d52e11e5100dcf93cf863be90e646120c203f2d
Evidence Package Digest: ee015cda57a52ed82a7fc67eab09e9f0611925d6249cc9c89c063324485020a2
Formal Fact Created: NO
Institution Freeze Created: NO
Current Overall Gate: IF-0007_EVIDENCE_REQUIRED
```

> 本文件证明一个精确历史证据数据库可以在不修改源文件、不伪造缺失内容、不删除旧事件的条件下迁移到当前证据运行结构。它只覆盖 `0.1.0` 到 `0.2.0` 的已审路径。

## 一、迁移命题

`0.2.0` 增加业务载荷摘要与记录完整内容摘要分离、投影重建和删除控制类型。`0.1.0` 数据库没有以下列：

```text
protected_records.content_digest
write_attempts.content_digest
write_conflicts.existing_content_digest
write_conflicts.competing_content_digest
```

迁移必须同时满足：

1. 历史源数据库字节不变；
2. 旧授权、保护记录、尝试、冲突和事件链不被覆盖；
3. 只从旧库确实保存的规范载荷和前驱身份推导新摘要；
4. 无法从摘要反推的旧请求和竞争载荷保持未知；
5. 不符合当前新增载荷字段的旧记录保留为历史，不伪装成当前合格记录；
6. 当前运行内核能够打开迁移结果，并追加合格后继记录；
7. 新旧事件必须保持为一条连续哈希链。

## 二、源证据固定

源证据：

```text
Evidence Package: CR-0014-PW-004
Source Package Digest: 77d45a57a976ffdb790c8759206f541de9e21fd95c0c2fce959043776ae6846c
Source Database Digest: 9e64da1355af98a939ae0c4cece065ca1b0d67d90afc7ae0d4c9c97865032f42
Source Protected Records: 12
Source Write Attempts: 59
Source Write Conflicts: 11
```

迁移从源数据库复制出新载体，只操作副本。执行前后重新计算源数据库摘要：

```text
Before: 9e64da1355af98a939ae0c4cece065ca1b0d67d90afc7ae0d4c9c97865032f42
After:  9e64da1355af98a939ae0c4cece065ca1b0d67d90afc7ae0d4c9c97865032f42
Result: SOURCE_UNCHANGED
```

## 三、保守摘要迁移

### 3.1 可推导内容

12 条旧保护记录保存了完整规范载荷与前驱记录标识，因此可以精确推导：

```text
Content Digest = digest(canonical payload + predecessor record identity)
```

23 条旧写入尝试的载荷摘要与其输出记录载荷摘要完全一致，可以从输出记录取得相同内容摘要。11 条冲突的既有侧也可从被保留记录推导。

```text
Legacy Protected Record Content Digests Derived: 12
Legacy Attempt Content Digests Derived: 23
Legacy Existing-conflict Content Digests Derived: 11
```

### 3.2 不可推导内容

旧数据库对拒绝、未授权、缺失前置和竞争载荷只保存载荷摘要，没有保存原始载荷与前驱字段。密码学摘要不能被反向恢复，因此迁移明确保存空值与不可恢复原因：

```text
Legacy Attempt Content Digests Unavailable: 36
Legacy Competing-conflict Content Digests Unavailable: 11
Total Explicit Unknowns: 47
```

没有使用载荷摘要冒充内容摘要，也没有构造占位哈希制造虚假完整性。

## 四、旧载荷现行适用性评估

逐条以当前目录重新验证 12 条历史记录：

```text
CURRENT_PAYLOAD_CONFORMANT: 9
LEGACY_RETAINED_NOT_CURRENTLY_CONFORMANT: 3
```

三条不符合当前新增字段要求的旧类型为：

```text
Registered Closure Completeness Record
Registered Projection Change Audit Record
Projection Publication Envelope
```

这些记录在 `0.1.0` 执行时是合法证据模式记录；迁移不否定其历史，也不让它们直接取得当前载荷资格。迁移后通过新语义键和前驱引用追加当前合格后继。

## 五、迁移后运行

当前内核成功打开迁移数据库并执行：

```text
Legacy Institution Record Idempotent Read/write Check
  -> Source Successor
  -> Dependency Closure Successor
  -> INCOMPLETE Completeness Successor
  -> Projection Rebuild Requirement
  -> INDETERMINATE Audit Successor
  -> Content-identical Publication Successor
  -> Legacy-cache Deletion Record
  -> Reject Deletion without Rebuild Requirement
```

结果：

```text
Post-migration Accepted Records: 7
Post-migration Negative Attempts: 1
Final Protected Record Count: 19
Final Write Attempt Count: 68
Final Write Conflict Count: 11
Legacy History Preserved: YES
Legacy Idempotency Preserved: YES
Audit / Publication Business Payload Identity: PASS
Deletion without Rebuild: REJECTED
Mixed-version Event Hash-chain: PASS
```

旧 59 个事件成为新 68 个事件链的精确前缀。迁移没有重写旧事件正文或摘要。

## 六、迁移载体与不可变边界

迁移副本增加三个追加式表：

```text
migration_lineage
migration_content_resolutions
migration_record_assessments
```

前者固定源摘要、源／目标实现、源计数和执行标识；后两者分别记录摘要可恢复性与当前载荷适用性。五个原表和三个迁移表总计安装 16 个更新／删除拒绝触发器。

```text
SQLite Integrity Check: ok
Foreign-key Failure Count: 0
SQLite User Version: 2
SQLite Journal Mode: delete
Append-only Trigger Count: 16
```

## 七、证据包

证据目录：

```text
evidence/runtime/CR-0016-MIGRATION-001/
```

清单覆盖七个文件：

- 输入清单；
- 迁移测试输出与汇总；
- 迁移过程汇总；
- 迁移后运行汇总；
- 总体汇总；
- 迁移数据库。

规范包摘要：

```text
ee015cda57a52ed82a7fc67eab09e9f0611925d6249cc9c89c063324485020a2
```

## 八、当前决定

```text
Source Evidence Immutability: PASS
Legacy Table Preservation: PASS
Legacy Event Prefix Preservation: PASS
Unknown Digest Non-fabrication: PASS
Current Payload Successors: PASS
Post-migration Protected Writes: PASS
Migration Evidence: PASS_FOR_REVIEWED_0_1_TO_0_2_PATH
Cross-provider Evidence: MISSING
Cross-project Evidence: MISSING
Cross-domain Evidence: MISSING
Full IF-0007 Evidence: NOT_COMPLETE
Freeze Review Eligibility: NO
Applicable Freeze Authority: NOT_ESTABLISHED
Institution Freeze: NOT_CREATED
Next Required Stage: EXTERNAL_CROSS_CONTEXT_EVIDENCE_REQUIRED
```

准确状态是：精确的 `0.1.0` 到 `0.2.0` 迁移路径已经闭环，但完整 `IF-0007` 仍缺跨提供方、跨项目和跨领域现实证据。
