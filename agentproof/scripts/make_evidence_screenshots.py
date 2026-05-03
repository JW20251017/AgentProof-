from __future__ import annotations

import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "demo-run"
ASSETS = ROOT / "outputs" / "upload-assets"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], max_width: int, fill: str, size: int = 28, bold: bool = False, line_gap: int = 10) -> int:
    fnt = font(size, bold=bold)
    x, y = xy
    for paragraph in text.split("\n"):
        if not paragraph:
            y += size + line_gap
            continue
        line = ""
        for char in paragraph:
            trial = line + char
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                draw.text((x, y), line, font=fnt, fill=fill)
                y += size + line_gap
                line = char
        if line:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += size + line_gap
    return y


def save_workflow() -> None:
    width, height = 1600, 980
    image = Image.new("RGB", (width, height), "#f7f4ec")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 110), fill="#111111")
    draw.text((60, 32), "AgentProof 多 Agent 工作流", font=font(42, True), fill="#ffffff")
    draw.text((60, 118), "从模糊申请目标到可提交证据包：每一步都有输出文件和审查记录", font=font(28), fill="#444444")

    boxes = [
        ("Intake", "提取目标、约束、风险"),
        ("Planner", "拆解代码、文档、截图、文案"),
        ("Draft", "生成 1200 字内申请答案"),
        ("Evidence", "整理可上传材料清单"),
        ("Reviewer", "检查真实性与完整度"),
    ]
    x, y = 70, 250
    box_w, box_h = 260, 170
    gap = 35
    colors = ["#e9f5db", "#d8ecff", "#fff1c7", "#eadcff", "#dff7f0"]
    for idx, (title, body) in enumerate(boxes):
        left = x + idx * (box_w + gap)
        draw.rounded_rectangle((left, y, left + box_w, y + box_h), radius=18, fill=colors[idx], outline="#222222", width=3)
        draw.text((left + 28, y + 28), title, font=font(34, True), fill="#111111")
        draw_wrapped(draw, body, (left + 28, y + 84), box_w - 56, "#333333", 25)
        if idx < len(boxes) - 1:
            arrow_x = left + box_w + 10
            draw.line((arrow_x, y + box_h // 2, arrow_x + gap - 20, y + box_h // 2), fill="#111111", width=5)
            draw.polygon(
                [
                    (arrow_x + gap - 20, y + box_h // 2),
                    (arrow_x + gap - 38, y + box_h // 2 - 12),
                    (arrow_x + gap - 38, y + box_h // 2 + 12),
                ],
                fill="#111111",
            )

    footer = (
        "输出：application_answer.md / workflow_log.md / evidence_checklist.md / run_manifest.json\n"
        "证明点：源码可运行、日志可审计、截图可上传、文案可直接填写。"
    )
    draw.rounded_rectangle((70, 580, 1530, 850), radius=18, fill="#ffffff", outline="#222222", width=2)
    draw.text((110, 620), "可提交证据闭环", font=font(36, True), fill="#111111")
    draw_wrapped(draw, footer, (110, 690), 1360, "#222222", 30)
    image.save(ASSETS / "evidence-workflow.png")


def save_run_log() -> None:
    manifest = json.loads((OUTPUT / "run_manifest.json").read_text(encoding="utf-8"))
    width, height = 1600, 1100
    image = Image.new("RGB", (width, height), "#101418")
    draw = ImageDraw.Draw(image)
    draw.text((55, 48), "AgentProof Demo Run", font=font(44, True), fill="#f7f4ec")
    draw.text((55, 108), f"Provider: {manifest['provider']} / {manifest['model']}", font=font(27), fill="#9fd6b8")
    draw.text((55, 150), f"Review score: {manifest['review_score']}/100", font=font(27), fill="#f7d774")

    y = 225
    for agent in manifest["agents"]:
        draw.rounded_rectangle((55, y, 1545, y + 115), radius=12, fill="#1d252c", outline="#3d4b55", width=2)
        draw.text((85, y + 22), agent["name"], font=font(30, True), fill="#ffffff")
        draw.text((355, y + 24), agent["objective"], font=font(24), fill="#d4d9dd")
        metrics = agent["metrics"]
        metric_text = f"chars={metrics['chars']}  approx_tokens={metrics['approx_tokens']}  sha256={metrics['sha256_12']}"
        draw.text((85, y + 70), metric_text, font=font(22), fill="#94a3b8")
        y += 140

    draw.text((55, 955), "Generated files:", font=font(28, True), fill="#ffffff")
    draw.text((280, 955), "application_answer.md, workflow_log.md, evidence_checklist.md, run_manifest.json", font=font(24), fill="#d4d9dd")
    image.save(ASSETS / "evidence-run-log.png")


def save_readme_preview() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    excerpt = "\n".join(readme.splitlines()[:34])
    width, height = 1600, 1200
    image = Image.new("RGB", (width, height), "#faf8f0")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 100), fill="#111111")
    draw.text((55, 28), "README 预览", font=font(38, True), fill="#ffffff")
    draw_wrapped(draw, excerpt, (65, 140), 1460, "#111111", 25, line_gap=8)
    image.save(ASSETS / "evidence-readme.png")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_workflow()
    save_run_log()
    save_readme_preview()
    print("Generated upload assets:")
    for path in sorted(ASSETS.glob("*.png")):
        print(f"- {path}")


if __name__ == "__main__":
    main()

