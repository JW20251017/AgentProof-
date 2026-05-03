# AgentProof Workflow Log

## IntakeAgent

Objective: 提取申请目标、已有约束、可证明材料和风险点。

Metrics:

```json
{
  "chars": 224,
  "approx_tokens": 140,
  "sha256_12": "161d60449f59",
  "agent": 7,
  "evidence": 10,
  "risk": 4
}
```

Output:

申请目标：用一个可运行的小型 Agent 项目证明申请人具备 AI 驱动交付能力。
核心约束：目前没有历史项目，所以必须即时构建真实项目，避免虚构账单或不存在的外部链接。
可证明材料：源码、README、运行日志、流程图、申请文案、截图、可选 GitHub 仓库链接。
主要风险：如果只提交文字描述，可信度不足；如果伪造 token 或账单，会有审核风险。
关键词计数：{'agent': 7, 'evidence': 10, 'risk': 4}

## PlannerAgent

Objective: 把申请材料任务拆成可执行的多 Agent 工作流。

Metrics:

```json
{
  "chars": 281,
  "approx_tokens": 176,
  "sha256_12": "a8496e66f86c"
}
```

Output:

工作流设计：
1. IntakeAgent 读取申请背景，抽取目标、限制和可证明材料。
2. PlannerAgent 设计交付路径，将任务拆成项目定位、代码实现、文档、证据截图和最终文案。
3. DraftAgent 生成 1200 字以内的中文申请回答，覆盖痛点、核心逻辑和影响力。
4. EvidenceAgent 生成审核可读的证据清单，标明每份材料如何证明项目真实存在。
5. ReviewerAgent 检查文案是否过度承诺、是否缺少数据、是否需要替换占位信息。
长链推理：先解决真实性和可验证性，再优化表达；复杂任务可并行扩展多个专项 Agent。

## DraftAgent

Objective: 生成可直接填写到申请表第 04 题的中文成果描述。

Metrics:

```json
{
  "chars": 577,
  "approx_tokens": 361,
  "sha256_12": "b2b82732760b"
}
```

Output:

我搭建了一个名为 AgentProof 的多 Agent 申请材料与证据包生成器，用于把一个模糊申请目标自动拆解为需求理解、方案规划、内容生成、证据整理和真实性审查几个阶段。它解决的核心痛点是：很多 AI 使用记录停留在临时对话里，缺少可复用、可验证、可提交的项目化成果，导致申请、评审或复盘时很难证明 AI 的实际工作价值。

核心逻辑上，IntakeAgent 先读取申请背景并提取约束和风险；PlannerAgent 将任务拆成项目代码、README、流程图、运行日志和最终文案；DraftAgent 生成 1200 字以内的申请回答；EvidenceAgent 生成可上传材料清单；ReviewerAgent 检查是否存在夸大、伪造或缺少证据的问题。整个流程支持本地确定性运行，也预留了 OpenAI-compatible API 接口，可在配置模型密钥后切换为真实模型驱动。

目前我已经用 Codex 辅助完成了项目骨架、Agent 流水线、示例输入、输出日志、README 和申请表内容生成。这个项目把一次性 AI 对话转化成了可运行的工作流和可审计的证据包，适合继续扩展为申请助手、项目复盘助手或团队内部的 AI 交付记录系统。对我个人来说，它已经把材料准备从零散手工整理变成了结构化自动生成，预计能节省 60%-80% 的重复整理时间。

## EvidenceAgent

Objective: 生成第 05 题可上传材料清单和每项材料的证明点。

Metrics:

```json
{
  "chars": 413,
  "approx_tokens": 258,
  "sha256_12": "7067fa0800e1"
}
```

Output:

建议上传材料：
1. evidence-workflow.png：展示 Intake、Planner、Draft、Evidence、Reviewer 五个 Agent 的协作链路。
2. evidence-run-log.png：展示一次真实本地运行输出，包括生成文件、评审分数和输出路径。
3. evidence-readme.png：展示项目 README、使用方式和可配置真实模型接口。
4. outputs/demo-run/workflow_log.md：完整运行日志，可证明项目不是单段文案。
5. outputs/demo-run/application_answer.md：第 04 题可直接使用的最终答案。
6. GitHub 链接：将 agentproof 文件夹上传为公开仓库后填写仓库地址。
注意：不要上传伪造账单。没有真实 token 账单时，优先上传运行日志、项目源码、截图和 GitHub 链接。

## ReviewerAgent

Objective: 审查申请材料是否具体、可信、可证明。

Metrics:

```json
{
  "chars": 213,
  "approx_tokens": 133,
  "sha256_12": "225a42fddd34",
  "review_score": 100
}
```

Output:

审查分数：100/100
检查项：{'under_1200_chars': True, 'has_pain_point': True, 'has_logic': True, 'has_impact': True, 'has_truthfulness_guardrail': True}
结论：材料具备项目名、工作流、可运行产物和上传证据。建议提交前把 GitHub 链接替换为真实仓库地址；如有真实账单或终端截图，可额外上传。
