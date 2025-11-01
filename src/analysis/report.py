from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
from pathlib import Path

# Load aggregated portfolio data
df = pd.read_csv("results/portfolio_aggregated.csv")

# Basic performance metrics
total_return = (1 + df["pnl"].fillna(0)).prod() - 1
sharpe = df["pnl"].mean() / df["pnl"].std() * (252 ** 0.5) if df["pnl"].std() != 0 else 0
win_rate = (df["pnl"] > 0).mean()

# Load equity curve image (optional)
img_path = Path("results/equity_curve.png")

# Per-asset summary if available
summary_data = []
for file in Path("results").glob("alpha*_multiasset.csv"):
    temp = pd.read_csv(file)
    if "pnl" in temp.columns:
        summary_data.append([file.stem, round(temp["pnl"].sum(), 4)])
if summary_data:
    summary_df = pd.DataFrame(summary_data, columns=["Alpha", "Total PnL"])
else:
    summary_df = pd.DataFrame(columns=["Alpha", "Total PnL"])

# --- Build PDF ---
doc = SimpleDocTemplate("results/performance_report.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elements = []

elements.append(Paragraph("<b>Multi-Asset Portfolio Performance Report</b>", styles["Title"]))
elements.append(Spacer(1, 12))

# Table for metrics
data = [
    ["Metric", "Value"],
    ["Total Return", f"{total_return*100:.2f}%"],
    ["Sharpe Ratio", f"{sharpe:.2f}"],
    ["Win Rate", f"{win_rate*100:.2f}%"]
]
t = Table(data, colWidths=[150, 150])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.grey),
    ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.black)
]))
elements.append(t)
elements.append(Spacer(1, 24))

# Per-asset summary
if not summary_df.empty:
    elements.append(Paragraph("<b>Per-Asset PnL Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    table_data = [summary_df.columns.tolist()] + summary_df.values.tolist()
    summary_table = Table(table_data, colWidths=[200, 150])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

# Embed equity curve image
if img_path.exists():
    elements.append(Paragraph("<b>Equity Curve</b>", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(Image(str(img_path), width=400, height=250))

doc.build(elements)
print("✅ Report generated → results/performance_report.pdf (with chart & PnL table)")
