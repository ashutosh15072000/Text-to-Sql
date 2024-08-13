from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini model and generate SQL query
def get_gemini_response(question, prompt):
    """
    Generate an SQL query based on the input question using the Gemini model.

    Args:
        question (str): The input question to convert to an SQL query.
        prompt (list): A list containing the prompt to guide the Gemini model.

    Returns:
        str: The generated SQL query.

    Example:
        >>> prompt = ["You are an expert in Converting English questions to SQL code! ..."]
        >>> question = "How many entries of records are presents?"
        >>> get_gemini_response(question, prompt)
        "SELECT COUNT(*) FROM STUDENT;"
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve query from the database
def read_sql_query(sql, db):
    """
    Execute an SQL query on a database and return the results.

    Args:
        sql (str): The SQL query to execute.
        db (str): The path to the database file.

    Returns:
        list: A list of tuples containing the query results.

    Example:
        >>> sql = "SELECT * FROM STUDENT;"
        >>> db = "student.db"
        >>> read_sql_query(sql, db)
        [(1, 'John', 20), (2, 'Jane', 22), ...]
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

### Define Your Prompt
prompt = [
    '''
    You are an expert in Converting English questions to SQL code!
    The SQL Database has the name STUDENT and has the following columns - NAME, CLASS, AGE
    For Example 1 - How many entries of records are presents?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
    also the sql code should not have ``` in beginning or end and sql word in output 
    ''' 
]

st.set_page_config(page_title="I can Retrieve Any SQL Query")

st.header("Gemini App to :blue[Retrieve SQL Data] 📰")

question = st.text_input(":blue[INPUT:] ", key="input")

submit = st.button("Answer")


## if submit is clicked
if submit:
    sql = get_gemini_response(question, prompt)
    st.subheader(":blue[Sql Command] For Above Question Using :blue[Gemini Pro] 💻",divider="orange")
    st.code(sql,language="sql")

    st.subheader("OUTPUT FROM  THE :blue[DATABASE 🔎]",divider="orange")
    rows = read_sql_query(sql,"student.db")
    for row in rows:
        st.markdown(row)
explain=st.button("Explaintion of the Query")
if explain:
        prompt_sql_command_explantion=['''
Explain the SQL command: \n\n
Break down the SQL command: into its components.\n\n 
Explain the function of each part and how they work together.\n\n 
Analyze the SQL command: in terms of its efficiency and potential performance implications.\n\n
Are there alternative ways to achieve the same result with better performance?\n\n
query is given at end \n\n
{sql}
''']
        explantion_of_the_query=get_gemini_response(question,prompt_sql_command_explantion)
        st.markdown(explantion_of_the_query)
