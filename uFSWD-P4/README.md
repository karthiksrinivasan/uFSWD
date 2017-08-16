# uFSWD-p4
Udacity Full Stack Web Development - Project 4 - Item Catalog

Disclaimer: I have reused some components from my other flask projects.
- Modules setup
- Requirements file
- Jinja macro for rendering bootstrap field

I have also used some of the basic setup from https://github.com/realpython/flask-skeleton

I have used the following python libraries to accomplish certain tasks:
- Flask-OAuthlib - For authenticating via google services
- Flask-Script - For managing the application using run.py
- Flask-SQLAlchemy - For creating ORM for tables in SQLlite
- Flask-WTF - For generating forms and validation
- Flask-Login - For managing login sessions
- Flask-Restless - For generating a JSON endpoint

# Instructions:
-
- Setup Virtual Environment:
  ```sh
  virtualenv -p python3 env ; source env/bin/activate
  ```
- Install python requirements
  ```sh
  pip install -r requirements
  ```
- Add Google Client ID
  ```sh
  Edit app/config.py with right google credentials
  ```  
- Initialize Database
  ```sh
  ./run.py db_initialize
  ```
- Run the application:
  ```sh
  ./run.py runserver -h 0.0.0.0 -p 8080
  ```
- Open the webpage: http://localhost:8080/
- Open Json endpoint:
  - Categories: http://localhost:8080/api/v1/catalog
  - Items: http://localhost:8080/api/v1/items
