# Reddit Realtime Data Pipeline

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Tools Used](#tools-used)
- [Project Steps](#project-steps)
- [Dashboard](#dashboard)

## Introduction
This project is a real-time data pipeline designed to collect, process, and visualize data from Reddit posts. By tracking metrics and details about posts in real time, we can extract insights into user engagement, popular topics, and more. 

## Project Overview
We designed a data pipeline that uses the Reddit API to collect post data, streams it using Apache Kafka, stores it in Cassandra, and visualizes it after querying. Key metrics include post title, author, subreddit, score, number of comments, and other engagement-related data. The pipeline is orchestrated and automated using Apache Airflow, and all components are containerized with Docker for easy deployment and management.

## Tools Used
- **Reddit API:** For fetching data about posts, including details like title, score, author, subreddit, and comments.
- **Apache Kafka:** For real-time data streaming and integration between components.
- **Cassandra:** As a NoSQL database for data storage and querying.
- **Apache Airflow:** For workflow orchestration and task scheduling.
- **Docker:** For containerizing and managing the project components (Airflow, Kafka, Cassandra).

## Project Steps

![Data Pipeline Architecture](https://github.com/houda-moudni/Reddit-Data-Pipeline/blob/main/statics/reddit_data_pipeline.png)

### Data Collection
- Developed scripts to extract Reddit post data using the Reddit API.
- Set up Kafka producers to stream data to Kafka topics.

### Data Streaming
- **Kafka Producers:** Streamed freshly scraped data from Reddit to specific Kafka topics.
- **Kafka Consumers:** Retrieved data from Kafka topics and stored it in Cassandra.

### Data Storage
- Verified data storage in Cassandra for historical analysis and efficient querying.

### Data Visualization
- Used ODBC Driver to connect Cassandra with Power Bi.
- Developed dashboards and visualizations to display Reddit post metrics using Power Bi.

### Workflow Orchestration
- Created Airflow DAGs to automate data collection, streaming, processing, and storage tasks.
- Scheduled regular workflows for data fetching, processing, and updating visualizations.

## Dashboard
**Reddit RealTime Dashboard**
![Dashboard](https://github.com/houda-moudni/Reddit-Data-Pipeline/blob/main/statics/reddit_dashboard.png)
The dashboard presents various Reddit post metrics like post subreddit, score, and comments in real time, helping users to monitor engagement and trends across subreddits.

## About
- **Houda Moudni**
- **email** : houdamoudni.01@gmail.com


