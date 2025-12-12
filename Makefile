
build:
	@docker build -t search-jobs .

run: 
	@docker run --rm -v ${PWD}:/app --env-file .env search-jobs