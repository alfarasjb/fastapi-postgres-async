from src.server import app
import logging
import uvicorn

# More Resources
# https://medium.com/@lawsontaylor/the-ultimate-fastapi-project-setup-fastapi-async-postgres-sqlmodel-pytest-and-docker-ed0c6afea11b

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Note: Uvicorn Issue on trailing slash returning non-ssl link.
# Reference: https://stackoverflow.com/questions/63511413/fastapi-redirection-for-trailing-slash-returns-non-ssl-link
# Solution: Add the flag `--forwareded-allow-ips '*'`
# You can also use FORWARDED_ALLOW_IPS as env var.
if __name__ == "__main__":
    # uvicorn src.main:app --host 0.0.0.0 port 8080 --reload
    uvicorn.run(app=app, host="0.0.0.0", port=8080, reload=True)


