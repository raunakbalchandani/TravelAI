import sqlite3
import openai
import mysql.connector

openai.api_key = 'openai-api-key'

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
    - cost INTEGER
    - package_type TEXT
    
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

    prompt = f"Determine if the following question is a database-related question or a general knowledge question. Strictly give Database or General knowledge:\n\n'{question}'"
    completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """\The function decides if the prompt needs access to database to answer query 
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
                response += f"From: {row[1]}, To: {row[2]}, Cost: ${row[3]}, Package: {row[4]}\n"
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



