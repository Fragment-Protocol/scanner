project_name := SCANNER
compose_file := dockerfiles/docker-compose.yml
compose := docker-compose -f $(compose_file) -p $(project_name)

help:
	@echo -e "\033[1mUSAGE\033[0m"
	@echo "  make COMMAND"
	@echo ""
	@echo "Commands:"
	@echo "  build		Build container"
	@echo "  install	Build and up all containers"
	@echo "  start		Start the built container"
	@echo "  stop		Stop the built container"
	@echo "  remove	Remove container"
	@echo "  top		Show docker top"
	@echo "  logs		Show docker logs"
	@echo "  clean		Remove python cache files"
	@echo ""
	@echo -e "\033[1mEXAMPLES\033[0m"
	@echo "  $$ make install"
	@echo ""

build:
	$(compose) build --parallel

install:
	$(compose) up -d

start:
	$(compose) start

stop:
	$(compose) stop

remove:
	$(compose) rm -s

top:
	$(compose) top

logs:
	$(compose) logs -f

clean:
	sudo find ./ -name '*.pyc' -print0 | xargs -0 --no-run-if-empty rm
	sudo find ./ -name '__pycache__' -print0 | xargs -0 --no-run-if-empty rm -r
