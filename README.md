# SENK 视频生产治理引擎

> 让本地视频生成从一次性黑箱，变成可验证、可修正、可审计的镜头生产过程。

[![许可证](https://img.shields.io/github/license/senk-io/senk-video-generator?label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](LICENSE)
[![测试](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml/badge.svg?branch=bakboem-dev)](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![平台](https://img.shields.io/badge/%E5%B9%B3%E5%8F%B0-Apple%20Silicon-111111?logo=apple)
![模型](https://img.shields.io/badge/%E6%9C%AC%E5%9C%B0%E6%A8%A1%E5%9E%8B-CogVideoX--2B-F97316)
![阶段](https://img.shields.io/badge/%E9%98%B6%E6%AE%B5-5%20%E7%A7%92%E9%95%9C%E5%A4%B4%E5%80%99%E9%80%89-2EA44F)

## 项目简介

SENK 是一个模型无关的视频生产治理与本地执行项目。模型生成候选画面，系统负责资源护栏、证据、确定性后处理和状态边界。

```text
创作意图 -> 镜头合同 -> 本地生成 -> 验证与修正 -> 人工评审 -> 时间线
```

生成完成不等于质量合格，候选存在也不等于已经进入时间线。

## 已验证进展

| 能力 | 当前观察 |
| --- | --- |
| 内存优化 | CogVideoX 八步同参数对照中，MPS 驱动峰值降低约 `63.884%`，新增换页为 `0` |
| 五秒生成 | 完成 `41` 帧来源生成，并派生为 `40` 帧、`8 fps`、精确 `5.000` 秒候选 |
| 语义连续 | 全部帧保留红色折纸船、水面、倒影和主要折痕 |
| 方向控制 | 第二镜头净向右约 `116.30` 像素，全部 `39` 个相邻位移均向右，未见重影或边缘接缝 |
| 自动回归 | `56` 个单元测试和 `1` 个迁移测试通过，测试不下载或运行模型 |

当前结果仍是技术候选，不是正式视觉质量接受，也不授权直接生成或装配三十秒视频。

## 快速开始

环境要求：支持 MPS 的 Apple Silicon Mac、macOS、Python `3.12`。当前证据使用 Python `3.12.11`。

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

真实模型运行前请先阅读[提供者兼容性试验](docs/provider-compatibility-trials.md)，确认没有残留生成进程，并检查合同中的内存与换页停止线。

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
| `tools/`、`experiments/` | 执行工具、派生工具和固定试验合同 |
| `evidence/runtime/` | 可复核的成功与失败证据样本 |
| `tests/`、`migration_tests/` | 不加载模型的回归测试 |

## 文档

- [项目愿景](foundation/00_ProjectVision.md)
- [治理制度](foundation/02_Governance.md)
- [证据模型](foundation/05_Evidence.md)
- [提供者兼容性与 Mac 实测](docs/provider-compatibility-trials.md)
- [三十秒样片工作流](docs/30-second-pilot.md)
- [作业控制台](operator_console/README.md)
- [观测台](observatory/README.md)

## 开源边界

模型权重和 Hugging Face 缓存不包含在仓库中，也不得提交到 Git。使用者须分别遵守模型、依赖和生成内容对应的许可与使用条件。

贡献前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)，安全问题请按 [`SECURITY.md`](SECURITY.md) 私密报告。项目代码和仓库文档采用 [`Apache-2.0`](LICENSE) 许可证。
