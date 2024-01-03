build:
    docker buildx build --platform linux/amd64 -t musababdullah/miftaahtranscripts:latest .

push:
	docker push musababdullah/miftaahtranscripts
