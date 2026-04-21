import json
import os
import uuid
from datetime import datetime, timezone

import boto3

kinesis_client = boto3.client("kinesis")
s3_client = boto3.client("s3")

KINESIS_STREAM_NAME = os.environ["KINESIS_STREAM_NAME"]
ERROR_BUCKET_NAME = os.environ["ERROR_BUCKET_NAME"]

REQUIRED_FIELDS = [
"event_id",
"customer_id",
"event_type",
"channel",
"amount",
"currency",
"event_timestamp"
]

def build_response(status_code, body):
return {
"statusCode": status_code,
"headers": {
"Content-Type": "application/json"
},
"body": json.dumps(body)
}

def parse_body(event):
body = event.get("body")

```
if body is None:
    raise ValueError("Request body is missing")

if isinstance(body, str):
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body is not valid JSON") from exc

if isinstance(body, dict):
    return body

raise ValueError("Unsupported request body format")
```

def validate_payload(payload):
missing_fields = [field for field in REQUIRED_FIELDS if field not in payload]

```
if missing_fields:
    return False, f"Missing required fields: {', '.join(missing_fields)}"

if not isinstance(payload["event_id"], str) or not payload["event_id"].strip():
    return False, "event_id must be a non-empty string"

if not isinstance(payload["customer_id"], str) or not payload["customer_id"].strip():
    return False, "customer_id must be a non-empty string"

if not isinstance(payload["event_type"], str) or not payload["event_type"].strip():
    return False, "event_type must be a non-empty string"

if not isinstance(payload["channel"], str) or not payload["channel"].strip():
    return False, "channel must be a non-empty string"

if not isinstance(payload["currency"], str) or not payload["currency"].strip():
    return False, "currency must be a non-empty string"

if not isinstance(payload["amount"], (int, float)):
    return False, "amount must be numeric"

try:
    datetime.fromisoformat(payload["event_timestamp"].replace("Z", "+00:00"))
except Exception:
    return False, "event_timestamp must be a valid ISO-8601 timestamp"

return True, "Payload is valid"
```

def write_invalid_record_to_s3(payload, reason):
timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H")
record_id = str(uuid.uuid4())

```
error_record = {
    "error_reason": reason,
    "received_at": datetime.now(timezone.utc).isoformat(),
    "payload": payload
}

key = f"invalid-records/{timestamp}/{record_id}.json"

s3_client.put_object(
    Bucket=ERROR_BUCKET_NAME,
    Key=key,
    Body=json.dumps(error_record).encode("utf-8"),
    ContentType="application/json"
)

return key
```

def send_to_kinesis(payload):
response = kinesis_client.put_record(
StreamName=KINESIS_STREAM_NAME,
Data=json.dumps(payload),
PartitionKey=payload["event_id"]
)
return response

def lambda_handler(event, context):
try:
payload = parse_body(event)

```
    is_valid, message = validate_payload(payload)

    if not is_valid:
        error_key = write_invalid_record_to_s3(payload, message)
        return build_response(
            400,
            {
                "message": "Invalid payload",
                "reason": message,
                "error_s3_key": error_key
            }
        )

    send_to_kinesis(payload)

    return build_response(
        200,
        {
            "message": "Payload processed successfully",
            "stream": KINESIS_STREAM_NAME,
            "event_id": payload["event_id"]
        }
    )

except ValueError as exc:
    error_key = write_invalid_record_to_s3(
        {"raw_event": event.get("body")},
        str(exc)
    )
    return build_response(
        400,
        {
            "message": "Bad request",
            "reason": str(exc),
            "error_s3_key": error_key
        }
    )

except Exception as exc:
    return build_response(
        500,
        {
            "message": "Internal server error",
            "reason": str(exc)
        }
    )
```
