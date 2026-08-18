# Day 21 - Week 3 Checkpoint

## AI Analysis Testing Results

Tested AI threat-level classification across 4 different custom detection rules:

| Rule ID | Alert Type | AI Threat Level |
|---------|-----------|------------------|
| 100100  | IAM Policy Change | High |
| 100102  | Access Denied/Unusual API | High |
| 100103  | Security Group Modification | High |
| 100104  | S3 Bucket Exposure | High |

## Key Finding (Important Observation)

The AI model classified ALL four alert types as "High" severity, regardless of actual risk 
differences. In a real SOC context, this is a meaningful limitation:

- S3 public exposure (100104) is genuinely High risk - correct
- Access Denied (100102) is typically Low/Medium in isolation - a single denied 
  API call is often just a misconfigured permission, not an active attack
- IAM policy detach (100100) severity depends heavily on context (who did it, 
  was it expected) - defaulting to High may not be accurate

## Why This Matters

This demonstrates a real-world AI security concern: LLMs tend toward "safe" over-classification, 
which in production would cause alert fatigue - if everything is High, analysts lose the ability 
to prioritize. This is a common issue with naive LLM-SOC integrations and a valid area for 
future improvement (e.g., few-shot examples in the prompt, or a calibrated severity rubric).

## Next Steps (Future Improvement)
- Add few-shot examples to the prompt showing what Low/Medium/High actually look like
- Consider a rules-based severity floor/ceiling combined with AI reasoning, rather than 
  pure AI judgment
