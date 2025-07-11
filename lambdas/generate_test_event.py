import base64

boundary = "------------------------testboundary"
file_path = "cart.jpg"
with open(file_path, "rb") as f:
    file_bytes = f.read()

multipart = f"""--{boundary}
Content-Disposition: form-data; name="file"; filename="cart.jpg"
Content-Type: image/jpeg

""".encode("utf-8") + file_bytes + f"""
--{boundary}--""".encode("utf-8")

encoded_body = base64.b64encode(multipart).decode()

event_json = {
    "body": encoded_body,
    "headers": {
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    },
    "isBase64Encoded": True
}

import json
with open("event.json", "w") as f:
    json.dump(event_json, f)

print("✅ event.json generated.")