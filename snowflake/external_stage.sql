USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE STAGE raw_events_stage
URL = 's3://your-raw-bucket-name/'
FILE_FORMAT = json_file_format;










USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE STAGE raw_events_stage
URL = 's3://your-raw-bucket-name/'
STORAGE_INTEGRATION = your_storage_integration_name
FILE_FORMAT = json_file_format;
