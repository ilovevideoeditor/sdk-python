from pathlib import Path

from setuptools import find_packages, setup

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="ilovevideoeditor-sdk",
    version="1.0.2",
    description=(
        "Official Python SDK for the iLoveVideoEditor cloud video rendering API "
        "— render videos programmatically from JSON scene descriptions and templates"
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author="iLoveVideoEditor",
    author_email="contact@ilovevideoeditor.com",
    url="https://ilovevideoeditor.com",
    project_urls={
        "Documentation": "https://ilovevideoeditor.com/docs",
        "SDK guides": "https://ilovevideoeditor.com/docs/sdks",
        "Source": "https://github.com/ilovevideoeditor/sdk-python",
        "Bug Tracker": "https://github.com/ilovevideoeditor/sdk-python/issues",
        "Homepage": "https://ilovevideoeditor.com",
        "Changelog": "https://github.com/ilovevideoeditor/sdk-python/blob/master/CHANGELOG.md",
    },
    license="MIT",
    keywords="video rendering api video-generation programmatic-video video-editing sdk ilovevideoeditor",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "ilovevideoeditor": ["py.typed"],
        "ilovevideoeditor_sdk": ["py.typed"],
    },
    python_requires=">=3.10",
    install_requires=[
        "urllib3>=1.25.3",
        "python-dateutil>=2.8.2",
        "pydantic>=2",
        "typing-extensions>=4.7.1",
    ],
)
