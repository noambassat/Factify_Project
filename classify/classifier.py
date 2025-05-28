# classify/classifier.py
import math
from models.openai_client import client

def classify_document(doc, model="gpt-4o"):
    prompt = f"""You will receive a short document excerpt. 
Classify it strictly as one of the following JSON values: "Invoice", "Contract", or "Earnings".
Only return the single word as a JSON string. For example: "Invoice".

Document excerpt:
{doc.raw_text[:250]}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        logprobs=True,
        top_logprobs=3,
        max_tokens=3
    )

    doc.predicted_label = response.choices[0].message.content.strip().strip('"')
    tokens_logprobs = [t.logprob for t in response.choices[0].logprobs.content]
    total_logprob = sum(tokens_logprobs)
    doc.label_confidence = {doc.predicted_label: round(math.exp(total_logprob), 3)}
    return doc
