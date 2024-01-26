# 🚀 Job Scraper

![GitHub release (latest by date)](https://img.shields.io/github/v/release/MarcCG0/jobboard-scraper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



## Overview
This project is a job scraper designed to extract job listings from various websites, currently supporting LinkedIn. It allows users to search for jobs based on specific locations and keywords.

## Prerequisites
- Python 3
- Docker (optional, for running the project using Docker)
- PostgreSQL

## Local Installation and Setup
1. **Clone the repository**
    ```bash
    git clone https://github.com/MarcCG0/job-scraper/edit/main/README.md
    cd job-scraper
    ```

2. **Install dependencies** (Skip this step if using Docker)
    ```bash
    pip install -r requirements.txt
    ```
    or
   ```bash
   poetry shell
   poetry install
   ```

4. **Environment Configuration**
    - Set up your database and other environment settings.

## Usage

### Running Locally
To run the scraper locally, use the following command:

```bash
python3 main.py --location "Barcelona" --keywords "Software Engineer"
```

Will scrape all the open Software Engineer positions in Barcelona. 

### Running with Docker
To run the scraper using Docker, use the following commands:

```bash
docker-compose build
docker-compose up
```

## Database Configuration
The scraper uses PostgreSQL for data storage. Here are some basic commands and configurations:

### Accessing the Database
- **Local Database:**
    - Host: `localhost`
- **Docker Container Database:**
    - Host: `db`

### Basic PSQL Commands
- Connect to the database:
    ```bash
    psql -U username -d database_name
    ```
## License
MIT License

Copyright (c) 2023 Marc Camps




