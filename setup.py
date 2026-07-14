from pathlib import Path

from setuptools import find_packages, setup

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="ilovevideoeditor-sdk",
    version="1.0.0",
    description="Official Python SDK for iLoveVideoEditor — cloud video rendering API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="iLoveVideoEditor",
    author_email="contact@ilovevideoeditor.com",
    url="https://ilovevideoeditor.com",
    project_urls={
        "Documentation": "https://ilovevideoeditor.com/docs",
        "Source": "https://github.com/ilovevideoeditor/sdk-python",
        "Bug Tracker": "https://github.com/ilovevideoeditor/sdk-python/issues",
    },
    license="MIT",
    keywords=["video", "video-rendering", "video-api", "ilovevideoeditor", "sdk"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.10",
    install_requires=[
        "urllib3>=1.25.3",
        "python-dateutil>=2.8.2",
        "pydantic>=2",
        "typing-extensions>=4.7.1",
    ],
)
