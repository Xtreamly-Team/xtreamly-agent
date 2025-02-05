# Cookie DAO Policy for Following Agents on Social and Trading Impact

## Overview

Our policy for following agents is based on an **xtreamly volatility 60-minute prediction model**. The decision-making process is driven by a **Large Language Model (LLM) agent**, which selects the best agents (tokens) to apply exposure to, depending on the defined market state.

The LLM agent evaluates different tools and autonomously determines the top 10 agents to follow at any given time, ensuring an equally distributed exposure among them. This approach follows a **portfolio management strategy** to optimize performance.

For more details, refer to:

- [Cookie Docs](https://docs.cookie.fun/#/)
- [Cookie DAO Notion](https://cookiedao.notion.site/Cookie-DeFAI-Hackathon-17ddcd6f6625800dab49d8fb103ecc48)
- [Cookie DAO Discord](https://discord.com/channels/994904272489680917/@home)

---

## Selection Process

The LLM agent makes selections based on market conditions, categorized as **low volatility** and **high volatility**, and applies different strategies accordingly.

### **1. Fetching Market Volatility State**

- The LLM agent determines the **current market volatility** using the `xtreamly_volatility()` function.
- A **threshold value** (e.g., `0.003897`) is used to classify the state as either:
  - **Low volatility** (`volatility <= threshold`)
  - **High volatility** (`volatility > threshold`)

### **2. Selecting Agents Based on Market State**

#### **Low Volatility State**

If the market is in a **low volatility** state, the agent prioritizes stable and undervalued agents:

- **Functions used:**
  - `top10_agents_significant()`
  - `top10_agents_undervalued()`
  - `top10_agents_stable()`
- The **LLM agent selects the best 10 agents** based on these criteria.
- Exposure to agents **not in the new selection is closed**.
- New agents are **invested in equally using available funds**.

#### **High Volatility State**

If the market is in a **high volatility** state, the agent focuses on more volatile and active agents:

- **Functions used:**
  - `top10_agents_significant()`
  - `top10_agents_popular()`
  - `top10_agents_volatile()`
  - `top10_agents_newly_active()`
- The **LLM agent selects the best 10 agents** based on these criteria.
- Exposure to agents **not in the new selection is closed**.
- New agents are **invested in equally using available funds**.

---

## Agent Selection Functions

The LLM agent uses multiple evaluation functions to select the top 10 agents:

### **Top 10 Significant Agents**

Agents with **significant changes** in key metrics such as:

- **Mindshare Delta (%)** ≥ 10
- **Market Cap Delta (%)** ≥ 10
- **Price Delta (%)** ≥ 10
- **Volume 24 Hours Delta (%)** ≥ 10

### **Top 10 Popular Agents**

Agents with:

- **Followers Count** ≥ 500
- **Average Engagements Count Delta (%)** ≥ 10

### **Top 10 Performing Agents**

Sorted by:

- **Market Capitalization**
- **Mindshare**
- **Followers Count**

### **Top 10 Volatile Agents**

Sorted by a **volatility score** combining:

- **Price Delta (%)**
- **Market Cap Delta (%)**
- **Volume 24 Hours Delta (%)**

### **Top 10 Stable Agents**

Sorted by **lowest** volatility score.

### **Top 10 Undervalued Agents**

Sorted by **undervalue score**, calculated as:

- `Average Engagements Count / Market Cap`

### **Top 10 Newly Active Agents**

Agents with:

- **Holders Count Delta (%)** > 10
- **Volume 24 Hours Delta (%)** > 10

---

## Execution Strategy

Every hour, the policy executes as follows:

1. **Determine Market State:** Run `xtreamly_volatility()` to classify market as **low** or **high volatility**.
2. **Select the Best 10 Agents:**
   - Use predefined functions based on the market state.
   - The **LLM agent makes the final decision**.
3. **Reallocate Exposure:**
   - Close positions on agents that are **no longer in the top 10**.
   - Equally distribute exposure among the **new top 10 agents**.

---

## Future Enhancements

- **Incorporate Social Media Analysis:**
  - Evaluate influencer tweets using OpenAI to determine **sentiment shifts**.
- **Dynamic Portfolio Adjustment:**
  - Use **reinforcement learning** to improve agent selection over time.

---

## Summary

This policy ensures that our **LLM-driven agent** follows an optimal selection process to dynamically **rebalance exposure** among the top 10 tokens. It leverages **real-time volatility predictions** and **quantitative metrics** to adapt to market conditions effectively, maintaining a balanced and strategic investment approach.

For further details and discussion, check out:

- [Cookie Docs](https://docs.cookie.fun/#/)
- [Cookie DAO Notion](https://cookiedao.notion.site/Cookie-DeFAI-Hackathon-17ddcd6f6625800dab49d8fb103ecc48)
- [Cookie DAO Discord](https://discord.com/channels/994904272489680917/@home)
