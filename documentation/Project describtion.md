# 🚀 Multiagent Application for Token Swapping with Cookie DAO Data Evaluation & Xtreamly Volatility Optimization

## 🌍 Overview

This project implements a **multiagent framework** 🤖 for user-driven token swaps within the **Cookie DAO** 🍪 ecosystem. Multiple agents collaborate to assist users in making **optimal swap decisions** while navigating **market volatility** 📈. A key feature is the **dynamic agent tool selection** based on the **Xtreamly Volatility 60-minute prediction model** ⏳.

### 🔑 Key Features:

- 🤝 **Multiagent decision-making**: LLM-powered agents analyze market data and provide recommendations.
- 🔄 **Dynamic agent selection**: Adaptive selection of top-performing agents based on real-time market conditions.
- 📊 **Xtreamly Volatility Prediction**: A predictive model optimizes tool selection and execution speed.
- 💰 **Swap management strategy**: Ensures an equally distributed exposure among high-potential tokens.

## ⚡ Chat Execution Strategy Overview

The system follows an **hourly execution policy** 🕒:

1. **Market Analysis** 📉: `xtreamly_volatility()` determines market conditions as **low** or **high** volatility.
2. **Agent Selection** 🎯:
   - Filters out tokens with a market capitalization below **$1M** 💰.
   - Ensures tokens have had trading activity in the last **24 hours** ⏰.
   - Selects only tokens with at least **one holder** 👥.
3. **Multiagent Tools Selection** 🛠️: The LLM agent selects functions based on market conditions.
4. **User Interaction** 💬: Agents provide insights and execute token swaps upon user request.

## 🤖 Multiagent Framework

The multiagent system consists of specialized LLM-driven agents, each fulfilling a unique role in optimizing investment decisions within the **Cookie DAO** 🍪 ecosystem.

- 🏛️ **Group Chat Manager**: Oversees agent collaboration and ensures seamless discussion flow.
- 📈 **Planner**: Identifies investment opportunities, queries the Researcher, and proposes investment strategies.
- 🔍 **Researcher**: Gathers real-time market data, validates potential investments, and executes confirmed trades.
- 🎯 **Executor**: Implements investments as directed, ensuring accurate and efficient execution.
- 🧑‍💻 **Human Proxy**: Serves as the bridge between the user and agents, collecting inputs and providing oversight.

## 🔍 Agent Selection Process

Agents are categorized based on **performance metrics** 📊:

### **1️⃣ Significant Agents**

- 📊 **Mindshare Delta (%)** ≥ 10
- 💰 **Market Cap Delta (%)** ≥ 10
- 📈 **Price Delta (%)** ≥ 10
- 🔄 **Volume 24 Hours Delta (%)** ≥ 10

### **2️⃣ Popular Agents**

- 👥 **Followers Count** ≥ 500
- 🔥 **Average Engagements Count Delta (%)** ≥ 10

### **3️⃣ Top Performing Agents**

- 🏆 Ranked by **Market Cap, Mindshare, and Followers Count**.

### **4️⃣ Volatile Agents**

- ⚡ Ranked using **Price Delta, Market Cap Delta, and Volume 24 Hours Delta**.

### **5️⃣ Stable Agents**

- 🛡️ Ranked by **lowest volatility score**.

### **6️⃣ Undervalued Agents**

- 💎 Sorted by `Average Engagements Count / Market Cap`.

### **7️⃣ Newly Active Agents**

- 🚀 **Holders Count Delta (%)** > 10
- 🔄 **Volume 24 Hours Delta (%)** > 10

## 🛠️ Multiagent Tool Selection Process

### **1️⃣ Fetching Market Volatility State**

- `xtreamly_volatility()` determines volatility.
- Market is classified as **low** or **high volatility** ⚖️ based on a threshold (e.g., `0.003897`).

### **2️⃣ Adaptive Agent Selection Based on Market Conditions**

#### **📉 Low Volatility Strategy**

Prioritizes **stability** and **undervaluation** 📊:

- 🏆 `agents_significant()` - Identifies influential agents.
- 🔥 `agents_popular()` - Detects agents driving sentiment.
- ⚡ `agents_volatile()` - Identifies aggressive opportunities.
- 💎 `agents_undervalued()` - Highlights safe investment choices.

**Exposure to underperforming agents is reduced, and funds are reallocated to the top agents.**

#### **📈 High Volatility Strategy**

Focuses on **maximizing returns** from market fluctuations 📉📈:

- 🏆 `agents_significant()` - Identifies leading influencers.
- 🔥 `agents_popular()` - Highlights sentiment-driven agents.
- 🛡️ `agents_stable()` - Provides defensive options.
- 🚀 `agents_newly_active()` - Detects recent high-engagement agents.

**User selects top agents and sets investment volume.**

## 🔄 Swap Execution

Token swaps are executed on **user request** 🏦:

```python
def invest(
  agentName: Annotated[str, "agentName"],
  volume: Annotated[float, "100.0"]
) -> str:
```

## 🚀 Xtreamly Data Engineering Process for Enhanced UX

To ensure optimal performance and user experience, **Xtreamly** streams **Cookie DAO data** at **15-minute intervals** ⏳, storing it in **Google Cloud BigQuery** ☁️.

Data loading is handled via API calls:

```bash
@app.post("/load_data")
def load():
  load_data_cookiedao()
  return "Loaded Cookie DAO data into BQ"
```

## 🔮 Future Enhancements

- 📢 **Social Media Sentiment Analysis**: OpenAI models to detect influencer-driven trends.
- 🤖 **Reinforcement Learning**: Dynamic optimization of agent selection.
- 📉 **Advanced Volatility Prediction**: Improved ETH price correlation models.
- 🏦 **Expanded Agent Pool**: More specialized agents for granular decision-making.
- 🔎 **Enhanced Cookie DAO Token Evaluation**: New volatility-based investment strategies.

## 📚 References

### 🍪 **Cookie DAO**

- 📄 [Cookie DAO Documentation](https://docs.cookie.fun/#/)
- 📑 [Cookie DAO Notion](https://cookiedao.notion.site/Cookie-DeFAI-Hackathon-17ddcd6f6625800dab49d8fb103ecc48)
- 🎙️ [Cookie DAO Discord](https://discord.com/channels/994904272489680917/@home)

### 🤖 **Multiagent Framework Systems**

Multi-agent LLMs involve **specialized language models collaborating** to solve complex tasks. This distributed approach enhances **accuracy, efficiency, and adaptability** 🏆.

In a multi-agent system, a user provides a high-level task, which is broken down into subtasks assigned to specialized agents. Each agent processes its task using an LLM, executes actions, and shares insights with other agents to achieve a collective goal.

We have selected **AutoGen** 🔄 as our framework due to its:

- 📡 **Flexible API** for defining agents and multi-agent communication.
- 🧠 **Integration with human inputs**, enabling AI-human collaboration.
- 🛠️ **Streamlined workflows** with built-in utilities like caching, API unification, and error handling.

Other frameworks such as LangChain, LangGraph, CrewAI, and AutoGPT also offer robust features. However, AutoGen stands out for its advanced capabilities in building complex, scalable multi-agent systems with an improved user experience.

### 🔮 **Xtreamly Volatility Prediction**

Full documentation available at **AI Volatility by Xtreamly.pdf** whitepaper 📑.
