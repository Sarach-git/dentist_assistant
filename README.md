# Dentistry RAG Chatbot (Flask)


## What this does
- **STRICT answers** for exact business facts (address, phone, hours, services, prices) from `data/clinic.json`.
- **Clinic RAG**: answers clinic-specific questions using your own files in `data/`.
- **General RAG**: answers general dental health questions from `general_knowledge/` with a brief disclaimer.
- Uses **ChromaDB** for vector search and a pluggable **LLM** (OpenAI by default).


## Setup
```bash
pip install -r requirements.txt

# run
python app.py
```

## Improve accuracy
- Keep **all exact facts** only in `clinic.json`. The app will *never* invent these.
- Put brochures, FAQs, treatment policies into `data//*.md` for better clinic-specific answers.
- Expand `general_knowledge/` with vetted content (summaries from guidelines you trust) so general answers cite your corpus rather than the model’s memory.


## Safety
- General guidance includes: *"This is general information, not a medical diagnosis."*
- For medical emergencies, ensure your content includes the correct phone and emergency instructions.


## Telegram (optional)
- Set `TELEGRAM_TOKEN` and `CHAT_ENDPOINT` in `.env` and run `python telegram_bot.py`.
