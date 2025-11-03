#!/usr/bin/env python3
"""
SigmaRecon Setup Script
The Ultimate Subdomain Enumeration Tool for 2026
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="sigmarecon",
    version="1.0.0",
    author="El3aref",
    author_email="",
    description="The Ultimate Subdomain Enumeration Tool for 2026",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/El3aref/SigmaRecon",
    project_urls={
        "Bug Reports": "https://github.com/El3aref/SigmaRecon/issues",
        "Source": "https://github.com/El3aref/SigmaRecon",
        "Documentation": "https://github.com/El3aref/SigmaRecon/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docker": [
            "docker>=6.0.0",
            "docker-compose>=1.29.0",
        ],
        "cloud": [
            "boto3>=1.26.0",
            "google-cloud-storage>=2.7.0",
            "azure-storage-blob>=12.14.0",
        ],
        "all": [
            "pytest>=6.0",
            "pytest-asyncio>=0.21.0", 
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
            "docker>=6.0.0",
            "docker-compose>=1.29.0",
            "boto3>=1.26.0",
            "google-cloud-storage>=2.7.0",
            "azure-storage-blob>=12.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sigma=sigmarecon.main:main",
            "sigmarecon=sigmarecon.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sigmarecon": [
            "config/examples/*.yml",
            "config/examples/*.yaml",
            "logging/config*.yaml",
        ],
    },
    zip_safe=False,
    keywords="subdomain enumeration, reconnaissance, cybersecurity, bug bounty, penetration testing, dns, certificates",
)