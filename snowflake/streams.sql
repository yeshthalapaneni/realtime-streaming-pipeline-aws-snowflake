USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE STREAM raw_events_stream
ON TABLE raw_events;
