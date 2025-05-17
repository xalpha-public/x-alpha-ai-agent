import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Import wallet_setup from coinbase.py
from coinbase import wallet_setup

app = Flask(__name__)
# Make CORS more permissive for development
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Add a route specifically for OPTIONS preflight requests
@app.route('/ai/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/ai/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200

# Add a basic health check endpoint
@app.route('/ai/')
def health_check():
    return jsonify({"status": "online", "message": "Flask chat API is running"}), 200

# Global variable to hold the initialized agent executor
agent_executor = None

def startup_agent_system():
    """Initializes the agent system by calling wallet_setup."""
    global agent_executor
    global agent_config
    print("Initializing agent system with wallet_setup...")
    try:
        # wallet_setup returns agent_executor and an initial agent_config.
        # We primarily need the agent_executor. The thread_id for conversation
        # will be handled per-request.
        # Using a placeholder thread_id for the initial setup.
        initialized_agent_executor, agent_config = wallet_setup(thread_id="flask_app_initial_setup")
        agent_executor = initialized_agent_executor
        
        if agent_executor:
            print("Agent executor initialized successfully via wallet_setup.")
        else:
            print("FATAL: wallet_setup did not return an agent executor. API chat endpoint will not function.")
            agent_executor = None # Ensure it's None if initialization failed
    except Exception as e:
        print(f"FATAL: Failed to initialize agent system using wallet_setup: {e}")
        import traceback
        traceback.print_exc()
        agent_executor = None

def run_agent(user_input: str, thread_id: str):
    """Runs the agent with the given user input and thread_id for conversation history."""
    global agent_executor
    if not agent_executor:
        # This should ideally be caught by chat_handler's check, but as a safeguard:
        raise RuntimeError("Agent executor is not initialized.")

    # Configuration for the specific agent call, using the provided thread_id
    # This allows the MemorySaver checkpointer in the agent to use the correct conversation history.
    call_specific_config = {"configurable": {"thread_id": thread_id}}
        
    try:
        messages = [HumanMessage(content=user_input)]
        # Invoke the agent executor
        if agent_config:
            response_data = agent_executor.invoke({"messages": messages}, agent_config)
        else:
            response_data = agent_executor.invoke({"messages": messages}, call_specific_config)
        
        # Extract the last message's content, assuming it's the agent's response.
        # For create_react_agent, response_data is typically a dict with a 'messages' key.
        if response_data and "messages" in response_data and response_data["messages"]:
            last_message = response_data["messages"][-1]
            if hasattr(last_message, 'content'):
                return str(last_message.content)
            else:
                # Fallback if content attribute is missing (e.g., if it's not a standard message object)
                print(f"Warning: Last message for thread {thread_id} lacked a 'content' attribute: {last_message}")
                return str(last_message)
        else:
            print(f"Unexpected response structure or empty messages from agent for thread {thread_id}: {response_data}")
            return "Agent processed the request but returned an unexpected response format or no messages."

    except Exception as e:
        print(f"Error during agent invocation for input '{user_input}' in thread '{thread_id}': {e}")
        import traceback
        traceback.print_exc() # Log the full traceback for debugging
        raise # Re-raise the exception to be caught by chat_handler

@app.route('/ai/chat', methods=['POST'])
def chat_handler():
    global agent_executor # Access the global agent_executor
    
    if not agent_executor: # Check if agent_executor is initialized
        return jsonify({"error": "Agent system (agent_executor) is not initialized or failed to load. Check server logs."}), 503

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    user_input = data['message']
    thread_id = data.get('thread_id', str(uuid.uuid4())) 

    try:
        # Call the new run_agent function, passing the user_input and thread_id
        response_content = run_agent(user_input, thread_id)
        
        if response_content is None:
            # This case might occur if run_agent explicitly returns None, though current logic aims to return a string.
            print(f"run_agent returned None for input: {user_input} in thread: {thread_id}")
            return jsonify({"error": "Agent returned an empty or null response.", "thread_id": thread_id}), 500

        return jsonify({"response": response_content, "thread_id": thread_id})

    except Exception as e:
        # Errors raised by run_agent will be caught here
        # The traceback is already printed in run_agent if an exception occurs there
        return jsonify({"error": f"Agent execution failed: {str(e)}", "thread_id": thread_id}), 500

if __name__ == '__main__':
    print("Loading .env variables...")
    load_dotenv() # Ensure .env is loaded before wallet_setup (called by startup_agent_system)
    # Note: The explicit 'from coinbase import run_agent' is removed as run_agent is now defined locally.

    startup_agent_system() # Initialize the agent_executor

    port = int(os.environ.get("FLASK_PORT", 8080))
    print(f"Starting Flask server on port {port}...")
    from waitress import serve
    serve(app, host='0.0.0.0', port=port) 