import os
from datetime import datetime
from fpdf import FPDF
from arq.connections import RedisSettings
from sqlmodel import Session, select

from app.database import engine
from app.models.transaction import Transaction

REPORT_DIR = os.path.join("app", "data", "reports")


class ExecutivePDF(FPDF):
    def header(self):
        self.set_fill_color(33, 38, 45)
        self.rect(0, 0, 210, 40, "F")
        self.set_xy(10, 12)
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "SPENDWISE", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(139, 148, 158)
        self.cell(
            0, 5, "EXECUTIVE FINANCIAL INTELLIGENCE", new_x="LMARGIN", new_y="NEXT"
        )
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(
            0,
            10,
            f"Confidential Report | Generated on {datetime.now().strftime('%Y-%m-%d')} | Page {self.page_no()}",
            align="C",
        )


async def generate_monthly_report(ctx, user_id: int):
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR, exist_ok=True)

    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.user_id == user_id)
        transactions = session.exec(statement).all()

    total_spend = sum(t.amount for t in transactions)
    count = len(transactions)
    avg_spend = total_spend / count if count > 0 else 0

    categories = {}
    for t in transactions:
        categories[t.category] = categories.get(t.category, 0) + t.amount

    top_category = max(categories, key=categories.get) if categories else "N/A"

    pdf = ExecutivePDF()
    pdf.add_page()
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(33, 38, 45)
    pdf.cell(0, 10, "Summary Insights", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_fill_color(246, 248, 250)
    pdf.set_draw_color(208, 215, 222)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)

    pdf.cell(90, 20, f" TOTAL BURN: ${total_spend:,.2f}", border=1, fill=True)
    pdf.cell(5, 20, "")
    pdf.cell(90, 20, f" AVG VELOCITY: ${avg_spend:,.2f}", border=1, fill=True)
    pdf.ln(25)

    pdf.cell(90, 20, f" TOP CATEGORY: {top_category.upper()}", border=1, fill=True)
    pdf.cell(5, 20, "")
    pdf.cell(90, 20, f" VOLUME: {count} TXNS", border=1, fill=True)
    pdf.ln(25)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(33, 38, 45)
    pdf.cell(0, 10, "Detailed Transaction Ledger", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_fill_color(33, 38, 45)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(35, 10, " DATE", border=0, fill=True)
    pdf.cell(45, 10, " CATEGORY", border=0, fill=True)
    pdf.cell(80, 10, " DESCRIPTION", border=0, fill=True)
    pdf.cell(30, 10, " AMOUNT", border=0, fill=True, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(33, 38, 45)
    fill = False
    for t in sorted(transactions, key=lambda x: x.date, reverse=True):
        pdf.set_fill_color(249, 250, 251) if fill else pdf.set_fill_color(255, 255, 255)
        display_date = (
            t.date.strftime("%Y-%m-%d") if hasattr(t.date, "strftime") else str(t.date)
        )
        pdf.cell(35, 8, f" {display_date}", fill=True)
        pdf.cell(45, 8, f" {t.category}", fill=True)
        desc = (
            (t.description[:40] + "...")
            if t.description and len(t.description) > 40
            else (t.description or "")
        )
        pdf.cell(80, 8, f" {desc}", fill=True)
        pdf.cell(30, 8, f"${t.amount:,.2f} ", fill=True, align="R")
        pdf.ln()
        fill = not fill

    filename = f"Statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)
    pdf.output(filepath)
    print("--- [EXECUTIVE REPORT GENERATED] ---")


class WorkerSettings:
    functions = [generate_monthly_report]
    redis_settings = RedisSettings(host="redis", port=6379)


if __name__ == "__main__":
    from arq.worker import run_worker

    # We must use flush=True so Docker shows the logs immediately
    print("--- [WORKER BOOT] ATTENDING REDIS QUEUE ---", flush=True)

    # This is the blocking call that keeps the container alive
    run_worker(WorkerSettings)
