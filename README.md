# Attack Surface Service

This project is a Flask-based web application designed to manage and monitor virtual machines (VMs) and firewall rules. It provides endpoints to retrieve attackers and statistics.

## Features

- **/api/v1/attack**: Retrieves attackers for a given VM.
- **/api/v1/stats**: Provides statistics about the VMs and requests.

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Setup

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd Attack-surface-service
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory with the following content:

    ```env
    CLOUD_ENV_FILE=inputs/input-0.json
    DATABASE_URL=sqlite:///app.db
    ```

5. **Ensure the `inputs` directory contains the input JSON file** (e.g., `input-0.json`).

## Initializing the Database

Before running the application, initialize the database:

```sh
python init_db.py
```

## Initializing the Database

Start the Flask application:

```sh
python app.py
```

The application will be available at http://127.0.0.1:5000/.


## Running Tests

To run the test suite, use:

```sh
python -m unittest discover -s tests
```



