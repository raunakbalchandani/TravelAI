# import sqlite3
# import openai

# openai.api_key = 'sk-proj-G0XB0f0wCmH1cQ0uH4VlT3BlbkFJ7D2aieoAPIeNE8E4o8JP'

# def get_packages(query):
#     conn = sqlite3.connect('travel_packages.db')
#     cursor = conn.cursor()

#     cursor.execute(query)
#     packages = cursor.fetchall()

#     conn.close()
#     return packages

# def generate_sql_query(prompt):
#     schema_description = """
#     The table name is 'packages' and the schema has the following columns:
#     - id INTEGER PRIMARY KEY
#     - from_city TEXT
#     - to_city TEXT
#     - package_type TEXT
#     - cost INTEGER
#     """

#     messages = [
#         {"role": "system", "content": "You are an assistant that translates natural language queries into SQL queries."},
#         {"role": "user", "content": f"Translate the following natural language query into an SQL query. {schema_description} Query: '{prompt}'"}
#     ]

#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     return response.choices[0].message.content

# def handle_query(natural_language_query):
#     sql_query = generate_sql_query(natural_language_query)
#     print(sql_query)
#     try:
#         results = get_packages(sql_query)
#         if results:
#             response = "Here are the results:\n"
#             for row in results:
#                 response += f"From: {row[1]}, To: {row[2]}, Package: {row[3]}, Cost: ${row[4]}\n"
#             return response
#         else:
#             return "No results found for your query."
#     except Exception as e:
#         return f"An error occurred: {e}"

# if __name__ == "__main__":
#     # Test the functions
#     #print(handle_query("Show me the packages from Mumbai to London"))
#     get_packages("SELECT * FROM packages WHERE from_city = 'Mumbai' AND to_city = 'London';")

# import sqlite3
# import openai

# openai.api_key = 'sk-proj-G0XB0f0wCmH1cQ0uH4VlT3BlbkFJ7D2aieoAPIeNE8E4o8JP'

# def get_packages(query):
#     conn = sqlite3.connect('travel_packages.db')
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute(query)
#         packages = cursor.fetchall()
#     except sqlite3.Error as e:
#         return f"An error occurred: {e}"
    
#     conn.close()
#     return packages

# def generate_sql_query(prompt):
#     schema_description = """
#     The table name is 'packages' and the schema has the following columns:
#     - id INTEGER PRIMARY KEY
#     - from_city TEXT
#     - to_city TEXT
#     - package_type TEXT
#     - cost INTEGER
#     """

#     messages = [
#         {"role": "system", "content": "You are an assistant that translates natural language queries into SQL queries."},
#         {"role": "user", "content": f"Translate the following natural language query into an SQL query. {schema_description} Query: '{prompt}'"}
#     ]

#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     sql_query = response.choices[0].message.content
#     sql_query = sql_query.replace("\n"," ")
#     # Sanitize the SQL query by removing unnecessary characters
#     #sql_query = sql_query.split(';')[0]  # Remove anything after the first semicolon
#     if sql_query[0] == '`':
#           return sql_query[7:-5]
#     else:
#         return sql_query

  

# def handle_query(natural_language_query):
#     sql_query = generate_sql_query(natural_language_query)
#     print("calling handle_query")
#     print(sql_query)
#     try:
#         results = get_packages(sql_query)
#         print(results)
#         if results:
#             response = "Here are the results:\n"
#             for row in results:
#                 response += f"From: {row[1]}, To: {row[2]}, Package: {row[3]}, Cost: ${row[4]}\n"
#                 #response += row
#             return response
#         else:
#             return "No results found for your query."
#     except Exception as e:
#         return f"An error occurred: {e}"

# if __name__ == "__main__":
#     # Test the functions
#     print(handle_query("Show me the packages from Mumbai to London"))
#     #handle_query("Show me the packages from Mumbai to London")

import sqlite3
import openai
import re
import mysql.connector

openai.api_key = 'sk-proj-G0XB0f0wCmH1cQ0uH4VlT3BlbkFJ7D2aieoAPIeNE8E4o8JP'

config = {
  'user': 'root',
  'password': 'admin123',
  'host': '127.0.0.1',  # if your MySQL server is running locally
  'database': 'travel_packages',
  'raise_on_warnings': True
}

def get_packages(query):
    conn = sqlite3.connect('travel_packages.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        packages = cursor.fetchall()
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    
    conn.close()
    return packages

def get_packages2(query):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        packages = cursor.fetchall()
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    
    conn.close()
    return packages

def generate_sql_query(prompt):
    schema_description = """
    The table name is 'packages' and the schema has the following columns:
    - id INTEGER PRIMARY KEY
    - from_city TEXT
    - to_city TEXT
    - package_type TEXT
    - cost INTEGER
    """

    messages = [
        {"role": "system", "content": "You are an assistant that translates natural language queries into SQL queries."},
        {"role": "user", "content": f"Translate the following natural language query into an SQL query and only display the sql code. {schema_description} Query: '{prompt}'"}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    sql_query = response.choices[0].message.content  # Correct way to access the content
    sql_query = sql_query.replace("\n", " ")
    if sql_query[0] == '`':
        return sql_query[7:-5]
    else:
        return sql_query



def get_chatgpt_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content

def detect_intent(question):
    print("intent")
    # Initialize weights
    gpt_weight = 0.8
    similarity_weight = 0.2

    prompt = f"Determine if the following question is a database-related question or a general knowledge question. Strictly give Database or General knowledge:\n\n'{question}'"
    #client = OpenAI(api_key=openai_api_key)
    completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a function. The function decides if the prompt needs access to database to answer query 
                            related to travel information, the db contains information for travel planning 
                            in following tables locations ,         
                1. Packages 
                    Purpose: Details of pre-arranged travel packages.
                    Key Data: Includes ID, from_city, to_city, package_type and cost."""},
                {"role": "user", "content": prompt}
            ]
        )
    output = completion.choices[0].message.content
    if output == "Database":
        return True
    else: 
        return False
    
# def detect_intent(question):
#     # Define keywords that typically indicate a database query
#     db_keywords = ['packages', 'travel', 'booking', 'flight', 'hotel', 'city', 'cost']
    
#     # Check if the question contains any of the database keywords
#     if any(keyword in question.lower() for keyword in db_keywords):
#         return "Database"
#     else:
#         return "General Knowledge"
#     print(completion)
#     gpt_response = completion.choices[0].message.content.strip()
#     print("\n\ngpt_response :", gpt_response)
#     gpt_score = 1 if "database" in gpt_response.lower() else 0

def handle_query(natural_language_query):
    sql_query = generate_sql_query(natural_language_query)
    print("calling handle_query")
    print(sql_query)
    try:
        results = get_packages2(sql_query)
        print(results)
        if results and len(results)!=0:
            response = "Here are the results:\n"
            for row in results:
                response += f"From: {row[1]}, To: {row[2]}, Package: {row[3]}, Cost: ${row[4]}\n"
            return response
        else:
            chatgpt_response = get_chatgpt_response(natural_language_query)
            return chatgpt_response
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Test the functions
    detect_intent("give me the popular tourist destinations around dubai")
    print(handle_query("Show me the packages from Dubai to Tokyo"))



