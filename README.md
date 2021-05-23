# Get Richer Data from BabyTime

Originally, this repository was going to be for Baby Tracker app.  However, it
doesn't support data sync between parents.  So my wife and I decided to use the
BabyTime app for data sync between us.  BabyTime has rich stats and metrics
already so it doesn't _need_ a Grafana dashboard... but I wanted one.

[BabyTime][1] is a newborn tracking app for breastfeeding, breast pumping, and
feeding your baby from the breast, pumped milk, or formula.  This processes data
and puts it into InfluxDB where richer reports can be generated using Grafana.

The following are supported tags for richer metrics on _Pumped Milk_ and
_Formula_ feeding events:

- Purple Nipple
- Spit Up
- Yellow Nipple

The app also supports a generic `Etc` field which can contain custom baby
events.  Since babies may have a tongue tie surgery, one must do `tongue
lift` exercises on the baby's tongue.  The following custom `Etc` events are
supported.

- Spit Up
- tongue lift

Sometimes a baby might spit up far later than a feeding.  So it makes sense to
track it with an Etc event in addition to bottle feeding.

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

Then, [configure your browser to browse the cluster web page][cluster-web] and
visit the address `http://portal.service.consul/grafana/`.

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

# Create the dashboard

Log into Grafana by visiting `http://portal.service.consul/grafana/` with
username `admin` and password `admin`.  It will prompt you to change the
password.

Import [the dashboard from this repository][dashboard-json].  If you've already
published your BabyTime data, then you should see some graphed metrics which you
can change the time period.

Update the dashboard to your liking.

# Screenshots

### 24h Data View

![24h view of feeding and breast pumping][24h-view]

### 7d Data View

![7d view of feeding volume, spit up events, and breast feeding time][7d-view]

# Data conversion

The following is a sample of BabyTime data exported from its app.

<details><summary>Data sample exported from BabyTime (Click to expand)</summary>

---

```
YYYY-MM-DD 04:47 PM
Type: Pumped Milk
Pumped Milk Total Amount(ml): 77 (ml)
Memo: Yellow Nipple
====================
YYYY-MM-DD 04:23 PM ~ YYYY-MM-DD 04:45 PM
Type: Breastfeeding (right)
Duration: 22 (min)
Breastfeeding Right: 22 (min)
Memo: Shield, let down
====================
YYYY-MM-DD 04:15 PM
Type: Pee
Diaper type: Pee
====================
YYYY-MM-DD 02:30 PM
Type: Pee
Diaper type: Both
====================
YYYY-MM-DD 01:55 PM
Type: Pumped Milk
Pumped Milk Total Amount(ml): 65 (ml)
Memo: Purple Nipple
====================
YYYY-MM-DD 01:30 PM ~ YYYY-MM-DD 01:50 PM
Type: Breastfeeding (right)
Duration: 20 (min)
Breastfeeding Right: 20 (min)
Memo: Shield
====================
YYYY-MM-DD 12:15 PM ~ YYYY-MM-DD 12:30 PM
Type: Pumping
Duration: 15 (min)
Pumping Left: 14 (min)
Pumping Right: 15 (min)
Pumping Total Amount(ml): 32 (ml)
Pumping Left Amount(ml): 15 (ml)
Pumping Right Amount(ml): 17 (ml)
Memo: Bottle Fed
====================
```

</details>

---

I converted the raw export data into JSON array time series data which is
ingested and published to InfluxDB.  Grafana is then used to create a dashboard
which answers questions our pediatrician or lactician asks about.

<details><summary>BabyTime converted to JSON time series (Click to expand)</summary>

---

```json
[
    {
        "event": "Feed Pumped Milk",
        "feed_pump_ml": 77,
        "notes": "Yellow Nipple",
        "time": "YYYY-MM-DD 04:47 PM EDT",
        "yellow_nipple": true
    },
    {
        "duration_min": 22,
        "event": "Breastfeeding",
        "feed_breast_right_min": 22,
        "notes": "Shield, let down",
        "time": "YYYY-MM-DD 04:23 PM EDT"
    },
    {
        "diaper_type": "Pee",
        "event": "Change Diaper",
        "pee": true,
        "time": "YYYY-MM-DD 04:15 PM EDT"
    },
    {
        "diaper_type": "Both",
        "event": "Change Diaper",
        "pee": true,
        "poop": true,
        "time": "YYYY-MM-DD 02:30 PM EDT"
    },
    {
        "event": "Feed Pumped Milk",
        "feed_pump_ml": 65,
        "notes": "Purple Nipple",
        "purple_nipple": true,
        "time": "YYYY-MM-DD 01:55 PM EDT"
    },
    {
        "duration_min": 20,
        "event": "Breastfeeding",
        "feed_breast_right_min": 20,
        "notes": "Shield",
        "time": "YYYY-MM-DD 01:30 PM EDT"
    },
    {
        "duration_min": 15,
        "event": "Pumping",
        "notes": "Bottle Fed",
        "pump_left_breast_min": 14,
        "pump_left_breast_ml": 15,
        "pump_right_breast_min": 15,
        "pump_right_breast_ml": 17,
        "pump_total_ml": 32,
        "time": "YYYY-MM-DD 12:15 PM EDT"
    }
]
```

</details>

---

[1]: https://www.babytime.care/
[2]: https://github.com/samrocketman/docker-compose-ha-consul-vault-ui
[3]: https://github.com/samrocketman/consul-influxdb
[4]: https://github.com/samrocketman/consul-kapacitor
[5]: https://github.com/samrocketman/consul-chronograf
[6]: https://github.com/samrocketman/consul-grafana
[24h-view]: ./dashboards/grafana/24h-data-view.png
[7d-view]: ./dashboards/grafana/7d-data-view.png
[cluster-web]: https://github.com/samrocketman/docker-compose-ha-consul-vault-ui#configure-your-browser
[dashboard-json]: ./dashboards/grafana/BabyTime.json
