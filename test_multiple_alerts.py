from opensearchpy import OpenSearch
from openai import OpenAI
import os
import json

wazuh_client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "SecretPassword"),
    use_ssl=True,
    verify_certs=False,
)

def fetch_latest_alert(rule_id):
    query = {
        "size": 1,
        "sort": [{"timestamp": {"order": "desc"}}],
        "query": {"match": {"rule.id": rule_id}}
    }
    result = wazuh_client.search(index="wazuh-alerts-*", body=query)
    if result["hits"]["total"]["value"] == 0:
        return None
    return result["hits"]["hits"][0]["_source"]

def analyze_alert(alert):
    description = alert.get("rule", {}).get("description", "N/A")
    level = alert.get("rule", {}).get("level", "N/A")
    event_name = alert.get("data", {}).get("aws", {}).get("eventName", "N/A")
    user_name = alert.get("data", {}).get("aws", {}).get("userIdentity", {}).get("userName", "N/A")
    timestamp = alert.get("timestamp", "N/A")

    api_key = os.environ.get("OPENROUTER_API_KEY")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    prompt = f"""You are a SOC analyst assistant. Analyze this security alert and respond ONLY with valid JSON in this exact format, no other text:

{{
  "threat_level": "Low" or "Medium" or "High",
  "summary": "exactly 2 sentences explaining what happened and why it matters"
}}

Alert to analyze:
Description: {description}
Wazuh Rule Level: {level}
Event: {event_name}
User: {user_name}
Timestamp: {timestamp}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"threat_level": "PARSE_ERROR", "summary": raw_output}

# ---- Test across all 4 custom rules ----
rule_ids_to_test = ["100100", "100102", "100103", "100104"]
rule_names = {
    "100100": "IAM Policy Change",
    "100102": "Access Denied / Unusual API",
    "100103": "Security Group Modification",
    "100104": "S3 Bucket Exposure"
}

for rule_id in rule_ids_to_test:
    print(f"\n{'='*50}")
    print(f"Testing Rule {rule_id} - {rule_names[rule_id]}")
    print('='*50)

    alert = fetch_latest_alert(rule_id)

    if not alert:
        print(f"No alert found in index for rule {rule_id}")
        continue

    result = analyze_alert(alert)
    print(f"Threat Level: {result['threat_level']}")
    print(f"Summary: {result['summary']}")
