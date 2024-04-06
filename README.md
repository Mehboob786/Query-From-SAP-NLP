## SAP Query Generator and Database Helper API
This repository hosts a Python-based solution combining AI-driven natural language processing and database management functionalities tailored for SAP Business One databases. It enables users to generate SQL queries from natural language questions and execute these queries against a database, along with a summary of the retrieved data.

# Contents
SAPQureyGenAI.py: Implements an interface with Google's generative AI to create and validate SQL queries based on natural language inputs, ensuring compatibility with SAP Business One database schemas.
DBHelper.py: Manages database connections and operations, including query execution and error handling, for MS SQL Server databases.
main.py: A FastAPI application that serves endpoints for generating SQL queries from user questions and summarizing query results.
## Getting Started
Prerequisites

1. Python 3.8+
2. An SAP Database with MS SQL Server
3. Access to Google's generative AI services
# Installation
Clone the repository:
```
git clone https://github.com/Mehboob786/Query-From-SAP-NLP.git
cd uery-From-SAP-NLP
```
Install required Python packages:

Ensure you have Python and pip installed on your machine.
Install dependencies from requirements.txt:
```
pip install -r requirements.txt
```
Set up environment variables:

Create a .env file in the root directory.
Add your database credentials and Google API key:
```
db_user=your_database_user
db_password=your_database_password
db_host=your_database_host
db_name=your_database_name
GoogleAPI=your_google_api_key
```
# Run the FastAPI application:
```
uvicorn main:app --reload
```
# Usage
The API provides endpoints for generating and validating SQL queries based on natural language inputs, executing those queries, and summarizing the results:

Generate SQL Query: POST /SAP/GenerateQuery
Generate and Summarize SQL Query: POST /SAP/SAPQuerySummary
Use HTTP clients like cURL, Postman, or browser-based tools to interact with these endpoints.