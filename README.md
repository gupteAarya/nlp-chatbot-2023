# Gizmo Bot
<p align="start">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,github" />
  </a>
</p>

<img width="1024" height="500" alt="gizmobot-banner" src="https://github.com/user-attachments/assets/1b12b0a4-c62b-4edc-ba72-a89fb6095870" />

**A retrieval-based NLP chatbot that can tell you everything about the event it was made for.**

This project was built as my submission for **Gizmo Geeks 2023**, an offline hackathon in Mumbai organised by a high school, where I represented my school. Ask it anything about the event (schedule, venue, rules, prizes, teams) and it replies with the closest match from its trained data. It uses Python's `difflib` for matching, with no machine learning model.

**It runs locally on your own device, no internet is needed.**

## The Problem Statement

The problem statement given to us was to make a chatbot that can answer any question about the above mentioned event.

## The Implementation

This is a **retrieval-based** chatbot. It doesn't generate text, it looks for closest matches from its knowledge base.

1. **"Train":** load the event data (question-answer pairs) into memory (This technically isn't training since there exists no model, it uses this as a knowledge base every time)
2. **Match:** compare the user's message against every known question using `difflib`'s `get_close_matches()` function
3. **Respond:** return the answer attached to the closest match
4. **Fallback:** if nothing is similar enough, reply with a default message

Because every answer comes from the trained data, the bot **can't make things up**, in other words, it **cannot <a href="https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)">hallucinate</a>**.

It returns the most similar object with a similarity cutoff of 0.6.

## Features

- **Fuzzy matching:** tolerates typos and rephrasing
- **Local:** no API keys, no internet
- **Easy to retrain:** anyone can clone this repo and change the training data for their own use case
- **Hallucination-free:** answers come only from your data as mentioned above.

## Training The Chatbot
The chatbot can easily be trained from the terminal by running `python app.py` in your project root.

Here's how it works:
<img width="723" height="73" alt="Screenshot 2026-11-20 at 16 58 49" src="https://github.com/user-attachments/assets/49779403-0262-488c-b3af-1d3551c8c91a" />

After answering the question, the question answer key is automatically added to the `train.json` file in the required format.
<img width="991" height="437" alt="Screenshot 2026-11-20 at 16 59 13" src="https://github.com/user-attachments/assets/6bb297be-15b6-4bbd-999e-66a22b1af84c" />

1. You ask it a question, if it does not know the answer, it asks for it
2. You give it the answer
3. The answer is added to the `train.json` file

This makes it easy to train the bot as one doesn't have to spend time manually sorting out questions and answers in `train.json`


## Screenshots
<p align="center">
  <img width="455" height="802" alt="Chat interface GUI" src="https://github.com/user-attachments/assets/7037162b-f04f-4707-b816-fbb46e222e6e" />
  <br>
  <em>The main GUI.</em>
</p>
<p align="center">
  <img width="723" height="73" alt="Training interface CLI" src="https://github.com/user-attachments/assets/5f708e81-52b3-40f9-915e-db320861aa13" />
  <br>
  <em>Terminal CLI to train the chatbot.</em>
</p>

## Run It Yourself

### 1. Clone

```bash
git clone https://github.com/gupteAarya/nlp-chatbot-2023.git
cd nlp-chatbot-2023
```

### 2. Train it on your own data
"Training" here just means giving the bot your question-answer pairs. Open the data file (`train.json`, adjust to your actual file name) and use this format:

```json
{
  "when does the event start": "The event starts at 9:00 AM on Saturday.",
  "where is the venue": "The venue is [Venue Name], [City].",
  "what are the prizes": "1st place wins [prize]."
}
```

Alternatively, refer to the <a href="#training-the-chatbot"><b>Training The Chatbot</b></a> section.

- Use short, natural-sounding questions as keys
- Add several phrasings for important questions
- Keep answers short and factual

### 3. Run

```bash
python main.py
```
`main.py` is the main GUI file.

Then type your question:

```
You: whn does it start
Bot: The event starts at 9:00 AM on Saturday.
```

### 4. Tune it

The similarity cutoff controls how strict matching is. Lower values are more forgiving but more likely to give a wrong answer, and higher values are stricter but may miss typos.

```python
difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
```

## Technical Stack

- Python
- `difflib` (standard library)
- CustomTKinter (to build custom UI)
- TKinter

## Limitations

- It only knows what's in its data, so it can't answer anything else
- Matching is by text similarity, not meaning, so heavily reworded questions can miss
- No semantic understanding as is seen in modern RAG
- No context history of previous conversations

## Contributing

Open source, so feel free to fork it, retrain it for your own event, or open a PR.

## License

MIT. See [LICENSE](LICENSE).

## Status

**Archived: built in 2023 as a hackathon project** 
