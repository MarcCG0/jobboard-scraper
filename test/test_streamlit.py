import streamlit as st
import psycopg2
import pandas as pd


def connect_to_db():
    return psycopg2.connect(
        host="localhost" ,  
        database="jobopportunities",
        user="marc",
        password="password",
    )


def load_data():
    conn = connect_to_db()
    query = "SELECT * FROM job_opportunities"
    data = pd.read_sql(query, conn)
    conn.close()
    return data


def main():
    st.title("Job Opportunities Database Viewer")
    st.write("Viewing data from the job opportunities table:")

    try:
        data = load_data()
        st.write(data)
    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
