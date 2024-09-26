import sys
from tests import check, line

result = sys.stdin.read()
print(result)

line()

check("name" in result and "services" in result, "The compose file must be valid")

check("postgres" in result, "postgres service must be defined in the compose file")
check("pgadmin" in result, "pgadmin service must be defined in the compose file")

check("environment" in result, "You must define required environment variables for both of the services")

check("POSTGRES_PASSWORD" in result, "POSTGRES_PASSWORD environment variable is missing")
check("PGADMIN_DEFAULT_EMAIL" in result, "PGADMIN_DEFAULT_EMAIL environment variable is missing")
check("PGADMIN_DEFAULT_PASSWORD" in result, "PGADMIN_DEFAULT_PASSWORD environment variable is missing")

print("Success!")
