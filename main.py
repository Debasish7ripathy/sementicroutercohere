from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn
from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder
import os

# Initialize FastAPI app
app = FastAPI(title="Healthcare Management API", version="1.0.0")

# Initialize semantic router
encoder = OpenAIEncoder()

# Define routes (using your existing routes)
prior_Authentication = Route(
    name="Pre_Auth",
    utterances=[
        "I need to get prior authorization for a medical procedure.",
        "Can you help me with the prior authorization process?",
        "I need approval for an MRI. Can you help?",
    ]
)

appointment_Schedular = Route(
    name="Appointment_Schedular",
    utterances=[
        "I need to schedule an appointment. What information do you need from me?",
        "Can you help me schedule a procedure for next week?",
        "Is there availability for an MRI appointment this Friday?",
    ]
)

# Add more routes as needed...

routes = [prior_Authentication, appointment_Schedular]
route_layer = RouteLayer(encoder=encoder, routes=routes)

# Pydantic models for request/response validation
class AuthorizationRequest(BaseModel):
    procedure_name: str = Field(..., description="Name of the medical procedure")
    patient_id: str = Field(..., description="Unique identifier for the patient")
    insurance_id: str = Field(..., description="Patient's insurance ID")
    scheduled_date: Optional[str] = Field(None, description="Planned date for the procedure")

class AppointmentRequest(BaseModel):
    patient_id: str = Field(..., description="Unique identifier for the patient")
    service_type: str = Field(..., description="Type of medical service needed")
    preferred_date: str = Field(..., description="Preferred date for the appointment")
    doctor_id: Optional[str] = Field(None, description="Preferred doctor's ID")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")

# Function implementations
def verify_prior_auth(procedure_name: str, patient_id: str, insurance_id: str) -> dict:
    """Verifies prior authorization for a medical procedure."""
    print(f"Invoked: verify_prior_auth function with procedure: `{procedure_name}` "
          f"for patient ID: `{patient_id}`")
    
    # In a real implementation, this would check against a database
    return {
        "status": "approved",
        "auth_number": f"PA{datetime.now().strftime('%Y%m%d%H%M')}",
        "expiration_date": (datetime.now().replace(month=12, day=31)).strftime("%Y-%m-%d"),
        "procedure_name": procedure_name,
        "patient_id": patient_id,
        "insurance_id": insurance_id
    }

def schedule_appointment(patient_id: str, service_type: str, preferred_date: str) -> dict:
    """Schedules a medical appointment for a patient."""
    print(f"Invoked: schedule_appointment function for patient: `{patient_id}`, "
          f"service: `{service_type}`, date: `{preferred_date}`")
    
    # In a real implementation, this would interact with a scheduling system
    return {
        "appointment_id": f"APT{datetime.now().strftime('%Y%m%d%H%M')}",
        "confirmed_date": preferred_date,
        "service_type": service_type,
        "patient_id": patient_id,
        "location": "Main Clinic",
        "status": "scheduled"
    }

# API endpoints
@app.post("/chat", response_model=Dict[str, Any])
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint for processing natural language requests and routing to appropriate functions
    """
    route_result = route_layer(request.message)
    
    if route_result.name == "Pre_Auth":
        # In a real implementation, you'd extract these details using NLP or ask the user
        return {
            "type": "clarification",
            "message": "To process your authorization request, I need the following details:",
            "required_fields": ["procedure_name", "patient_id", "insurance_id"]
        }
    elif route_result.name == "Appointment_Schedular":
        return {
            "type": "clarification",
            "message": "To schedule your appointment, I need the following details:",
            "required_fields": ["service_type", "preferred_date", "patient_id"]
        }
    else:
        return {
            "type": "unknown",
            "message": "I'm not sure how to help with that request. Could you please clarify?"
        }

@app.post("/authorization", response_model=Dict[str, Any])
async def authorization_endpoint(request: AuthorizationRequest):
    """
    Endpoint for processing prior authorization requests
    """
    try:
        result = verify_prior_auth(
            procedure_name=request.procedure_name,
            patient_id=request.patient_id,
            insurance_id=request.insurance_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/appointment", response_model=Dict[str, Any])
async def appointment_endpoint(request: AppointmentRequest):
    """
    Endpoint for scheduling appointments
    """
    try:
        result = schedule_appointment(
            patient_id=request.patient_id,
            service_type=request.service_type,
            preferred_date=request.preferred_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
