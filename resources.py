import base64

with open("data/Alice_in_Wonderland.pdf", "rb") as pdf_file:
    PDF_FILE = base64.b64encode(pdf_file.read()).decode("utf-8")

# Regex to Match Screen Aggregates and Data Actions
DATA_ACTION_PATTERN = r'controller\.(callDataAction|callAggregateWithStartIndexAndClientVars)\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"'