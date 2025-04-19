import logging
from datetime import datetime, UTC
import random
from mcp_server.lambda_mcp import LambdaMCPServer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = LambdaMCPServer(name="Lambda MCP Server")

@mcp.tool()
def get_time() -> str:
    """Get the current UTC time in ISO format."""
    return datetime.now(UTC).isoformat()

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        A string describing the weather
    """
    temp = random.randint(15, 35)
    return f"The temperature in {city} is {temp}°C"

def lambda_handler(event, context):
    """AWS Lambda handler for MCP requests."""
    return mcp.handle_request(event, context)
