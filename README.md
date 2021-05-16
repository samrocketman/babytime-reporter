# Get Richer Data from BabyTime

[BabyTime][1] is a newborn tracking app for breastfeeding, breast pumping, and
feeding your baby from the breast, pumped milk, or formula.  This processes data
and puts it into influxdb where richer reports can be generated using Grafana.

Supported tags for richer metrics:

- Purple Nipple
- Spit Up
- Yellow Nipple

# Bottle Flow

The purple and yellow bottle nipples control how much flow a baby consumes while
feeding from a bottle.

Flow in order of fastest to slowest.

- Yellow Nipple
- Purple Nipple

# Provisioning influxdb

This assumes you've provisioned InfluxDB on a local Vault and Consul cluster
using Docker.

Provision the following projects in order:

- [Consul][2]
- [InfluxDB][3]
- [Kapacitor][4]
- [Chronograf][5]
- [Grafana][6]

[1]: https://www.babytime.care/
[2]: https://github.com/samrocketman/docker-compose-ha-consul-vault-ui
[3]: https://github.com/samrocketman/consul-influxdb
[4]: https://github.com/samrocketman/consul-kapacitor
[5]: https://github.com/samrocketman/consul-chronograf
[6]: https://github.com/samrocketman/consul-grafana