# adventodcode-2023

A repo to participate in the AdventOfCode 2023 event.


## Purpose

Good question I don't know either 😊.

## Usage

See [Makefile](./Makefile) for recipes or `make help`.

### Locally

```shell
cd adventofcode
sh testenv.sh
pytest .
```

### Docker

```shell
docker run -i -t --rm --name="adventofcode" -v adventofcode:/tmp -w /tmp python:3.8.14 /bin/bash # Start a container with python
sh testenv.sh
pytest .
```
