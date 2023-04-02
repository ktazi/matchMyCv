## Match my CV

### 1. Description

Match my CV is a university project made for the Engineering project module in 2022-2023.

This is a platform that automates the task of finding the best resume that matches an offer.

### 2. Installation

#### Front end

Navigate to the front_end folder
- `cd front_end`


Install dependencies
- `npm install`

#### Database

Install postgres for your distribution
- you can follow the instructions for your distribution in [here](https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/)


Create a new database
- `createdb -T template0 nouvelle_base -U nameOfuser`


Navigate to the database folder 
- `cd ../database`


Import the sql dump as a backup 
- `pg_restore -d nouvelle_base matchMyCv_database.sql -U nameOfuser`


#### Back end


Navigate to the back_end folder
- `cd ../back_end`


Create a new python 3.10.8 environment (the following instructions are for anaconda environments)
- `conda create --name name_env`   
- `conda activate name_env`
- `conda install python=3.10.8`


Install dependencies
- `pip install -r requirements.txt`


Put in config.json the absolute path to data/api/pdf and data/api/txt


In order to connect to the database, put in app.py instead of the strings

- in line 29 the name of your database 
- in line 30 the name of your postgresql user that accesses the database
- in line 31 the password of the user

#### File server 

Have python 3 installed

#### OCR

Install tesseract 

https://tesseract-ocr.github.io/tessdoc/Installation.html

### 3. Launch the app


#### Back end

Navigate to the front_end folder
- `cd back_end`


Run the line
- `python app.py`

#### File server

Navigate to the data folder
- `cd ../data`


Run the line
- `python http_server.py`

#### Front end

Navigate to the front_end folder
- `cd ../front_end`


Launch the front_end
- `npm run serve`

### 4. Utilization

Go to your web browser and write `http://localhost:8080/`

Note : all the pdf files must be inside the data/api/pdf folders and fetched from there