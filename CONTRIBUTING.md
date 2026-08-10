# 贡献指南

感谢你参与由 SENK 管理的 `senk-video-generator`。本项目接受问题报告、文档修正、验证器、提供者适配器和治理实现方面的贡献。

## 开始之前

- 先阅读 [`AGENTS.md`](AGENTS.md) 和与改动相关的 `foundation/`、`execution/`、`video/`、`verification/` 文档。
- 生成完成、技术合格、人工接受、正式选择、时间线绑定和发布是不同状态，不得在实现或文档中合并。
- 运行证据只记录观察，不得用测试通过或文件存在替代正式质量裁决。
- 不要提交模型权重、Hugging Face 缓存、访问令牌、个人凭据或机器专属路径。

## 本地环境

推荐使用 Python 3.12：

```bash
python3.12 -m venv .venv-provider-compat
.venv-provider-compat/bin/python -m pip install --upgrade pip
.venv-provider-compat/bin/python -m pip install -r requirements-provider-compat.txt
```

只运行不加载模型的测试时，可以安装较小的测试依赖集：

```bash
.venv-provider-compat/bin/python -m pip install -r requirements-test.txt
```

## 验证改动

提交前至少运行：

```bash
.venv-provider-compat/bin/python -m unittest discover -s tests -v
.venv-provider-compat/bin/python -m unittest discover -s migration_tests -v
```

涉及证据格式时，还应使用对应的 `tools/verify_*.py` 校验器复核既有样本。涉及模型运行时，必须先建立唯一执行标识、固定合同和资源停止线；失败证据必须保留，不能自动重试或覆盖。

## 提交与合并请求

- 每次提交只解决一个可说明、可验证的问题。
- 在合并请求中写明目标、非目标、验证命令、结果和尚未闭合的边界。
- 新能力需要同时说明输入合同、输出证据、失败关闭行为和与既有权威边界的关系。
- 不要通过删除失败记录、重写证据或放宽阈值让检查变绿。

## 报告问题

普通缺陷和功能建议可以使用 GitHub 议题。安全问题不要公开创建议题，请遵循 [`SECURITY.md`](SECURITY.md) 的私密披露流程。
