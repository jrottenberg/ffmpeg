# Welcome to ffmpeg docker image contributing guide <!-- omit in toc -->

Thank you for investing your time in contributing to our project! Any contribution you make will be reflected on [jrottenberg/ffmpeg](https://github.com/jrottenberg/ffmpeg) :tada:.

Read our [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.


## Opening an issue

Make sure you search exisiting issues, that there is no duplicate, before opening a new one. If you are raising a bug, give enough information so we can reproduce it locally:

- Command you ran
- Observed output
- Expected output


## Creating a PR

### Local change

Before you open a PR make the change locally and verify it passes pre-commit :


```sh
pip install pre-commit
pre-commit install # inside the local checkout
pre-commit run -a # to force a run, but it will execute on commits
```

Manual changes are expected in the `templates/` folder or `./update.py`

__Don't__ make changes directly into the _generated_ `docker-images/` folder. Updates are variant specific (`templates/Dockerfile-template.*`) or ffmpeg specific (`templates/Dockerfile-env` and `templates/Dockerfile-run`). Either way after a change, run `./update.py` to regenerate all the Dockerfile files.

If you forget and don't have pre-commit configured, the pre-commit step will fail anyway.


```sh
# Generates the Dockerfile for all variants
./update.py

pre-commit run -a # recommanded

# Test a specific variant
docker build -t my-build docker-images/VERSION/

# Make sure all variants pass before CI
find ffmpeg/ -name Dockerfile | xargs dirname | parallel --no-notice -j 4 --results logs docker build -t {} {}
```



# Reviewing


To make reviews simpler, try to limit changes to one functionnality or bug fix (no `and`)


# Merging the PR


Working on that project is not my day job, although I do enjoy maintaining it, I can't guarantee a review the same day.

Don't hesitate to ping me if an issue has been opened for too long.
