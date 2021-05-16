# Get Richer Data from BabyTime

[BabyTime][1] is a newborn tracking app for breastfeeding, breast pumping, and
feeding your baby from the breast, pumped milk, or formula.  This processes data
and puts it into InfluxDB where richer reports can be generated using Grafana.

The following are supported tags for richer metrics on _Pumped Milk_ and
_Formula_ feeding events:

- Purple Nipple
- Spit Up
- Yellow Nipple

# Bottle Flow

The purple and yellow bottle nipples control how much flow a baby consumes while
feeding from a bottle.

Flow in order of fastest to slowest.

- Yellow Nipple
- Purple Nipple

# Provisioning InfluxDB

This assumes you've provisioned InfluxDB on a local Vault and Consul cluster
using Docker.

Provision the following projects in order:

- [Consul][2]
- [InfluxDB][3]
- [Kapacitor][4]
- [Chronograf][5]
- [Grafana][6]

# Uploading stats to InfluxDB

1. From the app, go to _BabyTime Settings_, _Export (Download)_, _Daily Record
   (txt)_, and all of your records by emailing to yourself.
2. Download the activity zip file into the root of this repository.
3. Upload all data into InfluxDB by running the following command.
   ```bash
   make
   ```

Alternately, if you only want to create the `babytime-data.json` file, then run
the following command.

    make babytime-data.json

`babytime-data.json` is the daily record converted into a time-series JSON
array.  The JSON array is unsorted, but each JSON Object has a `time` key which
notes at what time an `event` occurred.

[1]: https://www.babytime.care/
[2]: https://github.com/samrocketman/docker-compose-ha-consul-vault-ui
[3]: https://github.com/samrocketman/consul-influxdb
[4]: https://github.com/samrocketman/consul-kapacitor
[5]: https://github.com/samrocketman/consul-chronograf
[6]: https://github.com/samrocketman/consul-grafana
