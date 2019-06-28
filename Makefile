.PHONY: help install uninstall

define helpmessage
The following tasks are available:
   - install (superuser)
   - uninstall (superuser)
endef
export helpmessage

help:
	@echo "$$helpmessage"

install:
	mkdir -p /opt/allegra/
	cp *.py /opt/allegra/
	cp db.sqlite /opt/allegra/
	cp allegra.service /etc/systemd/system/
	chown root:root /etc/systemd/system/allegra.service
	chmod 644 /etc/systemd/system/allegra.service
	systemctl daemon-reload

uninstall:
	systemctl stop allegra
	rm -rf /opt/allegra
	rm /etc/systemd/system/allegra.service
	systemctl daemon-reload
