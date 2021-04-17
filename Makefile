IMAGE="price_watch"
DOCKER_RUN=docker run $(IMAGE)
TAG="latest"

run: build
	$(DOCKER_RUN) rei_check

build: 
	docker build -t $(IMAGE) .

requirements.txt:
	pipenv lock -r > requirements.txt