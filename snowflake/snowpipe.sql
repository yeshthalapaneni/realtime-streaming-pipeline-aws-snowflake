USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE PIPE raw_events_pipe
AUTO_INGEST = TRUE
AS
COPY INTO raw_events (
event_id,
customer_id,
event_type,
channel,
amount,
currency,
event_timestamp
)
FROM (
SELECT
$1:event_id::STRING,
$1:customer_id::STRING,
$1:event_type::STRING,
$1:channel::STRING,
$1:amount::FLOAT,
$1:currency::STRING,
$1:event_timestamp::TIMESTAMP_NTZ
FROM @raw_events_stage
);
