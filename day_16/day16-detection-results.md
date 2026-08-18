# Day 16 - Attack Simulation Results

## Attack Details
- Target: soc-project-bucket-rashid2026 (S3 bucket)
- Method: Modified Block Public Access settings + added public-read bucket policy
- Action: PutBucketPolicy

## Detection Results
- Detection Rule: 100104 (Level 13)
- Rule Logic: Monitors PutBucketAcl, PutBucketPolicy, PutPublicAccessBlock events
- First Alert Timestamp: Aug 4, 2026 @ 04:18:14.637
- Second Alert Timestamp: Aug 4, 2026 @ 04:20:34.083
- Status: SUCCESSFULLY DETECTED

## Detection Pipeline (What Happened)
AWS CloudTrail (logged the API call)
-> S3 Bucket (stored CloudTrail log file)
-> Wazuh aws-s3 wodle (pulled the log, 5-min poll interval)
-> Custom Rule 100104 (matched the event, generated alert)
-> Wazuh Dashboard (alert visible to analyst)

## Remediation Taken
- Bucket policy deleted immediately after test
- Block Public Access re-enabled (all 4 settings)
- Bucket confirmed private again

## What a Real SOC Analyst Would Do Next (If This Were a Real Incident)
1. Immediately verify who made the change (check aws.userIdentity.userName in the alert)
2. Check if any data was actually accessed publicly during the exposure window (S3 access logs)
3. Revert the bucket to private (done)
4. Investigate if the credentials/account that made the change were compromised
5. Review CloudTrail for any other suspicious activity from the same user/IP around that time
6. File an incident report and notify relevant stakeholders

## Key Learning
Detection latency in this test included AWS CloudTrail's natural delivery delay (typically 5-15 min) 
plus Wazuh's 5-min polling interval. This combined lag reflects a real-world SIEM limitation - 
not a flaw in the custom rule logic itself. In production environments, this could be reduced 
using CloudTrail -> CloudWatch Logs -> real-time Lambda triggers instead of periodic S3 polling.
