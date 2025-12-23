import asyncio
import os
from datetime import datetime
from fpdf import FPDF
from arq.connections import RedisSettings


async def generate_monthly_report(ctx, user_id: int):
    # Ensure the data directory exists
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    # Simulate processing time
    await asyncio.sleep(5)

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, "SpendWise Financial Report")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(40, 10, f"User ID: {user_id}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.ln(20)
    pdf.multi_cell(
        0,
        10,
        "This is a summary of your financial activity. In a production app, you would query the database here to list actual transactions.",
    )

    # Generate a unique filename
    filename = f"report_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(DATA_DIR, filename)

    # Save the file
    pdf.output(filepath)
    print(f"Successfully saved report: {filepath}")


class WorkerSettings:
    functions = [generate_monthly_report]
    redis_settings = RedisSettings(host="redis", port=6379)


if __name__ == "__main__":
    from arq.worker import run_worker

    run_worker(WorkerSettings)
