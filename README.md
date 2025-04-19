<<<<<<< HEAD
# Lambda MCP Server Demo (HTTP) 

> This server requires a client that supports HTTP.  There are very few clients that currently support MCP/HTTP, as such there is a client included in this repo. 

This project demonstrates a powerful and developer-friendly way to create serverless [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol) tools using [AWS Lambda](https://aws.amazon.com/lambda/?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code). It showcases how to build a stateless, serverless MCP server with minimal boilerplate and an excellent developer experience.

The included client demonstrates integration with [Amazon Bedrock](https://aws.amazon.com/bedrock/?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code), using the Bedrock Converse API and [Amazon Nova Pro](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) to build an intelligent agent.

## Example

After you import LambdaMCPServer, this is all the code you need:

```Python
from lambda_mcp.lambda_mcp import LambdaMCPServer

# Create the MCP server instance
mcp_server = LambdaMCPServer(name="mcp-lambda-server", version="1.0.0")

@mcp_server.tool()
def say_hello_world() -> int:
    """Say hello world!"""
    return "Hello MCP World!"

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    return mcp_server.handle_request(event, context) 
```

That's it! :) 

## What is it?

This is a proof-of-concept implementation of an MCP server running on AWS Lambda, along with a TypeScript client that demonstrates its functionality. The project consists of two main components:

1. **Lambda MCP Server**: A Python-based serverless implementation that makes it incredibly simple to deploy cloud hosted MCP tools.
2. **TypeScript HTTP Client**: A demonstration client that shows how to interact with the Lambda MCP server using Amazon Bedrock's Converse API _(At the time of writing the TypeScript MCP SDK was one of the only if not THE only SDK to support HTTP)_.

## Example Tools

The server comes with three example tools that demonstrate different use cases:

1. `get_time()`: Returns the current UTC time in ISO format
1. `get_weather(city: str)`: Simulates weather data for a given city
1. `count_s3_buckets()`: Counts [AWS S3](https://aws.amazon.com/s3/?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) buckets in your account

## Getting Started

### Prerequisites

- [AWS Account](https://aws.amazon.com/free/?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) with appropriate permissions
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) installed
- [Node.js and npm](https://nodejs.org/) (for the client)
- [Docker](https://docs.docker.com/get-docker/) (for the client)
- [Python 3.9+](https://www.python.org/downloads/)
- Access to [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) in your AWS account
- [Amazon Nova Pro](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) enabled in your Amazon Bedrock model access settings

### Amazon Bedrock Setup

Before running the client, ensure you have:

1. [Enabled Amazon Bedrock access](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) in your AWS account
2. [Enabled the Amazon Nova Models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) in your Bedrock model access settings
3. Appropriate [IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) to invoke Bedrock APIs

### Server Deployment

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```

1. Navigate to the server directory:
   ```bash
   cd server-http-python-lambda
   ```

1. Deploy using SAM:
   ```bash
   sam build
   sam deploy --guided
   ```

   Note: This deploys an unauthenticated endpoint for demonstration purposes. For production use, implement appropriate authentication using [AWS API Gateway authorizers](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code).

### Client Setup

1. Navigate to the client directory:
   ```bash
   cd client-http-typescript-docker
   ```

1. Run the helper script:
   ```bash
   run-client.sh
   ```

## Adding New Tools

The Lambda MCP Server is designed to make tool creation as simple as possible. Here's how to add a new tool:

1. Open `server/app.py`
2. Add your new tool using the decorator pattern:

```python
@mcp_server.tool()
def my_new_tool(param1: str, param2: int) -> str:
    """Your tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
=======
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
>>>>>>> 403628c3c7f8352646fe09e4925852074fa17026
        
    Returns:
        Description of return value
    """
<<<<<<< HEAD
    # Your tool implementation
    return f"Processed {param1} with value {param2}"
```

That's it! The decorator handles:
- Type validation
- Request parsing
- Response formatting
- Error handling
- MCP Documentation generation

## Notes

- At the time of writing the [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk?tab=readme-ov-file#streamable-http) is one of the few (if only) implementations that support HTTP-based MCP communication.
- For production use, consider adding authentication and authorization using [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

For AWS security best practices, refer to the [AWS Security Documentation](https://docs.aws.amazon.com/security/?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code) and [Amazon Bedrock security best practices](https://docs.aws.amazon.com/bedrock/latest/userguide/security.html?trk=64e03f01-b931-4384-846e-db0ba9fa89f5&sc_channel=code).

## License

This library is licensed under the [MIT-0 License](https://github.com/aws/mit-0). See the LICENSE file.
=======
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
>>>>>>> 403628c3c7f8352646fe09e4925852074fa17026
