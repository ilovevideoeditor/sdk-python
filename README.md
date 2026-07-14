# ilovevideoeditor-sdk

Official Python SDK for iLoveVideoEditor — render videos programmatically with a cloud video API.

iLoveVideoEditor is a cloud video rendering API: submit a JSON scene description (VideoJSON) or a template, queue a render, and download the resulting MP4/WebM. This SDK is the official Python client — it ships a high-level client with polling and progress callbacks on top of a fully typed, auto-generated OpenAPI client covering every API resource.

[![PyPI version](https://img.shields.io/pypi/v/ilovevideoeditor-sdk.svg)](https://pypi.org/project/ilovevideoeditor-sdk/) [![Python versions](https://img.shields.io/pypi/pyversions/ilovevideoeditor-sdk.svg)](https://pypi.org/project/ilovevideoeditor-sdk/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Docs](https://img.shields.io/badge/docs-ilovevideoeditor.com-blue)](https://ilovevideoeditor.com/docs/sdks) [![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/56628364-3f13fc43-a1e0-489a-804a-dc0582999ddf?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D56628364-3f13fc43-a1e0-489a-804a-dc0582999ddf%26entityType%3Dcollection%26workspaceId%3Df6303c1d-8772-405a-8999-6b6077bd13a5)
- API reference: [OpenAPI spec](https://ilovevideoeditor.com/docs/api/openapi.yaml) · [Postman collection](https://ilovevideoeditor.com/docs/api/postman-collection.json)

## Features

- **Render videos from JSON** — submit a VideoJSON scene description and get back a downloadable MP4/WebM
- **Blocking or queued renders** — `render()` submits, polls, and returns the finished result; `queue_render()` + `get_render()` let you poll on your own schedule
- **Progress callbacks** — track render status and percent completion while you wait
- **Fresh download URLs** — refresh signed download URLs for completed renders at any time
- **Template support** — list public templates and fetch individual template definitions
- **Full API coverage** — the bundled low-level client (`ilovevideoeditor_sdk`) exposes renders, templates, projects, assets, billing, API keys, integrations, renditions, tools, webhooks, and workflows
- **Typed** — fully annotated, ships `py.typed`, pydantic v2 models throughout

## Installation

```bash
pip install ilovevideoeditor-sdk
```

or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install ilovevideoeditor-sdk
```

Requires Python 3.10 or newer.

## Quick start

```python
from ilovevideoeditor import iLoveVideoEditorClient

client = iLoveVideoEditorClient(api_key="vf_live_xxx")

video_json = {
    "name": "hello-world",
    "layers": [
        {"type": "composition", "width": 1920, "height": 1080, "fps": 30},
    ],
}

# Submit, poll until done, and return the finished render
result = client.render(
    video_json,
    on_progress=lambda status, progress: print(f"{status} — {progress}%"),
)

print(result.download_url)
```

All high-level methods:

- `client.render(video_json, poll_interval=2.0, max_wait=300.0, on_progress=None)` → submit + poll + return a `RenderResult` (`job_id`, `status`, `progress`, `url`, `download_url`, `error`, `created_at`, `completed_at`)
- `client.queue_render(video_json)` → submit and return `{"job_id", "status"}` immediately
- `client.get_render(job_id)` → current status of a render job as a `RenderResult`
- `client.refresh_url(job_id)` → fresh signed download URL for a completed render
- `client.list_templates()` → list public templates
- `client.get_template(template_id)` → get a single template

Need the full API surface? Use the generated low-level client directly:

```python
import ilovevideoeditor_sdk
from ilovevideoeditor_sdk.api.render_api import RenderApi

config = ilovevideoeditor_sdk.Configuration(host="https://api.ilovevideoeditor.com")
config.api_key["ApiKeyAuth"] = "vf_live_xxx"

with ilovevideoeditor_sdk.ApiClient(config) as api_client:
    render_api = RenderApi(api_client)
    # e.g. render_api.estimate_render_cost(...)
```

## Authentication

Create an API key in the [iLoveVideoEditor dashboard](https://ilovevideoeditor.com/dashboard) — keys are prefixed with `vf_live_`. Pass it as `api_key` when constructing the client; the recommended practice is to keep it in an environment variable rather than hardcoding it:

```python
import os
from ilovevideoeditor import iLoveVideoEditorClient

client = iLoveVideoEditorClient(api_key=os.environ["ILOVEVIDEOEDITOR_API_KEY"])
```

## Documentation

- Docs: https://ilovevideoeditor.com/docs
- SDK guides: https://ilovevideoeditor.com/docs/sdks
- PyPI page: https://pypi.org/project/ilovevideoeditor-sdk/

## Other official SDKs

- Node.js/TypeScript: [@ilovevideoeditor/sdk-node](https://www.npmjs.com/package/@ilovevideoeditor/sdk-node) (repo: https://github.com/ilovevideoeditor/sdk-node)
- Ruby: [ilovevideoeditor-sdk](https://rubygems.org/gems/ilovevideoeditor-sdk) (repo: https://github.com/ilovevideoeditor/sdk-ruby)
- PHP: [ilovevideoeditor/sdk](https://packagist.org/packages/ilovevideoeditor/sdk) (repo: https://github.com/ilovevideoeditor/sdk-php)
- Go: [github.com/ilovevideoeditor/sdk-go](https://pkg.go.dev/github.com/ilovevideoeditor/sdk-go) (repo: https://github.com/ilovevideoeditor/sdk-go)

## License

MIT
