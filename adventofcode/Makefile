## ------------------------------------------------------------------------
## The purpose of this Makefile is to build/test the adventofcode solution.
## By default, all solutions are executed. To test a specific solution, you
## should define the "SOLUTION" environment variable with the folder name
## of the solution you want to test.
## e.g: SOLUTION=Day1 make solution
## ------------------------------------------------------------------------
##
## Environement Variables
##
##    SOLUTION:		         allow to define the solution to test
##    ADVENTOFCODE_DEBUG:	 print debug log

# LOCAl VAR
TBD_LATER ?= TBD_LATER
PYTHON_IMAGE ?= python:3.8.14

##
## Help
##
.DEFAULT_GOAL := help
.PHONY: help
help:: ## show this help text
	@gawk -vG=$$(tput setaf 2) -vR=$$(tput sgr0) ' match($$0, "^(([^#:]*[^ :]) *:)?([^#]*)##([^#].+|)$$",a) { \
	    if (a[2] != "") { printf "    make %s%-18s%s %s\n", G, a[2], R, a[4]; next }\
	    if (a[3] == "") { print a[4]; next }\
	    printf "\n%-36s %s\n","",a[4]\
	  }' $(MAKEFILE_LIST)
	@echo "" # blank line at the end

##
## Build Binary/Manifest
##
.PHONY: all
all: solution ## Start all solution

##
## Test solution(s)
##
.PHONY: solution
solution: ## Test some solution (by default all solution are tested)
	python3 ${PWD}/${SOLUTION}

docker-solution: ## Test some solution with docker (by default all solution are tested)
	docker run --rm  -v ${PWD}/${SOLUTION}:/tmp/workspace -w /tmp/workspace ${PYTHON_IMAGE} python .
