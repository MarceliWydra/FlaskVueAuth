# Flask + Vue.js Auth example



## Setup Flask APP

1. Clone repository
2. Install Flask dependencies

```sh
$ pip install requirements.txt

```
3. Init database

Create the tables and run the migrations:

```sh
$ python run.py create_db
$ python run.py db init
$ python run.py db migrate
```

4. Create example user

```sh
$ python run.py create_users
```
### Run the Application

```sh
$ python run.py runserver
```

### Testing

```sh
$ python run.py tests
```

## Setup Vue APP
```sh
$ cd client
$ yarn install
```
## Run Vue APP
```sh
$ yarn run serve
```
