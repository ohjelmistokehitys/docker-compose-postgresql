# Docker Compose and PostgreSQL

The goal of this assignment is to get familiar with core Docker and Docker Compose concepts and features, such as volumes, ports, and environment variables. At the same time, we get to work with real tools like PostgreSQL and pgAdmin.

In this assignment, we use the [**PostgreSQL** database](https://hub.docker.com/_/postgres) and the [**pgAdmin** administration tool](https://www.pgadmin.org/), but the same principles can also be applied to other databases. The assignment is quite similar to the Docker Compose example shown in the [PostgreSQL Docker image documentation](https://hub.docker.com/_/postgres) and the example in Docker’s blog post [How to Use the Postgres Docker Official Image](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/). The clearest difference is that this assignment uses pgAdmin to manage the database, while the examples above use [Adminer](https://hub.docker.com/_/adminer/).


## Recommended background material

* [How to Use the Postgres Docker Official Image (docker.com)](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/)
* [`docker compose` CLI reference (docker.com)](https://docs.docker.com/reference/cli/docker/compose/)
* [Compose file reference (docker.com)](https://docs.docker.com/reference/compose-file/)
* [DevOps with Docker, chapter 3 (mooc.fi)](https://courses.mooc.fi/org/uh-cs/courses/devops-with-docker/chapter-3)
* [Docker Compose will BLOW your MIND!! (YouTube, NetworkChuck)](https://youtu.be/DM65_JyGxCo)


## Why Docker Compose?

Docker Compose is often a better choice than writing separate `docker run` commands, especially when there are multiple services to start. Docker Compose simplifies managing complex environments with a single YAML file. This makes setting up the environment easier and less error-prone when all configurations and dependencies are in one place.

Docker Compose manages volumes and networks automatically and, among other things, connects all services defined in the same file to the same network so they can communicate with each other. Sharing the same YAML file with others, for example through version control, is also smooth and reduces differences between different developers’ environments and other environments.


## PostgreSQL

PostgreSQL is a popular open-source relational database that can be used for a wide range of purposes:

> *PostgreSQL, often simply "Postgres", is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards-compliance. As a database server, its primary function is to store data, securely and supporting best practices, and retrieve it later, as requested by other software applications, be it those on the same computer or those running on another computer across a network (including the Internet). It can handle workloads ranging from small single-machine applications to large Internet-facing applications with many concurrent users.*
>
> What is PostgreSQL? https://hub.docker.com/_/postgres

PostgreSQL is available as a ready-made Docker image in the Docker Hub container registry: https://hub.docker.com/_/postgres. In this assignment, you only need to use the ready-made image and read its documentation. Dockerfiles are not needed in this exercise.


# Assignment: installing a database server and an administration UI

When developing an application, you often need a separate database with test data so you can modify it freely without affecting other users or developers. In this assignment, you will use a Docker Compose file to create an environment where PostgreSQL runs in a container, the database is initialized to the desired starting state, data persists regardless of the container lifecycle, and you can manage the database with a tool called pgAdmin.

> *"While it’s possible to use the Postgres Official Image in production, Docker Postgres containers are best suited for local development. This lets you use tools like Docker Compose to collectively manage your services. You aren’t forced to juggle multiple database containers at scale, which can be challenging."*
>
> Tyler Charboneau, 2022. [How to Use the Postgres Docker Official Image](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/)

The Docker Compose setup in this assignment is well suited for **development environments**, where you need a quickly available database. There are differing opinions about containerizing databases in production environments. Some support using containers for production databases because containers are easy to move and scale. Others oppose the idea because databases may require more complex management and performance tuning, which can be challenging in container-based environments.


## docker-compose.yml

This assignment repository already contains a [docker-compose.yml](./docker-compose.yml) file where all Docker definitions for this task should be written. Always test your solutions first with `docker compose up`, and stop services with `docker compose down` before the next attempt. You can find other possible commands in the [`docker compose` command documentation](https://docs.docker.com/reference/cli/docker/compose/).

The [docker-compose.yml](./docker-compose.yml) file already contains two services: `postgres` and `pgadmin`:

```yaml
services:
  postgres:
    image: postgres:latest        # https://hub.docker.com/_/postgres
    container_name: database

  pgadmin:
    image: dpage/pgadmin4:latest  # https://hub.docker.com/r/dpage/pgadmin4/
    container_name: database-admin
```

Both **services** are based on ready-made Docker images. Service names (`postgres` and `pgadmin`) can be chosen freely, and the services can connect to each other using those names:

> *"By default, any service can reach any other service at that service's name."*
>
> https://docs.docker.com/compose/networking/#link-containers

`container_name` defines the name you can use yourself when running Docker commands against running containers.


## Part 1: starting services and environment variables (20%)

Try starting the services defined in [docker-compose.yml](./docker-compose.yml) with `docker compose up`. Docker automatically pulls the required images and creates containers from them. The containers start, but soon crash because required environment variables such as passwords are missing.

Read the error messages printed by the containers and the PostgreSQL Docker image documentation at https://hub.docker.com/_/postgres. Documentation for pgAdmin 4 is available at https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html. From these sources, you can find the required **environment variables** that must be set when starting containers.

Next, define [`environment` blocks](https://docs.docker.com/reference/compose-file/services/) for both services in [docker-compose.yml](./docker-compose.yml), and add the required environment variables mentioned in the documentation. You can also find hints about required variables in the error messages from `docker compose up`. Optional environment variables do not need to be set, so in the simplest case only a few variables are needed.

Set passwords and usernames to secure random strings that you do not use elsewhere. You can use, for example, the [F‑Secure Strong Password Generator](https://www.f-secure.com/en/password-generator) service to create passwords.

After setting the required environment variables, run `docker compose up` again. The `database` container should now print `database system is ready to accept connections` to the logs, and `database-admin` should print `[INFO] Listening at: http://[::]:80 (1)`. Note that the first startup of the pgAdmin container takes quite a while.

💡 *In general, storing passwords and usernames in a YAML file and adding them to version control is a bad idea. We will fix this later in the assignment.*


## Part 2: volumes (20%)

### `/var/lib/postgresql/data`

Next, we want PostgreSQL database data to remain available regardless of whether containers are stopped or removed. This is done by using a Docker **volume**, which stores data on the host system.

So, define a `volume` for the database service so that an external volume is mounted to `/var/lib/postgresql/data` inside the container. This ensures database data is preserved even if the container is removed. You can find more guidance, for example, in the article [How to Use the Postgres Docker Official Image](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/).

### `/docker-entrypoint-initdb.d/`

PostgreSQL supports automatic database initialization when it is started for the first time. In the documentation, this feature is referred to as an **initialization script**. In practice, on first startup, the container scans a specific directory for SQL and shell scripts, which lets us initialize database contents to the desired starting state:

> *"If you would like to do additional initialization in an image derived from this one, add one or more \*.sql, \*.sql.gz, or \*.sh scripts under /docker-entrypoint-initdb.d (creating the directory if necessary). After the entrypoint calls initdb to create the default postgres user and database, it will run any \*.sql files, run any executable \*.sh scripts, and source any non-executable \*.sh scripts found in that directory to do further initialization before starting the service."*
>
> Initialization scripts. https://hub.docker.com/_/postgres

In this assignment, we want to automatically add the **Chinook sample database** to the database server. Its creation script is already available in this repository’s [`sql` directory](./sql/). Mount the host machine’s `./sql` directory into the database service as `/docker-entrypoint-initdb.d/`, so the database is initialized automatically.

### Restart

Finally, stop the services you started with `docker compose down` and start them again with `docker compose up`. This time, the terminal should show many log lines from the `postgres` service stating that tables and rows are being created in the database (*CREATE TABLE* and *INSERT*).

> [!TIP]
> Add both volumes to the YAML file at once, and only then start the services. If you first define the `/var/lib/postgresql/data` volume and start the database, the database will be initialized empty, and initialization scripts will no longer have any effect on later startups.
>
> If this has already happened and the database was initialized empty, you can remove volumes and start services once more:
>
> ```sh
> docker compose down --volumes
> docker compose up
> ```


## Part 3: `exec`, `psql`, and database queries (20%)

The **Chinook** database used above is an open [MIT-licensed](https://github.com/lerocha/chinook-database/blob/master/LICENSE.md) sample database containing music store data such as artists, albums, tracks, and customers. It is designed to provide a realistic yet simple database structure that is useful for practicing SQL queries and database administration. In this assignment, Chinook is used because its contents are diverse and easy to understand.

After you start the containers defined in [docker-compose.yml](./docker-compose.yml), they are visible in Docker commands just like containers started without Compose.

Run `docker ps` and verify the containers are running. The PostgreSQL container name (*container_name*) is set to `database` in the YAML file, so you can open a bash shell inside that container with the following command:

```
docker exec -it database /bin/bash
root@a1b2c3d4:/#
```

To use PostgreSQL from the command line, you can use the `psql` tool. `psql` allows running queries and other database operations from the command line, which is often useful especially during development. `psql` comes preinstalled in the official PostgreSQL Docker image.

Once you have the bash prompt open (that is, you see a prompt similar to the example above), you can use `psql` either in interactive mode or by running individual queries with `-c`. Try the following query, which searches for all tracks whose name contains either `hello` or `world`:

```sh
# if you set a username with the POSTGRES_USER environment variable:
psql -U $POSTGRES_USER -d chinook_auto_increment -c "SELECT name FROM Track WHERE name ILIKE '%hello%' OR name ILIKE '%world%'"

# if you did not set POSTGRES_USER (default username is `postgres`)
psql -U postgres -d chinook_auto_increment -c "SELECT name FROM Track WHERE name ILIKE '%hello%' OR name ILIKE '%world%'"
```

In the commands above, the database username is set with the `-U` parameter. If you defined a username in the Compose file environment variables, you can use it here. Otherwise, use the default username `postgres`. The `-d` parameter defines the database name, which in this case is `chinook_auto_increment`. The database name is defined in [sql/Chinook_PostgreSql_AutoIncrementPKs.sql](./sql/Chinook_PostgreSql_AutoIncrementPKs.sql). Finally, the `-c` parameter defines the SQL query to run.


**Save the list of track names printed by the command into [hello-world.txt](./hello-world.txt).**

💡 *You can save output either by copying text to the clipboard and pasting it into a file, or by redirecting output directly to a file with the `>` operator. If you redirect output to a file, you can copy the file “out” of the container using the [`docker cp` command](https://docs.docker.com/reference/cli/docker/container/cp/). You could also mount `hello-world.txt` into the container with a volume, but that is not required.*


## Part 4: opening ports (20%)

The PostgreSQL container listens on port **5432** by default, and the pgadmin4 container on port **80**. Publish these ports from containers to the host by adding `ports` definitions for both services in [docker-compose.yml](./docker-compose.yml).

> [!TIP]
> On the host, you can use any ports: they do not need to be the same as container internal ports. You can also bind ports only to `127.0.0.1`, in which case these containers should not be visible outside your machine.

You can now try starting services with `docker compose up`. You should now be able to access the pgAdmin container web UI in your browser using the host port you mapped for the `database-admin` service. Note that first startup of the pgadmin service takes quite a long time, so wait at least until the terminal reports that it is listening internally on port 80.


## Part 5: pgAdmin 4

[**pgAdmin 4**](https://www.pgadmin.org/) is a web-based graphical administration tool for PostgreSQL databases. It allows developers to run SQL queries, inspect database tables, and manage users and database settings without relying only on command-line tools.

> *pgAdmin is a management tool for [PostgreSQL](https://www.postgresql.org/) and derivative relational databases such as [EnterpriseDB's](https://www.enterprisedb.com/) EDB Advanced Server. It may be run either as a web or desktop application. For more information on the features offered, please see the [Features](https://www.pgadmin.org/features/) and [Screenshots](https://www.pgadmin.org/screenshots/) pages.*
>
> What is pgAdmin 4? https://www.pgadmin.org/faq/

Try signing in to pgAdmin in your web browser using the email and password you set in the pgAdmin container environment variables.

Signing in to the pgAdmin tool itself does not yet connect to the database; that connection must be configured separately. You can add database server details from the Dashboard view via the “Add new server” link. By default, services defined in the same Docker Compose file can connect to each other directly by service name, so use `postgres` as the database host name/address. Use the same username and password you set earlier for the Postgres container. If you did not define a username, the default username is `postgres`.

You can find more detailed instructions for using pgAdmin through search engines and in the tool’s own documentation. You can start, for example, with [pgAdmin Tutorial - How to Use pgAdmin (YouTube, Database Star)](https://youtu.be/WFT5MaZN6g4?feature=shared&t=160). However, for this assignment, you do not need to use pgAdmin to manipulate the database; it is enough to sign in and successfully establish a connection.

🔐 *In production, databases are usually administered in other ways, such as command-line tools or automated processes, and a graphical UI may not be used. If pgAdmin or a similar admin tool were used in production, access to it should be restricted very carefully.*


### 🚀 Extra: pgAdmin and servers.json

Database server settings can be added to pgAdmin automatically so that you do not need to enter them manually in the web UI. This can be done with the `/pgadmin4/servers.json` file, which can be mounted into the container as a volume. You can find additional information about using `servers.json` with Docker Compose, for example, in [this StackOverflow discussion](https://stackoverflow.com/a/64626964). If you want, you can define database settings using that file.

This assignment repository includes a ready-made [servers.json example file](./servers.json) that you can use as a starting point. The username defined in the file must be updated if you set a name other than `postgres` in earlier steps. A description of the JSON format is available in [pgAdmin’s own documentation](https://www.pgadmin.org/docs/pgadmin4/latest/import_export_servers.html#json-format).

Note that changes to `servers.json` do not take effect automatically in already existing containers, so after adding the volume you need to recreate the container (`docker compose down`):

> *"Note that server definitions are only loaded on first launch, i.e. when the configuration database is created, and not on subsequent launches using the same configuration database."*
>
> /pgadmin4/servers.json. https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#mapped-files-and-directories


## Part 6: managing secrets with a .env file (20%)

Storing secrets, such as usernames and passwords, directly in a Docker Compose file is not secure, because the Compose file is intended to be stored in version control and shared between parties. Also, different environments usually require different settings, so for that reason too, changing values should not be hardcoded.

Next, environment variables must be moved to a separate `.env` file, which is not added to version control. `.env` is already listed in this assignment’s [.gitignore](./.gitignore), so it should not accidentally end up in version control.

**Create a new file named .env** in this directory and add the required secrets for both services, for example in this format:

```
# These are just sample passwords, never use them in a real project

# postgres
POSTGRES_USER=null_pointer_expert
POSTGRES_PASSWORD=zt7kYOwBv527uFLj5bf5M3K4SIIhcP01

# pgadmin
PGADMIN_DEFAULT_EMAIL=datasaurus_rex@example.com
PGADMIN_DEFAULT_PASSWORD=Xjyl7THN5Kiz86F7PI7mz1s6Yf436GtD
```

**Update the docker-compose.yml file** to use environment variables from `.env`. Add `env_file` blocks for both services. Also replace hardcoded values with environment variable references, or remove individual variables from the YAML file entirely:

```yaml
services:
  postgres:
    image: postgres:latest
    container_name: database
    # ...

    env_file: ".env"

    # variables can now reference values from the file, or be removed entirely:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
...
```

You can find more information in [Docker Compose documentation](https://docs.docker.com/compose/environment-variables/set-environment-variables/#use-the-env_file-attribute).

💡 *With Docker Compose, you could also use different .env files for different services. However, for this assignment’s automatic grading, it is important that you use only a file named `.env`.*


> [!IMPORTANT]
> If you use different usernames or passwords at this stage than before, you may need to recreate containers (`docker compose down`) and remove the volume (`docker volume rm`) for changes to take effect. This is because passwords provided through environment variables are used, for example, during database initialization, and changing an environment variable does not change saved user data.
>
> > *"the Docker specific variables will only have an effect if you start the container with a data directory that is empty; any pre-existing database will be left untouched on container startup.*"
> >
> > postgres. Docker Official Image. https://hub.docker.com/_/postgres


## Submitting solutions

When you have solved part or all of the tasks and committed your answers, submit your solutions for evaluation with `git push`. Git push automatically triggers a workflow that tests all your commands and returns either a pass or fail result.

After GitHub Actions has checked your solution, you can see the result on your repository’s [Actions tab](../../actions/workflows/classroom.yml). The evaluation typically takes a couple of minutes.

By opening the latest “GitHub Classroom Workflow” run from the link above, you can see detailed grading information. At the bottom of the page, you can see your points. By clicking the “Autograding” heading, you can inspect the grading steps and their results in more detail.


# Licenses

## Docker

> "The Docker Engine is licensed under the Apache License, Version 2.0. See LICENSE for the full license text."
>
> "However, for commercial use of Docker Engine obtained via Docker Desktop within larger enterprises (exceeding 250 employees OR with annual revenue surpassing $10 million USD), a paid subscription is required."
>
> https://docs.docker.com/engine/


## PostgreSQL

> "PostgreSQL is released under the PostgreSQL License, a liberal Open Source license, similar to the BSD or MIT licenses."
>
> https://www.postgresql.org/about/licence/


## pgAdmin

> "pgAdmin 4 is released under the PostgreSQL licence."
>
> https://www.pgadmin.org/licence/


## Chinook database

The Chinook database was created by [Luis Rocha](https://github.com/lerocha) and is licensed under the [MIT License](https://github.com/lerocha/chinook-database/blob/master/LICENSE.md).


## This learning material

This assignment was developed by Teemu Havulinna and is licensed under the [Creative Commons BY-NC-SA license](https://creativecommons.org/licenses/by-nc-sa/4.0/).

ChatGPT language model and GitHub Copilot AI assistant were used in implementing the assignment text, source code, and tests.
