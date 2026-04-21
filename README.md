# Real-Time Streaming Data Pipeline (AWS to Snowflake)

## Overview

This project implements a real-time data streaming pipeline using AWS and Snowflake. It simulates event ingestion through an API, processes incoming data, streams it using Kinesis, and stores it in S3 before making it available in Snowflake for querying.

The goal is to demonstrate how to design and connect multiple cloud services to build a scalable, event-driven data pipeline with minimal operational overhead.

---

## Architecture Summary

The pipeline follows this flow:

Postman → API Gateway → Lambda → Kinesis Data Streams → Kinesis Firehose → S3 → Snowflake (Snowpipe)

Data is generated using Postman and sent as HTTP requests to API Gateway. Lambda validates and routes the data. Valid records are streamed through Kinesis and delivered to S3 via Firehose. Snowflake continuously ingests the data from S3 using Snowpipe.

---

## Components

### API Layer

* API Gateway acts as the entry point for all incoming data
* Accepts HTTP POST requests containing event payloads

### Processing Layer

* Lambda function processes incoming requests
* Validates schema and structure of data
* Routes valid data to Kinesis
* Sends invalid records to an S3 error bucket

### Streaming Layer

* Kinesis Data Streams captures real-time data
* Provides buffering and decoupling between ingestion and delivery

### Delivery Layer

* Kinesis Firehose reads from Kinesis and delivers data to S3
* Handles batching and efficient data transfer

### Storage Layer

* S3 stores data in JSON format
* Separate buckets for valid and invalid data

### Data Warehouse Layer

* Snowflake is used for querying and analytics
* External stage connects Snowflake to S3
* Snowpipe continuously loads new data into tables

---

## Data Flow

1. Postman sends event data via HTTP POST request
2. API Gateway receives the request and triggers Lambda
3. Lambda validates the payload:

   * Valid data is sent to Kinesis Data Streams
   * Invalid data is written to an S3 error bucket
4. Kinesis streams the data in real time
5. Firehose delivers streaming data to S3
6. Snowpipe detects new files in S3 and loads them into Snowflake tables
7. Data becomes available for querying in Snowflake

---

## Deployment Steps

1. Create IAM roles and policies for API Gateway, Lambda, Kinesis, Firehose, and S3 access

2. Create two S3 buckets:

   * One for valid data
   * One for error data

3. Set up Kinesis:

   * Create a Kinesis Data Stream
   * Create a Firehose delivery stream connected to S3

4. Create Lambda function:

   * Add validation logic
   * Configure routing to Kinesis or S3

5. Configure API Gateway:

   * Create POST endpoint
   * Integrate with Lambda

6. Configure Snowflake:

   * Create database and schema
   * Create external stage pointing to S3
   * Create target tables

7. Enable Snowpipe:

   * Configure auto-ingestion from S3 to Snowflake

8. Test the pipeline:

   * Send sample requests via Postman
   * Validate data in S3 and Snowflake

---

## Sample Payload

```json
{
  "event_id": "12345",
  "user_id": "u1001",
  "event_type": "purchase",
  "amount": 249.99,
  "event_time": "2026-04-21T10:15:30Z"
}
```

---

## Repository Structure

```bash
realtime-streaming-pipeline/
│
├── README.md
├── architecture/
├── lambda/
├── snowflake/
├── postman/
├── docs/
├── sample_data/
└── screenshots/
```

---

## Key Design Decisions

* API Gateway and Lambda used for simple, scalable ingestion
* Kinesis used for real-time streaming and decoupling
* Firehose used to simplify delivery into S3 without custom consumers
* S3 used as the raw data layer for durability and cost efficiency
* Snowpipe used for near real-time ingestion into Snowflake without manual loads

---

## What This Project Demonstrates

* End-to-end real-time data pipeline design
* Integration across multiple AWS services
* Serverless data processing
* Streaming data ingestion patterns
* Cloud data warehousing with Snowflake

---

## Future Improvements

* Add infrastructure as code using Terraform
* Add monitoring using CloudWatch and alerts
* Add schema validation framework
* Add downstream transformations using dbt
* Add CI/CD pipeline for deployment

---

## Author

Yeshwanth Kumar
Data Engineer
AWS | Snowflake | Streaming Systems
