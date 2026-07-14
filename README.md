# iLoveVideoEditor Python SDK (High-Level Wrapper)

This is the **official high-level Python SDK** for iLoveVideoEditor.
It wraps the auto-generated OpenAPI client with ergonomic method names,
polling logic, and typed result objects.

## Installation

```bash
pip install ilovevideoeditor-sdk
```

*(Requires the generated OpenAPI client to be installed or bundled.)*

## Quick Start

```python
from ilovevideoeditor import iLoveVideoEditorClient

client = iLoveVideoEditorClient(api_key="vf_live_xxx")

# Submit and poll until done
result = client.render(
    {"name": "Hello", "layers": [...]},
    on_progress=lambda status, progress: print(f"{status} — {progress}%"),
)

print(result.download_url)
```

## Methods

- `client.queue_render(video_json)` → submit and return `{"job_id", "status"}`
- `client.render(video_json, ...)` → submit + poll + return `RenderResult`
- `client.get_render(job_id)` → get status
- `client.refresh_url(job_id)` → fresh download URL
- `client.list_templates()` → list public templates
- `client.get_template(id)` → get single template
