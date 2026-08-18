# Cost Governance

## AWS Budget Alert
- Budget name: soc-project-monthly-budget
- Threshold: $5/month
- Alert trigger: 80% of budgeted amount, sent via email
- Purpose: Cost anomalies (e.g. an unexpected spike from a compromised or misconfigured 
  resource) are often an early warning sign of a security incident, not just a billing issue. 
  A tight budget threshold on a project this size acts as a lightweight anomaly detector 
  alongside the security-specific detection rules (Wazuh/GuardDuty).

## Free Tier Confirmation
The entire project (VPC, EC2 t2.micro instance, S3 storage, CloudTrail, IAM roles, 
Terraform-managed duplicate infrastructure during testing) was built and tested within 
AWS Free Tier limits. No charges beyond the free tier were incurred during development.

## Why This Matters
Security engineers who only think about access controls and detection rules miss half the 
picture - cost-consciousness reflects an understanding of the business context security 
operates within, and cost anomalies are frequently the first observable signal of compromise 
in real incidents (e.g. cryptomining on a hijacked EC2 instance).
