FROM mysql:8.0

COPY Docker/MySQL/my.cnf /etc/mysql/conf.d/my.cnf
COPY Docker/MySQL/init.sql /docker-entrypoint-initdb.d/
