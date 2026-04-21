# Architecture Notes

## Overview

This project implements a real-time data pipeline that ingests event data through an API, processes and validates it, streams it using AWS services, and loads it into Snowflake for analytics.

The architecture is designed to be serverless, scalable, and loosely coupled. Each component has a specific responsibility, allowing the pipeline to handle real-time data reliably while keeping operational overhead low.

---

## End-to-End Flow

Postman → API Gateway → Lambda → Kinesis Data Streams → Kinesis Firehose → S3 → Snowflake (Snowpipe → Streams → Tasks)

---

## Design Approach

The pipeline is structured in distinct layers:

* Ingestion Layer
* Processing Layer
* Streaming Layer
* Storage Layer
* Data Warehouse Layer

This separation ensures that each stage can scale independently and can be modified without impacting the entire system.

---

## Ingestion Layer

**Component:** Amazon API Gateway

API Gateway serves as the entry point for all incoming data. It exposes an HTTP endpoint that accepts POST requests containing event payloads.

Key responsibilities:

* Accept external requests
* Route requests to downstream processing
* Provide a scalable and managed API interface

Reason for choice:
API Gateway provides a fully managed way to handle incoming traffic without managing servers. It integrates directly with Lambda, making it suitable for event-driven ingestion.

---

## Processing Layer

**Component:** AWS Lambda

Lambda is triggered by API Gateway for every incoming request. It acts as the validation and routing layer.

Key responsibilities:

* Validate incoming payload structure
* Perform basic data checks
* Route valid records to Kinesis Data Streams
* Route invalid records to an S3 error bucket

Error handling:
Invalid or malformed records are not dropped. They are written to a separate S3 bucket for further inspection and debugging.

Reason for choice:
Lambda allows execution of lightweight processing logic without maintaining infrastructure. It scales automatically with incoming requests.

---

## Streaming Layer

**Component:** Amazon Kinesis Data Streams

Kinesis Data Streams is used to capture real-time event data after validation.

Key responsibilities:

* Buffer incoming data streams
* Decouple ingestion from downstream delivery
* Support high-throughput streaming workloads

Reason for choice:
Kinesis provides low-latency streaming and allows multiple consumers if needed in the future.

---

## Delivery Layer

**Component:** Amazon Kinesis Firehose

Firehose reads data from Kinesis Data Streams and delivers it to S3.

Key responsibilities:

* Batch streaming data
* Convert and deliver records efficiently
* Reduce the need for custom consumer applications

Reason for choice:
Firehose simplifies data delivery by handling buffering, batching, and retries automatically. This reduces operational complexity.

---

## Storage Layer

**Component:** Amazon S3

S3 is used as the raw data storage layer.

Key responsibilities:

* Store incoming data in JSON format
* Maintain durable and cost-effective storage
* Separate valid and invalid data into different buckets

Design choice:
Two buckets are used:

* Raw data bucket for valid records
* Error bucket for invalid records

Reason for choice:
S3 provides high durability and is well-suited for storing large volumes of raw data for downstream processing.

---

## Data Warehouse Layer

**Component:** Snowflake

Snowflake is used as the analytics layer where data becomes queryable.

### External Stage

An external stage is configured to connect Snowflake to the S3 bucket.

Purpose:

* Allow Snowflake to read files stored in S3
* Serve as the source for Snowpipe ingestion

### Snowpipe

Snowpipe is used for continuous ingestion of data from S3 into Snowflake tables.

Key responsibilities:

* Automatically detect new files in S3
* Load data into Snowflake without manual intervention

Reason for choice:
Snowpipe enables near real-time ingestion and eliminates the need for scheduled batch loads.

---

## Transformation Layer

**Components:** Snowflake Streams and Tasks

After raw data is loaded into Snowflake, it is processed into curated datasets.

### Streams

* Track changes in the raw table
* Enable incremental processing

### Tasks

* Execute scheduled or triggered transformations
* Move and transform data from raw tables to curated tables

Reason for choice:
Streams and Tasks allow incremental data processing without reprocessing entire datasets, making the pipeline efficient and scalable.

---

## Data Flow Details

1. A client sends an HTTP POST request with event data using Postman
2. API Gateway receives the request and invokes Lambda
3. Lambda validates the payload

   * Valid records are sent to Kinesis Data Streams
   * Invalid records are written to an S3 error bucket
4. Kinesis streams the data in real time
5. Firehose reads from Kinesis and delivers data to S3
6. Data is stored in S3 as JSON files
7. Snowpipe detects new files and loads them into Snowflake
8. Streams capture changes in the raw table
9. Tasks process the data into curated tables
10. Curated data becomes available for analytics

---

## Key Design Decisions

* API Gateway and Lambda were used to enable a fully serverless ingestion layer
* Kinesis Data Streams was chosen to handle real-time streaming and decouple ingestion from delivery
* Firehose was used to simplify data delivery to S3 without building custom consumers
* S3 was used as a durable raw data layer
* Snowpipe was used to enable continuous ingestion into Snowflake
* Streams and Tasks were used to support incremental transformations

---

## Scalability Considerations

* API Gateway and Lambda scale automatically with incoming requests
* Kinesis Data Streams can scale by adjusting shard count
* Firehose handles batching and throughput scaling internally
* S3 scales automatically for storage
* Snowflake separates storage and compute, allowing independent scaling

---

## Limitations

* Schema validation is basic and handled within Lambda
* No advanced data quality framework is implemented
* Monitoring and alerting are not fully configured
* Infrastructure is manually provisioned (no Terraform or IaC)

---

## Future Improvements

* Add infrastructure as code using Terraform
* Implement centralized monitoring using CloudWatch
* Add alerting for pipeline failures
* Introduce data quality validation frameworks
* Add CI/CD for automated deployment
* Enhance transformation logic using dbt or advanced Snowflake models

---
