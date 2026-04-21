USE DATABASE realtime_streaming_db;
USE SCHEMA streaming_schema;

CREATE OR REPLACE FILE FORMAT json_file_format
TYPE = 'JSON';
