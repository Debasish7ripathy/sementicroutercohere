# Healthcare Management API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [API Reference](#api-reference)
5. [Semantic Routing](#semantic-routing)
6. [Examples](#examples)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Overview

The Healthcare Management API is a robust system designed to handle various healthcare-related requests using natural language processing and semantic routing. It provides endpoints for prior authorization, appointment scheduling, and general healthcare inquiries.

### Key Features
- Natural language processing for request interpretation
- Prior authorization verification
- Appointment scheduling
- Extensible semantic routing system

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/your-org/healthcare-api.git
cd healthcare-api
```

2. Install required dependencies:
```bash
pip install fastapi uvicorn pydantic semantic-router openai
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | API key for OpenAI services | Yes |
| PORT | Port to run the API server (default: 8000) | No |
| HOST | Host to run the API server (default: 0.0.0.0) | No |

### Running the API
```bash
python main.py
```
Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

## API Reference

### Endpoints

#### 1. Chat Endpoint
Process natural language requests and route to appropriate functions.

```
POST /chat
```

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "type": "string",
  "message": "string",
  "required_fields": ["string"]
}
```

#### 2. Authorization Endpoint
Handle prior authorization requests for medical procedures.

```
POST /authorization
```

**Request Body:**
```json
{
  "procedure_name": "string",
  "patient_id": "string",
  "insurance_id": "string",
  "scheduled_date": "string" (optional)
}
```

**Response:**
```json
{
  "status": "string",
  "auth_number": "string",
  "expiration_date": "string",
  "procedure_name": "string",
  "patient_id": "string",
  "insurance_id": "string"
}
```

#### 3. Appointment Endpoint
Schedule medical appointments.

```
POST /appointment
```

**Request Body:**
```json
{
  "patient_id": "string",
  "service_type": "string",
  "preferred_date": "string",
  "doctor_id": "string" (optional)
}
```

**Response:**
```json
{
  "appointment_id": "string",
  "confirmed_date": "string",
  "service_type": "string",
  "patient_id": "string",
  "location": "string",
  "status": "string"
}
```

#### 4. Health Check Endpoint
Verify API operational status.

```
GET /health
```

**Response:**
```json
{
  "status": "string",
  "timestamp": "string"
}
```

## Semantic Routing

The API uses semantic routing to interpret and direct natural language requests to appropriate endpoints.

### Supported Route Categories
1. Prior Authorization (`Pre_Auth`)
2. Appointment Scheduling (`Appointment_Schedular`)

### Route Examples
- "I need to get prior authorization for an MRI"
- "Can you help me schedule an appointment for next week?"
- "Is there availability for a CT scan on Friday?"

## Examples

### Python Example
```python
import requests

BASE_URL = "http://localhost:8000"

# Chat request
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "I need authorization for an MRI"}
)
print(response.json())

# Authorization request
response = requests.post(
    f"{BASE_URL}/authorization",
    json={
        "procedure_name": "MRI",
        "patient_id": "P12345",
        "insurance_id": "INS789"
    }
)
print(response.json())
```

### cURL Example
```bash
# Chat request
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message":"I need to schedule an appointment"}'

# Appointment request
curl -X POST "http://localhost:8000/appointment" \
     -H "Content-Type: application/json" \
     -d '{
           "patient_id": "P12345",
           "service_type": "MRI",
           "preferred_date": "2024-06-15"
         }'
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages.

### Common Error Codes
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

### Error Response Format
```json
{
  "detail": "Error description"
}
```

## Best Practices

1. Always handle API responses and errors appropriately
2. Use appropriate timeout settings for API calls
3. Implement rate limiting in your client applications
4. Keep your API key secure and never expose it in client-side code

## Troubleshooting

### Common Issues

1. Authentication Failures
   - Ensure your API key is set correctly
   - Verify the API key has not expired

2. Routing Issues
   - Check if your query matches any existing route patterns
   - Try rephrasing your request

3. Performance Issues
   - Ensure you're not exceeding rate limits
   - Check your network connection

### Getting Help

For additional support:
1. Check the [GitHub issues](https://github.com/your-org/healthcare-api/issues)
2. Contact support at support@yourhealthcareapi.com

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-05-01 | Initial release |
