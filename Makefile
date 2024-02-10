# Makefile

# Set the default target to run when you just type 'make'
.PHONY: test
default: test

# Define a 'test' target that runs pytest to execute your tests
test: 
	@echo "Running PyTest..."
	pytest tests

# Define a 'docker-build' target for building Docker images
docker-build:
	@echo "Building Docker image..."
	docker build . -t vim