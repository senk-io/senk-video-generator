# CR-0002 单一候选合并后语义差异审查

## 审查信息

```text
Review ID: CR-0002-CONSTITUTION-CANDIDATE-SEMANTIC-DIFF
Review Type: Post-consolidation Semantic Diff Review
Status: COMPLETED
Result: PASS_WITH_INDEPENDENT_CONSISTENCY_REVIEW_REQUIRED
Executable: NO
Reviewed Candidate: CR-0002-CONSTITUTION-CANDIDATE
Compared Sources: CR-0002-R2 + CR-0002-R3 + CR-0002-R4 + CR-0002-R5
Reviewer: Codex
Authority: User-delegated proposal review authority
Institution Freeze Created: NO
```

> 本文件只验证单一候选是否忠实合并已通过最终组合复审的规范语义，不是独立单一候选一致性审查，也不是制度冻结。

## 审查方法

本轮逐条检查：

1. 每个 R2 至 R5 规则是否映射到单一候选规则；
2. 被替代定义是否已经从规范正文移除；
3. 合并是否产生未获审查授权的新值域、状态、权威或时间语义；
4. 同一概念是否仍存在竞争定义；
5. 历史来源是否通过映射保留而未成为并列规范；
6. 不可执行、无权威和未冻结边界是否保持。

判定类型：

```text
PRESERVED
CONSOLIDATED
NARROWED_BY_REVIEWED_AMENDMENT
RENAMED_WITH_SEMANTIC_IDENTITY
REMOVED_AS_SUPERSEDED
UNMAPPED
```

只有 `UNMAPPED = 0` 才能通过本轮。

## 总体结果

```text
R2 Rules Mapped: 43 / 43
R3 Rules Mapped: 32 / 32
R4 Rules Mapped: 31 / 31
R5 Rules Mapped: 34 / 34
Total Source Rules Mapped: 140 / 140
Unmapped Source Rules: 0
Unreviewed Normative Additions: 0
Duplicate Normative Definitions Observed: 0
Historical Proposal Mutation: 0
Overall Result: PASS_WITH_INDEPENDENT_CONSISTENCY_REVIEW_REQUIRED
```

合并自检曾发现外部依据资格和决策权威适用性被错误扩大为四值接口。该范围漂移已在本审查落盘前纠正：

```text
External Basis Qualification:
  QUALIFIED | NOT_QUALIFIED | INDETERMINATE

Decision Authority Applicability:
  APPLICABLE | NOT_APPLICABLE | INDETERMINATE

Non-application Proof Qualification only:
  QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED

Proof and Exemption Applicability only:
  APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
```

因此，R4 的四值兼容修订没有隐式传播到未获授权的外部解析类型。

## R2 逐条映射

| 来源规则 | 单一候选 | 差异类型 | 说明 |
|---|---|---|---|
| `DM-R2-01` | `DM-C-01` | `PRESERVED` | 实际权威行使建立决策行为 |
| `DM-R2-02` | `DM-C-02` | `PRESERVED` | 决策不吸收相邻职责 |
| `DM-R2-03` | `DM-C-03` | `PRESERVED` | 一个决策实例一个主要权威 |
| `DM-R2-04` | `DM-C-04` | `PRESERVED` | 裁决倾向与迁移类型分离 |
| `DM-R2-05` | `DM-C-05` | `PRESERVED` | `NO_ACTION` 历史与目标迁移分离 |
| `DM-R2-06` | `DM-C-06` | `PRESERVED` | 外部依据资格保持 R2 三值接口 |
| `DM-R2-07` | `DM-C-07` | `PRESERVED` | 外部权威适用性保持 R2 三值接口 |
| `DM-R2-08` | `DM-C-08` | `PRESERVED` | 外部解析绑定同一决策坐标 |
| `DM-R2-09` | `DM-C-09` | `PRESERVED` | 解析计算、登记和准入分权 |
| `DM-R2-10` | `DM-C-10` | `PRESERVED` | 不可变决策尝试记录 |
| `DM-R2-11` | `DM-C-11` | `PRESERVED` | 候选记录无正式事实地位 |
| `DM-R2-12` | `DM-C-12` | `PRESERVED` | 稳定决策键和幂等 |
| `DM-R2-13` | `DM-C-17` | `CONSOLIDATED` | 准入计算权与 R3 登记契约组合 |
| `DM-R2-14` | `DM-C-18` | `PRESERVED` | 确定性否定与未知失败关闭 |
| `DM-R2-15` | `DM-C-19` | `NARROWED_BY_REVIEWED_AMENDMENT` | 增加内容同一登记字段 |
| `DM-R2-16` | `DM-C-19` | `PRESERVED` | `ADMISSIBLE` 不等于决策事实 |
| `DM-R2-17` | `DM-C-20` | `PRESERVED` | 受保护权威写入成立事实 |
| `DM-R2-18` | `DM-C-22` | `PRESERVED` | 写入与归因不可分割 |
| `DM-R2-19` | `DM-C-23` 至 `DM-C-35` | `NARROWED_BY_REVIEWED_AMENDMENT` | 三值解析保留，证明和投影闭合 |
| `DM-R2-20` | `DM-C-35` | `PRESERVED` | 解析和投影不授权策略 |
| `DM-R2-21` | `DM-C-36` | `PRESERVED` | 决策事实先于目标迁移 |
| `DM-R2-22` | `DM-C-37` | `PRESERVED` | 目标状态不能反推决策事实 |
| `DM-R2-23` | `DM-C-38` | `PRESERVED` | 目标失败不抹除决策事实 |
| `DM-R2-24` | `DM-C-39` | `PRESERVED` | 多权威保持多个决策事实 |
| `DM-R2-25` | `DM-C-40` | `PRESERVED` | 槽位模式与裁决倾向分离 |
| `DM-R2-26` | `DM-C-42` 至 `DM-C-43` | `NARROWED_BY_REVIEWED_AMENDMENT` | 豁免增加资格与适用性完整链 |
| `DM-R2-27` | `DM-C-40` 至 `DM-C-41` | `PRESERVED` | 组合解析器无联合权威 |
| `DM-R2-28` | `DM-C-44` | `PRESERVED` | 最终决策保持独立 |
| `DM-R2-29` | `DM-C-45` | `PRESERVED` | 合法性审查是派生解释 |
| `DM-R2-30` | `DM-C-47` 至 `DM-C-49` | `CONSOLIDATED` | 历史认识和当前重述分离 |
| `DM-R2-31` | `DM-C-47` 至 `DM-C-49` | `NARROWED_BY_REVIEWED_AMENDMENT` | 宽泛时间字段规范化为五类时间 |
| `DM-R2-32` | `DM-C-46` | `NARROWED_BY_REVIEWED_AMENDMENT` | 增加内容同一和谱系 |
| `DM-R2-33` | `DM-C-50` | `PRESERVED` | 审查只支持失效请求 |
| `DM-R2-34` | `DM-C-51` | `PRESERVED` | 失效由新决策事实建立 |
| `DM-R2-35` | `DM-C-52` | `PRESERVED` | 失效不删除历史 |
| `DM-R2-36` | `DM-C-53` | `PRESERVED` | 传播只消费已提交失效事实 |
| `DM-R2-37` | `DM-C-54` | `PRESERVED` | 更正只修复表示缺陷 |
| `DM-R2-38` | `DM-C-55` | `NARROWED_BY_REVIEWED_AMENDMENT` | 增加内容同一登记和谱系 |
| `DM-R2-39` | `DM-C-56` 至 `DM-C-57` | `NARROWED_BY_REVIEWED_AMENDMENT` | 追加投影增加双时间和发布分权 |
| `DM-R2-40` | `DM-C-58` | `PRESERVED` | 更正不改变事实成立状态 |
| `DM-R2-41` | `DM-C-59` | `PRESERVED` | 人工创意裁决可审计 |
| `DM-R2-42` | `DM-C-60` | `CONSOLIDATED` | 专属契约吸收已审查新增接口 |
| `DM-R2-43` | `DM-C-61` | `PRESERVED` | 制度冻结决策更高门槛 |

## R3 逐条映射

| 来源规则 | 单一候选 | 差异类型 | 说明 |
|---|---|---|---|
| `DM-R3-01` | `DM-C-13` | `PRESERVED` | 通用登记契约不传播授权 |
| `DM-R3-02` | `DM-C-14` | `PRESERVED` | 登记授权完整边界 |
| `DM-R3-03` | `DM-C-16` | `PRESERVED` | 候选与登记载荷内容同一 |
| `DM-R3-04` | `DM-C-15` | `PRESERVED` | 登记尝试和三值结果 |
| `DM-R3-05` | `DM-C-15` 至 `DM-C-16` | `PRESERVED` | 登记失败不修改现实 |
| `DM-R3-06` | `DM-C-13` 至 `DM-C-16` | `CONSOLIDATED` | 逐类型授权统一为一套规范接口 |
| `DM-R3-07` | `DM-C-23` | `PRESERVED` | 证明名称不等于合格证明 |
| `DM-R3-08` | `DM-C-24` | `PRESERVED` | 候选证明固定作用域和来源 |
| `DM-R3-09` | `DM-C-25` | `NARROWED_BY_REVIEWED_AMENDMENT` | 资格值域由 R4 规范化 |
| `DM-R3-10` | `DM-C-25` 至 `DM-C-26` | `NARROWED_BY_REVIEWED_AMENDMENT` | 适用性和投影由 R4 规范化 |
| `DM-R3-11` | `DM-C-27` | `PRESERVED` | 完备性证明必须外部合格 |
| `DM-R3-12` | `DM-C-27` | `NARROWED_BY_REVIEWED_AMENDMENT` | `ABORTED` 增加四值冲突与闭包 |
| `DM-R3-13` | `DM-C-29` | `NARROWED_BY_REVIEWED_AMENDMENT` | 谱系关系由 R5 规范化 |
| `DM-R3-14` | `DM-C-30` 至 `DM-C-35` | `NARROWED_BY_REVIEWED_AMENDMENT` | 当前投影改为规范四值解析投影 |
| `DM-R3-15` | `DM-C-40` | `PRESERVED` | 一个记录一个槽位 |
| `DM-R3-16` | `DM-C-41` | `PRESERVED` | 组合候选完整载荷 |
| `DM-R3-17` | `DM-C-41` | `PRESERVED` | 组合登记内容同一 |
| `DM-R3-18` | `DM-C-42` | `NARROWED_BY_REVIEWED_AMENDMENT` | 豁免适用性由 R4 补齐 |
| `DM-R3-19` | `DM-C-43` | `PRESERVED` | `EXEMPT` 需要正向证明 |
| `DM-R3-20` | `DM-C-41` 至 `DM-C-43` | `PRESERVED` | 组合谱系不覆盖历史 |
| `DM-R3-21` | `DM-C-46` | `PRESERVED` | 审查登记内容同一 |
| `DM-R3-22` | `DM-C-49` | `NARROWED_BY_REVIEWED_AMENDMENT` | 投影键使用 R4 规范时间 |
| `DM-R3-23` | `DM-C-49` | `PRESERVED` | 当前合法性投影保存谱系 |
| `DM-R3-24` | `DM-C-56` | `PRESERVED` | 更正五类时间分离 |
| `DM-R3-25` | `DM-C-55` | `PRESERVED` | 更正内容同一和谱系 |
| `DM-R3-26` | `DM-C-56` | `PRESERVED` | 历史读取和当前重述分离 |
| `DM-R3-27` | `DM-C-57` | `PRESERVED` | 决策读投影稳定键 |
| `DM-R3-28` | `DM-C-57` | `PRESERVED` | 构建、发布和事实分权 |
| `DM-R3-29` | `DM-C-57` | `PRESERVED` | 投影保存来源和谱系 |
| `DM-R3-30` | `DM-C-04`、规范因果路径 | `RENAMED_WITH_SEMANTIC_IDENTITY` | 非准入尝试替代拒绝歧义 |
| `DM-R3-31` | `DM-C-28`、规范因果路径 | `RENAMED_WITH_SEMANTIC_IDENTITY` | 未知只属于解析认识 |
| `DM-R3-32` | 规范因果路径 | `CONSOLIDATED` | 修订路径直接成为规范路径 |

## R4 逐条映射

| 来源规则 | 单一候选 | 差异类型 |
|---|---|---|
| `DM-R4-01` | `DM-C-25` | `PRESERVED` |
| `DM-R4-02` | `DM-C-25` | `PRESERVED` |
| `DM-R4-03` | `DM-C-25` | `PRESERVED` |
| `DM-R4-04` | `DM-C-26` | `PRESERVED` |
| `DM-R4-05` | `DM-C-26` | `PRESERVED` |
| `DM-R4-06` | `DM-C-26` | `PRESERVED` |
| `DM-R4-07` | `DM-C-26` | `PRESERVED` |
| `DM-R4-08` | `DM-C-26` | `PRESERVED` |
| `DM-R4-09` | `DM-C-26` | `CONSOLIDATED` |
| `DM-R4-10` | `DM-C-27` | `PRESERVED` |
| `DM-R4-11` | `DM-C-42` | `PRESERVED` |
| `DM-R4-12` | `DM-C-42` | `PRESERVED` |
| `DM-R4-13` | `DM-C-42` | `PRESERVED` |
| `DM-R4-14` | `DM-C-42` | `PRESERVED` |
| `DM-R4-15` | `DM-C-42` | `PRESERVED` |
| `DM-R4-16` | `DM-C-42` | `PRESERVED` |
| `DM-R4-17` | `DM-C-42` | `PRESERVED` |
| `DM-R4-18` | `DM-C-43` | `PRESERVED` |
| `DM-R4-19` | `DM-C-47` | `PRESERVED` |
| `DM-R4-20` | `DM-C-48` | `PRESERVED` |
| `DM-R4-21` | `DM-C-48` | `PRESERVED` |
| `DM-R4-22` | `DM-C-48` | `PRESERVED` |
| `DM-R4-23` | `DM-C-48` | `CONSOLIDATED` |
| `DM-R4-24` | `DM-C-48` | `CONSOLIDATED` |
| `DM-R4-25` | `DM-C-47` | `PRESERVED` |
| `DM-R4-26` | `DM-C-49` | `PRESERVED` |
| `DM-R4-27` | `DM-C-49` | `PRESERVED` |
| `DM-R4-28` | `DM-C-47` 至 `DM-C-49` | `PRESERVED` |
| `DM-R4-29` | 规范提交解析路径 | `CONSOLIDATED` |
| `DM-R4-30` | 规范组合路径 | `CONSOLIDATED` |
| `DM-R4-31` | 规范合法性路径 | `CONSOLIDATED` |

## R5 逐条映射

| 来源规则 | 单一候选 | 差异类型 |
|---|---|---|
| `DM-R5-01` | `DM-C-30` | `PRESERVED` |
| `DM-R5-02` | `DM-C-30` 至 `DM-C-31` | `PRESERVED` |
| `DM-R5-03` | `DM-C-31` | `PRESERVED` |
| `DM-R5-04` | `DM-C-28` | `PRESERVED` |
| `DM-R5-05` | `DM-C-30` | `PRESERVED` |
| `DM-R5-06` | `DM-C-33` | `CONSOLIDATED` |
| `DM-R5-07` | `DM-C-33` | `PRESERVED` |
| `DM-R5-08` | `DM-C-33` | `PRESERVED` |
| `DM-R5-09` | `DM-C-31` | `PRESERVED` |
| `DM-R5-10` | `DM-C-31` | `PRESERVED` |
| `DM-R5-11` | `DM-C-31` | `PRESERVED` |
| `DM-R5-12` | `DM-C-31` | `PRESERVED` |
| `DM-R5-13` | `DM-C-32` | `PRESERVED` |
| `DM-R5-14` | `DM-C-32` | `PRESERVED` |
| `DM-R5-15` | `DM-C-32` | `PRESERVED` |
| `DM-R5-16` | `DM-C-32` | `PRESERVED` |
| `DM-R5-17` | `DM-C-32` | `PRESERVED` |
| `DM-R5-18` | `DM-C-32` | `PRESERVED` |
| `DM-R5-19` | `DM-C-34` | `PRESERVED` |
| `DM-R5-20` | `DM-C-34` | `PRESERVED` |
| `DM-R5-21` | `DM-C-33` 至 `DM-C-34` | `PRESERVED` |
| `DM-R5-22` | `DM-C-34` | `PRESERVED` |
| `DM-R5-23` | `DM-C-34` | `PRESERVED` |
| `DM-R5-24` | `DM-C-29` | `PRESERVED` |
| `DM-R5-25` | `DM-C-29` | `CONSOLIDATED` |
| `DM-R5-26` | `DM-C-29`、`DM-C-33` | `PRESERVED` |
| `DM-R5-27` | `DM-C-33` | `PRESERVED` |
| `DM-R5-28` | `DM-C-31` 至 `DM-C-33` | `PRESERVED` |
| `DM-R5-29` | `DM-C-35` | `PRESERVED` |
| `DM-R5-30` | `DM-C-20`、`DM-C-35` | `PRESERVED` |
| `DM-R5-31` | `DM-C-35` | `PRESERVED` |
| `DM-R5-32` | `DM-C-33`、`DM-C-35` | `PRESERVED` |
| `DM-R5-33` | 规范提交解析投影路径 | `CONSOLIDATED` |
| `DM-R5-34` | `DM-C-30`、规范视图语义 | `CONSOLIDATED` |

## 被取代定义清理检查

| 被取代定义 | 单一候选状态 | 结果 |
|---|---|---|
| `Illegal or Rejected Decision Attempt Record` | 不作为规范类型出现 | `PASS` |
| `Decision Fact Status Unknown` | 不作为决策事实状态出现 | `PASS` |
| `NOT_QUALIFIED` 作为证明资格值 | 仅外部依据资格保留；证明资格已用 `DISQUALIFIED` | `PASS` |
| `NOT_APPLICABLE` 作为证明适用性值 | 仅外部权威适用性保留；证明适用性已用 `INAPPLICABLE` | `PASS` |
| `Current Commit Resolution Projection` 作为规范类型 | 仅作为显示别名说明 | `PASS` |
| 提交投影三值 | 单条解析三值、投影四值已经分离 | `PASS` |
| `Review Effective At / Review As Of / Reviewed At` 作为新规范字段 | 仅在旧字段规范化说明中存在 | `PASS` |
| `SUPERSEDES_FOR_CURRENT_PROJECTION` 作为规范提交谱系关系 | 不作为规范关系出现 | `PASS` |
| 来源摘要证明闭包完整 | 明确禁止 | `PASS` |

## 新增规范检查

单一候选新增的规范表达均可追溯到已审查修订：

| 候选新增表达 | 来源 | 结果 |
|---|---|---|
| `DM-C` 统一编号 | 合并技术需要，不改变语义 | `PASS` |
| 单一统一类型边界 | R2 类型表与 R3-R5 新类型合并 | `PASS` |
| 外部解析三值和证明接口四值并存 | R2 与 R4 作用域分离 | `PASS` |
| `Resolution Projection` 规范类型 | R5 | `PASS` |
| 五类合法性时间 | R4 | `PASS` |
| 逐类型派生登记授权 | R3 | `PASS` |

```text
Unreviewed Normative Additions: NONE
```

## 历史与冻结边界

```text
R2-R5 Historical Files Modified: NO
Historical Review Files Modified: NO
Foundation Frozen Files Modified: NO
Runtime Authority Created: NO
Runtime Records Created: NO
Institution Freeze Created: NO
```

本轮只创建单一候选和语义差异记录。

## 剩余要求

本轮通过后仍必须执行：

```text
Independent Single Candidate Consistency Review
Freeze Dependency Readiness Audit
IF-0007 Evidence and Authority Closure
```

在独立一致性审查以前：

```text
Candidate Status: CONSISTENCY_REVIEW_REQUIRED
Model-level Blockers: NOT_EVALUATED
Institution Freeze Eligibility: FAIL
```

## 决定

1. 确认 R2 至 R5 的 140 条来源规则全部映射；
2. 确认没有未映射规则或未审查规范新增；
3. 确认被取代定义没有作为竞争规范保留；
4. 将本轮结果登记为 `PASS_WITH_INDEPENDENT_CONSISTENCY_REVIEW_REQUIRED`；
5. 不修改单一候选以外的历史提案或冻结制度；
6. 不创建冻结标识或运行时权威；
7. 下一步只执行单一候选独立一致性审查。
