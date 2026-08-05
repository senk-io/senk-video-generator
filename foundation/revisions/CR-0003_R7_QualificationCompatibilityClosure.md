# 提交模型第七修订版：资格兼容闭合增补

## 提案信息

```text
Proposal ID: CR-0003-R7
Title: Commit Model — Qualification Compatibility Closure
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: BOUNDED_CORRECTION
Applies To: CR-0003-R4 + CR-0003-R5 + CR-0003-R6
Revises: CR-0003-R6 within qualification compatibility scope only
Review Basis: CR-0003-R6-LOCAL-REVIEW
Reviewer: Codex
External Approval Required: NO
Consolidation Required Before Freeze: YES
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
```

> 本文件只关闭资格跨版本解释的最后一个阻断簇。它不是冻结制度，不授权资格计算、提交解析、投影发布或任何正式状态迁移。

## 使用方式

下一轮最终闭合复核对象是：

```text
CR-0003-R4 Commit Core
+ CR-0003-R5 Epistemic Evolution Amendment
+ CR-0003-R6 Epistemic Closure Amendment
+ CR-0003-R7 Qualification Compatibility Closure
```

本文件只在资格认识偏序、资格跨版本解释和兼容域身份范围内收紧前序草案。其他语义继续由 `R4`、`R5` 和 `R6` 提供。

## 修订范围

本版只处理：

1. 资格结果的认识偏序；
2. 资格 `FORWARD_INTERPRETABLE` 的非放大映射；
3. 资格变化需要重新资格计算时的明确路径；
4. 精确契约版本与兼容域快照的互斥键模式；
5. 多注册表认识截点的因果闭包；
6. 制度冻结状态的可验证引用。

本版不修改：

- 资格结果和提交结果的值域；
- 未应用证明类型；
- 依赖闭包算法；
- 提交主干；
- 决策模型或制度冻结门槛。

## 新增类型边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Qualification Epistemic Strength` | 偏序值 | 表达资格结果的认识强度 | 资格投影规则 |
| `Qualification Scope Mode` | 枚举值 | 选择精确契约或兼容域快照键 | 资格投影键 |
| `Qualification Compatibility Domain Snapshot` | 不可变制度快照 | 固定可比较契约版本集合 | 资格治理制度 |
| `Qualification Forward Interpretation Contract` | 版本化制度契约 | 定义资格结果的非放大解释 | 资格治理制度 |
| `Institution Freeze Reference` | 制度引用值 | 证明所用制度版本已合法冻结 | 制度注册表 |
| `Knowledge Boundary Vector` | 复合边界值 | 固定各来源注册表的认识截点 | 时间查询坐标 |

## QC-01 资格结果必须拥有独立认识偏序

最低资格认识偏序为：

```text
INDETERMINATE <= QUALIFIED
INDETERMINATE <= DISQUALIFIED
QUALIFIED and DISQUALIFIED are incomparable terminals
```

该偏序只比较认识强度，不表示资格生命周期顺序，也不允许把 `QUALIFIED` 和 `DISQUALIFIED` 排成优先级。

## QC-02 资格冲突不属于更高或更低认识等级

```text
CONFLICTED
!= stronger than QUALIFIED
!= stronger than DISQUALIFIED
!= weaker than either terminal
```

`CONFLICTED` 表示同一可比较作用域内存在相反终局来源。它必须保留冲突引用，不能通过数值评分、来源数量或登记时间选择结果。

## QC-03 资格前向解释必须使用专用契约

资格规则版本被声明为 `FORWARD_INTERPRETABLE` 时，除 R5 的通用字段外，还必须引用 `Qualification Forward Interpretation Contract`：

```text
Source Qualification Rule Version
Target Qualification Interpretation Version
Qualification Scope Mode
Source and Target Scope Identity
Total Deterministic Qualification Mapping
Qualification Epistemic Strength Mapping
Field Presence Preservation
Evidence Reference Preservation
Qualification Record Reference Preservation
Mapping Rule Version
Compatibility Evidence References
Institution Freeze Reference
```

缺少任一必需字段时，兼容关系只能是 `UNKNOWN_COMPATIBILITY`。

## QC-04 资格前向解释不得放大认识强度

最低合法映射为：

```text
InterpretQualification(INDETERMINATE)
  -> INDETERMINATE

InterpretQualification(QUALIFIED)
  -> QUALIFIED or INDETERMINATE

InterpretQualification(DISQUALIFIED)
  -> DISQUALIFIED or INDETERMINATE

InterpretQualification(CONFLICTED sources)
  -> CONFLICTED or INDETERMINATE
```

禁止：

```text
INDETERMINATE -> QUALIFIED
INDETERMINATE -> DISQUALIFIED
QUALIFIED -> DISQUALIFIED
DISQUALIFIED -> QUALIFIED
CONFLICTED -> one selected terminal
UNRESOLVED field -> VALUE
```

## QC-05 资格解释不得改变作用域身份

资格前向解释只能在同一稳定资格作用域内执行：

```text
Same Candidate Proof ID
Same Commit Key
Same Qualification Scope Mode
Same exact contract version or same compatibility domain snapshot
Same Validity As Of
Same Knowledge Boundary Vector
```

任一项不同都必须产生新的投影键，不得在解释过程中静默迁移。

## QC-06 可能提高或转换资格确定性时必须重新资格计算

任何映射若可能提高认识强度、跨终局转换或改变作用域，兼容关系必须是：

```text
REQUIRES_RERESOLUTION
Required Re-resolution Kind: REQUALIFICATION
```

资格语境中的 `REQUALIFICATION` 表示重新执行证明资格计算，而不是只重新构建投影或重新解析提交结果。

## QC-07 重新资格计算必须复用既有独立权威链

```text
Original Candidate Non-application Proof Record
+ Applicable Source Evidence and Corrections
+ New Qualification Rule Version
+ Non-application Proof Qualification Execution Authority
-> New Candidate Proof Qualification Record

New Candidate Proof Qualification Record
+ Non-application Proof Qualification Registration Authority
+ Content-identical Admissibility Check
-> New Registered Proof Qualification Record
```

旧资格记录保持不变。解释器、投影器和兼容性记录创建者不能继承资格计算或登记权威。

## QC-08 重新资格计算后仍需重新建立适用性和闭包

新的已登记资格不能自动支持 `ABORTED`：

```text
New Registered Proof Qualification Record
  -> Qualification Applicability Resolution
  -> Current Proof Qualification Projection
  -> Dependency Closure Rebuild
  -> Independent Closure Completeness Qualification
  -> Commit Resolution or Projection Re-evaluation
```

任何中间步骤未决时保持 `INDETERMINATE`。

## QC-09 资格投影键必须声明互斥作用域模式

合法模式只有：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

每个 `Qualification Projection Key` 必须且只能选择一种模式。不得同时填写两种模式，也不得两者都省略。

## QC-10 精确契约模式只允许一个契约版本

```text
Qualification Scope Mode = EXACT_CONTRACT_VERSION
  -> Exact Commit Contract Version required
  -> Compatibility Domain fields = NOT_APPLICABLE
```

该模式不得消费其他契约版本，即使版本号相邻或名称相同。

## QC-11 兼容域模式必须绑定不可变快照

```text
Qualification Scope Mode = COMPATIBILITY_DOMAIN_SNAPSHOT
  -> Qualification Compatibility Domain Snapshot required
  -> Exact Contract Version field = NOT_APPLICABLE
```

快照至少包含：

```text
Compatibility Domain ID
Compatibility Domain Version
Exact Member Commit Contract Versions
Membership Digest
Membership Rule Version
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
```

## QC-12 兼容域成员变化必须产生新版本和新投影键

```text
Membership Change
  -> New Compatibility Domain Version
  -> New Membership Digest
  -> New Qualification Projection Key
```

不得修改旧快照、复用旧摘要或让同一个投影键在不同时点指向不同成员集合。

## QC-13 兼容域成员关系必须具有制度权威和证据

兼容域快照只有同时满足以下条件才能进入资格投影：

```text
Applicable Qualification Governance Institution
Authorized Domain Membership Establishment
Compatibility Evidence for every included version relation
Exact Member Enumeration
Registered Immutable Snapshot
Valid Institution Freeze Reference
```

兼容域创建者不得用“属于同一产品”“版本更高”或“字段相似”代替语义兼容证据。

## QC-14 认识截点必须是多注册表稳定边界向量

`Knowledge Cutoff` 的规范结构为：

```text
Knowledge Boundary Vector:
  Registry Boundary Entries[]
  Vector Digest
  Boundary Rule Version
  Established At
```

每个条目至少绑定：

```text
Registry ID
Registry Scope
Inclusive Watermark or Exact Source Set
Boundary Authority Reference
```

显示层可以提供单一时间标签，但规范推导必须使用完整边界向量。

## QC-15 多注册表边界向量必须因果闭合

```text
Included Record
  -> every required referenced dependency
     must be included within its registry boundary
     or institutionally marked NOT_APPLICABLE
```

若边界内记录引用了边界外的必需来源：

```text
Knowledge Boundary Vector = CAUSALLY_INCOMPLETE
Closure Completeness = INDETERMINATE
Projection = INDETERMINATE
```

不得用不同注册表的独立水位拼出一个因果不一致但表面完整的快照。

## QC-16 制度状态必须由冻结引用证明

运行时使用的解释契约、兼容记录、兼容域和来源排除依据必须引用 `Institution Freeze Reference`：

```text
Freeze ID
Institution ID
Institution Version
Frozen Content Digest
Freeze Decision Reference
Freeze Authority Reference
Freeze Evidence Package Reference
Effective Scope
Validity Interval
```

`Institution Status` 显示文本、文件路径、模型声明或配置值不能替代冻结引用。

冻结引用解析属于独立受权执行，适用治理制度必须声明：

```text
Institution Freeze Reference Resolution Execution Authority Type
```

该授权只允许读取制度注册表并验证标识、摘要、作用域和有效区间，不允许创建冻结决定、修改制度记录或扩大契约适用范围。

## QC-17 冻结引用不适用或无法验证时必须失败关闭

```text
Freeze Reference Missing
or Digest Mismatch
or Scope Mismatch
or Validity Not Established
  -> Contract not usable for runtime projection
  -> Compatibility = UNKNOWN_COMPATIBILITY
  -> Projection = INDETERMINATE
```

冻结引用证明制度资格，不证明具体资格结果或投影结果正确。

## QC-18 资格兼容角色不能自证

- 资格兼容域创建者不能证明自身成员关系正确；
- 资格解释器不能创建或冻结解释契约；
- 资格解释器不能重新执行资格计算；
- 资格投影器不能把不安全映射改标为安全；
- 制度冻结引用解析者不能创建冻结决定；
- 依赖闭包构建器不能忽略边界外但被必需引用的来源。

## 资格跨版本完整路径

```text
Qualification Projection Key
  -> select exactly one Qualification Scope Mode
       -> EXACT_CONTRACT_VERSION
       or COMPATIBILITY_DOMAIN_SNAPSHOT

Qualification Rule Versions
  -> IDENTICAL_SEMANTICS
       -> direct comparison
  -> FORWARD_INTERPRETABLE
       -> frozen Qualification Forward Interpretation Contract
       -> non-amplifying qualification mapping
  -> REQUIRES_RERESOLUTION with REQUALIFICATION
       -> new qualification candidate
       -> independent registration
       -> applicability and closure rebuild
  -> INCOMPATIBLE or UNKNOWN_COMPATIBILITY
       -> INDETERMINATE

Knowledge Boundary Vector
  -> per-registry completeness
  -> causal closure
  -> qualification truth table
  -> epistemically bounded result
```

## 权威操作矩阵增补

| 角色 | 可以 | 不得 |
|---|---|---|
| `Qualification Forward Interpreter` | 按冻结非放大契约解释资格记录 | 提高确定性、跨终局转换 |
| `Proof Qualifier` | 在既有资格执行授权下重新计算资格 | 登记自身结果、修改旧资格 |
| `Qualification Projection Builder` | 对稳定键和因果闭合来源执行真值表 | 改变键模式、修改兼容域成员 |
| `Institution Freeze Reference Resolver` | 验证冻结引用、摘要和作用域 | 创建冻结决定或制度权威 |

资格兼容关系、解释契约和兼容域快照只能通过 `IF-0007` 的制度提案、审查和冻结路径建立，不属于运行时角色输出。运行时冻结引用解析授权、R5 的前向解释执行授权、R6 的资格投影执行授权以及 R4 的资格计算与登记授权必须保持独立，并满足 `R4` 的完整授权作用域要求。

## 非法状态候选增补

- 把资格 `INDETERMINATE` 前向解释为终局资格；
- 在 `QUALIFIED` 和 `DISQUALIFIED` 之间前向转换；
- 需要重新资格计算时只重新构建投影；
- 解释器继承资格计算或登记权威；
- 一个资格投影键同时使用精确契约和兼容域模式；
- 兼容域成员变化后复用旧域版本或投影键；
- 用可变成员查询代替不可变兼容域快照；
- 用版本号、新旧关系或产品身份推断资格语义兼容；
- 用单一时间戳替代规范的多注册表边界向量；
- 使用因果不闭合的来源边界产生终局资格或投影；
- 用制度状态文本、文件存在或模型声明替代冻结引用；
- 冻结引用摘要或作用域不匹配时继续解释资格结果。

## 对第六修订版的收紧映射

| `R6` 位置 | `R7` 收紧 |
|---|---|
| `EC-07` 至 `EC-11` | 增加资格认识偏序、资格专用非放大映射和互斥键模式 |
| `EC-02`、`EC-12` 至 `EC-18` | 把认识截点固定为多注册表因果闭合边界向量 |
| `EC-22`、`EC-23` | 增加兼容域快照身份和可验证制度冻结引用 |

## 保留的冻结门槛

即使本增补通过最终闭合复核，仍必须满足：

1. `R4 + R5 + R6 + R7` 已合并为单一候选文档；
2. 合并稿已经通过完整一致性和类型审查；
3. `CR-0002-R1` 或兼容决策模型已经冻结；
4. 来源注册表、资格治理制度和制度注册表能够提供本模型要求的边界与引用；
5. 已建立满足 `IF-0007` 的制度证据包、冻结权威、冻结决定和唯一版本边界。

## 当前审查状态

```text
Revision Scope: PASS
Qualification Epistemic Partial Order: PASS_WITH_REVIEW
Qualification Forward Interpretation Safety: PASS_WITH_REVIEW
Qualification Re-resolution Semantics: PASS_WITH_REVIEW
Qualification Scope Mode Exclusivity: PASS_WITH_REVIEW
Compatibility Domain Snapshot Identity: PASS_WITH_REVIEW
Knowledge Boundary Vector: PASS_WITH_REVIEW
Causal Closure: PASS_WITH_REVIEW
Institution Freeze Reference: PASS_WITH_REVIEW
Historical Immutability: PASS
Projection / Formal Fact Separation: PASS
Policy Separation: PASS
Consolidation Status: REQUIRED
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Model Review Readiness: REVIEW_REQUIRED
Institution Freeze Eligibility: FAIL
```

建议动作：由 Codex 对最后阻断簇及 `R4 + R5 + R6 + R7` 的组合影响执行最终闭合复核。若通过，再进入单一候选稿合并；不得从本修订自动产生候选资格或制度冻结。
