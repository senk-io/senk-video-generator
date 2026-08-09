# Wan2.1 与 CogVideoX 在苹果芯片 Mac 上的兼容性观察

## 1. 文档性质

本文记录 `CR-0019` 的现实观察，供安装、复现和后续低内存方案设计使用。它不是模型选型结论，不评价画面质量，不建立跨提供方证据合同，也不构成制度冻结。

观察环境是 36GB 统一内存的苹果芯片 Mac，项目运行环境为 `Python 3.12.11`。依赖版本固定在仓库根目录的 `requirements-provider-compat.txt`。

## 2. 权重安装位置

项目不托管第三方模型权重。`huggingface_hub` 默认将权重保存在：

```text
~/.cache/huggingface/hub/
```

本轮对应的缓存目录名称为：

```text
models--Wan-AI--Wan2.1-T2V-1.3B-Diffusers
models--zai-org--CogVideoX-2b
```

可复现的纯下载、离线快照验证、环境安装和完整试运行命令见 `docs/provider-compatibility-trials.md`。

## 3. Wan2.1-T2V-1.3B 真实生成观察

```text
Model ID: Wan-AI/Wan2.1-T2V-1.3B-Diffusers
Snapshot: 0fad780a534b6463e45facd96134c9f345acfa5b
Execution ID: CR-0019-WAN-MAC-001
Observation: OBSERVED_OUTPUT_AVAILABLE
```

本次从首次下载开始，成功完成快照解析、管线装载、Metal 转移、推理、解码、视频导出和证据校验。

```text
总耗时: 2730.198 秒
快照解析: 2661.848 秒
管线装载: 30.467 秒
Metal 转移: 8.183 秒
推理与解码: 21.666 秒
视频导出: 3.362 秒
输出: 17 帧，416×240，8 fps，2.13 秒
进程树最大常驻内存: 7,556,562,944 字节
Metal 当前分配峰值: 16,240,202,240 字节
Metal 驱动分配峰值: 30,979,096,576 字节
系统交换空间启动值: 20,838,285,312 字节
系统交换空间峰值: 44,226,379,776 字节
```

因此，当前机器和固定低成本参数下已经观察到一次成功生成。但这次运行造成了明显内存压力：系统交换空间相对启动值增加约 23.39GB。这个结果不能外推到标准质量参数、并发执行或长期生产负载。

证据包位于：

```text
evidence/runtime/CR-0019-WAN-MAC-001/
```

可使用仓库校验器重新检查文件闭包、摘要和隐私路径边界。

## 4. CogVideoX-2B 纯下载观察

```text
Model ID: zai-org/CogVideoX-2b
Snapshot: 1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01
Generation Executed: NO
Runtime Compatibility: UNKNOWN
```

纯下载共解析 19 个文件，模型仓库逻辑大小为 13,775,572,738 字节，本地缓存约 13G。下载耗时 1196.81 秒，下载进程最大常驻内存为 4,005,658,624 字节。完成后检查结果为 0 个 `.incomplete` 文件，精确修订号可在离线模式下重新解析。

该过程只调用 `huggingface_hub.snapshot_download`。它没有导入 PyTorch，没有建立 `CogVideoXPipeline`，没有使用 Metal，也没有执行视频生成。因此当前只能确认权重已经完整下载，不能确认 CogVideoX-2B 在这台 Mac 上可装载或可推理。

## 5. 后续低内存试运行边界

CogVideoX 的下一次验证应作为新执行单元，至少先设计并记录：

1. 装载前的可用内存和交换空间基线；
2. 分阶段装载及中央处理器卸载策略；
3. Metal 分配上限与主动停止阈值；
4. 单提示词、单种子、单输出的最小参数；
5. 超限时保留失败证据且不自动重试的规则。

在该方案获得明确执行授权前，不应把下载完成自动升级为生成验证。
