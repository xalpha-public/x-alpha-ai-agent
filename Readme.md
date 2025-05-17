# X-Alpha: Crypto Agent API

## 1. Overview

This project provides the backend API for an AI-powered agent designed to interact with Ethereum-based blockchains. It serves as a core component for a larger X-ALPHA's larger vision to simplify investments and reduce, enabling features that require on-chain data access and transaction capabilities.

The agent is built using Python, leveraging:
*   **Coinbase AgentKit** to provide tools for on-chain interactions through an `EthAccountWalletProvider`.
*   **Google's Gemini (gemini-2.0-flash)** for language understanding and generation.
*   **Langchain and LangGraph** for structuring the agent and managing conversational flow with memory.
*   **Flask** to expose the agent's capabilities via a simple REST API.

The system securely manages an Ethereum wallet, allowing the agent to perform actions like querying token balances, interacting with smart contracts (e.g., Uniswap), and retrieving blockchain data.

## 2. Features

*   **AI Chat Agent:** Interactive chat endpoint (`/ai/chat`) powered by Google's Gemini (gemini-2.0-flash model) via Langchain.
*   **Conversational Memory:** Maintains context across multiple interactions within the same conversation using a `thread_id` managed by LangGraph's `MemorySaver`.
*   **On-Chain Interaction via Coinbase AgentKit:**
    *   **Wallet Management:** Securely manages an Ethereum wallet (loaded from private key, file, or newly generated) using `EthAccountWalletProvider`.
    *   **Action Providers:** Equipped with tools for interacting with:
        *   ERC20 tokens (`erc20_action_provider`)
        *   Pyth Network oracles (`pyth_action_provider`)
        *   Core wallet functions (`wallet_action_provider`)
        *   Wrapped Ether (WETH) (`weth_action_provider`)
        *   Uniswap (`uniswap_action_provider`)
*   **Flask-based API:**
    *   Endpoint for chat: `POST /ai/chat`
    *   Health check endpoint: `GET /ai/`
*   **CORS Enabled:** Configured for permissive CORS, suitable for development.
*   **Environment-Driven Configuration:** Key settings (API keys, RPC URLs, etc.) are managed through environment variables.

## 3. Tech Stack

*   **Backend Framework:** Flask
*   **AI/LLM Framework:** Langchain, LangGraph
*   **LLM Provider:** Google Generative AI (Gemini)
*   **Blockchain Interaction:** Coinbase AgentKit, web3.py
*   **Wallet Management:** EthAccountWalletProvider (from Coinbase AgentKit)
*   **Environment Management:** python-dotenv
*   **WSGI Server:** Waitress
*   **Programming Language:** Python 3.10+

## 4. Setup and Installation

**Prerequisites:**
*   Python 3.10 or higher
*   Access to an Ethereum RPC URL (e.g., Infura, Alchemy, or a local node)

**Steps:**

1.  **Clone the Repository (if applicable):**
    ```bash
    # git clone <repository_url>
    # cd x-alpha-agent
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory of the project by copying the `.env.example` file:
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file with your specific configurations:
    ```env
    # Google API Key for Gemini LLM
    GOOGLE_API_KEY="your_google_api_key"

    # Ethereum Wallet Private Key (optional, will be generated if not provided)
    # IMPORTANT: Keep this secret and secure. Do not commit it to version control.
    PRIVATE_KEY="your_0x_prefixed_private_key"

    # Ethereum Network Chain ID (e.g., 1 for Mainnet, 11155111 for Sepolia, 8453 for Base)
    # Default is 8453 as per coinbase.py
    CHAIN_ID="8453"

    # Ethereum RPC Provider URL
    PROVIDER_URL="your_ethereum_rpc_url"

    # Flask Server Port (optional, defaults to 8080)
    FLASK_PORT="8080"
    ```

## 5. Running the Application

Once the setup is complete, you can run the Flask application:

```bash
python demo_app.py
```

The server will start, typically on `http://0.0.0.0:8080` (or the port specified in `FLASK_PORT`). You will see log messages indicating that the agent system is being initialized and the server is running.

Example output:
```
Loading .env variables...
Initializing agent system with wallet_setup...
RPC URL: your_ethereum_rpc_url
Wallet data saved to wallet_data_8453.txt
Agent executor initialized successfully via wallet_setup.
Starting Flask server on port 8080...
Serving on http://0.0.0.0:8080
```

## 6. API Endpoints

*   **Health Check:**
    *   `GET /ai/`
    *   Description: Verifies that the API is running.
    *   Response:
        ```json
        {
            "status": "online",
            "message": "Flask chat API is running"
        }
        ```

*   **Chat with Agent:**
    *   `POST /ai/chat`
    *   Description: Sends a message to the AI agent and receives a response. Maintains conversation context using `thread_id`.
    *   Request Body (JSON):
        ```json
        {
            "message": "Your query for the agent",
            "thread_id": "optional_unique_string_for_conversation_tracking"
        }
        ```
        If `thread_id` is not provided, a new one will be generated.
    *   Success Response (JSON):
        ```json
        {
            "response": "Agent's response content",
            "thread_id": "used_or_generated_thread_id"
        }
        ```
    *   Error Response (JSON):
        ```json
        {
            "error": "Error message detailing the issue",
            "thread_id": "used_or_generated_thread_id"
        }
        ```
        Status codes `400` (Bad Request), `500` (Internal Server Error), or `503` (Service Unavailable) may be returned in case of errors.

*   **OPTIONS Preflight Requests:**
    *   `OPTIONS /ai/`
    *   `OPTIONS /ai/<path:path>`
    *   Description: Handles CORS preflight requests. Standard for cross-origin API access.

## 7. Wallet Management

The application uses `coinbase.py` (specifically the `wallet_setup` function) to manage an Ethereum wallet. The private key is sourced with the following priority:
1.  From the `PRIVATE_KEY` environment variable.
2.  From a local file named `wallet_data_<CHAIN_ID>.txt` (e.g., `wallet_data_8453.txt` if `CHAIN_ID` is 8453).
3.  If neither is found, a new Ethereum account is generated, and its private key and chain ID are saved to `wallet_data_<CHAIN_ID>.txt` for persistence across sessions.

**Security Note:** The `wallet_data_*.txt` file contains the private key. Ensure this file is kept secure and is included in your `.gitignore` if you are using version control.

## 8. Future Development (Project Vision)

*   Develop the full marketplace UI/UX for Investors and Crypto Projects for analysis and trading.
*   Expand agent capabilities with more specialized tools for financial analysis, project vetting, and market research using XALPHA's APIS.

This README provides a guide to understanding, setting up, and running the current AI agent API component of the larger marketplace application.
This is just a demo app and the agent's capabilities can be further extended. The live version might differ based on the features implemented on https://x-alpha.ai
