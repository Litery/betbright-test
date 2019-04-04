# Solution to the test supplied during recruitment process

### Setup
To run the cli tool
> docker-compose build

> docker-compose up

> docker-compose exec app /bin/bash

> ./run_app.sh

To run tests

> docker-compose -c docker-compose-tests.yml build

> docker-compose -c docker-compose-tests.yml up

### Notes
Due to the limit of ORM usage I decided on using aioredis and simple 
serialization of Python dataclasses to store data to avoid difficult 
and finicky parts of the ORM: mapping, relationships, migrations, 
transactions, query building and problems of overall rigidity of SQL.

### Frameworks used worth mentioning
**aioredis** - for communication with redis

**asynctest** - to ease up testing asynchronous code

**injector** - increasing QoL with dependency injection