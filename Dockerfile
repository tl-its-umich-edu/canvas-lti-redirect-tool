# FROM python:3.10-slim-bookworm

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     build-essential apt-transport-https default-libmysqlclient-dev pkg-config netcat-traditional vim-tiny jq python3-dev git curl && \
#     apt-get upgrade -y && \
#     apt-get clean -y && \
#     rm -rf /var/lib/apt/lists/*

# # Set the working directory    
# WORKDIR /code

# # Sets the local timezone of the docker image
# ARG TZ
# ENV TZ ${TZ:-America/Detroit}
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # EXPOSE port 3000 to allow communication to/from server
# EXPOSE 3000

# # Install dependencies
# COPY requirements.txt /code/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the project code into the container
# COPY . /code/


# Use an official Python runtime image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 3000

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .