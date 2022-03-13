[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# Parallel Link Crawler

 A command line script that you can call with a url and it will begin crawling all links on that website and printing out every link it finds to stdout, preventing traverse to another domaind different from the original.

## Prepare Environment

This project has three dependencies that must be installed before you can run the script.

### Automate python environment creation (requires make on path)

 If you wanna go fast, this command below will create a new python virtual environment and install the required dependencies.

  ```shell
 make configure_production
 ```

### Install requirements manually

 Create python virtual environment, install dependencies and you are ready to go.
 (You can use any kind of environment creation as pipenv, conda, venv, etc.)

   ```shell
 python3 -m venv venv
 ```

 Activate the virtual environment and install the requirements.

  ```shell
    source venv/bin/activate
```

## Usage

The script should be called using `./crawl`

- Arguments:
  - `-n` [Optional] - If not supplied, default to 1.
  - The URL to start crawling from.

Examples:

```shell
./crawl -n 20 https://books.toscrape.com/
```

```shell
./crawl -n 5 https://crawler-test.com/
```

```shell
./crawl -n 5 https://amazon.com/
```

## TODO

    - Unit test to assert values received and returned by the functions.
    - Better memory handling/sharing, since the approach used here lies on GIL lack of performance.
    - Scaling to the stars: Implement this on a docker environment, moving memory management to a central Mem Cache software (e.g Redis), would allow scalating to a large number of concurrent kubernetes pods, each of them with n internal process running. (e.g 100 process, inside a docker container that is scaled up to 1000 Kubernetes Pods, would lead to 100K simultaneous requests).
