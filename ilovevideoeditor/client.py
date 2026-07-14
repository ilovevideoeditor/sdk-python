"""High-level iLoveVideoEditor client with polling and friendly method names."""

import time
from datetime import datetime
from typing import Callable, Optional

import ilovevideoeditor_sdk
from ilovevideoeditor_sdk.api.render_api import RenderApi
from ilovevideoeditor_sdk.api.templates_api import TemplatesApi
from ilovevideoeditor_sdk.models.queue_render_request import QueueRenderRequest
from ilovevideoeditor_sdk.models.render_job import RenderJob
from ilovevideoeditor_sdk.rest import ApiException


class iLoveVideoEditorClient:
    """A thin, ergonomic wrapper over the auto-generated OpenAPI client.

    Usage:
        client = iLoveVideoEditorClient(api_key="vf_live_xxx")
        result = client.render({"name": "Hello", "layers": [...]})
        print(result.download_url)
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.ilovevideoeditor.com",
    ):
        if not api_key:
            raise ValueError("api_key is required")

        self._config = ilovevideoeditor_sdk.Configuration(host=base_url)
        self._config.api_key["ApiKeyAuth"] = api_key

        self._api_client = ilovevideoeditor_sdk.ApiClient(self._config)
        self._render = RenderApi(self._api_client)
        self._templates = TemplatesApi(self._api_client)

    @staticmethod
    def _progress_percent(progress: object) -> float:
        """Normalize the API progress payload to a percent number.

        The API returns progress as an object ({done, total, percent});
        older jobs may return a bare number or nothing at all.
        """
        if progress is None:
            return 0.0
        if isinstance(progress, (int, float)):
            return float(progress)
        percent = getattr(progress, "percent", None)
        return float(percent) if percent is not None else 0.0

    def _to_result(self, status: RenderJob) -> "RenderResult":
        return RenderResult(
            job_id=str(status.job_id),
            status=status.status,
            progress=self._progress_percent(status.progress),
            url=status.url,
            error=status.error,
            created_at=status.created_at,
            completed_at=status.completed_at,
        )

    def queue_render(
        self,
        video_json: dict,
    ) -> dict:
        """Submit a VideoJSON payload and return the queued job ID."""
        body = QueueRenderRequest(video_json=video_json)
        queued = self._render.queue_render(body)
        return {"job_id": str(queued.job_id), "status": queued.status}

    def render(
        self,
        video_json: dict,
        *,
        poll_interval: float = 2.0,
        max_wait: float = 300.0,
        on_progress: Optional[Callable[[str, float], None]] = None,
    ) -> "RenderResult":
        """Submit a VideoJSON payload and block until the render finishes.

        Args:
            video_json: The VideoJSON scene definition.
            poll_interval: Seconds between status polls.
            max_wait: Maximum seconds to wait before raising TimeoutError.
            on_progress: Optional callback(status, progress_percent).

        Returns:
            RenderResult with job_id, status, download_url, etc.
        """
        body = QueueRenderRequest(video_json=video_json)
        queued = self._render.queue_render(body)
        job_id = str(queued.job_id)

        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            status = self._render.get_render_status(job_id)
            if on_progress:
                on_progress(status.status, self._progress_percent(status.progress))

            if status.status == "completed":
                refresh = self._render.refresh_render_url(job_id)
                return RenderResult(
                    job_id=job_id,
                    status=status.status,
                    progress=self._progress_percent(status.progress),
                    url=status.url,
                    download_url=refresh.download_url,
                    error=status.error,
                    created_at=status.created_at,
                    completed_at=status.completed_at,
                )

            if status.status == "failed":
                return self._to_result(status)

            time.sleep(poll_interval)

        raise TimeoutError(f"Render {job_id} did not complete within {max_wait}s")

    def get_render(self, job_id: str) -> "RenderResult":
        """Fetch the current status of a render job."""
        status = self._render.get_render_status(job_id)
        return self._to_result(status)

    def refresh_url(self, job_id: str) -> str:
        """Refresh and return the download URL for a completed render."""
        result = self._render.refresh_render_url(job_id)
        return result.download_url

    def list_templates(self) -> list:
        """List all public templates."""
        return self._templates.list_templates().templates

    def get_template(self, template_id: str) -> dict:
        """Get a single template by ID."""
        return self._templates.get_template(template_id).template


class RenderResult:
    """Convenience container for a render job result."""

    def __init__(
        self,
        *,
        job_id: str,
        status: str,
        progress: float = 0.0,
        url: Optional[str] = None,
        download_url: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ):
        self.job_id = job_id
        self.status = status
        self.progress = progress
        self.url = url
        self.download_url = download_url
        self.error = error
        self.created_at = created_at
        self.completed_at = completed_at

    def __repr__(self) -> str:
        error_part = f' error="{self.error}"' if self.error else ""
        return (
            f"<RenderResult id={self.job_id} status={self.status} "
            f"progress={self.progress}%>{error_part}>"
        )
