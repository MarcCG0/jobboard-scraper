from typing import List

import psycopg2

from src.models.jobopportunity.models import JobOpportunity


class PsqlDBLoader:
    """Connection via terminal:
    1. Install desktop PSQL
    2. bash: psql -U user_name -d database_name
    3. Once inside the DB, query SQL to do whatever
    """

    def __init__(
        self,
        database_host: str,
        database_name: str,
        user: str,
        password: str,
        table_name: str,
    ):
        """Initialize the PsqlDBloader."""
        self.database_host = database_host
        self.database_name = database_name
        self.user = user
        self.password = password
        self.table_name = table_name

    def load_jobs(self, scraped_jobs: List[JobOpportunity]):
        db_params = {
            "host": self.database_host,
            "database": self.database_name,
            "user": self.user,
            "password": self.password,
        }

        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            table_name = self.table_name

            for job_opportunity in scraped_jobs:
                # Assuming job_opportunity.model_dump() returns a dictionary
                document = job_opportunity.model_dump()

                # Construct an INSERT query
                insert_query = f"INSERT INTO {table_name} ({', '.join(document.keys())}) VALUES ({', '.join(['%s'] * len(document))})"

                # Execute the INSERT query
                cursor.execute(insert_query, list(document.values()))

            # Commit changes and close the connection
            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            print(f"Error: {e}")
