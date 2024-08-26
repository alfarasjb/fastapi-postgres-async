# Dockerfile
# Use the pgvector image as the base
FROM pgvector/pgvector:pg16

# Copy initialization scripts (if any)
COPY ./docker/pgvector/init-db.sh /docker-entrypoint-initdb.d/

# Make sure scripts in docker-entrypoint-initdb.d are executable
RUN chmod a+x /docker-entrypoint-initdb.d/*.sh