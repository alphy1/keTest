# keTest

## To run the application:
1. Clone the repository: 
```git clone https://github.com/alphy1/keTest```
2. Create file `secret_key.json` with the `SECRET_KEY` for django. If file is not present, the `SECRET_KEY` will be generated automatically.
Example:
```
{
  "SECRET_KEY": <YOUR SECRET KEY>
}
```
3. Run docker-compose:
```docker-compose up```
4. Go to this url to see admin panel: `http://0.0.0.0:8000/admin`
5. Use the following credentials to login:
```
login: admin
password: 11223344
```
