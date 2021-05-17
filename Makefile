.PHONY: babytime_data_import clean clean-all example run

TZ := $(shell date +%Z)

run: babytime_data_import

help:
	@echo 'Run make with no arguments to process BabyTime metrics.'
	@echo 'Other ways to run make:'
	@echo '    make baby_tracker_data_import'
	@echo '    make clean'
	@echo '    make clean-all'
	@echo '    make example'

babytime-data.json:
	ls *.zip
	if ! ls *.txt; then unzip *.zip; fi
	TZ=$(TZ) ./process_activity_txt.py *.txt > babytime-data.json

babytime_data_import: babytime-data.json
	docker run --network docker-compose-ha-consul-vault-ui_internal --dns 172.16.238.2 --dns 172.16.238.2 --rm -v "$(PWD):/mnt" telegraf telegraf --once -config /mnt/babytime-telegraf.conf

example:
	docker run --rm telegraf telegraf config > telegraf-example.conf

clean:
	rm *.json *.txt

clean-all: clean
	rm *.zip
