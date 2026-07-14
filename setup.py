from setuptools import setup, find_packages

setup(
    name="ilovevideoeditor-sdk",
    version="1.0.0",
    description="Official Python SDK for iLoveVideoEditor — cloud video rendering API",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "urllib3>=1.25.3",
        "python-dateutil>=2.8.2",
        "pydantic>=2",
        "typing-extensions>=4.7.1",
    ],
)
