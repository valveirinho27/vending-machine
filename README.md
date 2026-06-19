# Change Machine

Small Python vending machine project with a domain/services/utils architecture and unit tests.

## Project structure

```text
src/
├── constants.py
├── domain/
│   ├── coins.py
│   ├── product.py
│   └── vending_machine.py
├── services/
│   └── change_maker.py
└── utils/
	└── formatting.py
```

## Run the app

```bash
python main.py
```

## Install test dependencies

```bash
pip install -r requirements.txt
```

## Run tests

```bash
pytest -q
```

