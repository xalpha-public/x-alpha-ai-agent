# Crypto VC & Project Marketplace Agent API

## 1. Overview

This project is the backend API for a marketplace application designed to connect Venture Capitalists (VCs) with crypto utility projects. The platform aims to provide comprehensive details for both VCs and projects, enabling VCs to conduct thorough research and projects to find relevant VCs in their domain. A matchmaking feature is also envisioned to facilitate connections.

This component specifically provides an AI-powered chat interface, allowing users to interact with an agent capable of performing on-chain actions and queries via the Coinbase AgentKit and Langchain.

## 2. Features

*   **AI Chat Agent:** Interactive chat endpoint (`/ai/chat`) powered by Google's Generative AI (Gemini).
*   **On-Chain Interaction:** The agent can interact with Ethereum-based blockchains (e.g., send transactions, query data, interact with contracts) using a configured wallet.
*   **Wallet Management:** Securely manages an Ethereum wallet, either by using a provided private key, loading from a file, or generating a new one.
*   **Extensible Agent Capabilities:** Leverages Coinbase AgentKit and Langchain for integrating various tools and action providers (e.g., ERC20, Pyth, Uniswap).
*   **Flask-based API:** Built with Flask, providing a robust and simple web server.
*   **CORS Enabled:** Configured for permissive CORS settings, suitable for development environments.
*   **Health Check:** Basic health check endpoint (`/ai/`) to verify API status.

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

The application uses `coinbase.py` to manage an Ethereum wallet:
*   It first checks for a `PRIVATE_KEY` in the `.env` file.
*   If not found, it attempts to load a wallet from a file named `wallet_data_<CHAIN_ID>.txt` (e.g., `wallet_data_8453.txt`).
*   If no existing wallet is found, a new Ethereum account is generated, and its private key is saved to `wallet_data_<CHAIN_ID>.txt` for persistence across sessions.
*   **Security Note:** The generated `wallet_data_*.txt` file contains the private key. Ensure this file is kept secure and is included in your `.gitignore` if you are using version control.

## 8. Future Development (Project Vision)

*   Develop the full marketplace UI/UX for Investors and Crypto Projects for analysis and trading.
*   Expand agent capabilities with more specialized tools for financial analysis, project vetting, and market research using XALPHA's APIS.

This README provides a guide to understanding, setting up, and running the current AI agent API component of the larger marketplace application.
This is just a demo app and can vary from the actual integration on https://x-alpha.ai
