# 开源视频模型兼容性试运行

本指南说明如何复现 `Wan2.1-T2V-1.3B`、`CogVideoX-2B` 的苹果芯片本地兼容性试运行，以及 `MiniMax-H3` 开放平台 `V2` 的受控远端试运行。它只验证指定后端能否完成请求、执行、输出和证据闭包，不评价视频质量，也不创建跨提供方制度合同。

## MiniMax H3 远端效果试验

`MiniMax-H3` 于 `2026-07-31` 发布。官方资料说明其支持文本、图像、视频、音频统一上下文，可输出最长 `15` 秒、最高 `2K`、带原生双声道音频的视频。当前固定试验只使用文本输入与较低的 `768P`、`5` 秒、`16:9` 参数，用于和既有虚构儿童哭泣特写候选作受限语义观察，不形成严格成本或速度基准。

本机不执行公开权重。官方完整仓库逻辑体积约 `464.24 GiB`；官方 `ComfyUI` 文生视频量化组合由约 `19.53 GiB` 视频模型、`14.61 GiB` 文本编码器、`4.85 GiB` 视频 VAE 和 `0.56 GiB` 音频 VAE 组成，合计约 `39.55 GiB`。这个体积已超过当前机器的 `36GB` 统一内存，且 `NVFP4/AWQ` 文本编码器尚无本项目验证过的 `MPS` 执行路径。不得通过下载权重或放宽换页预算碰运气。

官方来源：

- [MiniMax H3 发布说明](https://minimaxi.com/blog/minimax-h3)
- [MiniMax H3 公开权重仓库](https://github.com/MiniMax-AI/MiniMax-H3)
- [MiniMax H3 开放平台 V2 接口](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [ComfyUI MiniMax H3 工作流](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)

固定合同位于：

```text
experiments/provider_compatibility/minimax_h3_fictional_child_crying_closeup_v1.json
```

先把密钥放入未跟踪的 `.env` 并载入当前终端。适配器只检查 `MINIMAX_API_KEY` 是否存在，不在任何输出、日志或证据中记录其值：

```bash
cp .env.example .env
# 编辑 .env，填写 MINIMAX_API_KEY
set -a
. ./.env
set +a
```

默认只执行无费用预检，不提交任务：

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial
```

预检通过后，必须显式加入 `--execute` 和新的执行标识才会提交计费任务：

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial \
  --execute \
  --execution-id MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

适配器固定连接 `https://api.minimax.io`，调用 `/v2/video_generation`，轮询 `/v2/query/video_generation/{task_id}`，成功后立即下载临时输出地址。签名下载地址和授权头不会进入证据。自动技术门禁要求输出短边为 `768` 像素、约 `5` 秒、`24 fps`，并包含 `32 kHz` 双声道音频。

如果本地轮询在远端任务进入终态前失败或超时，适配器会调用 `/v2/video_generation/{task_id}` 尝试取消，并把结果写入 `cancellation_attempt.json`。官方接口只允许取消排队任务，运行中任务可能拒绝取消；因此关闭本地终端不等于云端执行已经停止，必须依据取消证据或随后查询到的终态判断实际费用边界。

独立校验：

```bash
.venv-provider-compat/bin/python -m tools.verify_minimax_h3_evidence \
  evidence/runtime/MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

校验成功只表示模型标识、请求参数、任务终态、媒体技术属性、文件摘要、证据闭包和凭据扫描一致。虚构儿童近景、哭泣语义、清晰泪水滚落、下唇颤动、身份连续性、安全表演语境、呼吸或抽泣声音以及音画同步全部保留为逐帧与人工创意评审；不得由生成适配器自行判定通过。

## 1. 运行边界

固定试运行合同位于：

```text
experiments/provider_compatibility/trial_contract.json
```

两个模型共享相同英文提示词和随机种子。英文是因为 `CogVideoX-2B` 官方模型卡声明其提示输入只支持英文。首次试运行减少帧数和去噪步数以控制时间与内存；这些参数不能用作正式质量基准。

固定合同要求模型级分阶段驻留、`65%` MPS 建议工作集上限、运行中至少 `5 GiB` 可用内存以及最多 `4 GiB` 新增换页。连续低于可用内存预算或换页增长超过预算时，父进程会请求子进程保存停止证据并释放资源。

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

控制台默认位于 `http://127.0.0.1:4320/`，完整说明见 [`../operator_console/README.md`](../operator_console/README.md)。当前只有 Wan2.1 文生视频路径允许启动。CogVideoX 已形成最小去噪和独立小瓦片解码证据，但尚未形成一体化低内存作业和质量验收，因此控制台继续失败关闭。

第一次低内存验证应保持以下默认值：

```text
生成档位: wan_probe
执行策略: mps_model_offload_bounded
MPS 建议工作集比例: 0.75
参数: 256×144，9 帧，1 步，8 fps
```

内存探针成功但画面不可辨识时，下一档使用 `wan_quality_probe`：保持 `256×144`、`9` 帧和同一提示词，只把推理步数提高到 `4`。这一步用于隔离“步数对质量与耗时的影响”；在它形成现实证据前，不应同时提高分辨率。

控制台会把这些值写入 `operator-job.v4` 作业请求。启动前必须同时满足至少 `16 GiB` 可用内存和不超过 `4 GiB` 现有换页。运行器先设置进程级 MPS 上限，再单独装载文本编码器，在无梯度推理模式下以叶级顺序卸载形成提示词嵌入并释放，之后才装载 Transformer 与 VAE；推理后释放钩子、管线引用和 MPS 缓存。运行证据分别记录限制配置、组件驻留策略、文本编码器释放、MPS 峰值和最终释放，不能只凭页面选择断言策略已经生效。

需要在浏览器中实时观看阶段、内存、换页、MPS、日志和证据形成过程时，先在另一个终端启动只读观测台：

```bash
.venv-provider-compat/bin/python -m observatory --open
```

观测台的完整说明见 `observatory/README.md`。它不启动或控制试运行；低层命令行方式仍要求独立明确授权，并且不会替代控制台的风险确认体验。下面不带作业规格的命令读取固定兼容性合同，具备 MPS 比例、运行中可用内存、新增换页限制和 Wan 专用文本编码器提前释放，但不执行控制台的启动前换页恢复门禁；它只用于独立兼容性证据，不应作为日常生成入口。

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

CogVideoX 固定八步质量探针：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-8STEP-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_8_steps.json
```

十六步对照使用 `cogvideox_quality_16_steps.json` 和新的执行标识。三十二步材质与雨景探针使用 `cogvideox_quality_32_steps.json`，继续保持九帧和全部固定输入，只增加推理步数：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps.json
```

三个九帧受控合同只允许相对四步基线改变推理步数；模型快照、提示词、种子、画幅、帧数、引导系数、帧率和资源预算保持不变。它们只建立质量观察，不自动创建质量接受或控制台启动权限。三十二步合同还明确禁止直接生成五秒或进入三十秒时间线。

三十二步固定提示词仍没有形成清楚折痕后，折纸提示词对照使用独立合同，只把提示词中的主体描述改为折叠纸艺和清晰三角折痕；步数、种子、九帧画幅和全部资源边界保持不变：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-ORIGAMI-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps_origami_prompt.json
```

这个合同仍只允许九帧输出，不自动生成五秒。只有折纸结构、主体语义和场景语义逐帧闭合后，才能单独建立新的四十一帧资源合同。

九帧折纸门禁通过后，五秒折纸候选使用独立合同 `cogvideox_five_second_32_steps_origami.json`。合同保持 `65%` MPS 上限、至少 `5 GiB` 可用内存停止线和最多 `4 GiB` 新增换页停止线，并禁止自动重试：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-32STEP-ORIGAMI-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_32_steps_origami.json
```

该合同生成 `41` 帧源输出，再裁切为 `40` 帧、`8 fps`、精确 `5` 秒。若主体质心仍超过既有稳定阈值，只能使用绑定来源摘要的 `cogvideox_origami_temporal_stability_v1.json` 派生新证据，不得修改来源或重跑模型。

九帧分阶段严格对照闭合后，五秒候选观察使用独立合同 `cogvideox_five_second_16_steps.json`。该合同固定十六步质量基线、`41` 帧源输出、`65%` MPS 上限、至少 `5 GiB` 可用内存停止线和最多 `4 GiB` 新增换页停止线；只有源输出完整形成后，运行器才按 `DROP_LAST_FRAME` 派生 `40` 帧、`8 fps`、精确 `5` 秒的 `derived_5s.mp4`：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-16STEP-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_16_steps.json
```

五秒合同只允许单次受控执行；失败时保留证据且不自动重试。成功也只产生候选观察，不创建正式质量接受、控制台权限、跨提供方合同、制度冻结或三十秒时间线。运行前仍必须独立确认没有生成进程、内存压力正常并记录换页基线。

既有五秒候选出现主体位置抖动时，可以在不重新运行模型、不修改来源证据的前提下，使用固定派生合同 `cogvideox_temporal_stability_v1.json` 形成一个独立的技术稳定候选。合同锁定来源视频摘要，以首尾红色主体质心之间的直线路径进行整数像素平移，边缘采用复制填充，再执行权重为 `1:4:1` 的对称三帧混合：

```bash
.venv-provider-compat/bin/python -m tools.stabilize_cogvideox_candidate \
  --execution-id LM-COGVIDEOX-STABILITY-DERIVATION-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_temporal_stability_v1.json
```

该派生不使用模型或 MPS，不覆盖来源资产，也不修复模型没有生成的雨滴、纸张折痕或水面细节。观察阈值只约束主体是否保留、相邻质心跳变和面积变化；全部满足也不等于视觉质量接受、镜头选择或时间线绑定。

第二镜头九帧来源已经保留折纸结构、水面和倒影，但提示词要求向右时实际净向左。该偏差不得用模型自动重试或水平镜像隐藏，因为水平镜像也会反转已经正确的船头朝向。固定派生合同 `cogvideox_shot_002_rightward_direction_v1.json` 锁定来源执行标识和视频摘要，以首帧主体质心为起点建立净向右 `32` 像素的直线路径，逐帧执行最近整数像素平移、边缘复制和 `1:4:1` 对称三帧混合：

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_direction_v1.json
```

执行预算只有一次派生和零次模型运行。派生后要求九帧都保留红色主体、首尾净向右至少 `24` 像素、八个相邻横向位移都至少为 `0.5` 像素、最大相邻质心跳变不超过 `5.5` 像素、平均跳变不超过 `4.5` 像素、最大相邻主体面积变化不超过 `13%`。工具同时导出九张独立复核图和一张九帧联系图。阈值满足只闭合九帧方向控制观察；不得直接外推到四十一帧，也不得创建视觉接受、镜头选择或时间线绑定。

首次且唯一一次执行 `LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-20260810T023111Z` 将首尾净横向位移从向左 `18.775` 像素改为向右 `31.804` 像素，证明固定平移路径能够改变整体方向观察。但是最后一个相邻步回退 `1.726` 像素，最大相邻质心跳变为 `9.954` 像素，平均跳变为 `4.981` 像素，最大相邻主体面积变化为 `15.767%`，四项门禁没有闭合。全部九帧保留折纸船、水面和倒影，但第 `4`、`5`、`7`、`8`、`9` 帧出现可见的半透明双轮廓。证据包通过独立完整性校验，结果为 `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`；该结果只登记为方向纠正成功、技术稳定性和视觉完整性未通过，不追加第二次派生。

针对已经成立的重影偏差，后续策略必须使用新合同 `cogvideox_shot_002_rightward_spatial_only_v2.json`，重新绑定原始九帧来源而不是绑定失败派生。该合同保持同一条净向右 `32` 像素目标轨迹，但只执行整数像素空间平移，不做任何跨帧混合：

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_v2.json
```

这一合同只验证方向轨迹、主体保留和是否引入新重影。来源既有的主体面积波动必须继续报告，但不属于纯空间方向派生能够修复的对象，也不能被该合同用作扩大到四十一帧的依据。执行预算仍为一次派生和零次模型运行。

唯一执行 `LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-20260810T023643Z` 输出九帧、`768×496`、`8 fps`、`1.13` 秒的视频。九个相邻横向位移全部为正，最小为 `2.453` 像素，首尾净向右 `33.541` 像素，平均相邻质心跳变为 `4.264` 像素；这些方向观察均满足合同。但是最大相邻质心跳变为 `6.103` 像素，超过预设 `5.5` 像素上限 `0.603` 像素，因此自动门禁仍未全部闭合。来源固有的面积波动继续存在，派生后最大相邻主体面积变化为 `20.729%`。

全部九帧复核确认折纸主轮廓、三角纸面、主要折痕、水面和倒影持续存在，船头保持朝右，未见上一轮半透明双轮廓，也未见边缘复制接缝。证据包通过专用校验，结果为 `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`。该结果证明移除跨帧混合解决了新增重影，但只登记为视觉修复成功且方向轨迹接近门禁；不得把单项最大跳变偏差或既有面积波动视为已经闭合。

针对最大单步跳变超出 `0.603` 像素的独立偏差，后续合同 `cogvideox_shot_002_rightward_spatial_only_24px_v3.json` 只把九帧目标净位移从 `32` 像素收窄到 `24` 像素，继续绑定原始来源并保持纯空间平移。所有观察阈值原样保留，不允许把最大跳变上限从 `5.5` 像素调高：

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-24PX-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_24px_v3.json
```

该合同同样只有一次派生和零次模型运行预算。即使全部方向阈值与人工视觉检查闭合，来源固有的面积波动仍是未解决观察，后续只能据此设计四十一帧合同，不得直接执行四十一帧。

唯一执行 `LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-24PX-20260810T025213Z` 输出九帧、`768×496`、`8 fps`、`1.13` 秒的视频，摘要为 `9e6abf1f535d0eb1d065c45663c30e5f0cddd28c717c233772116ceac45452c9`。首尾净向右 `24.961` 像素，八个相邻横向位移全部为正且最小为 `0.777` 像素；最大相邻质心跳变为 `5.028` 像素，平均为 `3.225` 像素，全部预设方向阈值闭合。

全部九帧复核确认折纸主轮廓、三角纸面、主要折痕、水面和倒影持续存在，船头保持朝右，未见重影、双轮廓或边缘复制接缝。证据包通过独立校验，结果为 `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`，且 `all_observation_thresholds_met` 为真。该结果登记为第二镜头九帧低速方向控制基线，不创建视觉质量接受、镜头选择或时间线绑定。最大相邻主体面积变化仍为 `20.737%`；四十一帧执行前必须单独建立资源合同和绑定未来来源摘要的四十帧方向派生设计，不得假定九帧配方可直接外推。

第二镜头四十一帧资源合同为 `cogvideox_five_second_32_steps_shot_002.json`。它保持三十二步、`41` 帧、`65%` MPS 上限、至少 `5 GiB` 可用内存停止线和最多 `4 GiB` 新增换页停止线；资源预算引用第二镜头九帧实测峰值和既有折纸四十一帧实测峰值，结论为不放宽任何硬限制：

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-32STEP-SHOT-002-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_32_steps_shot_002.json
```

该模型合同只允许一次执行，失败时保留证据且不自动重试。源输出为 `41` 帧，成功后裁切为 `40` 帧、`8 fps`、精确 `5` 秒的 `derived_5s.mp4`。方向提示是否被模型遵守只记录观察，不在生成阶段自动接受或触发派生。

四十帧方向派生目前只存在设计 `cogvideox_shot_002_five_second_direction_design_v1.json`，状态固定为 `UNBOUND_SOURCE_NOT_EXECUTABLE`。设计按九帧基线的每帧约 `3` 像素换算为四十帧净向右 `117` 像素，保持纯空间平移并禁止跨帧混合。它不得预造来源执行标识或摘要；只有四十一帧源证据独立校验、全部四十帧保留可测主体并取得真实摘要后，才能创建新的绑定合同并在提交后执行。背景平移是否破坏静态相机意图必须作为四十帧人工检查项，不能由九帧结果推断通过。

唯一执行 `LM-COGVIDEOX-5S-32STEP-SHOT-002-20260810T030029Z` 完成了 `41` 帧源输出和 `40` 帧精确五秒派生。总耗时 `1678.695` 秒，其中推理 `1666.570` 秒、中央处理器小瓦片解码 `334.633` 秒；MPS 驱动分配峰值为 `6,562,824,192` 字节，进程树常驻内存峰值为 `15,602,139,136` 字节，系统已用内存峰值为 `30,058,528,768` 字节，启动与峰值换页均为 `2,232,090,624` 字节，没有新增换页。证据校验结果为 `VERIFIED_OBSERVATION_PACKAGE`。

全部 `41` 帧保留红色折纸轮廓、暗色三角折痕、水面和倒影，没有主体崩塌或严重形变。源输出最大相邻主体面积变化为 `6.228%`，明显低于第二镜头九帧来源的 `21.895%`。但是模型仍未遵守方向提示：精确五秒派生首尾净向左 `53.262` 像素，最小相邻横向位移为 `-7.597` 像素，最大相邻质心跳变为 `7.602` 像素。派生视频摘要为 `06efd281e3fca0037f4c0aafb94f8683e255563681c55d5377e05a0391643825`。该结果形成合格的五秒方向派生来源观察，不创建方向接受；后续绑定合同必须引用这一真实执行标识和摘要。

来源证据提交后，绑定合同 `cogvideox_shot_002_five_second_rightward_bound_v1.json` 才获得执行资格。合同固定上述真实执行标识和摘要，以每帧 `3` 像素建立四十帧净向右 `117` 像素轨迹，最大空间平移限制为 `192` 像素，保持边缘复制且禁止跨帧混合；工具必须输出全部四十张逐帧复核图和五列联系图：

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-5S-RIGHTWARD-BOUND-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_five_second_rightward_bound_v1.json
```

绑定派生预算为一次执行和零次模型运行。自动观察要求首尾净向右至少 `100` 像素、每个相邻横向位移至少 `0.5` 像素、最大相邻质心跳变不超过 `5.5` 像素、平均不超过 `4.5` 像素，并保留全部四十帧主体。人工检查还必须确认折痕、水面、倒影、船头朝向、边缘接缝和背景平移没有破坏静态相机意图；自动阈值满足不能替代这些视觉观察。

唯一执行 `LM-COGVIDEOX-SHOT-002-5S-RIGHTWARD-BOUND-20260810T033318Z` 形成 `40` 帧、`768×496`、`8 fps`、精确 `5.000` 秒的方向控制视频，摘要为 `73278576b53bff3126582cd630f3a3c3a907f6f78b6e25ebde99159eb6a49616`。首尾净向右 `116.300` 像素，三十九个相邻横向位移全部为正且最小为 `1.500` 像素；最大相邻质心跳变为 `4.861` 像素，平均为 `3.043` 像素，全部自动方向阈值闭合。最大相邻主体面积变化为 `6.354%`，与来源的 `6.228%` 接近。

全部四十帧复核确认折纸轮廓、暗色三角折痕、水面和倒影持续存在，未见重影、双轮廓、主体崩塌或边缘复制接缝，也未观察到明显的刚性镜头平移。专用证据校验结果为 `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`，`all_observation_thresholds_met` 为真。该结果登记为第二镜头精确五秒低速向右技术候选，不创建视觉质量接受、正式选择或时间线绑定，也不授权直接装配三十秒视频。

虚构儿童哭泣特写使用独立合同 `cogvideox_quality_32_steps_fictional_child_crying_closeup.json`，固定为 `CogVideoX-2B`、9 帧、32 步、8 fps，并明确禁止五秒扩展、自动重试、伤害叙事、正式接受和时间线绑定：

```bash
.venv-provider-compat/bin/python tools/run_provider_compatibility_trial.py \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-FICTIONAL-CHILD-CRYING-CLOSEUP-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps_fictional_child_crying_closeup.json
```

唯一执行 `LM-COGVIDEOX-32STEP-FICTIONAL-CHILD-CRYING-CLOSEUP-20260810T081709Z` 成功输出 9 帧、`768×496`、8 fps、`1.13` 秒候选，摘要为 `aec19a34c213b270a8d563ed07b017fa00855d7df087d4d9e3ecc9035a59f351`。总耗时 `276.868` 秒，其中推理 `260.281` 秒、中央处理器解码 `91.094` 秒；MPS 驱动分配峰值为 `4,367,155,200` 字节，进程树常驻内存峰值为 `14,135,918,592` 字节，换页峰值较启动增加 `3,798,728,704` 字节，没有触发停止线。证据包通过独立校验。

全部九帧保持浅色头发虚构幼儿的面部身份与近距离构图，未见严重面部坍缩、伤害、瘀伤、血迹、虐待、威胁、文字或标志。眼角泪珠、闭眼和悲伤表情持续可见，但未观察到清晰泪水滚落或下唇颤动，因此哭泣动作语义只形成部分观察。该候选不创建视觉质量接受、选择决策或后续五秒执行许可。

如果完整 CogVideoX 执行已经保存 `denoised_latents.safetensors`，可在不重复去噪的前提下单独执行 `180×120` 中央处理器小瓦片解码：

```bash
.venv-provider-compat/bin/python -m tools.decode_cogvideox_latent \
  --source-execution-id LM-COGVIDEOX-CPU-DECODE-R2-20260809T175503Z \
  --execution-id LM-COGVIDEOX-SMALL-TILE-DECODE-YYYYMMDDTHHMMSSZ
```

启动前至少需要 `16 GiB` 可用内存。现有换页超过 `4 GiB` 时，只有 macOS 权威内存压力级仍为正常值 `1` 才允许把它判为历史残留；运行期间仍以至少 `5 GiB` 可用内存和最多 `4 GiB` 新增换页作为硬停止条件。每个执行标识只允许使用一次。

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

.venv-provider-compat/bin/python -m tools.verify_cogvideox_decode_evidence \
  evidence/runtime/LM-COGVIDEOX-SMALL-TILE-DECODE-20260809T181252Z

.venv-provider-compat/bin/python -m tools.verify_cogvideox_stability_evidence \
  evidence/runtime/LM-COGVIDEOX-STABILITY-DERIVATION-20260809T192825Z

.venv-provider-compat/bin/python -m tools.verify_cogvideox_direction_evidence \
  evidence/runtime/LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-20260810T023111Z
```

校验器检查清单摘要、文件闭包、请求与执行标识、输出摘要以及公开仓库禁止出现的绝对用户路径。对于控制台创建的受控作业，它还核对固定生成档位、执行策略、MPS 比例、策略激活和推理后的主动释放观察。校验通过只表示证据包可重新审计，不表示视频质量合格或提供者适用性已经通过。

## 8. 低内存验收顺序

低内存实现与真实运行观察必须分开判断。代码和无模型回归测试通过后，按以下顺序建立现实证据：

1. 使用“内存探针”档位，保持 `75%` MPS 上限和分阶段驻留，只执行一个 Wan2.1 作业；
2. 确认没有其他生成进程，启动前可用内存至少 `16 GiB` 且现有换页不超过 `4 GiB`；
3. 在观测台持续查看统一内存、换页增长、MPS 峰值和阶段变化；
4. 运行结束后校验证据包，核对推理后主动释放记录；
5. 只有探针稳定闭合，才允许使用“低内存生成”档位；
6. CogVideoX 已完成分阶段去噪、小瓦片中央处理器解码、41 帧源输出、精确五秒派生输出、一次非模型时序稳定派生和三十二步九帧质量探针；水面与雨景语义得到改善，但纸张折痕和正式质量验收仍未闭合，因此控制台继续保持阻断。

文本编码器独立阶段形成两次真实失败观察：`LM-WAN-STAGED-PROBE-20260809T161019Z` 证明模型级卸载会让完整 UMT5 进入 MPS；`LM-WAN-LEAF-PROBE-20260809T161726Z` 证明直接调用 `encode_prompt` 时若未禁用自动求导，叶级卸载仍会累积中间状态并触及上限。启用叶级顺序卸载与 `torch.inference_mode()` 后，`LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` 完成了提示词编码、文本编码器释放、去噪管线装载、推理、视频导出和证据闭包。该结果只允许认定固定内存探针可运行，不得外推到更高档位或画面质量。

## 9. 当前 Mac 实测记录

以下数字是一次特定机器、依赖和参数下的观察，不是产品规格或性能承诺。

| 模型 | 当前结论 | 精确快照 | 关键观察 |
| --- | --- | --- | --- |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` | 已完成一次真实生成与证据闭包 | `0fad780a534b6463e45facd96134c9f345acfa5b` | 缓存约 27G；总耗时 2730.198 秒，其中首次快照解析 2661.848 秒；17 帧、416×240、8 fps；Metal 驱动分配峰值 30,979,096,576 字节；交换空间较启动时增加约 23.39GB |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 低内存探针 | 管线和分阶段策略成功激活，推理阶段由换页护栏终止 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、1 步；管线装载 28.482 秒；MPS 驱动采样峰值 4,210,524,160 字节；新增换页 9,075,425,280 字节，超过 8 GiB 预算；无视频输出；执行标识 `LM-WAN-PROBE-20260809T152435Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 无梯度叶级探针 | 已完成受控生成和独立证据闭包 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、1 步、8 fps；总耗时 23.444 秒；MPS 驱动峰值 8,413,462,528 字节；系统换页峰值未超过启动值；输出 11,712 字节；执行标识 `LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 质量探针 | 运行闭合但语义不可辨识 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、4 步、8 fps；总耗时 28.624 秒；MPS 驱动峰值 8,413,462,528 字节；换页没有增长；输出 32,028 字节；画面仍为蓝紫色块，不能识别红色纸船；执行标识 `LM-WAN-QUALITY-PROBE-20260809T170134Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 16 步平衡探针 | 运行闭合并首次出现语义形态 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、16 步、8 fps；总耗时 33.684 秒，其中推理 9.331 秒；MPS 驱动峰值 8,413,462,528 字节；换页没有增长；中央出现红色主体与水面结构，但纸船轮廓仍粗糙；执行标识 `LM-WAN-BALANCE-PROBE-20260809T170402Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 8 步平衡回测 | 运行闭合，确定当前最低可辨识档位 | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`、9 帧、8 步、8 fps；总耗时 30.685 秒，其中推理 5.945 秒；MPS 驱动峰值 8,413,462,528 字节；换页没有增长；全部 9 帧保留红色船体、两端尖角和水面层次，轮廓优于本次 16 步输出；执行标识 `LM-WAN-BALANCE-BACKTEST-20260809T170657Z` |
| `zai-org/CogVideoX-2b` | 八步为最低可辨识点；三十二步为当前九帧质量基线 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 八步同参数分阶段对照总耗时 104.597 秒，MPS 驱动峰值 4,367,155,200 字节，换页增长为 0；相较旧完整管线八步，MPS 驱动峰值降低 63.884%，九帧船体语义保持；三十二步进一步形成更清楚的倒影、涟漪和雨景语义，但纸张折痕仍不足；执行标识 `LM-COGVIDEOX-8STEP-STAGED-20260809T184407Z` |
| `zai-org/CogVideoX-2b` 三十二步质量探针 | 九帧雨景与水面改善；折纸材质仍未闭合 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 总耗时 247.653 秒；MPS 驱动峰值 4,367,155,200 字节，新增换页为 0；九帧全部保留船体，最大相邻质心跳变由十六步的 15.54 px 降至 10.58 px，平均值由 7.90 px 降至 4.29 px；水面倒影和同心涟漪明显增强，但最大主体面积变化升至 15.42%，且没有清晰纸张折痕；执行标识 `LM-COGVIDEOX-32STEP-QUALITY-20260809T193147Z` |
| `zai-org/CogVideoX-2b` 三十二步折纸提示词探针 | 首次形成稳定可辨识的折纸结构 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 只改变提示词主体描述；总耗时 220.365 秒，MPS 驱动峰值 4,356,620,288 字节，新增换页为 0；九帧全部形成交叠三角纸面和持续对角折线，并保留水面倒影与涟漪；但最大相邻质心跳变为 20.45 px、最大主体面积变化为 17.08%，只通过九帧质量门禁，尚未证明五秒连续性；执行标识 `LM-COGVIDEOX-32STEP-ORIGAMI-QUALITY-20260809T193843Z` |
| `zai-org/CogVideoX-2b` 三十二步折纸五秒候选 | 41 帧质量与资源闭合 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 总耗时 1331.091 秒；MPS 驱动峰值 6,562,824,192 字节，新增换页为 0；41 帧全部保留折纸面、折痕、水面和倒影，并派生精确 5 秒；原始最大相邻质心跳变 7.40 px；执行标识 `LM-COGVIDEOX-5S-32STEP-ORIGAMI-20260809T194654Z` |
| 折纸五秒时序稳定派生 | 技术连续性阈值全部通过 | 同上 | 不重跑模型；最大相邻质心跳变从 7.40 px 降至 1.27 px，平均值从 3.46 px 降至 0.70 px，最大面积变化降至 2.15%；40 帧折纸结构和场景语义保持；执行标识 `LM-COGVIDEOX-ORIGAMI-STABILITY-DERIVATION-20260809T201042Z` |
| `zai-org/CogVideoX-2b` 五秒候选观察 | 技术闭合；运动连续性仍需处理 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 十六步生成 41 帧并派生 40 帧、8 fps、精确 5 秒；总耗时 828.230 秒，MPS 驱动峰值 6,562,824,192 字节，新增换页为 0；全部 41 帧保留红色船体，但最大相邻质心跳变约 45.1 px，不能登记正式质量接受；执行标识 `LM-COGVIDEOX-5S-16STEP-20260809T190026Z` |
| `zai-org/CogVideoX-2b` 五秒时序稳定派生 | 技术连续性阈值闭合；仍待人工质量接受 | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | 锁定既有五秒来源摘要，不重新运行模型；输出 40 帧、8 fps、精确 5 秒，全部帧保留船体；最大相邻质心跳变由约 45.1 px 降至 2.78 px，平均值由约 12.29 px 降至 1.37 px，最大面积变化为 12.08%；40 帧逐帧未见边缘接缝或明显双影，但雨滴、折痕和水面细节仍不足；执行标识 `LM-COGVIDEOX-STABILITY-DERIVATION-20260809T192825Z` |

Wan2.1 的既有成功证据位于 `evidence/runtime/CR-0019-WAN-MAC-001/`，第一轮低内存失败证据位于 `evidence/runtime/LM-WAN-PROBE-20260809T152435Z/`，当前无梯度叶级探针成功证据位于 `evidence/runtime/LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z/`，四步质量证据位于 `evidence/runtime/LM-WAN-QUALITY-PROBE-20260809T170134Z/`，十六步平衡证据位于 `evidence/runtime/LM-WAN-BALANCE-PROBE-20260809T170402Z/`，八步平衡回测证据位于 `evidence/runtime/LM-WAN-BALANCE-BACKTEST-20260809T170657Z/`。在同一提示词、种子、画幅、帧数、引导系数和帧率下，4 步不可辨识，8 步可辨识，因此 8 步是当前试验范围内的最低可用点；该结论不外推到其他提示词、种子、分辨率或模型。CogVideoX 的各轮证据均位于对应的 `evidence/runtime/<execution-id>/` 目录，并已通过适用校验器。三十二步固定提示词建立了当前原提示词质量基线；折纸提示词对照进一步闭合了九帧折纸结构门禁，因此允许下一步单独设计四十一帧合同，但不自动证明五秒连续性，也不解除人工质量接受、控制台作业或三十秒时间线阻断。

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
