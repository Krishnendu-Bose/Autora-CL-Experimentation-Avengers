# Avengers - Closed Loop Experiment

## Overview

This project implements the Stroop task as a closed-loop experiment using the Autora framework. The experiment consists
of sampling trials, running theories, and updating conditions based on the results.

## Prerequisites

- Python 3.8 or greater
- Virtualenv
- Pip

## Setting up the Environment

### Install Python

Download and install Python from the official website: [Python Downloads](https://www.python.org/downloads/).

### Install Virtualenv

Install Virtualenv using pip:

```shell
pip install virtualenv
```

## Setting up the Project

### Clone the Repository

Clone the repository to your local machine:

```shell
git clone https://github.com/Krishnendu-Bose/Autora-CL-Experimentation-Avengers.git
cd Autora-CL-Experimentation-Avengers
```

### Create a Virtual Environment

Create a virtual environment in the project directory:

```shell
virtualenv venv
```

Activate the virtual environment:

- On Windows:

  ```shell
  .\venv\Scripts\activate
  ```

- On macOS/Linux:

  ```shell
  source venv/bin/activate
  ```

### Install Dependencies

Install the required dependencies using pip:

```shell
pip install -r requirements.txt
```

## Running the Experiment

The main script for running the experiment is `autora_workflow.py`. This script contains the logic for sampling trials,
running theories, and updating conditions.

### Running the Script

To run the experiment, execute the following command:

```shell
python autora_workflow.py
```

### Understanding the Workflow

The workflow consists of several key functions:

- `run_iteration`: Runs a single iteration of the experiment.
- `run_experiment_with_max_uncertainty`: Runs the experiment with conditions sampled based on maximum uncertainty.
- `report_linear_fit`: Reports the linear fit of the model.

### Example Output

The script will print the linear fit of the models at the end of the experiment:

```shell
y = <coefficient> x + <intercept>
```

## Additional Information

For more advanced options and detailed documentation, visit
the [Autora Documentation](https://autoresearch.github.io/autora/).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.