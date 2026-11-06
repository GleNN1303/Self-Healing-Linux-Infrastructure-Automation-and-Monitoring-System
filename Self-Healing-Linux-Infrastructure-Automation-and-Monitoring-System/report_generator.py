from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

doc = SimpleDocTemplate(
    f"reports/report_{datetime.now().date()}.pdf"
)

styles = getSampleStyleSheet()

elements = []

elements.append(
    Paragraph(
        "Self-Healing Linux Infrastructure Report",
        styles['Title']
    )
)

elements.append(
    Paragraph(
        f"Generated On: {datetime.now()}",
        styles['Normal']
    )
)

elements.append(Spacer(1,20))

try:
    with open("logs/system.log","r") as f:

        logs = f.read()

        elements.append(
            Paragraph(
                logs.replace("\n","<br/>"),
                styles['Normal']
            )
        )

except:
    elements.append(
        Paragraph(
            "No Logs Found",
            styles['Normal']
        )
    )

doc.build(elements)

print("PDF Report Generated")
