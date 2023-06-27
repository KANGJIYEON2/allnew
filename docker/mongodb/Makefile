build:
	docker build -t mysql .
run:
	docker run -d -p 27017:27017 -v \Users\BIT\Documents\GitHub\allnew\MongoDB:/app -v/Uers/BIT/Documents/GitHub/docker/mongo/data:/data/db --name mongo mongo
exec:
	docker exec -it mysql /bin/bash
logs:
	docker logs mongo
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
