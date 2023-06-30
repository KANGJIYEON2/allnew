build:
	docker build -t weather-gr .
run:
	docker run -it -d -p 8000:8000 -v \allnew\node:/app --name weather-gr weather-gr
exec:
	docker exec -it weather-gr /bin/bash
logs:
	docker logs weather-gr
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
k8sinit:
	docker commit weather weathers
	docker tag weather hihello516/weathers
	docker push hihello516/weathers
	docker rm -f $$(docker ps -aq)
	docker rmi hihello516/weathers
	docker rmi $$(docker images -q)
appdep:
	kubectl apply -f deployment.yal
appsvc:
	kubectl apply -f service.yaml
getdep:
	kubectl get deployment
getsvc:
	kubectl get svc -o wirde
getpod:
	kubectl get pod -o wirde
delsvc:
	kubectl delete svc weathers
deldep:
	kubectl delete deployment weathers
