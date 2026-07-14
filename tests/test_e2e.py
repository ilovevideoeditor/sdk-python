"""End-to-end tests for the Python SDK against a local Prism mock server."""

import os

import pytest

import ilovevideoeditor_sdk
from ilovevideoeditor import iLoveVideoEditorClient
from ilovevideoeditor_sdk.api.health_api import HealthApi
from ilovevideoeditor_sdk.api.projects_api import ProjectsApi
from ilovevideoeditor_sdk.api.render_api import RenderApi
from ilovevideoeditor_sdk.api.templates_api import TemplatesApi
from ilovevideoeditor_sdk.models.estimate_render_cost_request import EstimateRenderCostRequest
from ilovevideoeditor_sdk.models.queue_render_request import QueueRenderRequest


BASE_URL = os.environ.get("SDK_TEST_BASE_URL", "http://127.0.0.1:4010")
API_KEY = os.environ.get("SDK_TEST_API_KEY", "test-key")
BEARER_TOKEN = os.environ.get("SDK_TEST_BEARER_TOKEN", "test-token")


@pytest.fixture
def config():
    cfg = ilovevideoeditor_sdk.Configuration(host=BASE_URL)
    cfg.api_key["ApiKeyAuth"] = API_KEY
    cfg.access_token = BEARER_TOKEN
    return cfg


@pytest.fixture
def api_client(config):
    return ilovevideoeditor_sdk.ApiClient(config)


def test_health_check(api_client):
    health = HealthApi(api_client)
    status = health.health_check()
    assert isinstance(status.status, str)
    assert len(status.status) > 0


def test_list_templates(api_client):
    templates_api = TemplatesApi(api_client)
    result = templates_api.list_templates()
    assert isinstance(result.templates, list)


def test_queue_render():
    client = iLoveVideoEditorClient(api_key=API_KEY, base_url=BASE_URL)
    video_json = {
        "name": "e2e-test",
        "layers": [
            {"type": "composition", "width": 1920, "height": 1080, "fps": 30}
        ],
    }
    result = client.queue_render(video_json)
    assert result["job_id"]
    assert result["status"]


def test_estimate_render_cost(api_client):
    render_api = RenderApi(api_client)
    video_json = {
        "name": "e2e-test",
        "layers": [
            {"type": "composition", "width": 1920, "height": 1080, "fps": 30}
        ],
    }
    body = EstimateRenderCostRequest(video_json=video_json)
    estimate = render_api.estimate_render_cost(body)
    assert isinstance(estimate.cost, (int, float))
    assert isinstance(estimate.estimated_duration, (int, float))


def test_list_projects(api_client):
    projects_api = ProjectsApi(api_client)
    result = projects_api.list_projects(page=1, limit=10)
    assert isinstance(result.projects, list)
    assert isinstance(result.total, int)
    assert isinstance(result.page, int)
