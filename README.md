# Hospital Appointment Management System

This is a class-project to simulate a hospital appointment system using **Python** and **PostgreSQL / PLpgSQL**. The system allows for managing patients, doctors, and appointments via SQL stored procedures and a Python wrapper for interaction.

## Features

- Add / remove / update patients  
- Add / remove / update doctors  
- Schedule appointments (while checking for conflicts)  
- View upcoming appointments by doctor or patient  
- View all doctors, all patients  
- Basic reporting (e.g. number of appointments per doctor)  
- Error handling (invalid inputs, scheduling conflicts, etc.)

## Architecture & Design

- `schema.sql` contains:  
   - Database schema (tables: patients, doctors, appointments)  
   - Stored procedures, functions, and views for key operations  
- `Hospital Appointment Management System.py` contains:  
   - Python code that connects to the database  
   - Functions that execute SQL operations  
   - Command-line interface or script logic for calling those functions  

## Setup / Installation

1. Install **PostgreSQL** (version X.Y)  
2. Create a new database, e.g. `hospital_db`  
3. Run the `schema.sql` script to set up the tables, procedures, etc  
   ```bash
   psql -U <username> -d hospital_db -f schema.sql
