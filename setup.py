from setuptools import setup, find_packages

setup(
    name="wise_pair",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.3.3",
        "flask-sqlalchemy==3.1.1",
        "flask-migrate==4.0.5",
        "sqlalchemy==2.0.25",
        "psycopg2-binary==2.9.9",
        "flask-jwt-extended==4.6.0",
        "boto3==1.34.36",
        "python-dotenv==1.0.1",
        "pydantic==2.5.3",
        "werkzeug==2.3.7",
        "minio==7.2.0",
        "email-validator==2.1.0.post1",
        "flask-cors==4.0.0",
        "pytest==7.4.3",
        "alembic==1.13.1",
        "Pillow==10.1.0",
    ],
) 