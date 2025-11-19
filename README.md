# Youtube-Data-Analysis
Youtube data analysis using apache flink and Apache Kafka

Project Overview

This project collects and analyzes real time YouTube data from the Aaj Tak news channel. The goal is to understand viewer behaviour by monitoring video performance as soon as new content is uploaded. You gather information such as views, likes, comments, publish time, and descriptions. This data is streamed continuously, processed instantly, and stored so that it can be visualized on dashboards and used for deeper analytics.

Components Used

The project uses the YouTube Data API, Kafka, Apache Flink, Elasticsearch, and Kibana.

The YouTube Data API gives you live information about new videos posted on Aaj Tak. A Python script acts as a producer, continuously requesting the API and sending the data into Kafka.

Kafka works as the message streaming platform. It temporarily stores the incoming live data and acts like a real time buffer that forwards the data to Flink.

Apache Flink is the real time processing engine. It reads data from Kafka, processes it as soon as it arrives, extracts useful fields, and converts the stream into structured records that are ready for analysis.

Elasticsearch stores the final processed data. It allows very fast searching, filtering, and analysis. Once the data is inside Elasticsearch, it becomes easy to create visualizations.

Kibana connects to Elasticsearch and allows you to build dashboards and graphs such as daily views, the best and worst performing videos, peak upload times, and audience engagement trends.

The Data Pipeline

The pipeline begins with the producer that collects data from the Aaj Tak channel. It sends this data continuously into Kafka. Kafka forwards every new event into Flink. Flink processes the records one by one and forwards the cleaned and structured output into Elasticsearch. Finally, Kibana reads this data from Elasticsearch and displays it in a dashboard where insights can be viewed live.

In a simple path, the data flows as YouTube API to Kafka to Flink to Elasticsearch to Kibana.

What the Project Finds

This project focuses on understanding viewer behaviour for the Aaj Tak YouTube channel.

You find which videos receive the most views, which ones perform poorly, and how quickly they grow. You also track likes and comments which helps measure engagement. By checking publish time and comparing it with performance, you can identify the time of day when videos get maximum attention from viewers.
Over time, the system can show patterns, such as whether morning news performs better than evening news.

If comment analysis or sentiment analysis is added later, you can also understand what viewers liked or disliked in each video.

The system is designed to run continuously so insights always remain updated and help in understanding real time audience behaviour.
