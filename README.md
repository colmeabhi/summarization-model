# Summary Generator

A small Flask website that summarises text. You paste in an article, pick how long you
want the summary to be, and it gives back the most important sentences from the text.

It is an **extractive** summariser: every sentence is scored with 8 features (TF-ISF,
proper nouns, named entities, position, length, etc.), the scores are smoothed with PCA
(this replaced the old Theano RBM) and the best sentences are kept in their original order.

## Project structure

```
app.py                      # creates the flask app and registers the blueprints
config.py                   # settings (debug, max text length, port...)
routes/
    pages.py                # website pages: home, how it works, about
    api.py                  # json api: /api/summarize and the old /post_summary
    errors.py               # 404 / 405 / 413 / 500 pages
    utils.py                # input checks shared by pages and api
summarygenerator/
    preprocessing.py        # splitting into sentences, stopwords, pos tagging
    features.py             # the sentence scoring features
    entity.py               # named entity counting with nltk
    feature_enhancer.py     # PCA step (replacement for the RBM)
    summary.py              # puts everything together -> summarize()
    resources.py            # nltk downloads, stopwords, regexes
templates/                  # jinja templates (base.html + one per page)
static/                     # css and js
tests/                      # pytest tests
```

## Running it locally

Needs Python 3.10 or newer.

```bash
git clone https://github.com/colmeabhi/summarization-model.git
cd summarization-model

python3 -m venv .venv
source .venv/bin/activate        # windows: .venv\Scripts\activate

pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:5001 in your browser.

The first start takes a bit longer because NLTK downloads its data (punkt, stopwords,
the pos tagger and the NE chunker) into `~/nltk_data`.

### Settings

These can be set as environment variables:

| Variable      | Default             | What it does                          |
|---------------|---------------------|---------------------------------------|
| `PORT`        | `5001`              | port the server runs on               |
| `FLASK_DEBUG` | `0`                 | set to `1` to turn on debug mode      |
| `SECRET_KEY`  | `dev-key-change-me` | change this if you deploy it anywhere |

## API

`POST /api/summarize`

```bash
curl -X POST http://localhost:5001/api/summarize \
     -H 'Content-Type: application/json' \
     -d '{"text": "Your paragraph text here.", "length": "short"}'
```

`length` can be `short`, `medium` (default) or `long`.

Response:

```json
{
  "summary": "The picked sentences joined together.",
  "sentences": ["The picked sentences", "..."],
  "original_count": 7,
  "summary_count": 3,
  "original_words": 80,
  "summary_words": 30
}
```

The old endpoint `POST /post_summary` with `{"textString": "..."}` still works and
returns `{"summary": "..."}`.

## Deploying for free (Render)

The repo has a `render.yaml` file, so Render can set everything up by itself.

1. Make an account on https://render.com (you can sign in with GitHub).
2. Click **New +** -> **Blueprint** and pick this repository.
3. Render reads `render.yaml`, click **Apply** and wait for the build (around 5 minutes).
4. The site will be at `https://summary-generator-xxxx.onrender.com`.

After that every push to the branch redeploys it.

Note: on the free plan the site goes to sleep after 15 minutes with no visitors, so the
first visit after that takes about a minute to load.

## Tests

```bash
pip install pytest
python -m pytest
```
