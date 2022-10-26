from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = (
    "Simple implementation of json web token based user authentication in flask."
)

APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Ahmed Emad"
AUTHOR_EMAIL = "ahmedemmahmoud@gmail.com"
PROJECT_URLS = {
    "Documentation": "https://github.com/ahmedemad242/Flask-JWT-Authentication/blob/main/README.md",
    "Bug Tracker": "https://github.com/ahmedemad242/Flask-JWT-Authentication/issues",
    "Source Code": "https://github.com/ahmedemad242/Flask-JWT-Authentication",
}
INSTALL_REQUIRES = [
    "Flask==2.1.0",
    "Flask-Bcrypt",
    "Flask-Cors",
    "Flask-Migrate",
    "flask-restx",
    "Flask-SQLAlchemy",
    "PyJWT",
    "python-dateutil",
    "python-dotenv",
    "requests",
    "urllib3",
    "werkzeug==2.1.2",
    "psycopg2",
]

EXTRAS_REQUIRE = {
    "dev": [
        "black",
        "flake8",
        "pre-commit",
        "pydocstyle",
        "pytest",
        "pytest-clarity",
        "pytest-dotenv",
        "pytest-flask",
        "tox",
    ]
}

setup(
    name="Flask-JWT-Authentication",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/ahmedemad242/Flask-JWT-Authentication",
    project_urls=PROJECT_URLS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
