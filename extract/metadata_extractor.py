# extract/metadata_extractor.py
import json
from models.prompts import LABEL_PROMPTS
from models.openai_client import client

def extract_metadata(doc, model="gpt-4o"):
    prompt = LABEL_PROMPTS[doc.predicted_label].format(text=doc.raw_text)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    doc.metadata.update(data)
    return doc
