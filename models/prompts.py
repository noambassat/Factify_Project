# models/prompts.py

invoice_prompt = """
You will receive an Invoice text. Extract the following fields and return them in **JSON format**:
- vendor (the issuing company or provider)
- amount (total to pay)
- due_date (or null if missing)
- line_items (array of items, each with description and amount)


If a field is missing, return it as null.
Return only a valid JSON object.


Invoice text:
{text}
"""

contract_prompt = """
You will receive a Contract text. Extract the following fields and return them in **JSON format**:
- parties (array of the names involved)
- effective_date (when the contract starts)
- termination_date (when the contract ends). If the text describes only a duration (e.g. "24 months from the effective date"), calculate the exact termination date.
- key_terms (list of important clauses or conditions)

If a field is missing, return it as null.
Return only a valid JSON object.

Contract text:
{text}
"""


earnings_prompt = """
You will receive a Report text. Extract the following fields and return them in **JSON format**:
- reporting_period (e.g. Q1 2025, or date range)
- key_metrics (a dictionary of important financial or operational numbers)
- executive_summary (brief summary or highlights)

If a field is missing, return it as null.
Return only a valid JSON object.

Report text:
{text}
"""

LABEL_PROMPTS = {
    "Invoice": invoice_prompt,
    "Contract": contract_prompt,
    "Earnings": earnings_prompt
}
