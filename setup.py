from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() if fh else ""

setup(
    name="PyOBD",
    version="0.3.0",
    description="BYMA Market Data Library - Open Data API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Franco Lamas, Nacho Herrera, St1tch',
    author_email="francomlamas@gmail.com",
    url="https://github.com/franco-lamas/PyOBD",
    packages=find_packages(exclude=["tests", "scripts", "docs"]),
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "urllib3>=2.0.0",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
    },
    python_requires=">=3.10",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
