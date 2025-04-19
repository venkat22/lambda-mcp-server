# MCP Lambda Server

A serverless implementation of an MCP (Model Control Protocol) server using AWS Lambda and API Gateway. This server provides a scalable, serverless backend for handling MCP requests through HTTP endpoints.

> TESTED: With MCP client written in TypeScript using `StreamableHTTPClientTransport` from `@modelcontextprotocol/sdk/client/streamableHttp.js`, as this was the only available HTTP client at the time.

## Overview

This project implements an MCP-compliant server that runs on AWS Lambda, exposing its functionality through API Gateway. It uses a Python MCP framework to handle requests and provides several example tools that can be called through the MCP protocol.

### Features

- Serverless architecture using AWS Lambda and API Gateway
- MCP-compliant tool handling
- Lambda layer core MCP functionality
- Example tools including:
  - Current time retrieval
  - Weather information (mock data)
  - Hello world greeting

## Prerequisites

- Python 3.12
- AWS CLI configured with appropriate credentials
- AWS SAM CLI
- An AWS account with permissions to create Lambda functions and API Gateway resources

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd mcp_lambda_server
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies
```

## Deployment

The project uses AWS SAM for deployment. To deploy:

1. Build the SAM application:
```bash
sam build
```

2. Deploy to AWS:
```bash
sam deploy --guided  # First time deployment
sam deploy  # Subsequent deployments
```

After deployment, the API endpoint URL will be displayed in the outputs.

## Project Structure

- `function/` - Contains the Lambda function code
  - `mcp_function/app.py` - Main Lambda handler and MCP tools implementation
- `lambda_layer/` - Contains dependencies for the Lambda layer
- `events/` - Sample event payloads for testing
- `template.yaml` - SAM template defining AWS resources
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

## Available Tools

### 1. get_time()
Returns the current UTC time in ISO format.

### 2. get_weather(city: str)
Returns simulated weather information for the specified city.

### 3. hello_world(name: str = "World")
Returns a greeting message with the specified name.

## Development

### Adding New Tools

To add new tools to the server, modify `function/mcp_function/app.py`:

1. Import any required dependencies
2. Use the `@mcp_server.tool()` decorator to register new tools
3. Implement the tool function with appropriate type hints and docstrings

Example:
```python
@mcp_server.tool()
def my_new_tool(param: str) -> str:
    """Tool description.
    
    Args:
        param: Parameter description
        
    Returns:
        Description of return value
    """
    return f"Result: {param}"
```

## Configuration

The server configuration is managed through the following files:

- `template.yaml` - AWS resource configuration
- `samconfig.toml` - SAM CLI configuration
- `.envrc` - Local environment configuration (if using direnv)

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 
