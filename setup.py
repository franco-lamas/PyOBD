from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() if fh else ""

setup(
    name="PyOBD",
    version="0.1.0",
    description="BYMA Market Data Library - Open Data API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NEST",
    url="https://gitlab.dlnc.duckdns.org/st1tch_bl/pyobd",
    packages=find_packages(exclude=["tests", "scripts", "docs"]),
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "urllib3>=1.26.0",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
