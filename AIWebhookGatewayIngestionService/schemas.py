from pydantic import BaseModel, Field


class WebhookPayload(BaseModel):
    event_type: str = Field(..., examples=["feedback.received"])
    source: str = Field(..., examples=["customer_portal"])
    content: str = Field(
        ..., min_length=10, examples=["The service was fast, but the UI is confusing."]
    )


class IngestResponse(BaseModel):
    status: str
    message: str
    trace_id: str
