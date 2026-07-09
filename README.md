# 🥪 rollForSammy

A random sandwich generator built with Flask, vanilla JS, and a healthy respect for pickles. Pick your constraints (exact counts, random ranges, or full exclusions) and let it roll a sandwich for you — from Pickleman's-style options.

**Live demo:** [rollforsammy.onrender.com](https://rollforsammy.onrender.com/)
> Note: the live site isn't auto-deployed on every push — it's updated manually once a feature feels finished.

## What it does

- Generates a random sandwich: base bread, meats, cheeses, toppings, and sauces
- Every sandwich always gets a base (bread/wrap) — the one non-optional part
- Two ways to control each ingredient category:
  - **Exact amount** — always include exactly N items
  - **Random max** — roll a random amount between 0 and N
- Exclude specific ingredients entirely (e.g. no onions, ever)
- Duplicates are allowed by design (you might get two servings of bacon — that's the game)

## Tech stack

- **Backend:** Python, Flask, served with Waitress
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Deployment:** Render

## How it works

The Flask app keeps a small in-memory state for your settings (`meat`, `cheese`, `topping`, `sauce` counts) and a list of excluded ingredients:

- `POST /submit-exclusions` — saves which ingredients to leave out
- `POST /submit-choice` — sets an exact count for a category
- `POST /submit-random` — sets a random-range max for a category
- `POST /run-function` — builds the sandwich: filters each ingredient list against your exclusions, rolls the right number of items per category (exact or random depending on your choice), and returns it all as JSON

The frontend calls these endpoints and renders whatever comes back.

## Running it locally

\```bash
git clone https://github.com/AidenDoesCode/rollForSammy.git
cd rollForSammy
pip install -r requirements.txt
python main.py
\```

The app will start on `http://localhost:8000` by default (or whatever `PORT` env variable you set).

## What I learned building this

This was a learning project first, sandwich generator second. Main things I picked up:

- **Flask fundamentals** — routing, handling POST form data with `request.form`, returning JSON with `jsonify`, and structuring a small multi-route app
- **Frontend/backend communication** — connecting vanilla JS on the frontend to Flask routes on the backend, and thinking through the request/response cycle instead of just running everything client-side
- **HTML & CSS refresher** — rebuilding front-end fundamentals from scratch after a while away from them
- **JavaScript for the frontend** — handling form submissions and rendering dynamic content without a framework
- **Managing state on a server** — using global dictionaries to track user settings between requests, and the tradeoffs that come with that approach (works fine for a single-user demo, wouldn't scale as-is to multiple concurrent users)
- **Deploying a Flask app** — getting it running on Render with Waitress as the production server instead of Flask's built-in dev server

## Possible next steps

- Move from global state to per-session state so multiple people can use it without stepping on each other's settings
- Let users save/name favorite sandwich configs
- Add images or a more visual sandwich "build" display

## License

No license specified yet.
