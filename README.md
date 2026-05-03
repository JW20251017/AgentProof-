AgentProof
AgentProof 是一个小型多 Agent 申请材料与证据包生成器。它面向“需要证明自己具备 AI / Agent 实践能力，但缺少可整理项目材料”的场景，把一次性对话变成可运行、可审查、可截图、可提交的项目化产物。

解决的痛点
很多 AI 使用过程只存在于聊天窗口、终端输出或临时笔记中。申请项目、复盘项目或向他人展示 AI 交付能力时，单纯描述“我用了 AI”可信度不够，伪造账单或不存在的项目链接又有明显风险。AgentProof 的目标是把真实工作流沉淀成证据包：源码、运行日志、README、流程图、最终文案和证据清单都可以被审查。

工作流


IntakeAgent目标/约束/风险
PlannerAgent拆解交付路径
DraftAgent生成申请回答
EvidenceAgent整理上传材料
ReviewerAgent真实性审查
Evidence Pack文案/日志/截图/清单
Agent 分工
IntakeAgent：读取申请背景，提取目标、已有约束、可上传材料和风险点。
规划师Agent：将任务拆分为代码实现、文档、运行日志、截图和最终文案。
草稿师Agent：生成1200字以内的中文申请回答。
证据师Agent：生成第05题可上传材料清单。
审核师Agent：检查文案是否具体、可信、可证明。
本地运行
cd agentproof
python -m agentproof.cli --brief examples/application_brief.md --out outputs/demo-run
python scripts/make_evidence_screenshots.py
运行后会生成：

outputs/demo-run/application_answer.md
outputs/demo-run/workflow_log.md
outputs/demo-run/evidence_checklist.md
outputs/demo-run/run_manifest.json
outputs/upload-assets/evidence-workflow.png
outputs/upload-assets/evidence-run-log.png
outputs/upload-assets/evidence-readme.png
使用真实模型
默认运行模式是本地确定性模式，不伪造模型调用。如果你想让每个 Agent 调用真实模型，可以配置 OpenAI-compatible 接口：

$env:AGENTPROOF_API_KEY="你的 API Key"
$env:AGENTPROOF_API_BASE="https://api.openai.com/v1"
$env:AGENTPROOF_MODEL="gpt-4.1-mini"
python -m agentproof.cli --brief examples/application_brief.md --out outputs/remote-run --remote
这会在 run_manifest.json 中记录实际使用的 provider 和 model，方便后续作为更强的佐证材料。

申请材料建议
申请表第 04 题可以使用 docs/submission-content.md 中的成果描述。第 05 题建议上传 outputs/upload-assets 下的三张图片，并在链接栏填写 GitHub 仓库地址。

重要提醒：不要上传伪造账单或不存在的项目链接。没有历史项目时，用这个仓库、运行日志和截图证明“现在已经完成了一个真实项目”，通过率通常比纯文字包装更稳。
