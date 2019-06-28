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
	@echo "Copying files to /opt/allegra"
	@mkdir -p /opt/allegra/
	@cp *.py /opt/allegra/
	@cp db.sqlite /opt/allegra/
	@echo "Installing systemd service"
	@cp allegra.service /etc/systemd/system/
	@chown root:root /etc/systemd/system/allegra.service
	@chmod 644 /etc/systemd/system/allegra.service
	@echo "Creating 'allegra' service-user, if needed"
	@useradd -r -s /usr/sbin/nologin allegra 2>/dev/null || true
	@systemctl daemon-reload
	@echo "Install complete.\nTo start the service: sudo systemctl start allegra"

uninstall:
	@echo "Stopping the service"
	@systemctl stop allegra
	@echo "Removing allegra from /opt/allegra"
	@rm -rf /opt/allegra
	@echo "Removing the allegra service"
	@rm /etc/systemd/system/allegra.service
	@systemctl daemon-reload
	@echo "Uninstall complete."
