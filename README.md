# AWS Cross-Account STS ISS Tracker

---

A serverless AWS pipeline demonstrating secure cross-account access using STS AssumeRole — no static credentials, no long-lived keys.

## The Problem

In real AWS environments, workloads span multiple accounts — production, staging, shared services, security tooling. The naive solution is to create IAM users with static access keys and paste them into applications. This is how companies get breached. Static keys don't expire, they get committed to GitHub, stolen from environment variables, and used for months before anyone notices.

## The Solution

AWS Security Token Service (STS) eliminates static keys entirely. A Lambda function in Account A assumes a role in Account B and receives temporary credentials that expire after one hour. No persistent credentials anywhere in the codebase.

## Architecture






## How It Works - flow

1. Lambda in Account A calls the Open Notify ISS API and fetches the real-time location of the International Space Station
2. Lambda calls STS AssumeRole targeting a specific role ARN in Account B
3. Account B's IAM role trust policy allows Account A to assume it
4. STS returns temporary credentials valid for 1 hour
5. Lambda uses those credentials to write the ISS JSON payload to S3 in Account B
6. Credentials expire — nothing persists

## evidence 

## Successful Lambda Execution
Lambda in Account A executed successfully, fetching ISS data and writing to Account B's S3 bucket via STS temporary credentials.

![Lambda Success](lambda-success.png)

## ISS Data in Account B S3 Bucket
JSON file written to iss-tracker-data-bucket in Account B, confirming cross-account write succeeded.

![S3 Object](s3-object.png)

## Account B IAM Role
Cross-account role in Account B with AmazonS3FullAccess and trust policy allowing Account A.

![IAM Role](iam-role.png)

## Scoped STS Policy in Account A
Inline policy on Lambda execution role showing sts:AssumeRole scoped to one specific role ARN in Account B — least privilege in action.

![STS Policy](sts-policy.png)

## Trust Policy
Account B role trust policy showing Account A (532025488915) as the only trusted principal.

![Trust Policy](trust-policy.png)

## Security Design

- **No static keys** — temporary credentials only, expiring after 1 hour
- **Least privilege** — Lambda execution role has one permission: `sts:AssumeRole` on one specific ARN
- **Scoped access** — Account B role allows only `s3:PutObject` on one specific bucket
- **Auditable** — every AssumeRole call is logged in CloudTrail

## Sample Output

```json
{
  "name": "iss",
  "id": 25544,
  "latitude": -23.54116651065,
  "longitude": 177.576465627,
  "altitude": 429.09884601276,
  "velocity": 27545.759523619,
  "visibility": "daylight",
  "retrieved_at": "2026-06-03T18:26:40.934366"
}
```

## AWS Services Used

| Service | Account | Purpose |
|---------|---------|---------|
| Lambda | A | Runs the function |
| STS | A | Issues temporary credentials |
| IAM | A | Lambda execution role with scoped AssumeRole |
| IAM | B | Cross-account role with trust policy |
| S3 | B | Stores ISS location data |

## Repository Structure


## Key Learning

This project demonstrates a pattern used in every serious multi-account AWS environment. Understanding STS AssumeRole and cross-account IAM trust relationships is a core skill for cloud security and DevSecOps roles.
