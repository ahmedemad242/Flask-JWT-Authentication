# Flask-JWT-Authentication
A simple implementation of ```json web token``` based user authentication in flask which includes the following features:
- Access token
- Refresh Token
- Revoking/ Blacklisting refresh tokens
- Refresh token recycling

## Installation
### Virtual environments

``` 
$ python -m venv venv
$ .\venv\scripts\activate
$ pip install --upgrade pip setuptools wheel
$ pip install -e .[dev]
```

### Running
 
```
$ flask run
```

### Application Structure

```
app/
├── run.py
├── setup.py
├── tests
└── src/FlaskJWT
    ├── config.py
    ├── models
    ├── util
    └── api
        └── auth     
```

## API documentation
The API is documented using Swagger UI. Run server and navigate to ```/api/v1/ui```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
