from opensearchpy import OpenSearch
from openai import OpenAI
import boto3
import json

# ---- Fetch API key securely from AWS Secrets Manager ----
def get_openrouter_key():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId="soc-project/openrouter-api-key")
    return response["SecretString"]

# ---- Connect to Wazuh Indexer ----
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

def analyze_alert(alert, api_key):
    description = alert.get("rule", {}).get("description", "N/A")
    level = alert.get("rule", {}).get("level", "N/A")
    event_name = alert.get("data", {}).get("aws", {}).get("eventName", "N/A")
    user_name = alert.get("data", {}).get("aws", {}).get("userIdentity", {}).get("userName", "N/A")
    timestamp = alert.get("timestamp", "N/A")

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

# ---- Main ----
if __name__ == "__main__":
    api_key = get_openrouter_key()
    alert = fetch_latest_alert("100104")

    if not alert:
        print("No alert found")
        exit(1)

    print("=== Raw Alert ===")
    print(f"Description: {alert.get('rule', {}).get('description', 'N/A')}")
    print()

    result = analyze_alert(alert, api_key)

    print("=== AI Analysis (Structured) ===")
    print(f"Threat Level: {result['threat_level']}")
    print(f"Summary: {result['summary']}")
