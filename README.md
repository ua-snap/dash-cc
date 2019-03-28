# SNAP Community Charts

## Running locally

To run the application locally, install [pipenv](https://pipenv.readthedocs.io/en/latest/).  This app needs `python3` to run; if that's not your default python, adjust the command below (i.e. `python3` instead of `python`).

```bash
cd /path/to/this/repo
pipenv install
export GTAG_ID='abc' # google analytics ID, nonce for dev
export REQUESTS_PATHNAME_PREFIX='/' # see below for more info
pipenv run python application.py
```

The application will be available at [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Deployment on AWS

Before deploying, update the `requirements.txt` file:

```sh
pipenv clean
pipenv run pip freeze > requirements.txt
git commit -am'updating requirements.txt'
```

When deploying on AWS Elastic Beanstalk, a few environment variables must be set:

 * `GTAG_ID`: property ID for Google Analytics, no default value
 * `REQUESTS_PATHNAME_PREFIX`: Path prefix on host, should be `/` for local development and `/tools/community-charts/` for current deploy on AWS
