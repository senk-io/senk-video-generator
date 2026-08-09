# CR-0019 两个开源视频模型低成本兼容性试运行

## 一、试运行身份

```text
Proposal ID: CR-0019-LOW-COST-PROVIDER-COMPATIBILITY-TRIAL
Status: EXECUTION_AUTHORIZED
Authority Source: PROJECT_OWNER
Providers: Wan2.1-T2V-1.3B + CogVideoX-2B
Target Device: CURRENT_APPLE_SILICON_MAC
Cross-provider Contract Created: NO
Institution Freeze Created: NO
```

## 二、预期

本轮只建立以下可观察事实：

1. 官方模型快照能否解析并下载；
2. 管线能否在当前依赖版本中装载；
3. 管线能否进入 `mps` 执行上下文；
4. 固定提示词、种子和低成本参数能否完成推理；
5. 结果能否解码为视频并生成内容摘要；
6. 各阶段耗时、进程树内存、系统内存、换页和 Metal 分配能否被记录；
7. 成功或失败证据能否形成可独立校验的闭包。

## 三、执行授权与预算

```text
Allowed Generation Attempt Per Provider: 1
Environment Remediation Budget: 2
Timeout Per Provider Seconds: 7200
Prompt Count Per Provider: 1
Seed Count Per Provider: 1
Output Count Per Provider: 1
Publication Authority: NOT_GRANTED
Selection Authority: NOT_GRANTED
```

环境安装和显式依赖修复不计为模型生成重试。一次模型生成开始后，不得为了得到成功结果静默改变提示词、随机种子、分辨率、帧数、步数或精度。若发生失败，必须先保存该次现实；任何后继尝试须建立新的执行标识和策略依据。

## 四、非目标

- 不评价画面艺术质量；
- 不把文件存在裁决为正式接受；
- 不把两次低成本运行提升为跨提供方制度证据；
- 不验证生产吞吐、长期稳定性或标准质量参数；
- 不下载或提交第三方模型权重到项目仓库；
- 不把 WorkFit 引入本项目证据链。

## 五、开源边界

试运行工具、固定依赖、使用文档、公开安全的观察证据和校验器进入项目仓库。模型权重继续由原模型发布方分发。任何公开证据都不得包含访问令牌、本机用户名、用户目录绝对路径、机器序列号、硬件唯一标识或未获授权的外部数据。
