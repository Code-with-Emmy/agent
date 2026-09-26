import os
from dotenv import load_dotenv
import json
import subprocess
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5-turbo"

SYSTEM_PROMPT = """You are a helpful assistant answering questions, writing code, and providing information. You have access to a set of tools that you can use to perform various tasks. Use the tools when appropriate, and provide clear and concise answers to the user's questions. and provide the output of the tools you use in your responses. If you are unsure about how to use a tool, ask for clarification or refer to the tool's documentation. Always prioritize providing accurate and helpful information to the user. and then when you are done, provide a summary of the tools you used and the output of those tools in your final response. If you encounter any errors while using a tool, provide a clear error message and suggest possible solutions or alternatives. Remember to be polite and professional in your responses, and always strive to assist the user to the best of your abilities. and when the user asks you to write code, make sure to provide the code in a code block and explain the code in detail. If the user asks you to write code in a specific programming language, make sure to follow their request and provide the code in that language. If the user asks you to write code for a specific task or problem, make sure to understand the requirements and provide a solution that meets those requirements. If the user asks you to write code that interacts with an API or external service, make sure to provide clear instructions on how to set up and use the API or service, and provide any necessary authentication or configuration details. Always prioritize providing accurate and helpful information to the user, and strive to assist them in achieving their goals. and also act as a code interpreter, and provide the output of the code you write in your responses. If you encounter any errors while executing code, provide a clear error message and suggest possible solutions or alternatives. Remember to be polite and professional in your responses, and always strive to assist the user to the best of your abilities. and when the user asks you to write code, make sure to provide the code in a code block and explain the code in detail. If the user asks you to write code in a specific programming language, make sure to follow their request and provide the code in that language. If the user asks you to write code for a specific task or problem, make sure to understand the requirements and provide a solution that meets those requirements. If the user asks you to write code that interacts with an API or external service, make sure to provide clear instructions on how to set up and use the API or service, and provide any necessary authentication or configuration details. Always prioritize providing accurate and helpful information to the user, and strive to assist them in achieving their goals."""

def get_tools(tool_type: str = None):
    """
    Get a list of tools available in the agent.

    Args:
        tool_type (str, optional): The type of tools to retrieve. If not specified, all tools will be returned.

    Returns:
        list: A list of tools available in the agent.
    """
    # Retrieve the list of tools from the agent
    tools = tracks.get_tools()

    # Filter tools by type if specified
    if tool_type:
        tools = [tool for tool in tools if tool["type"] == tool_type]

    return tools

def run_tool(tool_name: str, tool_input: dict):
    """
    Run a tool with the specified input.

    Args:
        tool_name (str): The name of the tool to run.
        tool_input (dict): The input parameters for the tool.

    Returns:
        dict: The output of the tool.
    """
    # Find the tool by name
    tools = get_tools()
    tool = next((tool for tool in tools if tool["name"] == tool_name), None)

    if not tool:
        return {"error": f"Tool '{tool_name}' not found."}

    # Run the tool and return the output
    try:
        output = subprocess.run(
            [tool["command"], json.dumps(tool_input)],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(output.stdout)
    except subprocess.CalledProcessError as e:
        return {"error": f"Error running tool '{tool_name}': {e.stderr}"}
    if not output.stdout:
        return {"error": f"Tool '{tool_name}' did not produce any output."}

def chat_with_agent(messages):
    """
    Chat with the agent using the specified messages.

    Args:
        messages (list): A list of messages to send to the agent.

    Returns:
        dict: The response from the agent.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
    )
    return response.choices[0].message.content


def main():
    """
    Main function to run the agent in a loop, allowing the user to interact with it.
    """
    messages = []
    while True:
        user_input = input("You: ")
        messages.append({"role": "user", "content": user_input})
        response = chat_with_agent(messages)
        print(f"Agent: {response}")
        messages.append({"role": "assistant", "content": response})

        if __name__ == "__main__":
            main()
            if messages[-1]["content"].lower() in ["exit", "quit"]:
                print("Exiting the agent. Goodbye!")
                break 

def read_file(file_path):
    """
    Read the contents of a file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The contents of the file.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path, content):
    """
    Write content to a file.

    Args:
        file_path (str): The path to the file to write.
        content (str): The content to write to the file.

    Returns:
        str: A message indicating success or failure.
    """
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"


def list_files(directory):
    """
    List the files in a directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list: A list of file names in the directory.
    """
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error listing files in directory: {str(e)}"

def delete_file(file_path):
    """
    Delete a file.

    Args:
        file_path (str): The path to the file to delete.

    Returns:
        str: A message indicating success or failure.
    """
    try:
        os.remove(file_path)
        return f"Successfully deleted {file_path}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

def execute_command(command):
    """
    Execute a shell command.

    Args:
        command (str): The command to execute.

    Returns:
        str: The output of the command or an error message.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing command: {result.stderr}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def get_environment_variable(var_name):
    """
    Get the value of an environment variable.

    Args:
        var_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable or an error message.
    """
    try:
        return os.getenv(var_name, f"Environment variable '{var_name}' not found.")
    except Exception as e:
        return f"Error retrieving environment variable: {str(e)}"

def set_environment_variable(var_name, value):
    """
    Set the value of an environment variable.

    Args:
        var_name (str): The name of the environment variable.
        value (str): The value to set for the environment variable.

    Returns:
        str: A message indicating success or failure.
    """
    try:
        os.environ[var_name] = value
        return f"Successfully set environment variable '{var_name}' to '{value}'"
    except Exception as e:
        return f"Error setting environment variable: {str(e)}"

def get_system_info():
    """
    Get information about the system.

    Returns:
        dict: A dictionary containing system information.
    """
    try:
        return {
            "platform": os.name,
            "current_working_directory": os.getcwd(),
            "user": os.getlogin(),
        }
    except Exception as e:
        return {"error": f"Error retrieving system information: {str(e)}"}

def get_python_version():
    """
    Get the version of Python currently in use.

    Returns:
        str: The Python version.
    """
    try:
        return f"Python version: {os.sys.version}"
    except Exception as e:
        return f"Error retrieving Python version: {str(e)}"

def get_installed_packages():
    """
    Get a list of installed Python packages.

    Returns:
        list: A list of installed packages.
    """
    try:
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.splitlines()
        else:
            return f"Error retrieving installed packages: {result.stderr}"
    except Exception as e:
        return f"Error retrieving installed packages: {str(e)}"

def get_network_info():
    """
    Get information about the network configuration.

    Returns:
        str: The network configuration information or an error message.
    """
    try:
        result = subprocess.run(["ipconfig" if os.name == "nt" else "ifconfig"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving network information: {result.stderr}"
    except Exception as e:
        return f"Error retrieving network information: {str(e)}"

def get_disk_usage():
    """
    Get information about disk usage.

    Returns:
        str: The disk usage information or an error message.
    """
    try:
        result = subprocess.run(["df", "-h"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving disk usage information: {result.stderr}"
    except Exception as e:
        return f"Error retrieving disk usage information: {str(e)}"

def get_memory_usage():
    """
    Get information about memory usage.

    Returns:
        str: The memory usage information or an error message.
    """
    try:
        result = subprocess.run(["free", "-h"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving memory usage information: {result.stderr}"
    except Exception as e:
        return f"Error retrieving memory usage information: {str(e)}"
    
def get_cpu_info():
    """
    Get information about the CPU.

    Returns:
        str: The CPU information or an error message.
    """
    try:
        result = subprocess.run(["lscpu"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving CPU information: {result.stderr}"
    except Exception as e:
        return f"Error retrieving CPU information: {str(e)}"

def get_gpu_info():
    """
    Get information about the GPU.

    Returns:
        str: The GPU information or an error message.
    """
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving GPU information: {result.stderr}"
    except Exception as e:
        return f"Error retrieving GPU information: {str(e)}"

def get_process_list():
    """
    Get a list of running processes.

    Returns:
        str: The list of running processes or an error message.
    """
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving process list: {result.stderr}"
    except Exception as e:
        return f"Error retrieving process list: {str(e)}"

def get_system_logs(log_file_path):
    """
    Get the contents of a system log file.

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        str: The contents of the log file or an error message.
    """
    try:
        with open(log_file_path, "r") as log_file:
            return log_file.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def get_system_uptime():
    """
    Get the system uptime.

    Returns:
        str: The system uptime or an error message.
    """
    try:
        result = subprocess.run(["uptime"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving system uptime: {result.stderr}"
    except Exception as e:
        return f"Error retrieving system uptime: {str(e)}"

def get_system_temperature():
    """
    Get the system temperature.

    Returns:
        str: The system temperature or an error message.
    """
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving system temperature: {result.stderr}"
    except Exception as e:
        return f"Error retrieving system temperature: {str(e)}"

def get_system_power_status():
    """
    Get the system power status.

    Returns:
        str: The system power status or an error message.
    """
    try:
        result = subprocess.run(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error retrieving system power status: {result.stderr}"
    except Exception as e:
        return f"Error retrieving system power status: {str(e)}"