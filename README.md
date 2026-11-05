# OmniDesk AI Support Engine

An enterprise-grade, multi-tool Customer Support AI Agent built with **FastAPI**, **Google GenAI SDK**, **ChromaDB**, and **Pydantic**.

## Key Architecture & Features
* **Metadata-Filtered Vector RAG (`rag_store.py`):** Custom sliding-window document chunker (`chunk_size=350`, `overlap=50`) indexing multi-paragraph company policies into persistent ChromaDB storage with category-based metadata filtering.
* **Defense-in-Depth Guardrails (`guardrails.py`):** Zero-latency input security filter blocking prompt injection and jailbreak attempts before reaching the LLM.
* **Human-in-the-Loop (HITL) Financial Safety Gate (`guardrails.py`):** Autonomous tool execution for order lookups and small refunds (`<= $50`), with a mandatory manager approval gate pausing execution for high-value refunds (`> $50`).
* **Stateful Multi-Tool Agent (`main.py`):** FastAPI `/support` microservice orchestrating multi-turn Automatic Function Calling (AFC) via `client.chats.create`.
* **Automated LLM-as-a-Judge QA (`evals.py`):** Rate-limit-paced evaluation suite grading agent responses for Faithfulness and Ground-Truth accuracy using structured Pydantic schemas.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt