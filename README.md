# AWS Cross-Account STS ISS Tracker

---

A serverless AWS pipeline demonstrating secure cross-account access using STS AssumeRole — no static credentials, no long-lived keys.

## Real World Parallel

This project directly mirrors a pattern used in production AWS environments across financial services, healthcare, and government.

**The scenario:** A bank runs a fraud detection service in a security account. When suspicious activity is detected it needs to write an alert into a separate logging account owned by the security team. The security team doesn't want the fraud service to have permanent access to their account — that would be a security risk in itself.

**The solution is identical to this project:**
- Fraud detection service (Account A) has one permission — assume a role in the logging account
- Logging account (Account B) exposes a role that trusts the fraud service and allows only S3 writes to one specific bucket
- Credentials are temporary, scoped, and audited via CloudTrail
- No static keys. No persistent access. No blast radius if credentials are ever compromised

## The Problem

In real AWS environments, workloads span multiple accounts — production, staging, shared services, security tooling. The wrong solution is to create IAM users with static access keys and paste them into applications. This is how companies get breached. Static keys don't expire, they get committed to GitHub, stolen from environment variables, and used for months before anyone notices.

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

![Lambda Success](https://github.com/ibrahimpandor/aws-cross-account-sts-iss-tracker/blob/main/Evidence/Image%2003-06-2026%20at%2019.26.jpeg)

## ISS Data in Account B S3 Bucket
JSON file written to iss-tracker-data-bucket in Account B, confirming cross-account write succeeded.

![S3 Object](https://github.com/ibrahimpandor/aws-cross-account-sts-iss-tracker/blob/main/Evidence/Image%2003-06-2026%20at%2019.31.jpeg)

## Account B IAM Role
Cross-account role in Account B with AmazonS3FullAccess and trust policy allowing Account A.

![IAM Role](https://github.com/ibrahimpandor/aws-cross-account-sts-iss-tracker/blob/main/Evidence/Image%2003-06-2026%20at%2019.38.jpeg)

## Scoped STS Policy in Account A
Inline policy on Lambda execution role showing sts:AssumeRole scoped to one specific role ARN in Account B — least privilege in action.

![STS Policy](https://github.com/ibrahimpandor/aws-cross-account-sts-iss-tracker/blob/main/Evidence/Image%2003-06-2026%20at%2019.44.jpeg)

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
- **latitude/longitude** — exact coordinates over Earth at the moment of capture. This reading placed the ISS over the South Pacific Ocean near Fiji
- **altitude** — 429km above Earth's surface, within the ISS's typical orbital range of 400–420km
- **velocity** — 27,545 km/h, approximately 8km per second, the speed required to maintain low Earth orbit
- **visibility** — daylight means the sun was illuminating the station at this moment
  
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

## Tools & Technologies Used

| Tool | Purpose |
|------|---------|
| AWS Lambda | Serverless function in Account A — runs the pipeline |
| AWS STS | Issues temporary cross-account credentials via AssumeRole |
| AWS IAM | Trust policies and scoped permissions across both accounts |
| Amazon S3 | Stores ISS location data in Account B |
| AWS Organizations | Manages both accounts under a single organisation |
| Python 3.12 | Lambda function runtime |
| boto3 | AWS SDK for Python — used to call STS and S3 |
| urllib | Built-in Python library for calling the ISS API |
| Open Notify / wheretheiss.at | Public API providing real-time ISS location data |
| GitHub | Version control and portfolio documentation |

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat-square&logo=aws-lambda&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-569A31?style=flat-square&logo=amazon-s3&logoColor=white)
![AWS IAM](https://img.shields.io/badge/AWS_IAM-DD344C?style=flat-square&logo=amazon-aws&logoColor=white)
![AWS STS](https://img.shields.io/badge/AWS_STS-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)
![boto3](https://img.shields.io/badge/boto3-SDK-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?style=flat-square&logo=github&logoColor=white)

