# Attack Simulation Plan - Day 15
## Target
S3 Bucket: soc-project-bucket-rashid2026
## Attack Scenario
Simulate accidental public exposure of S3 bucket (common real-world misconfiguration)
## Steps to Execute (Day 16)
1. Note exact start time (T0)
2. Disable "Block Public Access" on bucket
3. Add public-read bucket policy
4. Monitor Wazuh dashboard for rule 100104 trigger
5. Note detection time (T1)
6. Calculate: Detection Time = T1 - T0
7. Revert bucket to private immediately after test
## Detection Rule
Rule 100104 (level 13) - monitors PutBucketAcl, PutBucketPolicy, PutPublicAccessBlock events

## RESULTS - Day 16 Execution

- Attack executed: S3 bucket (soc-project-bucket-rashid2026) made public via PutBucketPolicy
- Detection: Rule 100104 triggered successfully (Level 13)
- First alert timestamp: Aug 4, 2026 @ 04:18:14.637
- Second alert timestamp: Aug 4, 2026 @ 04:20:34.083
- Detection mechanism confirmed working end-to-end: AWS CloudTrail -> S3 -> Wazuh aws-s3 wodle -> Custom Rule 100104
- Bucket reverted to private immediately after test (Block Public Access re-enabled, bucket policy deleted)
- Note: Detection latency includes AWS CloudTrail's inherent delivery delay (5-15 min) plus Wazuh's 5-min polling interval - this combined lag is a known real-world SIEM limitation, not a gap in the custom rule logic
