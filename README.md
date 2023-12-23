# adventodcode-2023

A repo to participate in the AdventOfCode 2023 event.


## Purpose

Good question I don't know either 😊.

Just kidding, it's an example solution implementation for the programming challenge [advent of code 2023](https://adventofcode.com/2023/) in python.

## Usage

See [Makefile](./adventofcode/Makefile).

```shell
cd adventofcode
make help
```

### Locally

```shell
cd adventofcode
make all
#or
python .
```

### Docker

```shell
cd adventofcode
make docker-solution
#or
docker run -i -t --rm --name="adventofcode" -v adventofcode:/tmp -w /tmp python:3.8.14 python .
```
