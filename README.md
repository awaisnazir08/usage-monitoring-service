# User Monitoring Microservice

This microservice enables user monitoring through bandwidth tracking, upload logging, deletion tracking, and daily usage summaries. It is deployed on Google Cloud Platform (GCP) and uses Flask for API handling, MongoDB for data storage, and a modular design for scalability.

## Table of Contents
- [Features](#features)
- [Endpoints](#endpoints)
- [Setup and Configuration](#setup-and-configuration)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Contact](#contact)

---

## Features
- Tracks user upload and deletion activities.
- Provides bandwidth usage alerts and daily summaries.
- Supports configurable daily bandwidth limits.
- Modular architecture with MongoDB integration.

---

## Endpoints
### Base URL
`/api/usage`

### 1. Check Upload Bandwidth
**Endpoint:** `/check-upload-bandwidth`

**Method:** `POST`

**Description:** Checks if a user is allowed to upload a file based on daily bandwidth usage.

**Request Body:**
```json
{
  "file_size": <size_of_file_in_bytes>
}
```

**Response:**
- **200:**
```json
{
  "allowed": true,
  "message": "Upload permitted"
}
```
- **400:**
```json
{
  "allowed": false,
  "message": "Daily bandwidth limit exceeded"
}
```

### 2. Log Upload
**Endpoint:** `/log-upload`

**Method:** `POST`

**Description:** Logs the details of an uploaded file and updates the user's usage records.

**Request Body:**
```json
{
  "file_name": "<file_name>",
  "file_size": <size_of_file_in_bytes>
}
```

**Response:**
- **200:**
```json
{
  "email": "<user_email>",
  "date": "<upload_date>",
  "total_upload_volume": <total_uploaded>,
  "uploads": [<upload_details>]
}
```
- **400:** Failure response.

### 3. Check Usage Alerts
**Endpoint:** `/check-usage-alerts`

**Method:** `GET`

**Description:** Checks if the user is nearing or exceeding their daily bandwidth limit.

**Response:**
- **200:**
```json
{
  "total_bandwidth_used": <bytes>,
  "bandwidth_total_limit": <limit>,
  "bandwidth_percentage_used": <percentage>,
  "bandwidth_checks": {
    "bandwidth_limit_approaching": <true_or_false>,
    "bandwidth_limit_exceeded": <true_or_false>
  }
}
```

### 4. Daily Summary
**Endpoint:** `/daily-summary`

**Method:** `GET`

**Description:** Provides a daily summary of a user's bandwidth consumption and upload statistics.

**Response:**
- **200:**
```json
{
  "email": "<user_email>",
  "date": "<current_date>",
  "total_bandwidth_limit": <limit>,
  "total_data_bandwidth_used": <bytes>,
  "remaining_bandwidth": <bytes>,
  "bandwidth_percentage_consumed": <percentage>,
  "upload_count": <count>,
  "uploads": [<upload_details>]
}
```

### 5. Log Deletion
**Endpoint:** `/log-deletion`

**Method:** `POST`

**Description:** Logs details of a file deletion and updates the user's usage records.

**Request Body:**
```json
{
  "file_name": "<file_name>",
  "file_size": <size_of_file_in_bytes>
}
```

**Response:**
- **200:**
```json
{
  "email": "<user_email>",
  "file_deleted": "<file_name>",
  "file_size": <size_of_file_in_bytes>,
  "updated_deletion_volume": <updated_volume>,
  "total_deletion_count": <count>
}
```

### 6. Reset Daily Usage
**Endpoint:** `/reset-daily`

**Method:** `POST`

**Description:** Resets the daily usage statistics for the user. Intended for administrative use.

**Response:**
- **200:**
```json
{
  "message": "Daily usage successfully reset."
}
```

---

## Setup and Configuration
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure MongoDB URI and daily bandwidth limit in `config.py`:
   ```python
   MONGO_URI = "your_mongo_connection_string"
   DAILY_BANDWIDTH_LIMIT = 104857600
   ```
4. Run the Flask application:
   ```bash
   flask run
   ```
5. Deploy the application to GCP or your preferred cloud provider.

---

## Technologies Used
- Flask
- MongoDB
- Google Cloud Platform (GCP)

---

## Usage
- Use the provided endpoints to monitor and manage user bandwidth usage.
- Ensure MongoDB is configured and accessible for storage.
- Utilize authentication with `AuthService` for secure access.

---


