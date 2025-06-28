.PHONY: install run build test lint clean dev

# Install dependencies
install:
	npm install

# Run the application in development mode
run:
	npm start

# Run in development mode
dev:
	npm start

# Build for production
build:
	npm run build

# Run tests
test:
	npm test

# Lint code
lint:
	npx eslint src/ --ext .js,.jsx,.ts,.tsx

# Format code
format:
	npx prettier --write src/

# Clean node_modules and reinstall
clean:
	rm -rf node_modules package-lock.json
	npm install

# Setup project (install dependencies)
setup: install
