from mcp_server.lambda_mcp import LambdaMCPServer
from datetime import datetime, UTC
import random

# Create the MCP server instance
mcp_server = LambdaMCPServer(name="mcp-lambda-server", version="1.0.0")

@mcp_server.tool()
def get_time() -> str:
    """Get the current UTC time in ISO format."""
    return datetime.now(UTC).isoformat()

@mcp_server.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        A string describing the weather
    """
    temp = random.randint(15, 35)
    return f"The temperature in {city} is {temp}°C"

@mcp_server.tool()
def hello_world(name: str = "World") -> str:
    """A simple hello world tool.
    
    Args:
        name: Name to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}!"

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    return mcp_server.handle_request(event, context) 