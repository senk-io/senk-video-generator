# MiniMax H3 接入与当前机器兼容性

## 1. 文档边界

本文件记录 `MiniMax-H3` 在 `2026-08-11` 可观察到的发布事实、公开权重规模、当前机器边界和适配器状态。它属于会随模型、量化方案和运行框架变化的提供者知识，不是制度冻结、模型选择结论或视觉质量接受。

## 2. 官方能力事实

MiniMax 于 `2026-07-31` 发布 `MiniMax-H3`。官方说明和公开仓库共同给出的能力包括：

- 统一理解文本、图像、视频和音频上下文；
- 输出 `4` 至 `15` 秒视频；
- 基础公开权重输出短边 `768` 像素，官方完整系统最高支持 `2K`；
- 输出 `24 fps` 视频与 `32 kHz` 原生双声道音频；
- `H3-Base-FL2VA` 支持文生音视频及首尾帧控制；
- `H3-Base-Ref2VA` 支持图像、视频和音频参考。

公开基础模型不包含完整的托管 `H3-Context-IR` 与 `H3-Regenerate-2K` 系统。把本地基础权重称为完整官方 `2K` 工作流是不准确的。

来源：

- [MiniMax H3 发布说明](https://minimaxi.com/blog/minimax-h3)
- [MiniMax H3 官方公开仓库](https://github.com/MiniMax-AI/MiniMax-H3)
- [MiniMax H3 开放平台 V2 接口](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [ComfyUI MiniMax H3 工作流](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)

## 3. 公开权重规模观察

通过公开模型仓库元数据观察到：

```text
MiniMaxAI/MiniMax-H3 revision: 9ac0dd7aabc2c651fcf0ace4c00b2bffd9c8c8a6
完整仓库逻辑体积: 498,474,749,553 字节，约 464.24 GiB
```

完整仓库同时包含原始 `FL2VA`、`Ref2VA` 与 `diffusers` 格式的重复组件，不能把 `464.24 GiB` 直接称为单条推理管线驻留量。官方 `ComfyUI` 文生视频量化组合的文件体积为：

```text
minimax_h3_fl2va_pruned_int8_convrot: 20,970,379,616 字节，约 19.53 GiB
qwen3vl_32b_minimax_h3_nvfp4_awq: 15,687,142,551 字节，约 14.61 GiB
minimax_h3_video_vae_fp16: 5,207,808,496 字节，约 4.85 GiB
minimax_h3_audio_vae_fp32: 605,254,808 字节，约 0.56 GiB
合计: 42,470,585,471 字节，约 39.55 GiB
```

文件总量不是精确运行峰值，但它已经大于当前机器的 `36GB` 统一内存。文本编码器格式还依赖 `NVFP4/AWQ` 路径，当前没有苹果芯片 `MPS` 的成功观察。基于这些事实，本项目禁止在当前机器直接下载并启动公开量化组合；此结论以后可由新的受控低内存实现和真实证据修订。

## 4. 当前适配器决策

当前使用官方开放平台 `V2` 远端接口：

```text
Provider key: minimax_h3
Provider identity: MiniMax
Model ID: MiniMax-H3
Execution backend: remote_api
Endpoint origin: https://api.minimax.io
Credential env: MINIMAX_API_KEY
```

固定首轮效果合同为 `768P`、`5` 秒、`16:9` 的虚构儿童安全表演哭泣特写，包含受约束的呼吸、抽泣与房间底噪描述。只有命令行显式给出 `--execute` 才允许提交计费任务；缺少密钥时只形成预检阻断，不创建空证据。

适配器自动验证任务终态、模型标识、请求参数、文件摘要、可解码视频、短边、帧率、时长和原生音频技术属性。它不拥有语义接受、创意接受、候选选择或时间线绑定权威。

## 5. 尚未形成的现实

截至本记录：

- 本机没有 `MINIMAX_API_KEY`，尚未提交真实远端计费任务；
- 尚无 `MiniMax-H3` 实际输出、任务用量或耗时证据；
- 尚无与既有 `CogVideoX-2B` 儿童哭泣特写的人工并排评审；
- 尚无苹果芯片本地权重装载、推理、解码或音频生成观察；
- 尚未把远端适配器开放到本地作业控制台。

因此当前只能认定“适配器实现与模拟接口测试闭合”；不能认定“效果已验证”“本地可运行”或“提供者已适合正式生产”。
