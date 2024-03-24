import google.generativeai as genai
import os
from dotenv import load_dotenv

safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]

class SAPQureyGenAI:
    apikey = None
   
    def __init__(self):
        load_dotenv()
        self.apikey = os.environ.get("GoogleAPI")
        # Assuming genai.configure is a method to configure the genai module
        genai.configure(api_key=self.apikey)
        
    def GenerateValidate(self,question):
        qry = self.GenerateQurey(question)
        finalquery = self.ValidateQurey(qry)
        return finalquery
    

    def GenerateQurey(slef, Qinput):
        generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

       
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)
        prompt_parts = [
    "input: When users pose questions in natural language regarding data retrieval from the SAP Business One database, it's crucial to respond with an accurate and executable SQL query. Are you familiar with the SAP Business One database schema? Provide a query that fulfills the following criteria: \n1. The query syntax is correct according to SAP Business One standards.\n2. All column names are accurate and follow the SAP Business One database schema.\n3. The query is executable within the SAP Business One environment.\n4. Correct primary keys are used for all documents.",
    "output: Provide a single valid SQL query that can be executed on the SAP Business One database server.",
    "input: Query: %s" % Qinput,
    "output: ",
]


        response = model.generate_content(prompt_parts)
        print("Generator")
        print(response.text)
        return response.text
   

    def ValidateQurey(self, Qurey):
                # Set up the model
        generation_config = {
        "temperature": 0.5,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

       

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        prompt_parts = [
            "input: As a Query Administrator or Validator for SAP Business One, your task is to verify and correct an SQL query. Ensure the syntax is correct, tables and column names are valid as per the SAP Business One database schema, and all spellings are accurate. Provide the corrected query in your response.",
            "output: Return a corrected and valid query in JSON format. For example: { Query :  Updated and valid Query }",
            "input: Query: %s" % Qurey,
            "output: ",
        ]

        response = model.generate_content(prompt_parts)
        print("Validator")
        print(response.text)
        return response.text



    def ValidateQureyError(self, Qurey, Error):
        # Set up the model
        generation_config = {
        "temperature": 0.5,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

       

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        prompt_parts = [
            "input: SAP Business One, As a Query Administrator or Validator for SAP Business One, verify the following for a given SQL query:\n1. Check the query syntax.\n2. Validate that the tables and column names are according to the SAP Business One database schema.\n3. Check spelling in the query.",
            "input 2: An error occurred while executing this query on the SAP Business One Server.",
            "output: Provide a corrected and valid query in JSON format. For example: { Query:  Updated and valid Query }",
            "input: Query: %s" % Qurey,
            "input 2: Error: getting the Error While Executing the Query on SAP Business One Server %s" % Error,
            "output: ",
        ]

        response = model.generate_content(prompt_parts)
        print("ValidateQureyError")
        print(response.text)
        return response.text


    def summary(self, Data, qurey ):
        # Set up the model
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

       

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        prompt_parts = [
        "input: Generate summaries of retries data from SAP Business One and queries posed by users. Summarize the trends, insights, and patterns observed in retries data, including reasons for retries, frequency of retries, and any correlations with user queries. Provide Detailed summaries that highlight key findings and actionable insights for stakeholders.",
        "output: Detailed Summary of about the data, Draw graph if it is possible",
        f"input: Qurey Asked By User to Retrive Data: {qurey}, Data Retrived from SAP Database Server: {Data} ",
        "output: ",
        ]

        response = model.generate_content(prompt_parts)
        print("ValidateQureyError")
        print(response.text)
        return response.text



