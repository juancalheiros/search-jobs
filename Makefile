.PHONY: build run

build:
	@docker build -t search-jobs .

run: 
	@docker run --rm \
	-v ${PWD}:/app \
	-v ${HOME}/.config/gcloud:/root/.config/gcloud \
	--env-file .env \
	search-jobs