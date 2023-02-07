# SNAP Community Charts

## Running locally

To run the application locally, install [pipenv](https://pipenv.readthedocs.io/en/latest/).

```bash
cd /path/to/this/repo
pipenv install
export FLASK_APP=application.py
export DASH_REQUESTS_PATHNAME_PREFIX='/' # see below for more info
export DATA_PREFIX='https://s3-us-west-2.amazonaws.com/community-charts/' # see below for more info
pipenv run flask run
```

The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Deployment on AWS

Before deploying, update the `requirements.txt` file:

```sh
pipenv clean
pipenv run pip freeze > requirements.txt
git commit -am'updating requirements.txt'
```

When deploying on AWS Elastic Beanstalk, a few environment variables must be set:

 * `DASH_REQUESTS_PATHNAME_PREFIX`: Path prefix on host, should be `/` for local development and `/tools/community-charts/` for current deploy on AWS
 * `DATA_PREFIX`: Location of the CSV files for each community. Set to https://s3-us-west-2.amazonaws.com/community-charts/ unless reading from local `data` subdirectory.
