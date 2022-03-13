# Diogo's Makefile standar colors
ifneq (,$(findstring xterm,${TERM}))
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	BLUE         := $(shell tput -Txterm setaf 6)
	RESET 		 := $(shell tput -Txterm sgr0)
else
	RED          := ""
	GREEN        := ""
	BLUE         := ""
	RESET        := ""
endif



.PHONY: help

help: ## Show this help message
	@echo "\n\n${BLUE}############################################# Diogo's Parallel Linkl Crawler ##############################################${RESET}"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "${BLUE}###########################################################################################################################${RESET}"

configure_devel: ## One line initial developer configuration
	if [ -d "venv" ]; then \
		rm -rf venv; \
    fi;
	python3 -m venv venv;
	bash -c "source venv/bin/activate && pip install -r requirements/base.txt && pip install -r requirements/develop.txt";
	pre-commit install
