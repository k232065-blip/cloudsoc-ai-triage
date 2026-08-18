# Manual Triage Fallback Checklist

If the AI analysis layer (fetch_and_analyze.py) is unavailable - API downtime, rate limits, 
or a result you don't trust - here is the manual process to triage a Wazuh alert directly.

## Step 1 - Identify the Alert
- Open Wazuh Dashboard -> Threat Hunting -> Events
- Note: rule.id, rule.level, rule.description, timestamp

## Step 2 - Pull the Raw Event Details
- Expand the alert (magnifying glass icon) to see the full CloudTrail event
- Key fields to check manually:
  - `aws.eventName` - what action was taken
  - `aws.userIdentity.userName` / `userIdentity.type` - who did it (and whether it was Root)
  - `aws.sourceIPAddress` - where the request came from
  - `aws.requestParameters` - exact parameters of the action (e.g. which bucket, which policy)
  - `aws.errorCode` - was the action successful or denied

## Step 3 - Establish Context (Ask These Questions)
- Is this user/role expected to perform this action? (Check against known team members/automation)
- Is the source IP recognized? (Office IP, VPN range, or unfamiliar?)
- Did this happen during expected working hours, or at an unusual time?
- Is this a one-off event, or part of a pattern? (Search the same user/IP across a wider time range)

## Step 4 - Cross-Reference Related Logs
- Search CloudTrail/Wazuh for other events from the same user or IP in the surrounding time window
- Check if this event correlates with any other alert (e.g. a Security Group change right 
  after an Access Denied event may indicate probing followed by a successful attempt)

## Step 5 - Determine Severity Manually
Use this as a floor - never go below Wazuh's own assigned rule level:
- Level 12+ (e.g. root login, S3 exposure): Treat as High regardless of context until proven otherwise
- Level 8-11 (e.g. policy changes, SG changes): Medium by default; escalate to High if the 
  actor/context is unrecognized
- Level 3-7 (e.g. general API activity): Low by default; escalate if it's part of a larger pattern

## Step 6 - Decide and Act
- If confirmed benign: document reasoning, close the alert
- If suspicious or confirmed malicious: 
  1. Immediately revert the change if it increased exposure (e.g. re-block public access, 
     revoke the security group rule)
  2. Rotate any credentials that may have been used maliciously
  3. Document the full timeline (see day16-detection-results.md for the format used in this project)
  4. Escalate per your organization's incident response process

## Why This Exists
This checklist is what fetch_and_analyze.py is automating and accelerating - not replacing. 
Every field the AI reads and reasons about in Step 3-5 here is manually inspectable in the 
Wazuh dashboard. Understanding this manual process is what allows an analyst to sanity-check 
AI output rather than blindly trust it - directly relevant given the prompt injection 
vulnerability documented in day24-prompt-injection-findings.md.
