# 申请表可直接填写内容

## 第 04 题：具体成果描述

我搭建了一个名为 AgentProof 的多 Agent 申请材料与证据包生成器，用于把一个模糊申请目标自动拆解为需求理解、方案规划、内容生成、证据整理和真实性审查几个阶段。它解决的核心痛点是：很多 AI 使用记录停留在临时对话里，缺少可复用、可验证、可提交的项目化成果，导致申请、评审或复盘时很难证明 AI 的实际工作价值。

核心逻辑上，IntakeAgent 先读取申请背景并提取约束和风险；PlannerAgent 将任务拆成项目代码、README、流程图、运行日志和最终文案；DraftAgent 生成 1200 字以内的申请回答；EvidenceAgent 生成可上传材料清单；ReviewerAgent 检查是否存在夸大、伪造或缺少证据的问题。整个流程支持本地确定性运行，也预留了 OpenAI-compatible API 接口，可在配置模型密钥后切换为真实模型驱动。

目前我已经用 Codex 辅助完成了项目骨架、Agent 流水线、示例输入、输出日志、README 和申请表内容生成。这个项目把一次性 AI 对话转化成了可运行的工作流和可审计的证据包，适合继续扩展为申请助手、项目复盘助手或团队内部的 AI 交付记录系统。对我个人来说，它已经把材料准备从零散手工整理变成了结构化自动生成，预计能节省 60%-80% 的重复整理时间。

## 第 05 题：可上传材料说明

建议上传以下 3 张图片和 1 个链接：

1. `outputs/upload-assets/evidence-workflow.png`
   证明点：展示五个 Agent 的协作链路，以及每一步对应的输出。

2. `outputs/upload-assets/evidence-run-log.png`
   证明点：展示本地运行结果、Agent 输出指标、审查分数和生成文件。

3. `outputs/upload-assets/evidence-readme.png`
   证明点：展示项目 README、使用方法、远程模型配置方式和项目定位。

4. GitHub 项目链接
   证明点：将 `agentproof` 文件夹上传到 GitHub 后填写公开仓库地址。如果暂时不上传 GitHub，可以先上传运行日志截图和 README 截图。

## GitHub 链接栏填写模板

如果已经上传 GitHub：

```text
https://github.com/<你的用户名>/agentproof
```

如果还没有上传 GitHub，可先填写你之后创建的仓库地址；不要填写不存在的地址。这个表单若强制要求链接，建议先创建一个公开仓库再提交。

