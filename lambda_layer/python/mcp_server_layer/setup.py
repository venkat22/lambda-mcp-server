from setuptools import setup, find_packages

setup(
    name="mcp_server_layer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.6.0",
        "python-dateutil>=2.8.2"
    ],
    author="Mike GC",
    description="MCP Server Lambda Layer",
    python_requires=">=3.9",
) 