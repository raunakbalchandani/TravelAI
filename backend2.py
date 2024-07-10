import sqlite3
import openai

# Initialize OpenAI client
openai.api_key = 'YOUR_API_KEY'

def get_packages(sql_query):
    conn = sqlite3.connect('travel_packages.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        return cursor.fetchall()
    finally:
        conn.close()

def generate_sql_query(prompt):
    response = openai.chat.completions.create(
        engine="text-davinci-003",  # Use an appropriate engine for SQL generation
        prompt=f"Translate this into a SQL query: {prompt}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

def handle_query(natural_language_query):
    if "package" in natural_language_query.lower():
        # Generate SQL query from natural language
        sql_query = generate_sql_query(natural_language_query)
        results = get_packages(sql_query)
        if results:
            return "\n".join(f"From: {row[1]}, To: {row[2]}, Package: {row[3]}, Cost: ${row[4]}" for row in results)
        return "No packages found matching your query."
    else:
        # Handle general queries with GPT-3.5
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=natural_language_query,
            max_tokens=100
        )
        return response.choices[0].text.strip()

if __name__ == "__main__":
    print(handle_query("Show me the packages from Mumbai to London"))
    print(handle_query("Tell me a joke"))
