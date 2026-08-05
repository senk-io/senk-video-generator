# 执行模型

本文件尚未获得独立制度冻结，必须服从 `IF-0001` 至 `IF-0005` 已建立的权威、预期、偏差、诊断和策略边界。任何重试、修复、重新规划、替换提供者、升级、人工评审或终止都必须由策略明确授权，执行器不得自行触发。

## 标准闭环

```text
Expectation
  -> Planning
  -> Execution
  -> Observation
  -> Verification
  -> Gap
  -> Diagnosis
  -> Policy
  -> Next Execution
```

执行的目的不是尽快得到一个文件，而是让每次行动产生可验证结果和可解释偏差。

## 单次执行契约

每个执行任务必须声明：

- 输入权威及版本；
- 允许修改的对象；
- 不得修改的上游意图；
- 预期输出；
- 验证方法；
- 失败边界；
- 执行者拥有的权限；
- 证据保存位置。

## 角色及权限边界

| 角色 | 可以做什么 | 不可以做什么 |
|---|---|---|
| Brief Agent | 整理创作目标 | 擅自批准目标 |
| Narrative Agent | 组织叙事结构 | 修改已冻结目标 |
| Script Agent | 生成和修订脚本 | 绕过脚本审批 |
| Shot Planner | 把脚本映射为镜头 | 宣称镜头已生成合格 |
| Prompt Compiler | 编译模型输入 | 修改镜头意图 |
| Generation Orchestrator | 调用模型、记录任务 | 选择自己的产物 |
| Asset Inspector | 执行技术与基础语义检查 | 作最终创意裁决 |
| Continuity Reviewer | 检查连续性 | 改写上游叙事 |
| Selection Agent | 排序并提出建议 | 默认拥有最终采纳权 |
| Timeline Composer | 装配已授权素材 | 删除核心论点或采用未选素材 |
| Quality Gate | 执行发布前检查 | 为了放行而降低标准 |
| Publication Agent | 生成平台派生版本 | 发布未获授权的成片 |

## 生产状态主链

```text
DRAFT
  -> PLANNED
  -> GENERATING
  -> CANDIDATES_READY
  -> UNDER_REVIEW
  -> SELECTED
  -> ASSEMBLED
  -> VERIFIED
  -> PUBLISHED
```

适用的失败和阻断状态包括：

```text
GENERATION_FAILED
TECHNICAL_INVALID
SEMANTIC_MISMATCH
CONTINUITY_FAILED
INVALIDATED
REQUIRES_HUMAN_DECISION
```

状态迁移必须具有前置状态、授权者、输入版本和证据。执行异常不是流程终点；必须先形成可追踪观察，依据冻结预期建立偏差，再由诊断解释偏差，最后由策略决定下一步。
