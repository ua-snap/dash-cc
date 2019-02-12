# SNAP Community Charts

## Running locally

To run the application locally, install [pipenv](https://pipenv.readthedocs.io/en/latest/).  This app needs `python3` to run; if that's not your default python, adjust the command below (i.e. `python3` instead of `python`).

```bash
cd /path/to/this/repo
pipenv install
pipenv run python app.py
```

The application will be available at http://127.0.0.1:8080/.

## Deploy to AWS EB

Before deploying, update the `requirements.txt` file:

```sh
pipenv clean
pipenv run pip freeze > requirements.txt
```

Environment variables to configure for this application:

```
DEBUG=False # set to True to enable debug on the server
```

Static path mappings:

```
/assets -> assets
```

These configurations are specified in the `.ebextensions/options.config` file.
