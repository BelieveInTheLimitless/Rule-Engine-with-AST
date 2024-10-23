# Rule-Engine-with-AST
A simple 3-tier rule engine application(Simple UI, API and Backend, Data) to determine user eligibility based on attributes like age, department, income, spend etc. The system uses Abstract Syntax Tree (AST) to represent conditional rules and allow for dynamic creation,combination, and modification of these rules.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)

## Features
- create_rule(rule_string): This function takes a string representing a rule and returns a Node object representing the corresponding AST.
- combine_rules(rules): This function takes a list of rule strings and combines them into a single AST.
- evaluate_rule(JSON data): This function takes a JSON representing the combined rule's AST and a dictionary data containing attributes (e.g., data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}).
  
## Technologies Used
- Python3
- HTML-CSS
- Flask
- Flask-SQLAlchemy
- MySQL (SQLAlchemy + PyMySQL client + Cryptography)
- Docker (v27.3.1)
- DockerCompose (v2.29.7)
- Linux (Ubuntu 24.04)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/BelieveInTheLimitless/Rule-Engine-with-AST
cd Rule-Engine-with-AST
```

### 2. Database Configuration
```bash
# Making sure MySQL is not interacting already
sudo systemctl stop mysql
```

### 3.Building and running the docker container
```bash
docker compose up --build
# This step may take a while to complete the database setup, have some snacks handy with you :)
```

### 4. Running the front-end application
```bash
#open
http://127.0.0.1:5000/
```

### 4. Exiting the application
```bash
# CTRL + C to stop the running container
docker compose down
```

## API Endpoints

- **Create rule**
  
  ![Screenshot from 2024-10-23 23-10-50](https://github.com/user-attachments/assets/55d26df5-a19a-4595-a464-c3631a510956)

- **Combine rules**
  
  ![Screenshot from 2024-10-23 23-11-01](https://github.com/user-attachments/assets/bfdc2a33-63a4-4c4b-8bed-57375f58e31e)

- **Evaluate rule**
  
  ![Screenshot from 2024-10-23 23-11-09](https://github.com/user-attachments/assets/044b28ab-c3ff-411b-bf30-1994465af0dc)


