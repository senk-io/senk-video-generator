# 一句话镜头规划草案

本切片把一句自然语言创作意图转换为可观察的非权威镜头草案。它不创建正式
`ShotSpec`，不调用视频提供者，也不产生质量通过、失败、选择或时间线绑定事实。

## 项目存续硬门槛

规划门、诊断门与对抗门是项目存续硬门槛：三门全过才能继续，任一不过即停项目。
冻结原文、现状差距和过线/停项目判定见
[`shot-planning-acceptance-gates.md`](./shot-planning-acceptance-gates.md)。
本文件只保留草案合同与历史观察，不得降低该门槛，也不得用缩文本、缩写顶覆盖或
缺证据补叙事冒充过线。

```text
一句话请求
  -> 显式语义约束
  -> 确定性原句事实提取与字段所有权
  -> 本地文本模型分阶段残余载荷
  -> 系统确定性合并
  -> 系统确定性上下文与可观察文本编译
  -> 结构观察
  -> 语义与可观察性检查
  -> 多次运行稳定性观察
  -> 人工或获授权策略决定后续动作
```

## 固定边界

- 第一至第七版请求和草案使用 `shot-planning-request.v1` 与
  `shot-planning-proposal.v1`；第八至第十二版并行使用 `shot-planning-request.v2` 与
  `shot-planning-proposal.v2`，不迁移或改写历史证据。
- 草案必须保持 `DRAFT_NON_AUTHORITATIVE`。
- 叙事节拍必须引用原句的精确字符区间，非标点内容不得遗漏。
- 场景按地点、时间或主要叙事目标变化拆分；镜头按单一画面用途拆分。
- 每个镜头只有一个 `primary_purpose` 和一个主要 `action`。
- 提供者专属提示词仍由后续 `ProviderAdapter` 编译。
- 自动观察不评价艺术质量，创意结果始终保留人工评审入口。
- 结构一致只表示重复输出结构相同，不表示镜头忠实或可接受。
- 受控语义一致单独观察构图、表演、灯光、连续性和镜头核心枚举，不用结构一致率
  代替这些字段的一致性。

## 本地模型提示

模型无关提示合同仍可单独生成：

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --print-prompt
```

调用方必须把实际 `model_id`、`model_version`、`run_id`、温度和随机种子写回每次
原始输出。验证工具不会补造这些执行证据。

当前有界参考试验固定使用 `Qwen/Qwen3-0.6B` 的修订
`c1899de289a04d12100db370d81485cdf75e47ca`。模型权重为 `1,503,300,328` 字节，
推理在本机 `MPS` 完成，不调用远端推理接口。省略 `--execute` 时只做预检：

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --execute \
  --execution-id LOCAL-SHOT-PLAN-QWEN3-V7-YYYYMMDDTHHMMSSZ
```

当前第七版把每轮规划固定拆成 `scene_context`、`beat_purpose`、`shot_core`、
`composition`、`performance`、`lighting` 和 `continuity` 七个单职责阶段；三轮共
二十一次调用，自动重试预算为零。场景上下文只输出受控标记，节拍动作复用同次运行
的完整 `shot_core.action_description`。稳定标识、原文区间、目标时长、主体引用、
模型修订、草案状态和可观察检查项均由系统按版本化合同确定性编译，小模型无权生成
这些治理字段或检查结论。

第七版仍是默认单请求复现实验，不代表通用镜头理解。跨请求观察使用独立的三用例
套件：雨中哭泣特写、室内微笑中景、自行车从左向右穿过夜间街道的固定相机全景。
每个用例固定三轮、每轮七阶段，总计六十三次调用；三个用例共享一次模型加载，
自动重试仍为零。保留期望只参与事后观察，不进入任何模型提示。

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite \
  --suite experiments/shot_planning/qwen3_0_6b_hybrid_source_facts_generalization_suite_v1.json

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite \
  --suite experiments/shot_planning/qwen3_0_6b_hybrid_source_facts_generalization_suite_v1.json \
  --execute \
  --execution-id LOCAL-SHOT-PLAN-QWEN3-HYBRID-SOURCE-FACTS-YYYYMMDDTHHMMSSZ
```

## 单次结构观察

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --proposal /absolute/path/to/proposal-001.json
```

## 重复运行稳定性观察

初次观察建议使用相同模型版本、提示合同和采样设置运行三次：

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --proposal /absolute/path/to/proposal-001.json \
  --proposal /absolute/path/to/proposal-002.json \
  --proposal /absolute/path/to/proposal-003.json
```

报告一方面记录场景数、节拍数、镜头数、用途序列、动作类别、景别、运镜、场景映射
和时长分布的结构一致率，另一方面独立记录镜头核心、构图、表演、灯光与连续性受控
字段及其整组标记的一致率。重复的
`proposal_id` 或 `run_id` 不会被重复计数；模型版本、提示合同或采样设置不一致时整组
比较失败关闭。报告只建立观察，不把某个一致率阈值解释为正式稳定或接受裁决。

## 单请求七轮本地观察

| 版本 | 严格 JSON | 可比较草案 | 主要观察 |
| --- | --- | --- | --- |
| `v1` | `0/3` | `0/3` | 三轮均出现代码围栏、治理字段层级错误并遗漏镜头数组 |
| `v2` | `3/3` | `0/3` | 裸 JSON 已稳定，但模型只返回嵌套模板的第一个场景项 |
| `v3` | `3/3` | `3/3` | 三阶段结构一致率 `1.0`，但人工复核发现“特写、哭泣、雨中”没有被忠实执行 |
| `v4` | `3/3` | `0/3` | 核心语义已稳定纠正，仍有五项构图、情绪、连续性和检查文本不可观察差异 |
| `v5` | `3/3` | `3/3` | 七阶段受控文本消除五项短文本差异；人工复核又发现地点、时间角色错误和 `ZOOM + LEFT + FAST` 不相容组合 |
| `v6` | `3/3` | `0/3` | 地点、时间与相机策略已收敛；模型仍把允许文本“持续降雨”“孩子在雨中哭泣”稳定缩写为“雨”“哭”，系统拒绝编译 |
| `v7` | `3/3` | `3/3` | 场景改为标记化上下文并复用完整核心动作；三轮七阶段原始输出逐阶段相同且提案阻断观察均为零，结构与受控语义最大精确组比例均为 `1.0` |

第五至第七版没有为了形成零差异而降低 `minimum_free_text_characters` 或接受缩写。
第七版结果证明当前请求在固定模型、修订、提示合同和受控词表下，可以形成三份结构
与受控语义一致的可比较草案；它没有证明艺术质量、通用请求覆盖率或视频生成效果，
所以草案仍保持 `DRAFT_NON_AUTHORITATIVE` 并要求人工创作复核。

## 多请求通用性观察

| 版本 | 严格解析运行 | 可比较草案 | 保留观察 | 主要观察 |
| --- | --- | --- | --- | --- |
| `v8` | `9/9` | `0/9` | `228` | 多候选以单元素数组输出；系统按合同拒绝类型错误，没有自动拆箱或修补 |
| `v9` | `9/9` | `3/9` | `153` | 标量候选消除数组形状问题；哭泣用例可编译但三轮都误选 `WIDE`，微笑与自行车用例仍被阶段约束阻断 |
| `v10` | `9/9` | `0/9` | `120` | 候选中文释义减少错误选择，但仍出现环境连续性错误、非法枚举以及把主体横向运动误判为相机 `PAN` |
| `v11` | `9/9` | `0/9` | `93` | 确定性提取分别锁定 `9/11/9` 个显式与可确定派生字段；模型没有写入锁定字段，但残余的连续性、构图和灯光选择仍阻断所有运行 |
| `v12` | 未执行 | 未执行 | 不适用 | 只新增版本化的否定、转折、复合词及主体/相机边界保护；当前没有真实模型套件证据 |

三轮内部受控指纹相同只能说明模型重复了相同选择；当选择本身错误时，不得把这种
一致性解释为语义稳定或质量通过。第十一版证明明确事实所有权能减少观察：雨中哭泣、室内微笑和自行车
用例每轮的受控值不匹配数分别从 `6/9/7` 降为 `5/7/6`，微笑用例的三轮提案也保留了精确原句回显。
但 `Qwen3-0.6B` 对剩余 `17–19` 个字段的跨阶段语义选择仍不足，两个用例在合并后被连续性
观察阻断，微笑用例也未满足可观察文本要求。下一步应在同一残余字段合同上比较更强的本地
文本模型，或只对新的明确、无歧义句式扩展确定性规则；不应推断未声明的连续性，也不应降低观察阈值。

第十二版不是对第十一版证据的覆盖修复。`trial.v11`、`extractor.v1`、`extraction.v1`
和 `hybrid prompt.v11` 保持封闭绑定；`trial.v12` 才绑定 `extractor.v2`、`extraction.v2`
和 `guarded prompt.v12`。`extractor.v2` 为每个词法命中记录 `ASSERTED`、`NEGATED`、
`CONTEXT_ONLY`、`UNRESOLVED` 或 `IGNORED_QUOTED`；命中已登记受控词法或守卫词根、且没有
受控同字段正向替代的明确否定，以及无法解析的已命中嵌套极性，会在证据落盘和模型调用前阻断。对抗回归覆盖“并非/从未/别/勿”、
“而是/反而/改用”受控纠正、肯定惯用语、非否定复合词、主体附近摄影机横向移动以及
“固定相机参数”等边界。现有三个正向用例在两版提取器下仍锁定相同的 `9/11/9` 个字段，
因此只能证明接线无回归，不能证明模型质量改善。

七轮证据包都可重新核对文件集合和摘要。第七版实际执行标识为
`LOCAL-SHOT-PLAN-QWEN3-V7-20260812T165514Z`，证据清单覆盖 `98` 个文件：

```bash
.venv-provider-compat/bin/python -m tools.verify_local_shot_planner_evidence \
  evidence/runtime/LOCAL-SHOT-PLAN-QWEN3-V7-20260812T165514Z
```

完整性复核结果为 `COMPLETE_AND_DIGEST_MATCHED`。该结果只说明证据文件集合和摘要与
固定合同一致，不是正式镜头规格或质量接受。

第八至第十一版套件证据也均可复核。第十一版执行标识为
`LOCAL-SHOT-PLAN-QWEN3-HYBRID-SOURCE-FACTS-20260813T022128Z`，记录了提取器、字段所有权、
模型残余载荷、确定性合并和套件汇总器的实现摘要；三用例共六十三次调用、一次模型加载、
零自动重试：

```bash
.venv-provider-compat/bin/python -m tools.verify_local_shot_planner_suite \
  evidence/runtime/LOCAL-SHOT-PLAN-QWEN3-HYBRID-SOURCE-FACTS-20260813T022128Z
```

复核结果同样为 `COMPLETE_AND_DIGEST_MATCHED`，但套件明确保留
`formal_shot_spec_created=false`、`formal_quality_acceptance_created=false` 和人工复核
要求。第十版执行仍保留为
`LOCAL-SHOT-PLAN-QWEN3-SEMANTIC-GLOSS-20260812T174803Z`；较早的 `v8`、`v9` 套件执行分别为
`LOCAL-SHOT-PLAN-QWEN3-GENERALIZATION-20260812T173104Z` 与
`LOCAL-SHOT-PLAN-QWEN3-SCALAR-GENERALIZATION-20260812T173628Z`；首次因实现缺口中止的
`LOCAL-SHOT-PLAN-QWEN3-GENERALIZATION-20260812T173012Z` 原样保留，不作为完整套件引用。
