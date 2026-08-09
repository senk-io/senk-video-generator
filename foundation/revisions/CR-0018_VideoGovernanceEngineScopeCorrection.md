# CR-0018 视频生产治理引擎边界纠偏

## 纠偏信息

```text
Correction ID: CR-0018-VIDEO-GOVERNANCE-ENGINE-SCOPE-CORRECTION
Status: COMPLETED
Decision Source: PROJECT_OWNER_CLARIFICATION
Repository Identity: senknet-video-generator
Product Domain: VIDEO_PRODUCTION_GOVERNANCE
WorkFit Dependency: PROHIBITED
Institution Freeze Created: NO
```

## 一、纠偏原因

`CR-0017` 正确识别了当前缺少现实的跨提供者、跨项目和跨领域证据，但其后续取得路径把“独立第二项目”收窄为另一个代码仓库，并把“跨领域”直接指向非视频产品。这一解释可能把 WorkFit 等无关产品引入视频生产治理引擎，超出了本项目边界。

本纠偏保留 `CR-0017` 的历史记录和缺失事实，不追溯改写审计；它只撤销其中未经授权的外部产品取得路径。

## 二、项目身份

```text
Canonical Project: senknet-video-generator
Local Carrier: /Users/bakboem/work/senk/senknet/senknet-video-generator
Remote Carrier: senk-io/senknet-video-generator
Carrier Count: 2
Independent Product Project Count Represented By Carriers: 1
```

本地目录负责开发、运行和证据生成，组织仓库负责版本协作、审查和远端保存。两者同步的是同一提交图、同一制度边界和同一证据历史，不得被计为跨项目证据。

## 三、与 WorkFit 的隔离

WorkFit 是独立产品，拥有自己的业务事实、权威、运行边界和发布责任。除非未来存在由双方分别授权、明示接口、最小数据合同和独立审查组成的正式集成提案，本项目必须满足：

- 不导入 WorkFit 业务事实作为视频治理真值；
- 不以 WorkFit 的运行、仓库或测试作为本项目现实样本；
- 不向 WorkFit 传播本项目制度权威；
- 不因基础制度具有通用表述而推定跨产品适用；
- 不修改 WorkFit 仓库来闭合本项目冻结门槛。

## 四、IF-0007 的有界解释

### 4.1 跨提供者

跨提供者证据必须来自至少两个真实视频生成提供者，在冻结输入、项目作用域、观察合同和裁决语义可比较的条件下运行。提供者知识文件、模拟返回或同一实现的并发运行不能替代现实提供者证据。

### 4.2 跨项目

“项目”首先指拥有独立视频生产目标、项目标识、冻结输入、执行记录和验收边界的视频生产项目实例，不等同于另一个代码仓库，也不等同于另一个 SENK 产品。

跨项目证据是否足以支持候选制度冻结，仍须由后续适用性提案明确样本独立性、污染隔离、权威边界和比较合同；本纠偏不预先宣告该门槛已经通过。

### 4.3 跨领域

本仓库的产品领域固定为视频生产。属于视频层的规则不得提升为跨领域基础制度。基础层候选若继续声称适用于视频以外的领域，仍须按 `IF-0007` 建立相应证据；但任何外部产品参与都必须另行取得明确授权，不能把 WorkFit 视为默认或推荐载体。

在完成基础层适用范围复审前，跨领域门槛保持阻断，不通过降低门槛、改名或复制样本解除。

## 五、当前决定

```text
CR-0017 Missing-evidence Facts: PRESERVED
CR-0017 External-product Acquisition Path: SUPERSEDED
WorkFit As Evidence Carrier: NOT_APPLICABLE
Local And Remote Repositories As Two Projects: REJECTED
Cross-provider Gate: BLOCKED
Cross-project Gate: BLOCKED_PENDING_APPLICABILITY_CONTRACT
Cross-domain Gate: BLOCKED_PENDING_FOUNDATION_SCOPE_REVIEW
Advance To Freeze: NO
```

下一阶段应先在 `senknet-video-generator` 内建立视频现实提供者接入与视频生产项目实例合同，再分别审查跨项目独立性和基础层跨领域主张。仓库生成与同步只建立项目载体，不创造现实适用性证据或制度冻结。
