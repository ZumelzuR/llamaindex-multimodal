# Project Title

## Setup Instructions

### 1. Create and Activate Virtual Environment

First, create a virtual environment:

```sh
python -m venv .env
```

Activate the virtual environment:

- On Windows:
    ```sh
    .\.env\Scripts\activate
    ```
- On macOS and Linux:
    ```sh
    source .env/bin/activate
    ```

### 2. Install Requirements

Next, install the required packages:

```sh
pip install -r requirements.txt
```

### Create .env file

Create a .env file and insert the values and the variables defined in .env.template

### 3. Start Jupyter Lab

To start Jupyter Lab and open the notebook named "notebook":

```sh
jupyter lab
```

### 4. Run the Application

To start the API application, run the following command:

```sh
sudo uvicorn main:app --reload --port 5000
```

### 5. API Endpoints

Run basic tests
```sh
pytest
```

### 6. API Endpoints

The application provides the following API endpoints:

#### Healthcheck

To check the health status of the application:

```http
GET /healthcheck
```

#### Chat

To send a message and receive a response from the assistant:

```http
POST /chat
```

Request Body:
```json
{
    "history": [],
    "message":"How are you?"
}
```

Response:
```json
{
    "assistant": "I'm good, thank you!"
}
```

#### Force Indexation

To force the indexation of data:

```http
POST /force-indexation
```

Response:
```json
{
    "message": "Done!"
}
```
