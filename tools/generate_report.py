# tools/generate_report.py
"""
OASIS Observatory – ASI Scenario Report Generator (v3.0)
Generates a PDF summarizing 10 maximally diverse ASI scenarios with narratives and multiple diagrams.
"""

from __future__ import annotations
import json
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepInFrame
)

from oasis.common.db import SCENARIO_DB_PATH
from oasis.logger import log

# ───────────────────────────────────────────────
# Settings
# ───────────────────────────────────────────────

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

AUTONOMY_MAP = {
    "none": 0.0, "limited": 0.2, "partial": 0.4,
    "significant": 0.6, "full": 0.8, "super": 1.0,
}

# ───────────────────────────────────────────────
# Step 1 – Load scenarios
# ───────────────────────────────────────────────

def load_scenarios() -> pd.DataFrame:
    query = "SELECT data FROM scenarios"
    with closing(sqlite3.connect(SCENARIO_DB_PATH)) as conn:
        raw_df = pd.read_sql_query(query, conn)

    rows = []
    for raw in raw_df["data"]:
        js = json.loads(raw)
        meta = js.get("metadata", {})
        core = js.get("core_capabilities", {})
        content = js.get("scenario_content", {})

        autonomy = str(core.get("autonomy_degree", "none")).lower()

        rows.append({
            "id": js.get("title", "Untitled"),
            "date": meta.get("created", "")[:10],
            "agency": float(core.get("agency_level", 0.0)),
            "autonomy_str": autonomy.capitalize(),
            "autonomy_num": AUTONOMY_MAP.get(autonomy, 0.0),
            "alignment": float(core.get("alignment_score", 0.0)),
            "narrative": content.get("narrative", "") or "",
        })

    return pd.DataFrame(rows)

# ───────────────────────────────────────────────
# Step 2 – Vectorize scenarios (numeric only)
# ───────────────────────────────────────────────

def vectorize(df: pd.DataFrame) -> np.ndarray:
    mat = df[["agency", "autonomy_num", "alignment"]].to_numpy().astype(float)
    mins = mat.min(axis=0)
    maxs = mat.max(axis=0)
    denom = np.where(maxs - mins == 0, 1, maxs - mins)
    norm = (mat - mins) / denom
    return norm

# ───────────────────────────────────────────────
# Step 3 – Select maximally diverse scenarios
# ───────────────────────────────────────────────

def select_diverse_scenarios(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if len(df) <= n:
        return df
    x = vectorize(df)
    total = x.shape[0]
    dist = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=2)
    selected = [np.random.randint(0, total)]
    while len(selected) < n:
        nearest_dist = dist[selected].min(axis=0)
        nearest_dist[selected] = -1
        next_idx = nearest_dist.argmax()
        selected.append(next_idx)
    return df.iloc[selected].reset_index(drop=True)

# ───────────────────────────────────────────────
# Step 4 – Plots
# ───────────────────────────────────────────────

def make_plot(df: pd.DataFrame, path: Path):
    plt.figure(figsize=(7.6, 6))
    sizes = 200 + 1600 * df["alignment"]
    plt.scatter(df["agency"], df["autonomy_num"], s=sizes, c="#1f77b4", alpha=0.8, edgecolors="white", linewidth=1.6)
    for _, r in df.iterrows():
        plt.annotate(r["id"][-6:], (r["agency"], r["autonomy_num"]), xytext=(6, 6), textcoords="offset points", fontsize=8, fontweight="bold")
    plt.xlabel("Agency Level")
    plt.ylabel("Autonomy (mapped)")
    plt.title("ASI Scenario Diversity Map\nDot size = Alignment Score")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig(path, dpi=240)
    plt.close()

def make_radar_chart(df: pd.DataFrame, path: Path):
    labels = ["Agency", "Autonomy", "Alignment"]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(6,6))
    for _, r in df.iterrows():
        values = [r["agency"], r["autonomy_num"], r["alignment"]]
        values += values[:1]
        plt.polar(angles, values, label=r["id"], alpha=0.6)
    plt.xticks(angles[:-1], labels)
    plt.title("ASI Scenario Radar Chart")
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=6)
    plt.tight_layout()
    plt.savefig(path, dpi=240)
    plt.close()

def make_distance_heatmap(df: pd.DataFrame, path: Path):
    x = vectorize(df)
    dist = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=2)
    plt.figure(figsize=(6,6))
    plt.imshow(dist, cmap="viridis")
    plt.colorbar(label="Euclidean Distance")
    plt.title("Scenario Distance Heatmap")
    plt.xticks(range(len(df)), df["id"], rotation=90, fontsize=6)
    plt.yticks(range(len(df)), df["id"], fontsize=6)
    plt.tight_layout()
    plt.savefig(path, dpi=240)
    plt.close()

def make_timeline(df: pd.DataFrame, path: Path):
    plt.figure(figsize=(7,3))
    years = [2025, 2030, 2050, 2100]
    for idx, r in enumerate(df.itertuples()):
        plt.hlines(idx, years[0], years[-1], color='grey', alpha=0.5)
        plt.plot([years[1]], [idx], 'o', color='blue')
        plt.text(years[-1]+2, idx, r.id, verticalalignment='center', fontsize=7)
    plt.yticks([])
    plt.xlabel("Year")
    plt.title("Scenario Timeline Example")
    plt.tight_layout()
    plt.savefig(path, dpi=240)
    plt.close()

def make_risk_scatter(df: pd.DataFrame, path: Path):
    plt.figure(figsize=(7,6))
    plt.scatter(df["alignment"], df["autonomy_num"], s=150, c=df["agency"], cmap="coolwarm", alpha=0.7)
    plt.colorbar(label="Agency Level")
    for _, r in df.iterrows():
        plt.text(r["alignment"]+0.01, r["autonomy_num"]+0.01, r["id"][-6:], fontsize=7)
    plt.xlabel("Alignment Score")
    plt.ylabel("Autonomy (mapped)")
    plt.title("ASI Risk Scatter")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=240)
    plt.close()

# ───────────────────────────────────────────────
# Step 5 – Build PDF
# ───────────────────────────────────────────────

def build_pdf(df: pd.DataFrame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    pdf_path = REPORT_DIR / f"OASIS_ASI_Report_{timestamp}.pdf"

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=60, bottomMargin=60)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BigTitle", parent=styles["Title"], fontSize=22, alignment=1))

    story = []

    # ── Cover Page ──
    styles.add(ParagraphStyle(name="CoverTitle", fontSize=32, leading=38, alignment=1, spaceAfter=30,
                              textColor=colors.HexColor("#0b1c3d")))
    styles.add(ParagraphStyle(name="CoverSubtitle", fontSize=18, leading=24, alignment=1, spaceAfter=60,
                              textColor=colors.HexColor("#2c3e50")))
    styles.add(ParagraphStyle(name="CoverDate", fontSize=12, alignment=1, textColor=colors.grey))

    story.append(Spacer(1, 3 * inch))
    story.append(Paragraph("OASIS OBSERVATORY", styles["CoverTitle"]))
    story.append(Paragraph("Artificial Superintelligence<br/>Scenario Report", styles["CoverSubtitle"]))
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph(f"Generated on {datetime.now():%B %d, %Y at %H:%M}", styles["CoverDate"]))
    story.append(PageBreak())


    # Summary Table
    story.append(Paragraph("Selected Scenarios Overview", styles["Heading1"]))
    story.append(Spacer(1, 12))

    table_data = [["Scenario ID", "Created", "Agency", "Autonomy", "Alignment"]]
    for _, r in df.iterrows():
        table_data.append([
            Paragraph(f"<b>{r['id']}</b>", styles["Normal"]),
            r["date"],
            f"{r['agency']:.3f}",
            r["autonomy_str"],
            f"{r['alignment']:.3f}"
        ])

    table = Table(table_data, colWidths=[2.8 * inch, 1.0 * inch, 0.9 * inch, 1.1 * inch, 1.1 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fafc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(PageBreak())

    # Generate plots
    plot_paths = []
    paths = {
        "diversity_map.png": make_plot,
        "radar_chart.png": make_radar_chart,
        "distance_heatmap.png": make_distance_heatmap,
        "timeline.png": make_timeline,
        "risk_scatter.png": make_risk_scatter
    }

    for fname, func in paths.items():
        path = REPORT_DIR / fname
        func(df, path)
        plot_paths.append(path)

    for path in plot_paths:
        story.append(Paragraph(path.stem.replace("_", " ").title(), styles["Heading1"]))
        story.append(Spacer(1, 6))
        story.append(KeepInFrame(0, 0, [Image(str(path.resolve()), width=7*inch, height=6*inch)], hAlign="CENTER"))
        story.append(PageBreak())

    # Scenario Narratives
    story.append(Paragraph("Scenario Narratives", styles["Heading1"]))
    story.append(Spacer(1, 20))
    for _, r in df.iterrows():
        story.append(Paragraph(f"<b>{r['id']}</b>", styles["Heading2"]))
        story.append(Paragraph(f"Agency {r['agency']:.3f} • Autonomy {r['autonomy_str']} • Alignment {r['alignment']:.3f}", styles["Normal"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(r["narrative"], styles["Normal"]))
        story.append(Spacer(1, 20))

    doc.build(story)

    # Cleanup
    for path in plot_paths:
        path.unlink(missing_ok=True)

    log.info(f"Report generated: {pdf_path}")

# ───────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────

def generate_pdf_report():
    df_all = load_scenarios()
    if df_all.empty:
        log.error("No scenarios available in the database.")
        return

    df = select_diverse_scenarios(df_all, n=10)
    build_pdf(df)

if __name__ == "__main__":
    generate_pdf_report()