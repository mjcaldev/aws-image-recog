# 🖼️ Smart Image Processing Pipeline

## 🧠 Summary

This is a fully serverless AWS application that automatically processes user-uploaded images. It resizes the image, runs content analysis via Amazon Rekognition, stores results in DynamoDB, and notifies the user via email or SMS.

---

## ⚙️ Check Blueprint.md for infrastrucutral notes

---

## 🚀 How to Deploy

1. Install the AWS SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

2. Clone this repo and navigate to the project folder:
   ```bash
   git clone https://github.com/your-username/image-pipeline-app.git
   cd image-pipeline-app
Build and deploy using SAM:

bash
Copy
Edit
sam build
sam deploy --guided
Follow prompts to create:

S3 bucket

Step Function

Lambda functions

DynamoDB table

Notification topic

🧪 How to Test
Upload a .jpg or .png image to your deployed S3 bucket.

Check:

✅ Resized image is saved

✅ Metadata appears in DynamoDB

✅ You receive a notification via SNS or SES