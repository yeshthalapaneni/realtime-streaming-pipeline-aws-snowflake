USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE TASK raw_to_curated_task
WAREHOUSE = COMPUTE_WH
SCHEDULE = '1 MINUTE'
AS
INSERT INTO curated_events (
event_id,
customer_id,
event_type,
channel,
amount,
currency,
event_timestamp,
processed_at
)
SELECT
event_id,
customer_id,
event_type,
channel,
amount,
currency,
event_timestamp,
CURRENT_TIMESTAMP()
FROM raw_events_stream
WHERE METADATA$ACTION = 'INSERT';
