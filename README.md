# senk-video-generator
> 这不是 SENK Workfit 的业务仓!!!.

> 由 SENK 管理，为 Seedance、本地开源模型及其他视频能力提供统一、可验证、可修正、可审计的受控生产过程。

[![许可证](https://img.shields.io/github/license/senk-io/senk-video-generator?label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](LICENSE)
[![测试](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml/badge.svg?branch=bakboem-dev)](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![管理](https://img.shields.io/badge/%E7%AE%A1%E7%90%86-SENK-111111)
![架构](https://img.shields.io/badge/%E6%9E%B6%E6%9E%84-%E6%8F%90%E4%BE%9B%E8%80%85%E6%97%A0%E5%85%B3-7C3AED)
![接入](https://img.shields.io/badge/%E6%8E%A5%E5%85%A5-Seedance%20%7C%20%E6%9C%AC%E5%9C%B0%E6%A8%A1%E5%9E%8B-0284C7)
![阶段](https://img.shields.io/badge/%E9%98%B6%E6%AE%B5-5%20%E7%A7%92%E9%95%9C%E5%A4%B4%E5%80%99%E9%80%89-2EA44F)

## 项目简介

`senk-video-generator` 是由 SENK 管理的模型无关视频生产项目。SENK 是项目所属公司的名称，不是视频模型、提供者或协议。项目通过 `ProviderAdapter` 隔离模型专属协议，可接入 Seedance、Veo、Kling、Runway、本地开源模型以及未来的其他视频能力。模型负责生成候选画面，本项目负责合同、资源护栏、证据、确定性后处理和状态边界。

```text
创作意图 -> 模型无关镜头合同 -> ProviderAdapter -> 任意模型 -> 验证与修正 -> 人工评审 -> 时间线
```

生成完成不等于质量合格，候选存在也不等于已经进入时间线。

## 模型边界

- Seedance 等高质量模型是正式能力提供者候选，只需在适配器层编译其请求和结果，不改变上层治理语义。
- 当前参考适配器包括本地 `CogVideoX-2B`、`Wan2.1-T2V-1.3B`，以及远端 `MiniMax-H3` 开放平台 `V2` 接口。三者的运行后端、费用、资源与证据合同彼此独立。
- 本地小模型用于低成本验证受控生成、资源停止线、证据闭包、后处理和人工选择流程，不代表项目的模型上限或最终画质目标。

### MiniMax H3 接入

`MiniMax-H3` 已作为独立 `ProviderAdapter` 接入。当前 `36GB` 苹果芯片机器不启动公开权重：官方 `BF16` 基础模型包含 `33B` 稠密视频变换器与完整 `Qwen3-VL-32B` 编码器；官方 `ComfyUI` 文生视频量化组合仍约 `39.55 GiB`，且尚无本机已验证的 `MPS` 量化算子路径。因此第一轮效果试验使用官方远端 `V2` 接口，不下载模型权重。

真实密钥只写入未跟踪的 `.env`：

```bash
cp .env.example .env
# 在 .env 中填写 MINIMAX_API_KEY
set -a
. ./.env
set +a
```

默认命令只做无费用预检；只有显式增加 `--execute` 才提交计费任务：

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial

.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial \
  --execute \
  --execution-id MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ

.venv-provider-compat/bin/python -m tools.verify_minimax_h3_evidence \
  evidence/runtime/MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

固定试验生成 `768P`、`5` 秒、`16:9`、`24 fps` 且包含 `32 kHz` 双声道音频的候选。自动校验只确认技术合同与证据闭包；哭泣语义、泪水滚落、身份连续性和音画情绪同步仍需人工评审。

### Seedance 接入准备

Seedance 适配器尚未实现，以下配置只建立安全的凭据入口，不会自动获得执行能力。根据 [BytePlus ModelArk 官方文档](https://docs.byteplus.com/en/docs/modelark/1520757)，先在控制台创建 API Key，然后写入本地环境：

```bash
cp .env.example .env
# 在 .env 中填写 ARK_API_KEY，不要把真实值提交到 Git
set -a
. ./.env
set +a
test -n "${ARK_API_KEY:-}" && echo "Seedance API Key 已载入"
```

`.env` 已被 Git 忽略。未来适配器只能在进程运行时读取 `ARK_API_KEY`；不得把密钥写入镜头合同、执行请求、日志、证据包或前端状态。

### 一句话镜头规划

本地文本模型可以先把一句创作意图输出为非权威的场景、叙事节拍和镜头草案，再由
确定性观察器检查原句覆盖、稳定标识、显式语义、单一镜头用途、主体引用、时长和
连续性。当前参考合同把每轮固定拆为 `scene_context`、`beat_purpose`、`shot_core`、
`composition`、`performance`、`lighting` 和 `continuity` 七个扁平阶段；三轮共
二十一次本地调用且不自动重试。场景角色、构图、表演、灯光和连续性标记由系统按
版本化合同展开，可观察检查项由请求约束和已选标记确定性派生。重复运行分别报告
结构一致率与受控语义一致率，但不会自动创建正式 `ShotSpec` 或质量裁决。

默认单请求命令仍保留已取证的 `v7` 哭泣特写基线。通用性观察另使用版本化的
`request.v2`、中立主体词表和三用例套件，避免把单一请求下的稳定性误写成跨请求
理解能力。已取证的 `v11` 先用失败关闭的确定性提取器锁定原句明确事实，模型只输出残余字段。
雨中哭泣、室内微笑和自行车用例分别锁定 `9`、`11`、`9` 个字段；`63/63`
次本地调用和 `9/9` 轮严格解析全部完成，模型没有写入锁定字段。保留观察从
`v10` 的 `120` 项降到 `93` 项，但残余的场景连续性、构图、灯光和动作连续性选择仍使
`0/9` 形成结构可观察草案。因此该 `0.6B` 路径仍只能提供诊断观察，不能自动批准镜头。

后续 `v12` 只收紧确定性边界：新增独立的提取器 `v2`，逐词法命中保留可重算的极性决定；
命中已登记受控词法或守卫词根的明确否定，若没有受控的同字段正向替代，会在证据落盘和模型调用前
阻断，不能再作为残余字段交给模型猜测。受控的“而是/反而/改用”纠正、肯定惯用语、主体/摄影机穿越和“固定相机参数”
另有固定边界。`v11` 继续永久绑定提取器 `v1`，既有证据不会被新语义重释。`v12` 目前只有
固定合同、对抗回归和伪模型证据重算，没有新的真实模型运行或质量提升结论。

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite \
  --suite experiments/shot_planning/qwen3_0_6b_hybrid_source_facts_generalization_suite_v1.json

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --contract experiments/shot_planning/qwen3_0_6b_guarded_source_facts_smile_trial_v12.json
```

完整合同与三次运行比较方式见[一句话镜头规划草案](docs/one-sentence-shot-planning.md)。

## 本地参考验证

| 能力 | 当前观察 |
| --- | --- |
| 内存优化 | CogVideoX 八步同参数对照中，MPS 驱动峰值降低约 `63.884%`，新增换页为 `0` |
| 五秒生成 | 完成 `41` 帧来源生成，并派生为 `40` 帧、`8 fps`、精确 `5.000` 秒候选 |
| 语义连续 | 全部帧保留红色折纸船、水面、倒影和主要折痕 |
| 方向控制 | 第二镜头净向右约 `116.30` 像素，全部 `39` 个相邻位移均向右，未见重影或边缘接缝 |
| 自动回归 | `161` 个单元测试和 `1` 个迁移测试通过，测试本身不下载或运行模型 |

这些结果证明受控生成过程可以闭合，不表示本地小模型是唯一运行路径，也不构成正式视觉质量接受。

## 快速开始

以下步骤用于复现当前本地 MPS 参考实现，要求支持 MPS 的 Apple Silicon Mac、macOS 和 Python `3.12`。当前证据使用 Python `3.12.11`。

```bash
git clone git@github.com:senk-io/senk-video-generator.git
cd senk-video-generator
python3.12 -m venv .venv-provider-compat
.venv-provider-compat/bin/python -m pip install --upgrade pip
.venv-provider-compat/bin/python -m pip install -r requirements-provider-compat.txt
```

只运行测试时，可以安装较小的依赖集：

```bash
.venv-provider-compat/bin/python -m pip install -r requirements-test.txt
.venv-provider-compat/bin/python -m unittest discover -s tests -v
.venv-provider-compat/bin/python -m unittest discover -s migration_tests -v
```

## 本地界面

```bash
.venv-provider-compat/bin/python -m operator_console --open
.venv-provider-compat/bin/python -m observatory --open
```

- 作业控制台：`http://127.0.0.1:4320/`
- 只读观测台：`http://127.0.0.1:4319/`

两个服务只允许绑定回环地址。控制台负责受控作业，观测台只读取状态，不启动模型或创建质量裁决。

## 运行受控探针

下面的 CogVideoX 命令只是本地参考探针。真实模型运行前请先阅读[提供者兼容性试验](docs/provider-compatibility-trials.md)，确认没有残留生成进程，并检查合同中的内存与换页停止线。

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-LOCAL-PROBE-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_8_steps.json

.venv-provider-compat/bin/python -m tools.verify_provider_compatibility_evidence \
  evidence/runtime/LM-COGVIDEOX-LOCAL-PROBE-YYYYMMDDTHHMMSSZ
```

每个执行标识只能使用一次。成功与失败证据都会保存在 `evidence/runtime/<execution-id>/`。校验通过只表示证据包可审计，不代表画面质量已经通过。

## 目录

| 目录 | 内容 |
| --- | --- |
| `foundation/`、`execution/`、`video/` | 治理、执行闭环与视频领域模型 |
| `operator_console/`、`observatory/` | 本地作业控制台与只读观测台 |
| `provider_adapters/` | 本地或远端提供者专属协议隔离层 |
| `tools/`、`experiments/` | 执行工具、派生工具和固定试验合同 |
| `evidence/runtime/` | 可复核的成功与失败证据样本 |
| `tests/`、`migration_tests/` | 不加载模型的回归测试 |

## 文档

- [项目愿景](foundation/00_ProjectVision.md)
- [治理制度](foundation/02_Governance.md)
- [证据模型](foundation/05_Evidence.md)
- [提供者兼容性与 Mac 实测](docs/provider-compatibility-trials.md)
- [一句话镜头规划草案](docs/one-sentence-shot-planning.md)
- [三十秒样片工作流](docs/30-second-pilot.md)
- [作业控制台](operator_console/README.md)
- [观测台](observatory/README.md)

## 开源边界

模型权重和 Hugging Face 缓存不包含在仓库中，也不得提交到 Git。Seedance 等外部能力的访问凭据同样不得进入仓库。使用者须分别遵守模型、服务、依赖和生成内容对应的许可与使用条件。

贡献前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)，安全问题请按 [`SECURITY.md`](SECURITY.md) 私密报告。项目代码和仓库文档采用 [`Apache-2.0`](LICENSE) 许可证。
