import os
import subprocess
import uvicorn


def start():
    proxy_headers = os.getenv("KC_PROXY_HEADERS") is not None
    uvicorn.run(
        "be_task_ca.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        proxy_headers=proxy_headers,
    )


def auto_format():
    subprocess.call(["black", "be_task_ca"])


def run_linter():
    subprocess.call(["flake8", "be_task_ca"])


def run_tests():
    subprocess.call(["pytest"])


def create_dependency_graph():
    subprocess.call(["pydeps", "be_task_ca", "--cluster"])


def check_types():
    subprocess.call(["mypy", "be_task_ca"])
