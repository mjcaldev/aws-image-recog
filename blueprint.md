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