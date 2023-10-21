
restore:
	pip install -r requirements.txt

run:
	python ./src/main.py

REPOSITORY=docker.io/darstaed/meross-prometheus-adapter
TAG=dev
container:
	docker buildx build --platform linux/arm64,linux/amd64 -f build/Dockerfile . -t ${REPOSITORY}:${TAG}
