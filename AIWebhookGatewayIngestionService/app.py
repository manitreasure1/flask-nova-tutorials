from typing import Literal

from flask import g
from flask_nova import FlaskNova, NovaBlueprint, Depend, to_thread
from schemas import WebhookPayload, IngestResponse
from dependencies import verify_webhook_signature
from tasks import process_webhook_ai_task


app = FlaskNova(__name__)
bp = NovaBlueprint("webhooks", __name__)


@bp.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest and process inbound webhooks",
)
async def ingest_webhook(
    payload: WebhookPayload, _auth=Depend(verify_webhook_signature)
) -> tuple[IngestResponse, Literal[202]]:

    trace_id = g.trace_id

    await to_thread(
        process_webhook_ai_task,
        event_type=payload.event_type,
        content=payload.content,
        trace_id=trace_id,
    )

    inget_response = IngestResponse(
        status="accepted", message="Webhook queued for processing", trace_id=trace_id
    )
    return inget_response, 202


app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
