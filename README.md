# Test task: 
## Web service for cash movement management (CMM)
____
### how to run:
**Option 1 with docker**    
1. Install docker
2. Clone the repository
3. Create .env file (copy from .env.example) and fill it by example
4. Run `docker compose up`
5. Open http://localhost:80/admin in browser
6. Login with `admin` and `admin`
7. Also you can visit:
 - http://localhost:80/swagger/ - for swagger documentation
 - http://localhost:80/redoc/ - for redoc documentation
 - http://localhost:80/api - from here u can use endpoints for your project
8. After that you can run `docker-compose down` to stop the service

**Option 2 manually**
1. Clone the repository
2. Activate virtual environment (`source venv/bin/activate`). 
Create it if it doesn't exist by typing `python3 -m venv venv`
3. Create .env file (copy from .env.example) and fill it by example
4. Install requirements (`pip install -r requirements.txt`)
5. Run `python manage.py migrate` to create database
6. Run `python manage.py create_example_data` to create example data
7. Run `python manage.py runserver 0.0.0.0:8000`
8. Open http://localhost:8000/admin in browser
9. Login with `admin` and `admin`
10. Also you can visit:
 - http://localhost:80/swagger/ - for swagger documentation
 - http://localhost:80/redoc/ - for redoc documentation
 - http://localhost:80/api - from here u can use endpoints for your project
11. To stop the server run type `CTRL+C` in console


## About project:
- The project uses django admin as main interface
- Project provides REST API for interacting with the database
- Project provides swagger and redoc documentation
- Project provides example data


```
Models:
    Transaction
        - date - The date of creation of the record is filled out automatically, but can be changed manually.
        - status - Status of the transaction. Foreign key.
        - type - Type of the transaction. Foreign key.
        - category - Contains category of transaction. Foreign key.
        - subcategory - Contains subcategory of transaction. Foreign key. 
            Note: Subcategory is regular category with not null parent_category
        - amount - Amount of funds in rubles. Specified with an accuracy of two decimal places.
        - description - free-form commentary to the entry (optional).
    
    Status
        - name - Name of the status. Example: "Бизнес" "Личное" "Налог"
    
    Type
        - name - Name of the type. Example: "Пополнение" "Списание"
    
    Category
        - name - Name of the category. Example: "VPS" "Avito"
        - parent_category - Parent category (optional). Example: "Инфраструктура" "Маркетинг"
        
```
