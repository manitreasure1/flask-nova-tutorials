```
[ External Webhook / Client ]
           │ (JSON Payload + W3C Trace Header)
           ▼
[ Flask-Nova Route ] ──(Validates via Pydantic)
           │
           ├──► Immediately returns 202 Accepted (with trace_id)
           │
           └──► Spawns `to_thread(process_event_async)`
                      │
                      ├──► Logs using `JSON_LOG` + `trace_id`
                      └──► Calls LLM API / Updates DB

```