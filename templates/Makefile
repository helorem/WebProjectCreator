PWD:=$(shell pwd)

deb: clean
	mkdir -p bin/@APPNAME@
	cp -r build/DEBIAN bin/@APPNAME@/DEBIAN
	mkdir -p bin/@APPNAME@/etc/init.d/
	cp conf/@APPNAME@.service bin/@APPNAME@/etc/init.d/@APPNAME@
	mkdir -p bin/@APPNAME@/etc/nginx/sites-available/
	cp conf/nginx_default.conf bin/@APPNAME@/etc/nginx/sites-available/@APPNAME@
	mkdir -p bin/@APPNAME@/var/www/@APPNAME@/
	cp -r src/* bin/@APPNAME@/var/www/@APPNAME@/
	mkdir -p bin/@APPNAME@/usr/bin/
	mv bin/@APPNAME@/var/www/@APPNAME@/api/@APPNAME@.sh bin/@APPNAME@/usr/bin/
	dpkg-deb --build bin/@APPNAME@ bin/@APPNAME@.deb

clean:
	rm -rf bin

deploy: deb
	cp build/Dockerfile.deploy bin/Dockerfile
	docker build -t @APPNAME@ bin

run:
	docker stop @APPNAME@ | exit 0
	docker rm @APPNAME@ | exit 0
	docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -dit --name=@APPNAME@ --expose=80 @APPNAME@ /lib/systemd/systemd systemd.unit=emergency.service
	docker exec -ti @APPNAME@ service @APPNAME@ start
	docker exec -ti @APPNAME@ service nginx start

deploy-dev:
	cp build/Dockerfile.dev bin/Dockerfile
	docker build -t @APPNAME@ bin

run-dev:
	docker stop @APPNAME@ | exit 0
	docker rm @APPNAME@ | exit 0
	docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -dit --name=@APPNAME@ -v "$(PWD)":"/mnt/src" --expose=80 @APPNAME@ /lib/systemd/systemd systemd.unit=emergency.service
	docker exec -ti @APPNAME@ /mnt/src/build/install_dev.sh
	docker exec -ti @APPNAME@ systemctl start @APPNAME@
	docker exec -ti @APPNAME@ systemctl start nginx

exec:
	docker exec -ti @APPNAME@ bash -l

install_nginx:
	build/install_nginx.sh

deploy-all: deploy run install_nginx

deploy-dev-all: deploy-dev run-dev install_nginx
