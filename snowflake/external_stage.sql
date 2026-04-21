USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE STAGE raw_events_stage
URL = 's3://your-raw-bucket-name/'
FILE_FORMAT = json_file_format;
