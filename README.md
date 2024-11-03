Here's a README file based on your description:

---

# Real-Time-Reddit-Data-Pipeline

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

**Pipeline Components:**
1. **Data Collection:** Collects Reddit post data using the Reddit API.
2. **Data Streaming:** Streams real-time data to Apache Kafka topics.
3. **Data Storage:** Stores processed data in Cassandra for efficient querying and analysis.
4. **Data Visualization:** Queries data in Cassandra and visualizes it.
5. **Workflow Orchestration:** Uses Apache Airflow to automate and manage workflows.

## Tools Used
- **Reddit API:** For fetching data about posts, including details like title, score, author, subreddit, and comments.
- **Apache Kafka:** For real-time data streaming and integration between components.
- **Cassandra:** As a NoSQL database for data storage and querying.
- **SQL Queries:** For querying stored data in Cassandra and generating insights.
- **Apache Airflow:** For workflow orchestration and task scheduling.
- **Docker:** For containerizing and managing the project components (Airflow, Kafka, Cassandra).

## Project Steps
### Setup and Configuration
1. **Environment Setup:** Installed and configured necessary tools, libraries, and Docker.
2. **Database Configuration:** Set up Cassandra and created keyspaces/tables for storing post data.
3. **API Configuration:** Configured API access and credentials for the Reddit API.
4. **Airflow Setup:** Installed and configured Apache Airflow for managing workflows.

### Data Collection
- Developed scripts to extract Reddit post data using the Reddit API.
- Set up Kafka producers to stream data to Kafka topics.

### Data Streaming
- **Kafka Producers:** Streamed freshly scraped data from Reddit to specific Kafka topics.
- **Kafka Consumers:** Retrieved data from Kafka topics and stored it in Cassandra.

### Data Storage
- Verified data storage in Cassandra for historical analysis and efficient querying.

### Data Processing and Querying
- Queried data using SQL to gain insights and prepare for visualization.
  
### Data Visualization
- Used SQL queries to extract relevant data from Cassandra.
- Developed dashboards and visualizations to display Reddit post metrics.

### Workflow Orchestration
- Created Airflow DAGs to automate data collection, streaming, processing, and storage tasks.
- Scheduled regular workflows for data fetching, processing, and updating visualizations.

## Dashboard
**Reddit_RealTime_Dashboard**
![Data Pipeline Architecture](https://github.com/houda-moudni/Reddit-Data-Pipeline/edit/main/README.md#:~:text=untitled%20folder-,reddit_dashboard,-.png)](https://github.com/houda-moudni/Reddit-Data-Pipeline/blob/main/untitled%20folder/reddit_dashboard.png)
Our dashboard presents various Reddit post metrics like post titles, subreddit, score, and comments in real time, helping users to monitor engagement and trends across subreddits.

***
## About
**Houda Moudni**
**email** : houdamoudni.01@gmail.com

---

