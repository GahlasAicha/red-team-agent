# 🛡️ Red Team Agent

An automated red-teaming tool that tests whether an AI-powered HR assistant 
can be tricked into leaking confidential data — and measures how well defenses stop it.

## The problem
AI assistants connected to internal documents (salaries, addresses, secret projects) 
can be manipulated into revealing confidential information through clever prompts.

## How it works
Three AI components work together in a loop:
- **Target** — an HR assistant (RAG + Gemini) that answers from company documents
- **Attacker** — an AI agent that generates social-engineering attacks and adapts when it fails
- **Judge** — automatically detects leaks by scanning answers for planted secrets (canaries)

## Defenses (defense in depth)
1. Input filter — blocks suspicious keywords
2. Strict system prompt — refuses to reveal confidential data
3. Output filter — blocks any answer containing a secret

## Results
| Version | Attack success rate |
|---|---|
| V1 (no defense) | 100% |
| With combined defenses | 0% |

## Tech stack
Python · Google Gemini API · ChromaDB (RAG) · Streamlit (dashboard)

## How to run
pip install -r requirements.txt
streamlit run dashbord.py

