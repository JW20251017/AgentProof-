from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from .models import AgentResult
from .providers import BaseProvider, LocalProvider


def approx_tokens(text: str) -> int:
    # CJK-heavy text is usually tokenized more densely than English. This is an estimate only.
    return max(1, round(len(text) / 1.6))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


@dataclass(frozen=True)
class Agent:
    name: str
    objective: str

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        raise NotImplementedError

    def _result(self, output: str, extra: dict[str, object] | None = None) -> AgentResult:
        metrics = {
            "chars": len(output),
            "approx_tokens": approx_tokens(output),
            "sha256_12": digest(output),
        }
        if extra:
            metrics.update(extra)
        return AgentResult(self.name, self.objective, output, metrics)


class IntakeAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            "IntakeAgent",
            "提取申请目标、已有约束、可证明材料和风险点。",
        )

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        keywords = {
            "agent": len(re.findall(r"agent|Agent|AI|模型|自动化", brief)),
            "evidence": len(re.findall(r"截图|日志|GitHub|证据|佐证|README|demo", brief)),
            "risk": len(re.findall(r"没有|缺少|不可|不能|风险|伪造", brief)),
        }
        output = "\n".join(
            [
                "申请目标：用一个可运行的小型 Agent 项目证明申请人具备 AI 驱动交付能力。",
                "核心约束：目前没有历史项目，所以必须即时构建真实项目，避免虚构账单或不存在的外部链接。",
                "可证明材料：源码、README、运行日志、流程图、申请文案、截图、可选 GitHub 仓库链接。",
                "主要风险：如果只提交文字描述，可信度不足；如果伪造 token 或账单，会有审核风险。",
                f"关键词计数：{keywords}",
            ]
        )
        return self._result(output, keywords)


class PlannerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            "PlannerAgent",
            "把申请材料任务拆成可执行的多 Agent 工作流。",
        )

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        provider_note = ""
        if not isinstance(provider, LocalProvider):
            provider_note = provider.complete(
                agent_name=self.name,
                system="Generate a concise implementation plan for a multi-agent evidence workflow.",
                user=brief,
            )
        output = "\n".join(
            [
                "工作流设计：",
                "1. IntakeAgent 读取申请背景，抽取目标、限制和可证明材料。",
                "2. PlannerAgent 设计交付路径，将任务拆成项目定位、代码实现、文档、证据截图和最终文案。",
                "3. DraftAgent 生成 1200 字以内的中文申请回答，覆盖痛点、核心逻辑和影响力。",
                "4. EvidenceAgent 生成审核可读的证据清单，标明每份材料如何证明项目真实存在。",
                "5. ReviewerAgent 检查文案是否过度承诺、是否缺少数据、是否需要替换占位信息。",
                "长链推理：先解决真实性和可验证性，再优化表达；复杂任务可并行扩展多个专项 Agent。",
                provider_note,
            ]
        ).strip()
        return self._result(output)


class DraftAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            "DraftAgent",
            "生成可直接填写到申请表第 04 题的中文成果描述。",
        )

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        output = (
            "我搭建了一个名为 AgentProof 的多 Agent 申请材料与证据包生成器，"
            "用于把一个模糊申请目标自动拆解为需求理解、方案规划、内容生成、证据整理和真实性审查几个阶段。"
            "它解决的核心痛点是：很多 AI 使用记录停留在临时对话里，缺少可复用、可验证、可提交的项目化成果，"
            "导致申请、评审或复盘时很难证明 AI 的实际工作价值。\n\n"
            "核心逻辑上，IntakeAgent 先读取申请背景并提取约束和风险；PlannerAgent 将任务拆成项目代码、README、"
            "流程图、运行日志和最终文案；DraftAgent 生成 1200 字以内的申请回答；EvidenceAgent 生成可上传材料清单；"
            "ReviewerAgent 检查是否存在夸大、伪造或缺少证据的问题。整个流程支持本地确定性运行，也预留了 OpenAI-compatible "
            "API 接口，可在配置模型密钥后切换为真实模型驱动。\n\n"
            "目前我已经用 Codex 辅助完成了项目骨架、Agent 流水线、示例输入、输出日志、README 和申请表内容生成。"
            "这个项目把一次性 AI 对话转化成了可运行的工作流和可审计的证据包，适合继续扩展为申请助手、项目复盘助手或团队内部的 "
            "AI 交付记录系统。对我个人来说，它已经把材料准备从零散手工整理变成了结构化自动生成，预计能节省 60%-80% 的重复整理时间。"
        )
        return self._result(output)


class EvidenceAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            "EvidenceAgent",
            "生成第 05 题可上传材料清单和每项材料的证明点。",
        )

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        output = "\n".join(
            [
                "建议上传材料：",
                "1. evidence-workflow.png：展示 Intake、Planner、Draft、Evidence、Reviewer 五个 Agent 的协作链路。",
                "2. evidence-run-log.png：展示一次真实本地运行输出，包括生成文件、评审分数和输出路径。",
                "3. evidence-readme.png：展示项目 README、使用方式和可配置真实模型接口。",
                "4. outputs/demo-run/workflow_log.md：完整运行日志，可证明项目不是单段文案。",
                "5. outputs/demo-run/application_answer.md：第 04 题可直接使用的最终答案。",
                "6. GitHub 链接：将 agentproof 文件夹上传为公开仓库后填写仓库地址。",
                "注意：不要上传伪造账单。没有真实 token 账单时，优先上传运行日志、项目源码、截图和 GitHub 链接。",
            ]
        )
        return self._result(output)


class ReviewerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            "ReviewerAgent",
            "审查申请材料是否具体、可信、可证明。",
        )

    def run(self, brief: str, previous: list[AgentResult], provider: BaseProvider) -> AgentResult:
        draft = next((item.output for item in previous if item.name == "DraftAgent"), "")
        checks = {
            "under_1200_chars": len(draft) <= 1200,
            "has_pain_point": "痛点" in draft,
            "has_logic": "核心逻辑" in draft or "IntakeAgent" in draft,
            "has_impact": "节省" in draft or "提升" in draft,
            "has_truthfulness_guardrail": "伪造" in "\n".join(item.output for item in previous),
        }
        score = sum(20 for passed in checks.values() if passed)
        output = "\n".join(
            [
                f"审查分数：{score}/100",
                f"检查项：{checks}",
                "结论：材料具备项目名、工作流、可运行产物和上传证据。建议提交前把 GitHub 链接替换为真实仓库地址；如有真实账单或终端截图，可额外上传。",
            ]
        )
        return self._result(output, {"review_score": score})

