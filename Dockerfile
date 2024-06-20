FROM python:3.10-slim-bookworm

EXPOSE 6000
WORKDIR /code
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential apt-transport-https libpq-dev netcat-traditional default-libmysqlclient-dev pkg-config python3-dev xmlsec1 git && \
    apt-get upgrade -y

# Install MariaDB from the mariadb repository rather than using Debians 
# https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/
RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash && \
    apt install -y --no-install-recommends libmariadb-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --verbosity 0 --noinput

ARG TZ
ENV TZ ${TZ:-America/Detroit}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["/code/start.sh"]