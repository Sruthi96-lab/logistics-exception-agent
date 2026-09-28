# 🚚 Logistics Exception Agent

### AI-powered logistics incident analysis with persistent learning using Hindsight

An AI agent that helps logistics teams analyze delivery exceptions, find relevant past experiences, recommend actions, and **learn from actual resolutions and outcomes**.

Built for the **AI Agents That Learn Using Hindsight** hackathon using **Vectorize Hindsight** as the persistent memory layer.



## 🧠 Problem

Logistics operations frequently face exceptions such as:

* 🚛 Vehicle breakdowns
* 📍 Incorrect or incomplete addresses
* ⏱️ Delivery delays
* 📦 Damaged packages
* ❌ Failed deliveries

Traditional systems can record these incidents, but they often do not effectively reuse the experience from previous incidents.

The same type of exception may happen again, requiring an operator to manually determine what action worked previously.



## 💡 Solution

The **Logistics Exception Agent** uses AI + persistent memory to turn previous logistics experiences into reusable operational knowledge.

When a new incident is reported, the agent:

1. Receives the incident details.
2. Searches Hindsight for relevant past experiences.
3. Filters the retrieved memories for relevant and successful resolutions.
4. Analyzes the available evidence.
5. Recommends an action based on documented experience.
6. Allows the operator to enter the actual resolution and outcome.
7. Saves that experience back into Hindsight.
8. Uses the accumulated knowledge for future incidents.

### 🔄 Learning Loop

```text
New Incident
     ↓
Recall Past Experiences
     ↓
Relevant Successful Memories
     ↓
AI Analysis
     ↓
Recommended Action
     ↓
Human Executes Resolution
     ↓
Actual Outcome Recorded
     ↓
Hindsight Memory
     ↓
Future Incidents Learn From It
```
## ✨ Key Features

### 🔎 Similar Incident Recall

The agent searches persistent Hindsight memory for incidents that are semantically relevant to the current exception.

### 🤖 Evidence-Based Recommendations

Recommendations are generated using documented past experiences rather than inventing unsupported resolutions.

### 🧠 Persistent Learning

Resolved incidents and their actual outcomes are stored in Hindsight so future incidents can benefit from previous experience.

### 👤 Human-in-the-Loop

The logistics operator remains responsible for confirming the actual resolution and outcome.

### 📊 Multiple Exception Types

The prototype supports:

* Vehicle Breakdown
* Address Error
* Delivery Delay
* Damaged Package
* Failed Delivery

### 🌐 Web Interface

A simple web dashboard allows users to:

* Enter an incident
* Analyze it
* View the AI recommendation
* Review similar incidents
* Record the actual resolution
* Record the outcome
* Teach the agent through Hindsight



## 🏗️ Architecture

```text
                  ┌─────────────────────┐
                  │   Logistics User    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Web Dashboard    │
                  │   HTML/CSS/JS       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     FastAPI API     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Logistics Agent     │
                  │ Analysis + Logic    │
                  └───────┬─────┬───────┘
                          │     │
             Recall       │     │ Recommendation
                          │     │
                          ▼     ▼
                  ┌─────────────────────┐
                  │ Hindsight Memory    │
                  │ Persistent Learning │
                  └─────────────────────┘
                          ▲
                          │
                  Resolution + Outcome
                          │
                          └────── Learning Loop
```



## 🔄 Agent Workflow

```text
User Activity / Incident
          ↓
Data Collection
          ↓
Incident Classification
          ↓
Hindsight Recall
          ↓
Memory Filtering
          ↓
AI Analysis
          ↓
Recommended Action
          ↓
Human Resolution
          ↓
Outcome Recording
          ↓
Hindsight Retain
          ↓
Future Learning
```



## 🧪 Example

### New Incident

```text
Incident ID: INC-301
Exception Type: Vehicle Breakdown
Location: Hyderabad
Priority: High

Description:
Delivery vehicle broke down while transporting a customer shipment.
```

### Agent Analysis

The agent searches Hindsight and finds relevant previous vehicle-breakdown experiences.

For example:

```text
Past Experience:
Vehicle breakdown during delivery
→ Replacement vehicle assigned
→ Shipment delivered successfully
```

### Recommendation

```text
Assign a replacement vehicle to resolve the current
incident and ensure successful delivery.
```

### Human Resolution

The operator records:

```text
Resolution:
Assigned a replacement vehicle to the shipment.

Outcome:
Shipment was delivered successfully.
'''

### Learning

The resolution and outcome are saved to Hindsight.

A future vehicle-breakdown incident can then retrieve this experience and use it as evidence.



## 🧠 Why Hindsight Matters

A normal chatbot can generate an answer from the current conversation.

This project demonstrates a different workflow:

```text
Past Experience
      ↓
Remember
      ↓
Recall
      ↓
Apply
      ↓
Resolve
      ↓
Learn
      ↓
Remember Again
```

Hindsight acts as the agent's **persistent memory layer**, allowing the system to retain operational experiences beyond a single interaction.

## 🛠️ Technology Stack

| Component         | Technology            |
| ----------------- | --------------------- |
| Backend           | Python                |
| API               | FastAPI               |
| Persistent Memory | Vectorize Hindsight   |
| Local LLM         | Ollama + Llama 3.2    |
| Frontend          | HTML, CSS, JavaScript |
| Data Validation   | Pydantic              |
| Configuration     | python-dotenv         |
| Development       | VS Code               |
| Version Control   | Git + GitHub          |



## 📁 Project Structure

```text
logistics-exception-agent/
│
├── app/
│   ├── agent.py
│   ├── main.py
│   ├── memory.py
│   └── models.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── data/
│   └── sample_incidents.json
│
├── load_demo_data.py
├── test_hindsight.py
├── test_memory.py
├── requirements.txt
├── README.md
└── .gitignore
```


## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sruthi96-lab/logistics-exception-agent.git
cd logistics-exception-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```



## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
HINDSIGHT_BASE_URL=your_hindsight_endpoint
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BANK_ID=logistics-agent
```

**Never commit `.env` or API keys to GitHub.**

The repository includes `.gitignore` to prevent secrets from being uploaded.


## 🤖 Local LLM Setup

This project uses **Ollama** for local AI inference.

Install Ollama and pull the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting the application.



## 📚 Load Demo Memories

The repository includes sample logistics incidents for demonstration.

Run:

```bash
python load_demo_data.py
```

This loads example incidents into Hindsight, including:

* Vehicle Breakdown
* Address Error
* Delivery Delay
* Damaged Package
* Failed Delivery



## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```



## 🧪 Demo Flow

### Scenario 1 — Vehicle Breakdown

```text
Create Incident
      ↓
Vehicle Breakdown
      ↓
Hyderabad
      ↓
High Priority
      ↓
Analyze
      ↓
Agent recalls successful experience
      ↓
Replacement vehicle recommended
      ↓
Operator resolves incident
      ↓
Resolution + outcome saved
```

### Scenario 2 — New Vehicle Breakdown

Create another vehicle-breakdown incident.

The agent can retrieve the previously stored successful experience and use it when generating its recommendation.

This demonstrates the core **remember → recall → apply → learn** loop.



## 🔌 API Endpoints

### Analyze Incident

```http
POST /api/incident
```

Accepts an incident and returns:

* AI analysis
* Recommended action
* Similar past incidents

### Resolve Incident

```http
POST /api/incident/resolve
```

Stores the actual resolution and outcome in Hindsight.



## 🔒 Safety and Reliability

The agent is designed to avoid treating every retrieved memory as a successful solution.

It distinguishes between:

* Relevant incidents
* Resolved incidents
* Successful outcomes
* Open or unresolved incidents

Recommendations are based on available documented evidence.

The system also uses a **human-in-the-loop** approach so the operator confirms the actual resolution and outcome.



## 🚀 Future Improvements

Potential extensions include:

* Real-time GPS and vehicle telemetry
* Automated route reassignment
* Integration with warehouse management systems
* Delivery partner APIs
* Risk and priority scoring
* Incident trend analytics
* Multi-agent logistics workflows
* Feedback-based recommendation improvement
* Authentication and role-based access
* Production database integration
* Deployment using cloud infrastructure



## 🎯 Hackathon Goal

This project demonstrates how an AI agent can move beyond a stateless chatbot by using persistent memory to:

**Remember → Recall → Reason → Act → Learn**

The key idea is simple:

> Every resolved logistics incident can become useful knowledge for the next one.



## 👩‍💻 Author

**Sruthi**

Computer Science Engineering Student

GitHub: [@Sruthi96-lab](https://github.com/Sruthi96-lab)



## 📌 Project Status

**Prototype / Hackathon Project**

Built as a demonstration of persistent-memory AI agents using Hindsight.
