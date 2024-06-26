FROM apache/airflow:2.9.1-python3.11 as baselinux
#pinned to airflow 2.3.2 for compatability with dbt-core
#FROM apache/airflow:latest-python3.9 AS builder

USER root

RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https 
# mssql-tools unixodbc-dev

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc



# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - 
# && curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

# RUN sed -i -E 's/(CipherString\s*=\s*DEFAULT@SECLEVEL=)2/\11/' /etc/ssl/openssl.cnf \
# && source ~/.bashrc

# FROM baseunix as sqlserver

# RUN apt-get install -y unixodbc
# RUN sudo apt-get update

# RUN curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18


# FROM sqlserver as requirements

# RUN python3.11 -m pip install -U pip setuptools && \
#     python3.11 -m pip install poetry==1.8.3

# COPY pyproject.toml poetry.lock ./
# RUN poetry export -f requirements.txt --without-hashes -o /requirements.txt 

FROM baselinux as app
USER airflow
RUN python3.11 -m pip install -U pip setuptools
# RUN python3.11 -m venv dbt_venv && source dbt_venv/bin/activate && \
#     python3.11 -m pip install --no-cache-dir dbt-sqlserver && deactivate



COPY requirements.txt .

RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# RUN apt-get purge -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*




