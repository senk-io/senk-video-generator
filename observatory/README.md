# SENKNET 本地视频构建观测台

本目录是一套完整、只读、仅本机开放的视频构建观测项目。它把项目现有模型缓存、执行状态、资源采样、日志、输出和证据包投影为一个实时网页，帮助开发者在不翻阅多个 JSON、JSONL 和日志文件的情况下理解当前现实。

观测台不启动模型、不修改证据、不执行重试、不创建裁决，也不把“文件存在”提升为正式事实或制度冻结。

需要从页面定义提示词、资源预算并显式启动或停止作业时，使用独立的 [`../operator_console/README.md`](../operator_console/README.md)。控制台默认位于 `http://127.0.0.1:4320/`，本观测台继续保持只读。

## 1. 功能范围

- 自动发现正在运行和历史提供者试运行；
- 展示执行登记、环境取证、模型快照、管线装载、Metal 转移、推理、导出、证据闭包八个阶段；
- 每秒刷新中央处理器、统一内存、交换空间和磁盘状态；
- 绘制进程树内存、系统内存、交换空间和 MPS 分配趋势；
- 展示 Wan2.1 与 CogVideoX 的精确修订、缓存大小、快照文件和未完成文件；
- 预览已经形成的缩略图和视频输出；
- 查看固定请求、依赖环境、活动进程和可筛选运行日志；
- 查看清单、证据文件、正式事实、跨提供方合同和制度冻结边界；
- 浏览提供者试运行、受保护写入、正确性与迁移证据包历史；
- 支持桌面与窄屏响应式布局。

## 2. 安装

观测台复用项目的兼容性试运行环境，不增加前端工具链或服务端依赖。在仓库根目录执行：

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

如果已经完成模型兼容性环境安装，不需要重复执行。

## 3. 启动

在仓库根目录执行：

```bash
.venv-provider-compat/bin/python -m observatory --open
```

默认地址：

```text
http://127.0.0.1:4319/
```

不希望自动打开浏览器时省略 `--open`：

```bash
.venv-provider-compat/bin/python -m observatory
```

自定义端口：

```bash
.venv-provider-compat/bin/python -m observatory --port 5319
```

按 `Ctrl+C` 停止观测台。服务拒绝绑定 `0.0.0.0` 或局域网地址，避免无意公开本机执行日志和资源状态。

## 4. 观看一次构建

终端一启动观测台：

```bash
.venv-provider-compat/bin/python -m observatory --open
```

终端二执行已获授权的兼容性试运行：

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider wan \
  --execution-id CR-0020-WAN-MAC-001
```

页面每秒刷新，不需要手动重载。新执行目录出现后会被自动发现；活动执行优先成为默认观察对象。历史执行可从顶部选择器或底部证据包历史切换。

执行命令本身仍受提案、策略、资源预算和授权约束。启动观测台不等于获得生成授权。

## 5. 状态口径

| 页面状态 | 含义 | 不代表 |
| --- | --- | --- |
| `正在构建` | 检测到对应父进程或工作进程 | 不代表最终能够产出 |
| `已观察到输出` | 摘要记录推理、导出和输出均已形成 | 不代表视频质量合格或正式采纳 |
| `证据已闭包` | 摘要与清单已经形成 | 不代表正式事实成立 |
| `未形成输出` | 本次执行现实未形成可用输出 | 不自动决定重试或更换模型 |
| `等待或已中断` | 执行目录未闭合且没有对应运行进程 | 不自动证明进程崩溃原因 |
| `状态未知` | 数据源不足以确定当前现实 | 不得视为通过 |

阶段状态只由现有文件、布尔观察、工作进程阶段和活动进程推导。观测台不会向证据目录写入任何补充状态。

## 6. 数据真源与刷新

| 观测区域 | 数据真源 | 刷新频率 |
| --- | --- | --- |
| 构建阶段 | `request.json`、`environment.json`、`worker_state.json`、`summary.json`、`manifest.json` | 1 秒 |
| 进程与本机资源 | `psutil` 只读采样 | 1 秒 |
| 历史资源曲线 | `process_metrics.jsonl`、`mps_metrics.jsonl` | 1 秒 |
| 运行日志 | `runtime.log` 末尾 96 KiB | 1 秒 |
| 输出预览 | `output.mp4`、`thumbnail.png` | 1 秒发现，浏览器按需读取 |
| 模型缓存 | `~/.cache/huggingface/hub/` | 15 秒 |
| 全部证据包 | `evidence/runtime/*/summary.json` 与 `manifest.json` | 1 秒 |

长资源序列在接口中最多保留 420 个等距采样点用于绘图；原始 JSONL 文件不会被修改或截断。

## 7. 本地接口

```text
GET /api/v1/health
GET /api/v1/dashboard
GET /api/v1/dashboard?execution_id=<EXECUTION_ID>
GET /media/<EXECUTION_ID>/output.mp4
GET /media/<EXECUTION_ID>/thumbnail.png
```

接口只有读取能力。视频端点支持 HTTP 字节范围，便于浏览器定位和播放；执行标识、媒体文件名和实际路径均经过白名单与目录边界检查。

## 8. 安全与隐私

- 默认且只允许回环地址；
- 不提供 `POST`、`PUT`、`PATCH` 或 `DELETE` 业务接口；
- 不返回模型权重内容或缓存绝对路径；
- 日志中的仓库路径、用户目录和常见用户路径会在返回前脱敏；
- 页面启用内容安全策略、禁止外部脚本、禁止被框架嵌入；
- 所有前端资源均位于仓库内，不依赖内容分发网络；
- 观测台不导入 PyTorch，不加载模型，不创建 MPS 分配。

本地页面仍可能展示固定提示词、执行日志和公开安全的证据摘要。不要把本机端口转发到公网。

## 9. 验证

只运行观测台测试：

```bash
.venv-provider-compat/bin/python -m unittest tests.test_observatory -v
```

运行全部测试：

```bash
.venv-provider-compat/bin/python -m unittest discover -s tests -v
```

观测台测试覆盖完整状态推导、未闭合执行、模型缓存状态、日志路径脱敏、本机绑定限制、静态页面、接口、内容安全策略、路径穿越阻断和媒体分段读取。

## 10. 故障排查

### 系统 Python 报告缺少 `psutil`

使用项目虚拟环境启动：

```bash
.venv-provider-compat/bin/python -m observatory
```

### 端口已经被占用

选择另一个本机端口：

```bash
.venv-provider-compat/bin/python -m observatory --port 5319
```

### 页面没有执行记录

确认仓库内存在 `evidence/runtime/<execution-id>/request.json`，并且 `request.json` 含有提供者对象。治理、正确性和迁移证据会进入证据包历史，但不会被错误展示成视频生成阶段。

### CogVideoX 显示缓存完整但没有生成历史

这是当前正确状态：缓存完整只说明模型文件下载闭合，不代表管线能够装载、进入 MPS 或完成推理。只有真实执行形成新的证据目录后，页面才会显示对应生成阶段。
