# 🖼️ Smart Image Processing Pipeline (AWS Serverless)

## 🧠 Summary
A fully serverless AWS application that processes images uploaded by users:
- Optimizes image size
- Analyzes content using Rekognition
- Saves results to DynamoDB
- Notifies user via email or SMS

This project demonstrates mastery of:
- Event-driven architecture
- Step Functions orchestration
- ML services (Rekognition)
- Serverless compute (Lambda)

---

## 🛠️ AWS Services Used

| Service      | Purpose                                      |
|--------------|----------------------------------------------|
| S3           | Store original and processed images          |
| Lambda       | Resize images, call Rekognition, store data  |
| Step Functions | Orchestrate multi-step flow                |
| Rekognition  | Detect labels or faces in uploaded images    |
| DynamoDB     | Store image metadata and analysis results    |
| SNS / SES    | Notify users via email or SMS                |
| IAM          | Handle permissions securely                  |

---

## 🚀 Architecture Diagram

```plaintext
Client → S3 Bucket (Upload Trigger)
          |
          ↓
     Lambda (Trigger Step Function)
          |
          ↓
┌─────────────────────────────────────────────┐
│           AWS Step Functions                │
│ ┌─────────┐ ┌───────────────┐ ┌──────────┐  │
│ │ Resize  │→│ Rekognition   │→│ Save to  │→ SNS/SES
│ │ Lambda  │ │ Label Lambda  │ │ DynamoDB │   Notification
│ └─────────┘ └───────────────┘ └──────────┘  │
└─────────────────────────────────────────────┘

/image-pipeline-app
│
├── /lambdas
│   ├── triggerStepFunction.py
│   ├── resizeImage.py
│   ├── rekognitionLabels.py
│   └── storeMetadata.py
│
├── /infrastructure
│   └── template.yaml   # AWS SAM or CloudFormation
│
├── /frontend (optional)
│   └── upload.html or React app
│
└── README.md

📐 Architecture Decisions
Decision	Reason
Event-driven via S3 trigger	Enables immediate pipeline execution on upload
Step Functions	Breaks down logic into modular steps; observability and retries
Multiple Lambdas	Single-responsibility functions = cleaner, testable, replaceable
DynamoDB	Scalable, serverless, and flexible metadata store
SNS/SES	Abstracts final user notification; can scale to multiple channels

🔒 Security Considerations
Least-privilege IAM roles via SAM-managed policies

No public access on S3 bucket

SNS topic is locked down to specific Lambda role

Environment variables used to inject table names securely

CloudWatch Logs used to monitor execution for debugging/traceability

🧭 Opportunities for Improvement
Add Cognito authentication for frontend uploads

Store resized image in a separate S3 folder (/processed/)

Add image type detection and conditional branching in Step Function

Add CloudWatch Alarms for failed executions

Store Rekognition confidence thresholds in a config parameter

🛣️ Future Extensions
Auto-tagging and search UI using labels in DynamoDB

Support for video uploads using AWS Elastic Transcoder

Implement versioned processing (e.g., v2 with moderation APIs)

Hook into EventBridge for downstream processing

Store analytics in Amazon Timestream or QuickSight