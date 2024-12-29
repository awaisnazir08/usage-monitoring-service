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



# Endpoint: Get Complete Usage Summary

This API endpoint provides a detailed summary of a user's usage statistics, including daily records and overall summary statistics. 

---

## **Endpoint**
### **GET** `/api/usage/complete-summary`

---

## **Authorization**
This endpoint requires authentication. You must include a valid token in the request header to access it.

- **Decorator Used**: `@AuthService.token_required`

---

## **Request**
### **Headers**
| Key           | Value           |
|---------------|-----------------|
| Authorization | Bearer `<token>` |

### **Parameters**
None

---

## **Response**
### **Status Code**
- **200 OK**: The request was successful, and usage statistics are returned.

### **Response Body**
The response is a JSON object containing:
1. **Summary Statistics**:
   - **Date Range**:
     - `start`: The start date of the records.
     - `end`: The end date of the records.
     - `total_days`: Total days in the date range.
     - `days_with_activity`: Number of days with recorded activity.
     - `days_without_activity`: Number of days without activity.
   - **Bandwidth Totals**:
     - `total_bandwidth_provided`: Total bandwidth allocated based on the date range.
     - `total_data_bandwidth_used`: Total data bandwidth used.
     - `total_volume_deleted`: Total volume of data deleted.
     - `overall_bandwidth_percentage_consumed`: Percentage of the total bandwidth consumed.
   - **Daily Averages**:
     - `average_daily_usage`: Average data bandwidth used per day.
     - `average_daily_deletions`: Average data deleted per day.
     - `average_daily_upload_count`: Average number of uploads per day.
     - `average_daily_deletion_count`: Average number of deletions per day.
     - `average_usage_on_active_days`: Average data bandwidth used on days with activity.
     - `average_deletions_on_active_days`: Average data deleted on days with activity.
   - **Activity Totals**:
     - `total_upload_count`: Total number of uploads.
     - `total_deletion_count`: Total number of deletions.

2. **Daily Records**:
   A list of daily usage records, each containing:
   - `email`: User's email address.
   - `date`: Date of the record.
   - `total_bandwidth_limit`: Daily bandwidth limit.
   - `total_data_bandwidth_used`: Bandwidth used on that day.
   - `total_volume_deleted`: Volume of data deleted on that day.
   - `remaining_bandwidth`: Remaining bandwidth for the day.
   - `bandwidth_percentage_consumed`: Percentage of the daily bandwidth used.
   - `upload_count`: Number of uploads on that day.
   - `deletion_count`: Number of deletions on that day.
   - `uploads`: List of upload details.
   - `deletions`: List of deletion details.

---

## **Example Response**

```json
{
  "email": "user@example.com",
  "summary_statistics": {
    "date_range": {
      "start": "2024-12-01",
      "end": "2024-12-29",
      "total_days": 29,
      "days_with_activity": 15,
      "days_without_activity": 14
    },
    "bandwidth_totals": {
      "total_bandwidth_provided": 2900,
      "total_data_bandwidth_used": 1200,
      "total_volume_deleted": 500,
      "overall_bandwidth_percentage_consumed": 41.38
    },
    "daily_averages": {
      "average_daily_usage": 41.38,
      "average_daily_deletions": 17.24,
      "average_daily_upload_count": 3.45,
      "average_daily_deletion_count": 2.07,
      "average_usage_on_active_days": 80,
      "average_deletions_on_active_days": 33.33
    },
    "activity_totals": {
      "total_upload_count": 100,
      "total_deletion_count": 60
    }
  },
  "daily_records": [
    {
      "email": "user@example.com",
      "date": "2024-12-29",
      "total_bandwidth_limit": 100,
      "total_data_bandwidth_used": 50,
      "total_volume_deleted": 20,
      "remaining_bandwidth": 50,
      "bandwidth_percentage_consumed": 50,
      "upload_count": 5,
      "deletion_count": 2,
      "uploads": [
        {"file_name": "example1.txt", "size": 10},
        {"file_name": "example2.txt", "size": 15}
      ],
      "deletions": [
        {"file_name": "example3.txt", "size": 5}
      ]
    }
  ]
}
```

