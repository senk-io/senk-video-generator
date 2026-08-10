# 30 秒样片工作流

本工作流把长视频目标缩小为一个可逐镜头验证的 30 秒项目。它不是让本地模型一次连续生成 30 秒，而是固定六个 5 秒镜头，分别生成候选、人工选择，再组装为时间线。

当前首个项目是 [`PILOT-RED-BOAT-30S-001.json`](../projects/PILOT-RED-BOAT-30S-001.json)：

| 镜头 | 时长 | 叙事作用 |
| --- | ---: | --- |
| `SHOT-001` | 5 秒 | 建立红色纸船与水面 |
| `SHOT-002` | 5 秒 | 平稳漂行 |
| `SHOT-003` | 5 秒 | 遇到微风 |
| `SHOT-004` | 5 秒 | 调整方向 |
| `SHOT-005` | 5 秒 | 穿过暖色倒影 |
| `SHOT-006` | 5 秒 | 抵达岸边 |

项目合同目前是 `DRAFT_NON_AUTHORITATIVE`。题材、镜头和提示词都可以修订，但修订会改变合同摘要；已载入但尚未登记的旧绑定会在预检时失败关闭，避免悄悄漂移。

## 安装与启动

复用提供者兼容性环境：

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

启动作业控制台与只读观测台：

```bash
.venv-provider-compat/bin/python -m operator_console --open
.venv-provider-compat/bin/python -m observatory --open
```

控制台默认位于 `http://127.0.0.1:4320/`，观测台默认位于 `http://127.0.0.1:4319/`。

## 逐镜头操作

1. 在页面顶部的 30 秒样片卡中选择“准备此镜头”。
2. 控制台会载入该镜头固定提示词、镜头绑定和新的执行标识；此时不会加载模型。
3. 检查固定生成档位和资源护栏，确认高内存风险，运行预检。
4. 预检通过后登记不可变作业，再输入完整执行标识启动。
5. 作业完成只代表存在候选输出。打开该作业，输入完整镜头标识，显式选择为当前镜头。
6. 如果候选不合适，重新准备同一镜头并形成新候选；新选择会追加到选择历史，不覆盖旧记录。
7. 六个镜头都有当前选择后，输入完整项目标识并组装结构样片。

作业失败不会使其他镜头失效。已经形成的候选、选择历史和执行证据会保留，因此可以从失败镜头继续。

## 状态与记录

镜头状态包括：

| 状态 | 含义 |
| --- | --- |
| `PLANNED` | 已有镜头合同，尚无作业 |
| `GENERATING` | 已登记或正在执行作业 |
| `CANDIDATES_READY` | 至少一个作业已形成输出，尚未人工选择 |
| `RETRY_AVAILABLE` | 既有尝试未形成可用候选，可以重试 |
| `SELECTED` | 本地操作者已明确选择当前候选 |

本机运行状态位于：

```text
.senknet/operator/
├── jobs/<job-id>/
└── pilots/<project-id>/
    ├── selections.jsonl
    ├── latest_assembly.json
    └── assemblies/<assembly-id>/
```

`selections.jsonl` 是带前序摘要的追加历史。组装清单记录每个镜头的来源作业、来源摘要、来源时长、目标时长以及循环、裁剪、缩放处理。

## 质量边界

当前 `Wan2.1-T2V-1.3B` 的已验证平衡档位只生成约 `1.13` 秒、`256×144` 的候选。组装器可以为结构预览循环短候选、统一为 5 秒并升采样到目标画布，但这些处理不能增加真实细节，也不能形成质量通过。

因此 30 秒工作分两道闸门：

1. 结构闸门：六镜头、精确 30 秒、来源可追踪、失败可续跑；
2. 质量闸门：主体连续、运动稳定、无严重形变、达到目标清晰度，并由人工观看确认。

只有结构闸门和质量闸门都满足，才能把样片称为合格。当前实现允许建立结构样片，但不会自动声明合格或发布。

当前逐镜头进展：`SHOT-001` 已形成精确五秒折纸候选并通过技术连续性阈值，但仍等待按完整镜头标识进行人工选择。`SHOT-002` 已完成四十一帧源探针和绑定真实摘要的四十帧纯空间方向派生。最终候选为 `40` 帧、`8 fps`、精确 `5` 秒，首尾净向右约 `116.30` 像素，三十九个相邻步骤全部向右，最大相邻跳变约 `4.86` 像素；全部帧保留折纸轮廓、折痕、水面和倒影，未见重影或边缘接缝。该结果建立第二镜头技术候选，不自动产生人工质量接受、正式选择或时间线绑定。

## Shot 002 关键帧自动调整

默认工作区使用 [`cogvideox_shot_002_keyframe_adjustment_v2.json`](../experiments/postprocessing/cogvideox_shot_002_keyframe_adjustment_v2.json)。操作者只需调整第 `1`、`10`、`20`、`30`、`40` 帧，系统会把以下参数自动展开到完整四十帧：

- `x_pixels`：正值向右；
- `y_pixels`：正值向下；
- `scale`；
- `rotation_degrees`：画面坐标中的正值为顺时针；
- `adjustment_reason`；
- `review_status`、评审者和评审时间。

四类参数分别使用不越过关键帧区间的单调三次插值。关键帧值会原样保留；如果某个自动帧仍有异常，可以在 `manual_overrides` 中增加单帧完整参数，覆盖插值结果。系统不会自动选择关键帧，也不会根据输出反向修改合同。

当前五个关键帧均为恒等变换和 `PENDING_REVIEW`，用于验证自动展开链路。修改关键帧或单帧覆盖时必须填写调整原因；记录 `HUMAN_APPROVED` 或 `HUMAN_REJECTED` 时必须填写评审者和时间。

每次渲染必须使用新的执行标识：

```bash
.venv-provider-compat/bin/python tools/render_keyframe_adjustments.py \
  --execution-id KEYFRAME-SHOT-002-<UNIQUE-ID>
```

渲染器只读取现有 `direction_controlled_5s.mp4`，不加载或运行模型，也不做跨帧像素混合。每次派生会生成独立且拒绝覆盖的证据目录，其中包含：

```text
expanded_frame_adjustments.json                # 5 个关键帧展开后的 40 帧参数
adjusted_frames/                               # 全部 40 帧调整结果
keyframe_adjusted_5s.mp4                       # 5 秒预览候选
before_after_keyframe_contact_sheet_40_frames.png
frame_mapping.json                             # 参数来源及关键帧区间
adjustment_summary.json
review_record.json
request.json
environment.json
summary.json
manifest.json
```

渲染后可独立重算插值并校验来源、输出、四十帧映射和未创建正式事实的边界：

```bash
.venv-provider-compat/bin/python tools/verify_keyframe_adjustment_evidence.py \
  evidence/runtime/KEYFRAME-SHOT-002-<UNIQUE-ID>
```

原始 [`cogvideox_shot_002_manual_frame_adjustment_v1.json`](../experiments/postprocessing/cogvideox_shot_002_manual_frame_adjustment_v1.json) 和 `render_manual_frame_adjustments.py` 继续保留为完整逐帧回退工具，不覆盖其既有证据。

存在自动展开和渲染结果不表示参数已获人工认可，也不创建正式视觉质量接受、镜头选择或时间线绑定。

## 验证

样片合同、绑定、选择摘要链和 30 秒组装测试不加载模型：

```bash
.venv-provider-compat/bin/python -m unittest tests.test_pilot_project -v
```

完整测试：

```bash
.venv-provider-compat/bin/python -m unittest discover -v
```
