from setuptools import setup, find_packages

setup(
    name="mcp-zotero",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.6.0",
        "pyzotero>=1.5.18",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.2",
    ],
    entry_points={
        "console_scripts": [
            "mcp-zotero=src.server:main",
        ],
    },
    description="MCP integration for Zotero",
    author="",
    license="ISC",
) 