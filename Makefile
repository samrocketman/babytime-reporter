.PHONY: run clean clean-all baby_tracker_data_import baby_time_data_import

run: baby_time_data_import

help:
	@echo 'Run make with no arguments to process BabyTime metrics.'
	@echo 'Other ways to run make:'
	@echo '    make baby_tracker_data_import'
	@echo '    make clean'
	@echo '    make clean-all'

baby-tracker-data.json:
	ls *.abt
	cat *.abt | gunzip | jq '.records' > baby-tracker-data.json

baby-time-data.json:
	ls *.zip
	if [ ! -f baby-time-data.json ]; then
		unzip *.zip
	fi
	ls *.txt
	./process_activity_txt.py *.txt > baby-time-data.json

baby_tracker_data_import: baby-tracker-data.json
	docker run --network docker-compose-ha-consul-vault-ui_internal --dns 172.16.238.2 --dns 172.16.238.2 --rm -v "$(PWD):/mnt" telegraf telegraf --once -config /mnt/baby-tracker-telegraf.conf

baby_time_data_import:
	docker run --network docker-compose-ha-consul-vault-ui_internal --dns 172.16.238.2 --dns 172.16.238.2 --rm -v "$(PWD):/mnt" telegraf telegraf --once -config /mnt/baby-tracker-telegraf.conf

clean:
	rm *.json *.txt

clean-all: clean
	git clean -xfd
