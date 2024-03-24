import json
import logging
from fastapi import FastAPI, HTTPException
from SAPQureyGen import SAPQureyGenAI  # Ensure this custom module is correctly implemented
from DBHelper import DBHelper  # Ensure DBHelper is defined as in the previous guidance

app = FastAPI()
db_helper = DBHelper()
generator_instance = SAPQureyGenAI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/SAP/GenerateQuery")
async def SAPQueryGenerator(question: str):
    query = None  # Define query with a default value at an appropriate scope
    try:
        queryjson = generator_instance.GenerateValidate(question)
        # Log the JSON string for debugging
        logging.debug(f"Received JSON: {queryjson}")
        
        try:
            cleaned_str = queryjson.strip('` \n').replace("json\n", "", 1)
            # Convert the JSON string to a Python dictionary
            print("cleaned_str")
            print(cleaned_str)
            response_dict = json.loads(cleaned_str)
            
            # Extract the query from the dictionary if possible
            query = response_dict.get('Query', 'No query found.').strip('` \n').replace("sql\n", "", 1).replace("\\n", "\n")
            print("query")
            print(query)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}")
            # Consider whether to return or raise an HTTPException here if JSON parsing fails

        logging.info("Final Query")
        logging.info(query)
        # Check if the query is not None
        if query is not None:
            # Execute the query
            result = db_helper.query_db(query)
        logging.info("Final result")
        logging.info(result)
        
        if result is not None:
            # Convert the DataFrame to JSON; orient='records' creates a list of records
            result_json = result.to_json(orient='records')
            return {"result": "Success", "data": result_json}
        else:
            raise HTTPException(status_code=500, detail="Explain A Bit More Your Qurey")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/SAP/SAPQuerySummary")
async def SAPQuerySummary(question: str):
    query = None  # Define query with a default value at an appropriate scope
    try:
        queryjson = generator_instance.GenerateValidate(question)
        # Log the JSON string for debugging
        logging.debug(f"Received JSON: {queryjson}")
        
        try:
            cleaned_str = queryjson.strip('` \n').replace("json\n", "", 1)
            # Convert the JSON string to a Python dictionary
            print("cleaned_str")
            print(cleaned_str)
            response_dict = json.loads(cleaned_str)
            
            # Extract the query from the dictionary if possible
            query = response_dict.get('Query', 'No query found.').strip('` \n').replace("sql\n", "", 1).replace("\\n", "\n")
            print("query")
            print(query)
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}")
            # Consider whether to return or raise an HTTPException here if JSON parsing fails

        logging.info("Final Query")
        logging.info(query)
        # Check if the query is not None
        if query is not None:
            # Execute the query
            result = db_helper.query_db(query)
        logging.info("Final result")
        logging.info(result)
        
        if result is not None:
            # Convert the DataFrame to JSON; orient='records' creates a list of records
            result_json = result.to_json(orient='records')
            summary = generator_instance.summary(result_json,question)
            return {"result": "Success", "Summary": summary}
        else:
            raise HTTPException(status_code=500, detail="No DataFound for this qurey or Explain A Bit More Your Qurey")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

