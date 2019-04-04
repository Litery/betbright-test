# Solution to the test supplied during recruitment process

### Setup
#### To run the cli tool
> docker-compose build

> docker-compose up

> docker-compose exec app /bin/bash

> ./run_app.sh

The cli is documented with argparse, making --help or -h very useful.

Validation is non restrictive for entities making all fields optional, 
but also making it easier to play around.

#### To run tests

> docker-compose -c docker-compose-tests.yml build

> docker-compose -c docker-compose-tests.yml up

### Notes
Due to the limit of ORM usage I decided on using aioredis and simple 
serialization of Python dataclasses to store data to avoid difficult 
and finicky parts of the ORM: mapping, relationships, migrations, 
transactions, query building and problems of overall rigidity of SQL.

Solution resulting from these decisions was quite interesting for me to write,
and very flexible. The next thing to implement would be some form of joining in repositories, to 
populate related entity's fields with children instances during querying and possibly allowing for
nested filtering.


### Frameworks used worth mentioning
**aioredis** - for communication with redis

**asynctest** - to ease up testing asynchronous code

**injector** - increasing QoL with dependency injection