# Xtreamly Agent

Welcome to the Xtreamly AI Agent.
The first super intelligent automated trading DeFi Agent.

This agent leverages Xtreamly's unique volatility predictions and Cookie DAO's market sentiment analysis to perform high yielding trading strategies.

## Architecture

![architecture.png](architecture.png)

## 🛠 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Xtreamly-Team/xtreamly-agent.git
   ```

   ```bash
   cd <repository-folder>
   ```

   And checkout to agenting branch:

   ```bash
   git checkout autogen
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Optional: Configure environment variables in a `.env` file (if needed for additional customizations).

## 🚀 Usage

1. Start the development server:

   ```bash
   python main.py
   ```

   By default, the server runs on port `8080`. This can be customized using the `PORT` environment variable.

2. Access the API in your browser or API testing tool at:

   ```
   http://localhost:8080
   ```

## ⚙️ Configuration

- **CORS Middleware:** Configured to allow specific origins (e.g., `localhost` on common development ports).
- **Environment Variables:** You need to set the `.env` variables to run data fetching:
  - OPENAI_API_KEY
  - FIRECRAWL_API_KEY
  - COOKIE_DAO_API

## 💻 Set Up Environment with Anaconda

Follow these steps to set up your development environment using Anaconda:

1. **Check Existing Environments**

   ```bash
   conda env list
   ```

2. **Create a New Environment**

   Create a new environment with Python 3.11.3:

   ```bash
   conda create -n xtreamly-agent python=3.11.3
   ```

3. **Activate the Environment**

   ```bash
   conda activate xtreamly-agent
   ```

4. **Install Dependencies**

   Use `pip` to install the dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. **Install Spyder Kernels (Optional)**

   If you are using Spyder IDE, install the required version of Spyder kernels:

   ```bash
   conda install spyder-kernels==2.4.4
   ```

6. **Build Docker Image**

   Build a Docker image for the application:

   ```bash
   docker build -t fastapi .
   ```

Your Anaconda environment is now set up, and you can proceed to run or develop the application.

## Knowledge

- https://www.youtube.com/watch?v=dW-qr_ntOgc&t=173s
- https://fastapi.tiangolo.com/advanced/websockets/
