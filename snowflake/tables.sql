USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE TABLE raw_events (
event_id STRING,
customer_id STRING,
event_type STRING,
channel STRING,
amount FLOAT,
currency STRING,
event_timestamp TIMESTAMP_NTZ,
ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE curated_events (
event_id STRING,
customer_id STRING,
event_type STRING,
channel STRING,
amount FLOAT,
currency STRING,
event_timestamp TIMESTAMP_NTZ,
processed_at TIMESTAMP_NTZ
);
