"""Setup script for syntechrev-polycodcal package."""

from setuptools import setup, find_packages

setup(
    name="syntechrev-polycodcal",
    version="0.1.0",
    description="Polymathic CodCal - A simple calculator library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SynTechRev",
    url="https://github.com/SynTechRev/SynTechRev-PolyCodCal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "certifi==2025.10.5",
        "charset-normalizer==3.4.3",
        "idna==3.10",
        "numpy==2.3.3",
        "pandas==2.3.3",
        "python-dateutil==2.9.0.post0",
        "pytz==2025.2",
        "requests==2.32.5",
        "six==1.17.0",
        "tzdata==2025.2",
        "urllib3==2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=25.9.0",
            "flake8>=7.3.0",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
