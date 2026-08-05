# 架构

## 架构定位

系统是一条模型无关的视频编译链。模型是外部、不稳定依赖；项目权威事实、状态、裁决和证据由本系统持有。

```text
Creative Intent
  -> Intermediate Representation
  -> Provider-specific Compilation
  -> Candidate Assets
  -> Verified Timeline
  -> Render Package
  -> Final Video
```

## 逻辑分层

1. **治理层**：权威、状态迁移、证据、质量门和策略。
2. **领域层**：视频意图、镜头、灯光、相机、角色、场景、情绪和音频规则。
3. **编译层**：把创作契约和镜头规格编译为模型、语音、字幕和时间线输入。
4. **适配层**：隔离 Seedance、Veo、Kling、FFmpeg 等专属协议。
5. **资产层**：保存候选资产、来源、版本、校验和状态。
6. **装配层**：只消费已获授权的选择决策，生成时间线和导出包。
7. **审计层**：保存事件、决策、验证证据和依赖失效记录。

## 核心组件

- Project Contract Registry
- Narrative and Script Registry
- Shot Registry
- Generation Task Registry
- Provider Adapters
- Asset Registry
- Verification Service
- Selection Decision Registry
- Dependency Graph
- Timeline Compiler
- Quality Gate
- Audit Ledger

## 中间表示边界

`CreativeBrief`、`NarrativeContract`、`ScriptSegment` 和 `ShotSpec` 是项目中间表示。模型专属提示词、语音输入、字幕文件、FFmpeg 参数和剪辑器工程都是编译产物。

提供者专属字段只能存在于适配器或编译产物中，不得污染权威领域对象。

## 数据原则

- 注册表保存正式事实，媒体存储保存二进制资产。
- 事件日志追加写入，用于审计，不替代当前状态读取模型。
- 时间线、报表、缓存和导出物可由权威事实重建。
- 所有实体使用稳定标识并引用标识，不复制权威内容。
- 模板目录 `templates/video-project/` 将在后续阶段逐步定义可实例化的最小生产仓库；当前不预先冻结字段契约。
