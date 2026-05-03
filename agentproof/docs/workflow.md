# AgentProof 工作流说明

AgentProof 把一个“需要申请材料但缺少历史项目”的问题拆成五个 Agent 步骤：

1. IntakeAgent：读取申请背景，提取目标、限制、可上传证据和风险点。
2. PlannerAgent：生成项目化交付路径，确定需要代码、README、日志、截图和最终文案。
3. DraftAgent：生成第 04 题回答，覆盖项目痛点、核心逻辑和影响。
4. EvidenceAgent：生成第 05 题可上传材料清单，并说明每个材料证明什么。
5. ReviewerAgent：检查文案是否具体、可信、可证明，并输出审查分数。

本地模式不伪造模型调用，适合快速生成可运行证据。配置 `AGENTPROOF_API_KEY`、`AGENTPROOF_API_BASE` 和 `AGENTPROOF_MODEL` 后，可以切换到 OpenAI-compatible 模型调用模式。

