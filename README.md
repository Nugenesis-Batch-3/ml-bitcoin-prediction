# ML Bitcoin Prediction System

This project is a machine learning API that provides endpoints for training and predicting sentiment analysis using LSTM models. The project is structured to be easily deployable using Docker and includes CI/CD workflows for automated testing and deployment.

## Project Description

This project is designed to provide an API for prediction bitcoin using sentiment analysis and LSTM models. The API includes endpoints for training the model and making predictions on new data.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.12 or later

### Local Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/Nugenesis-Batch-3/ml-bitcoin-prediction
cd ml-bitcoin-prediction
```

2. **Install Dependencies using Pipenv**:

```bash
Copy code
pip install pipenv
pipenv install --deploy --ignore-pipfile
```

3. **Run The App**:

Activate the pipenv shell:

```bash
pipenv shell
```

Create a `.env` file in the project root directory and add The following:

```
# FLASK Config
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG = 1

# MongoDB Config
MONGO_URI="mongodb+srv://nugenesis:z5MGlmxXAdKFHlAd@bitcoinpredictioncluste.qzcxmte.mongodb.net/?retryWrites=true&w=majority&appName=BitcoinPredictionCluster"

```

Run the Flask application:

```bash
flask run
```

### Contributing

1. Fork the repository.

2. Create a new branch:

```bash
git checkout -b feature-branch
```

3. Make your changes.

4. Commit your changes (git commit -m 'Add new feature').

```bash
git commit -m "Add new feature"
```

1. Push to the branch:

```bash
git push origin feature-branch
```

6. Open a pull request

Well Done!

Don't forget to have fun while coding 😜
