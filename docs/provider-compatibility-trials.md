# 开源视频模型兼容性试运行

本指南说明如何在苹果芯片 Mac 上复现 `Wan2.1-T2V-1.3B` 与 `CogVideoX-2B` 的低成本兼容性试运行。它只验证真实模型能否完成下载、装载、Metal 转移、推理、解码和证据输出，不评价视频质量，也不创建跨提供方制度合同。

## 1. 运行边界

固定试运行合同位于：

```text
experiments/provider_compatibility/trial_contract.json
```

两个模型共享相同英文提示词和随机种子。英文是因为 `CogVideoX-2B` 官方模型卡声明其提示输入只支持英文。首次试运行减少帧数和去噪步数以控制时间与内存；这些参数不能用作正式质量基准。

模型权重来自模型发布方，不进入本仓库。默认缓存位置由 `huggingface_hub` 管理，通常是 `~/.cache/huggingface/hub/`。证据包只记录模型标识、快照修订号、参数、阶段、资源观察和输出摘要，不记录本机用户名、序列号或硬件唯一标识。

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

## 4. 只下载模型，不执行生成

下载与生成是两个不同阶段。只想预取权重时，使用下面的命令；它只导入 `huggingface_hub`，不导入 PyTorch，不建立模型管线，也不使用 Metal。

Wan2.1：

```bash
HF_HUB_DISABLE_TELEMETRY=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download(
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    revision="0fad780a534b6463e45facd96134c9f345acfa5b",
))
PY
```

CogVideoX：

```bash
HF_HUB_DISABLE_TELEMETRY=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download(
    "zai-org/CogVideoX-2b",
    revision="1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
))
PY
```

下载完成后可离线确认精确快照；这个检查不会加载模型：

```bash
HF_HUB_OFFLINE=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

models = {
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers": "0fad780a534b6463e45facd96134c9f345acfa5b",
    "zai-org/CogVideoX-2b": "1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
}
for model_id, revision in models.items():
    print(snapshot_download(model_id, revision=revision, local_files_only=True))
PY
```

上述命令打印的路径应位于 Hugging Face 缓存的 `snapshots/<revision>/` 下。不要把该路径中的模型权重复制进项目仓库。

## 5. 执行完整兼容性试运行

以下命令会真正加载模型并生成视频，内存需求远高于纯下载。当前 36GB 统一内存 Mac 上的 Wan2.1 实测曾把 Metal 驱动分配推至约 30.98GB，并使系统交换空间增加约 23.39GB；执行前应先阅读第 8 节的实测记录，并关闭其他高内存任务。

日常本地操作优先使用独立作业控制台。它会在真实启动前执行资源预检、登记不可变请求，并要求再次输入完整执行标识：

```bash
.venv-provider-compat/bin/python -m operator_console --open
```

控制台默认位于 `http://127.0.0.1:4320/`，完整说明见 [`../operator_console/README.md`](../operator_console/README.md)。当前只有 Wan2.1 文生视频路径允许启动；CogVideoX 虽然缓存完整，但在形成独立运行证据前由控制台失败关闭。

第一次低内存验证应保持以下默认值：

```text
生成档位: wan_probe
执行策略: mps_model_offload_bounded
MPS 建议工作集比例: 0.75
参数: 256×144，9 帧，1 步，8 fps
```

内存探针成功但画面不可辨识时，下一档使用 `wan_quality_probe`：保持 `256×144`、`9` 帧和同一提示词，只把推理步数提高到 `4`。这一步用于隔离“步数对质量与耗时的影响”；在它形成现实证据前，不应同时提高分辨率。

控制台会把这些值写入 `operator-job.v3` 作业请求。启动前必须同时满足至少 `16 GiB` 可用内存和不超过 `4 GiB` 现有换页。运行器先设置进程级 MPS 上限，再单独装载文本编码器，在无梯度推理模式下以叶级顺序卸载形成提示词嵌入并释放，之后才装载 Transformer 与 VAE；推理后释放钩子、管线引用和 MPS 缓存。运行证据分别记录限制配置、组件驻留策略、文本编码器释放、MPS 峰值和最终释放，不能只凭页面选择断言策略已经生效。

需要在浏览器中实时观看阶段、内存、换页、MPS、日志和证据形成过程时，先在另一个终端启动只读观测台：

```bash
.venv-provider-compat/bin/python -m observatory --open
```

观测台的完整说明见 `observatory/README.md`。它不启动或控制试运行；低层命令行方式仍要求独立明确授权，并且不会替代控制台的风险确认体验。下面不带作业规格的命令读取历史固定合同，采用全量 MPS 驻留基线，不具备 `operator-job.v3` 的文本编码器提前释放、换页恢复门禁和进程级比例限制；它只用于复查旧证据，不应作为第一次低内存试运行入口。

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

## 6. 证据内容

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

## 7. 独立校验

```bash
.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-WAN-MAC-001

.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-COGVIDEOX-MAC-001
```

校验器检查清单摘要、文件闭包、请求与执行标识、输出摘要以及公开仓库禁止出现的绝对用户路径。对于控制台创建的受控作业，它还核对固定生成档位、执行策略、MPS 比例、策略激活和推理后的主动释放观察。校验通过只表示证据包可重新审计，不表示视频质量合格或提供者适用性已经通过。

## 8. 低内存验收顺序

低内存实现与真实运行观察必须分开判断。代码和无模型回归测试通过后，按以下顺序建立现实证据：

1. 使用“内存探针”档位，保持 `75%` MPS 上限和分阶段驻留，只执行一个 Wan2.1 作业；
2. 确认没有其他生成进程，启动前可用内存至少 `16 GiB` 且现有换页不超过 `4 GiB`；
3. 在观测台持续查看统一内存、换页增长、MPS 峰值和阶段变化；
4. 运行结束后校验证据包，核对推理后主动释放记录；
5. 只有探针稳定闭合，才允许使用“低内存生成”档位；
6. CogVideoX 仍保持阻断，必须建立自己的装载和推理观察后才能解除。

文本编码器独立阶段形成两次真实失败观察：`LM-WAN-STAGED-PROBE-20260809T161019Z` 证明模型级卸载会让完整 UMT5 进入 MPS；`LM-WAN-LEAF-PROBE-20260809T161726Z` 证明直接调用 `encode_prompt` 时若未禁用自动求导，叶级卸载仍会累积中间状态并触及上限。启用叶级顺序卸载与 `torch.inference_mode()` 后，`LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` 完成了提示词编码、文本编码器释放、去噪管线装载、推理、视频导出和证据闭包。该结果只允许认定固定内存探针可运行，不得外推到更高档位或画面质量。

## 9. 当前 Mac 实测记录

以下数字是一次特定机器、依赖和参数下的观察，不是产品规格或性能承诺。

| 模型 | 当前结论 | 精确快照 | 关键观察 |
| --- | --- | --- | --- |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` | 已完成一次真实生成与证据闭包 | `0fad780a534b6463e45facd96134c9f345acfa5b` | 缓存约 27G；总耗时 2730.198 秒，其中首次快照解析 2661.848 秒；17 帧、416×240、8 fps；Metal 驱动分配峰值 30,979,096,576 字节；交换空间较启动时增加约 23.39GB |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 低内存探针 | 管线和分阶段策略成功激活，推理阶段由换页护栏终止 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、1 步；管线装载 28.482 秒；MPS 驱动采样峰值 4,210,524,160 字节；新增换页 9,075,425,280 字节，超过 8 GiB 预算；无视频输出；执行标识 `LM-WAN-PROBE-20260809T152435Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 无梯度叶级探针 | 已完成受控生成和独立证据闭包 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、1 步、8 fps；总耗时 23.444 秒；MPS 驱动峰值 8,413,462,528 字节；系统换页峰值未超过启动值；输出 11,712 字节；执行标识 `LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 质量探针 | 运行闭合但语义不可辨识 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、4 步、8 fps；总耗时 28.624 秒；MPS 驱动峰值 8,413,462,528 字节；换页没有增长；输出 32,028 字节；画面仍为蓝紫色块，不能识别红色纸船；执行标识 `LM-WAN-QUALITY-PROBE-20260809T170134Z` |
| `zai-org/CogVideoX-2b` | 只完成下载；实际生成能力仍未知 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 19 个文件；逻辑大小 13,775,572,738 字节，缓存约 13G；纯下载 1196.81 秒；下载进程最大常驻内存 4,005,658,624 字节；未导入 PyTorch、未使用 Metal、未执行生成 |

Wan2.1 的既有成功证据位于 `evidence/runtime/CR-0019-WAN-MAC-001/`，第一轮低内存失败证据位于 `evidence/runtime/LM-WAN-PROBE-20260809T152435Z/`，当前无梯度叶级探针成功证据位于 `evidence/runtime/LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z/`，四步质量证据位于 `evidence/runtime/LM-WAN-QUALITY-PROBE-20260809T170134Z/`。CogVideoX 的下载成功不能推出管线可装载、可转移到 Metal 或可完成推理；这些结论必须等待另一次明确授权的低内存生成试运行。

更完整的观察解释见 `knowledge/Wan2.1_and_CogVideoX_Mac_Compatibility.md`。

## 10. 常见问题

### 内存压力或系统换页

小于 64GB 统一内存时，视频扩散模型很容易触发换页。证据中的进程树常驻内存、系统使用量、交换空间与 Metal 驱动分配量应一起阅读，不能把某一个数字称为模型的精确显存。

### Metal 不支持某个算子

试运行显式启用 `PYTORCH_ENABLE_MPS_FALLBACK=1`。不支持的算子可以退回中央处理器，日志与耗时会反映这一现实。若仍失败，应保留错误观察，不要无记录地更换后端。

### 首次运行时间很长

首次运行包含模型下载。`summary.json` 会分开记录快照解析、模型装载、推理和导出阶段；后续缓存命中不应与首次下载耗时混为一项指标。

### 为什么帧数和步数较低

本轮目标是建立实际可运行性与证据能力，不是质量评测。正式跨提供方合同必须另行冻结标准分辨率、帧数、步数、提示编译方式和可比观察，不能直接沿用本试运行参数。
