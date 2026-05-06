# Microsoft 365 Agents SDK - A2A Demo

A demo showing how the [Microsoft 365 Agents SDK]() can serve as an adapter to make an [A2A protocol](https://a2a-protocol.org) agent accessible through Microsoft Teams and Copilot 365.

## Demo

Watch [Microsoft 365 Agents SDK A2A Demo](https://youtu.be/lVJO2cMJeIc) on YouTube.

## Architecture

```
User <-> Teams / Copilot 365 <-> M365 Agents SDK Bot <-> A2A Client <-> A2A Agent
              (port 3978)                                        (port 8000)
```

The **Teams Agent** (built with the Microsoft 365 Agents SDK) receives messages from Teams or the Teams App Test Tool. It uses the A2A SDK's `ClientFactory` to forward each message to an **A2A Agent**, then returns the response back to the user in Teams.

## Prerequisites

- Python 3.10+
- Node.js and npm (for the Teams App Test Tool)

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install the Teams App Test Tool:

```bash
npm install -g @microsoft/teams-app-test-tool
```

## Running the Demo

You need three terminal windows:

**Terminal 1 - Start the A2A Agent (port 8000):**

```bash
python -m a2a_agent.main
```

**Terminal 2 - Start the Teams Agent (port 3978):**

```bash
python -m teams_agent
```

**Terminal 3 - Launch the Teams App Test Tool:**

```bash
teamsapptester
```

This opens a browser window with a Teams-like chat UI connected to the bot at `http://127.0.0.1:3978/api/messages`.

Send any message to see it forwarded to the A2A agent and echoed back. Send `/help` for usage info.

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `A2A_AGENT_URL` | `http://localhost:8000` | URL of the A2A agent |
| `A2A_PORT` | `8000` | Port for the A2A agent server |
| `PORT` | `3978` | Port for the Teams agent server |

## Project Structure

```
├── a2a_agent/              # A2A protocol agent
│   ├── agent.py            # AgentExecutor implementation
│   └── main.py             # A2A server setup and AgentCard
├── teams_agent/            # Microsoft 365 Agents SDK bot
│   ├── app.py              # AgentApplication with A2A client bridge
│   ├── start_server.py     # aiohttp server setup
│   └── __main__.py         # Entry point
├── requirements.txt
└── README.md
```
