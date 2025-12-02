.PHONY: help generate

help: ## List available commands and their descriptions
	@awk 'BEGIN {FS = ":.*?## "}; /^[a-zA-Z0-9_-]+:.*?## / {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

generate: ## Generate problem{id} with starter files (usage: make generate id=3)
	@if [ -z "$(id)" ]; then echo "Error: provide id=<int> (e.g. make generate id=3)"; exit 1; fi; \
	if ! echo "$(id)" | grep -Eq '^[0-9]+$$'; then echo "Error: id must be an integer"; exit 1; fi; \
	dir="problem$(id)"; \
	echo "Generating $$dir..."; \
	mkdir -p "$$dir"; \
	echo "# Problem $(id)" > "$$dir/description.md"; \
	printf '%s\n' '"""Solution for Problem $(id)."""' '' '' \
	'def sol():' '    # TODO: implement solution' '    pass' '' '' \
	'if __name__ == "__main__":' '    print(sol())' > "$$dir/sol.py"; \
	echo "Problem directory structure created at $$dir."
