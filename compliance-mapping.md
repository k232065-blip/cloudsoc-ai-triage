# Detection Rules — MITRE ATT&CK + Compliance Mapping

| Rule ID | Detection | MITRE Technique | Tactic | CIS AWS Foundations Control | UAE NESA Reference |
|---------|-----------|------------------|--------|------------------------------|---------------------|
| 100100 | IAM Policy Change | T1098.003 - Additional Cloud Roles | Persistence, Privilege Escalation | CIS 1.16 - Ensure IAM policies are attached only to groups or roles | NESA T3.5.2 - Access Control Change Monitoring |
| 100101 | Root Account Login | T1078.004 - Cloud Accounts | Defense Evasion, Persistence, Initial Access | CIS 1.7 - Eliminate use of the root user for administrative tasks | NESA T3.4.1 - Privileged Account Monitoring |
| 100102 | Access Denied / Unusual API | T1580 - Cloud Infrastructure Discovery | Discovery | CIS 3.1 - Ensure a log metric filter and alarm exist for unauthorized API calls | NESA T3.2.3 - Anomalous Activity Detection |
| 100103 | Security Group Modification | T1562.007 - Disable/Modify Cloud Firewall | Defense Evasion | CIS 3.10 - Ensure a log metric filter and alarm exist for security group changes | NESA T3.5.4 - Network Control Change Monitoring |
| 100104 | S3 Bucket Exposure | T1530 - Data from Cloud Storage | Collection, Exfiltration | CIS 2.1.1/2.1.2 - Ensure S3 buckets employ encryption and block public access | NESA T3.6.1 - Data Protection at Rest and in Transit |

## Why This Mapping Matters

Each detection rule was designed to catch a specific attacker technique (MITRE), but the same 
rule also happens to directly support a known compliance control (CIS/NESA). This is not a 
coincidence - it reflects a general pattern: most compliance frameworks exist precisely because 
the controls they mandate prevent or detect the attacker techniques MITRE catalogs. Mapping both 
together in one table demonstrates the ability to translate between "how would an attacker do 
this" and "what control does an auditor expect to see" - a skill needed when justifying security 
tooling investment to non-technical stakeholders or compliance teams.

Note: CIS AWS Foundations Benchmark control numbers referenced are from the general public 
benchmark structure. NESA references use the framework's general control categories (UAE NESA's 
detailed control catalog is not fully public: these should be validated against the specific 
control document in a real production/audit context).
