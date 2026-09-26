import chatgpt_tool_hub as cth
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# I want to read a file, but I don't want to read it directly. I want to use a tool to read the file for me. I want to use the read_file tool to read the file
# def get_tools(tool_type: str = None):
#     """
#     Get a list of tools available in the agent.

#     Args:
#         tool_type (str, optional): The type of tools to retrieve. If not specified, all tools will be returned.

#     Returns:
#         list: A list of tools available in the agent.
#     """
#     # Retrieve the list of tools from the agent
#     tools = cth.get_tools()

#     # Filter tools by type if specified
#     if tool_type:
#         tools = [tool for tool in tools if tool["type"] == tool_type]

#     return tools
import jeson

# Lets define a tool to read a file. The tool will take a file path as input and return the contents of the file. If the file is a JSON file, it will return the parsed JSON object. If the file is not found or cannot be read, it will return an error message.
def read_file(file_path):
    """
    Read the contents of a file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The contents of the file.
    """
    # with open(file_path, "r", encoding="utf-8") as file:
    #     return file.read()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read(
                encoding="utf-8"
            )
    except Exception as e:
        return f"Error reading file: {file_path}. Exception: {str(e)}"
        elseif file_path.endswith(".json"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                if isinstance(e, json.JSONDecodeError):
                    return f"Error decoding JSON file: {file_path}. Exception: {str(e)}"
                else:
                    return f"Error reading file: {file_path}. Exception: {str(e)}"

# TOOL_READ_FILE = cth.Tool(
#     name="read_file",
#     description="Read the contents of a file.",
#     parameters={
#         "type": "object",
#         "properties": {
#             "file_path": {
#                 "type": "string",
#                 "description": "The path to the file to read.",
#             },
#         },
#         "required": ["file_path"],
#     },
#     func=read_file,
# )

# Define the tool schema for the read_file tool
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "description": "Read the contents of a file.",
            "name": "read_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read.",
                    }
                },
                "required": ["file_path"]
            }
        },
        "required": ["file_path"],
    }
]

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# The main loop to interact with the model and handle tool calls
while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOL_SCHEMAS,
        # functions=TOOL_SCHEMAS,
        # function_call="auto",
    )
    message = response.choices[0].message
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = message["function_call"]["arguments"]
        if function_name == "read_file":
            file_path = function_args.get("file_path")
            if file_path:
                try:
                    file_contents = read_file(file_path)
                    messages.append({"role": "assistant", "content": f"File contents:\n{file_contents}"})
                except Exception as e:
                    messages.append({"role": "assistant", "content": f"Error reading file: {str(e)}"})
            else:
                messages.append({"role": "assistant", "content": "No file path provided."})
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    # No tool calls in the message, print the content and break the loop
    # No more tool calls mean the model is done and gives us a normal response, so we can print it and break the loop
    if not message.tool_calls:
        print(message.content)
        break

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function_call.arguments)
        print(f"I want to read_file: {tool_call.function_call.name} do you want to read this? {args}")
        
        result = read_file(args.get("file_path"))

        messages.append({"role": "assistant", "content": f"Result of the file: {result}", "tool_call": tool_call})
        print(f"Result of reading the file: {result}")

        tool_name = tool_call["name"]
        tool_args = tool_call["arguments"]
        if tool_name == "read_file":
            file_path = tool_args.get("file_path")
            if file_path:
                try:
                    file_contents = read_file(file_path)
                    messages.append({"role": "assistant", "content": f"File contents:\n{file_contents}"})
                except Exception as e:
                    messages.append({"role": "assistant", "content": f"Error reading file: {str(e)}"})
            else:
                messages.append({"role": "assistant", "content": "No file path provided."})

    if not response.choices[0].message.content:
        break
print("No more content from the model. Exiting...")