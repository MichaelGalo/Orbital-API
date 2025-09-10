# Orbital API

Orbital API is a **serverless, cloud-native microservice** deployed on **Google Cloud Run**. It provides access to curated datasets from the [Orbital Data Pipeline](https://github.com/MichaelGalo/Orbital-Data-Pipeline) lakehouse, enabling fast, scalable, and production-ready querying through a RESTful interface powered by **FastAPI** and **DuckDB/DuckLake**.  

This API is designed to integrate seamlessly into a larger microservices architecture, continuing the work and learnings developed at **Nashville Software School’s inaugural Data Engineering program**.  

---

## Overview

- **Framework**: FastAPI
- **Database Layer**: DuckDB with DuckLake for Google Cloud Storage integration  
- **Cloud Deployment**: Google Cloud Run
- **Storage**: Google Cloud Storage
- **Architecture**: Part of a **cloud-native microservices ecosystem**  

---

## Features

- **REST API with automatic docs** at `/docs` (Swagger UI) and `/redoc`  
- **Health check endpoint** for monitoring (`/health`)  
- **Dataset discovery endpoint** listing available datasets (`/datasets`)  
- **Parameterized dataset queries** with offset/limit pagination (`/datasets/{dataset_id}`)  
- **Cloud-native storage**: queries run against a GCS-hosted `ducklake.catalog` attached dynamically to DuckDB  
- **Serverless scaling** with Cloud Run  

---

## Endpoints

| Endpoint                    | Method | Description |
|------------------------------|--------|-------------|
| `/`                         | GET    | Welcome message and API overview |
| `/health`                   | GET    | Returns API health and timestamp |
| `/datasets`                 | GET    | Lists available datasets with IDs and names |
| `/datasets/{dataset_id}`    | GET    | Returns dataset records with pagination support (`offset`, `limit`) |

---

## Available Datasets

The API provides access to several cleaned datasets from the Orbital Data Pipeline:  

| ID | Dataset            |
|----|--------------------|
| 1  | Astronauts         |
| 2  | NASA APOD (Astronomy Picture of the Day) |
| 3  | NASA DONKI (Space Weather) |
| 4  | NASA Exoplanets    |

---

## Project Background

Orbital API was built as a continuation of my data engineering journey at **Nashville Software School**, where I was part of the **first cohort of the Data Engineering program**.  

It represents:  
- A practical application of **cloud-native microservices**  
- Hands-on use of **modern data lakehouse architectures**  
- A production-ready bridge between **raw data pipelines** and **end-user access**  
