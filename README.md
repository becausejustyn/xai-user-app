# XAI study demo

This Streamlit app shows an interface from an earlier research project. The project
studied how people assess visual explanations from an artificial intelligence model.
The final study used Qualtrics. This app is now a software demonstration.

The research materials for the project are in the
[saliency_map_bias_user_study](https://github.com/becausejustyn/saliency_map_bias_user_study)
repository.

## What the app does

The app has three tasks:

1. Compare two visual explanations.
2. Mark important points on an image.
3. Review the explanations.

The app does not ask for an identifier or demographic data. It does not connect to a
database. It keeps responses in the Streamlit session. A user can download the responses
as a JSON file.

## Run the app

Install [`uv`](https://docs.astral.sh/uv/), then run:

```shell
uv sync
uv run streamlit run Hello.py
```

Run the checks:

```shell
uv run ruff check .
uv run pytest
```

## Project structure

```text
Hello.py          Home page
app_utils.py      Shared data and image functions
pages/            Demo tasks
trials/README.md  Local data setup instructions
tests/            Automated checks
```

## Data and security

The public demo has no database code or credentials. Do not commit `.env` files,
Streamlit secrets, service-account files, or research responses.

This demo is not an active research study. Add the required consent text, ethics approval,
privacy controls, and retention rules before you collect research data.

## Image source

The original prediction images came from the
[Diverse Human Faces Dataset](https://synthesis.ai/diverse-human-faces-dataset/) from
Synthesis AI. The repository does not include these images.

Each user must get the dataset from Synthesis AI and accept the applicable terms. Follow
the instructions on the Synthesis AI website to download the dataset. See
[`trials/README.md`](trials/README.md) for setup instructions.

## Related research

This demo comes from the study behind the paper
[Do Explanations Expose Bias? How Saliency Maps Affect Judgements of Biased Face-Recognition Models](https://doi.org/10.3233/FAIA250936)
(ECAI 2025).

The notebooks, models, and trial data for the study are in the
[saliency_map_bias_user_study](https://github.com/becausejustyn/saliency_map_bias_user_study)
repository.

## License

This repository uses the [Apache License 2.0](LICENSE).
