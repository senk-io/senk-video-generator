# 开源视频模型兼容性试运行

本指南说明如何在苹果芯片 Mac 上复现 `Wan2.1-T2V-1.3B` 与 `CogVideoX-2B` 的低成本兼容性试运行。它只验证真实模型能否完成下载、装载、Metal 转移、推理、解码和证据输出，不评价视频质量，也不创建跨提供方制度合同。

## 1. 运行边界

固定试运行合同位于：

```text
experiments/provider_compatibility/trial_contract.json
```

两个模型共享相同英文提示词和随机种子。英文是因为 `CogVideoX-2B` 官方模型卡声明其提示输入只支持英文。首次试运行减少帧数和去噪步数以控制时间与内存；这些参数不能用作正式质量基准。

模型权重来自模型发布方，不进入本仓库。默认缓存位置由 `huggingface_hub` 管理，通常位于用户缓存目录。证据包只记录模型标识、快照修订号、参数、阶段、资源观察和输出摘要，不记录本机用户名、序列号或硬件唯一标识。

## 2. 前置条件

- 苹果芯片 Mac；
- 支持 Metal 的 macOS；
- 至少保留数十 GiB 可用磁盘给两个模型缓存；
- 已安装 `uv`；
- 能访问 Hugging Face 公共模型仓库；
- 运行期间关闭其他高内存任务。

本轮依赖在 `Python 3.12.11` 上冻结。不要使用系统 Python，也不要把虚拟环境或模型权重提交到 Git。

## 3. 安装路径

在仓库根目录执行：

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

验证 Metal 后端和两条模型管线：

```bash
.venv-provider-compat/bin/python - <<'PY'
import torch
from diffusers import CogVideoXPipeline, WanPipeline

print(torch.__version__)
print(torch.backends.mps.is_built())
print(torch.backends.mps.is_available())
print(WanPipeline.__name__)
print(CogVideoXPipeline.__name__)
PY
```

预期 `mps` 的构建状态和可用状态均为 `True`。若为 `False`，不要继续下载模型；先检查是否使用了原生 `arm64` Python、macOS 和 PyTorch 版本。

## 4. 执行方法

Wan2.1：

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider wan \
  --execution-id CR-0019-WAN-MAC-001
```

CogVideoX：

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider cogvideox \
  --execution-id CR-0019-COGVIDEOX-MAC-001
```

脚本默认把证据写入：

```text
evidence/runtime/<execution-id>/
```

每个执行标识只能使用一次。目录已经存在时脚本会失败关闭，防止覆盖既有证据。

## 5. 证据内容

完整执行会形成：

```text
environment.json
request.json
process_metrics.jsonl
mps_metrics.jsonl
runtime.log
worker_state.json
summary.json
output.mp4
thumbnail.png
manifest.json
```

如果模型下载、装载、转移、推理或导出失败，输出视频可能不存在；父进程仍会保存退出码、已完成阶段、错误观察与内存轨迹。失败证据不等于模型永久不支持 Mac，只证明指定版本、参数与机器上下文中的本次现实。

## 6. 独立校验

```bash
.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-WAN-MAC-001

.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-COGVIDEOX-MAC-001
```

校验器检查清单摘要、文件闭包、请求与执行标识、输出摘要以及公开仓库禁止出现的绝对用户路径。校验通过只表示证据包可重新审计，不表示视频质量合格或提供者适用性已经通过。

## 7. 常见问题

### 内存压力或系统换页

小于 64GB 统一内存时，视频扩散模型很容易触发换页。证据中的进程树常驻内存、系统使用量、交换空间与 Metal 驱动分配量应一起阅读，不能把某一个数字称为模型的精确显存。

### Metal 不支持某个算子

试运行显式启用 `PYTORCH_ENABLE_MPS_FALLBACK=1`。不支持的算子可以退回中央处理器，日志与耗时会反映这一现实。若仍失败，应保留错误观察，不要无记录地更换后端。

### 首次运行时间很长

首次运行包含模型下载。`summary.json` 会分开记录快照解析、模型装载、推理和导出阶段；后续缓存命中不应与首次下载耗时混为一项指标。

### 为什么帧数和步数较低

本轮目标是建立实际可运行性与证据能力，不是质量评测。正式跨提供方合同必须另行冻结标准分辨率、帧数、步数、提示编译方式和可比观察，不能直接沿用本试运行参数。
