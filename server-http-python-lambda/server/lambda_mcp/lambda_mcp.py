from lambda_mcp.types import (
    JSONRPCRequest, 
    JSONRPCResponse,
    JSONRPCError,
    InitializeResult,
    ServerInfo,
    Capabilities,
    TextContent,
    ErrorContent
)
import json
import logging
from typing import Optional, Any, Dict, Callable, get_type_hints, List
import inspect
import functools

logger = logging.getLogger(__name__)

class LambdaMCPServer:
    """A class to handle MCP protocol in AWS Lambda"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict] = {}
        self.tool_implementations: Dict[str, Callable] = {}
    
    def tool(self):
        """Decorator to register a function as an MCP tool.
        
        Uses function name, docstring, and type hints to generate the MCP tool schema.
        """
        def decorator(func: Callable):
            # Get function name and convert to camelCase for tool name
            func_name = func.__name__
            tool_name = ''.join([func_name.split('_')[0]] + [word.capitalize() for word in func_name.split('_')[1:]])
            
            # Get docstring and parse into description
            doc = inspect.getdoc(func) or ""
            description = doc.split('\n\n')[0]  # First paragraph is description
            
            # Get type hints
            hints = get_type_hints(func)
            return_type = hints.pop('return', Any)
            
            # Build input schema from type hints and docstring
            properties = {}
            required = []
            
            # Parse docstring for argument descriptions
            arg_descriptions = {}
            if doc:
                lines = doc.split('\n')
                in_args = False
                for line in lines:
                    if line.strip().startswith('Args:'):
                        in_args = True
                        continue
                    if in_args:
                        if not line.strip() or line.strip().startswith('Returns:'):
                            break
                        if ':' in line:
                            arg_name, arg_desc = line.split(':', 1)
                            arg_descriptions[arg_name.strip()] = arg_desc.strip()

            # Build properties from type hints
            for param_name, param_type in hints.items():
                param_schema = {"type": "string"}  # Default to string
                if param_type == int:
                    param_schema["type"] = "integer"
                elif param_type == float:
                    param_schema["type"] = "number"
                elif param_type == bool:
                    param_schema["type"] = "boolean"
                
                if param_name in arg_descriptions:
                    param_schema["description"] = arg_descriptions[param_name]
                    
                properties[param_name] = param_schema
                required.append(param_name)
            
            # Create tool schema
            tool_schema = {
                "name": tool_name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
            
            # Register the tool
            self.tools[tool_name] = tool_schema
            self.tool_implementations[tool_name] = func
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator

    def _create_error_response(self, code: int, message: str, request_id: Optional[str] = None, error_content: Optional[List[Dict]] = None) -> Dict:
        """Create a standardized error response"""
        error = JSONRPCError(code=code, message=message)
        response = JSONRPCResponse(jsonrpc="2.0", id=request_id, error=error, errorContent=error_content)
        
        return {
            "statusCode": self._error_code_to_http_status(code),
            "body": response.model_dump_json(),
            "headers": {
                "Content-Type": "application/json",
                "MCP-Version": "0.6"
            }
        }
    
    def _error_code_to_http_status(self, error_code: int) -> int:
        """Map JSON-RPC error codes to HTTP status codes"""
        error_map = {
            -32700: 400,  # Parse error
            -32600: 400,  # Invalid Request
            -32601: 404,  # Method not found
            -32602: 400,  # Invalid params
            -32603: 500,  # Internal error
        }
        return error_map.get(error_code, 500)
    
    def _create_success_response(self, result: Any, request_id: str) -> Dict:
        """Create a standardized success response"""
        response = JSONRPCResponse(jsonrpc="2.0", id=request_id, result=result)
        return {
            "statusCode": 200,
            "body": response.model_dump_json(),
            "headers": {
                "Content-Type": "application/json",
                "MCP-Version": "0.6"
            }
        }

    def handle_request(self, event: Dict, context: Any) -> Dict:
        """Handle an incoming Lambda request"""
        request_id = None
        
        try:
            # Log the full event for debugging
            logger.debug(f"Received event: {event}")
            
            # Validate content type
            headers = {k.lower(): v for k, v in event.get("headers", {}).items()}
            if headers.get("content-type") != "application/json":
                return self._create_error_response(-32700, "Unsupported Media Type")

            try:
                body = json.loads(event["body"])
                logger.debug(f"Parsed request body: {body}")
                request_id = body.get("id") if isinstance(body, dict) else None
                
                # Check if this is a notification (no id field)
                if isinstance(body, dict) and "id" not in body:
                    logger.debug("Request is a notification")
                    return {
                        "statusCode": 204,
                        "body": "",
                        "headers": {"Content-Type": "application/json", "MCP-Version": "0.6"}
                    }
                    
                # Validate basic JSON-RPC structure
                if not isinstance(body, dict) or body.get("jsonrpc") != "2.0" or "method" not in body:
                    return self._create_error_response(-32700, "Parse error", request_id)
                    
            except json.JSONDecodeError:
                return self._create_error_response(-32700, "Parse error")
            
            # Parse and validate the request
            request = JSONRPCRequest.model_validate(body)
            logger.debug(f"Validated request: {request}")
            
            # Handle initialization request
            if request.method == "initialize":
                logger.info("Handling initialize request")
                result = InitializeResult(
                    protocolVersion="2024-11-05",
                    serverInfo=ServerInfo(name=self.name, version=self.version),
                    capabilities=Capabilities(tools={"list": True, "call": True})
                )
                return self._create_success_response(result.model_dump(), request.id)
                
            # Handle tools/list request
            if request.method == "tools/list":
                logger.info("Handling tools/list request")
                return self._create_success_response({"tools": list(self.tools.values())}, request.id)
            
            # Handle tool calls
            if request.method == "tools/call":
                tool_name = request.params.get("name")
                tool_args = request.params.get("arguments", {})
                
                if tool_name not in self.tools:
                    return self._create_error_response(-32601, f"Tool '{tool_name}' not found", request.id)
                
                try:
                    result = self.tool_implementations[tool_name](**tool_args)
                    content = [TextContent(text=str(result)).model_dump()]
                    return self._create_success_response({"content": content}, request.id)
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    error_content = [ErrorContent(text=str(e)).model_dump()]
                    return self._create_error_response(-32603, f"Error executing tool: {str(e)}", request.id, error_content)

            # Handle unknown methods
            return self._create_error_response(-32601, f"Method not found: {request.method}", request.id)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return self._create_error_response(-32000, str(e), request_id) 