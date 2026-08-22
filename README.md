
DB:

```sql
sqlite> .schema
CREATE TABLE service_availabilities (
	date DATE, 
	service TEXT, 
	availability FLOAT
);

sqlite> .tables
service_availabilities

sqlite> select * from service_availabilities limit 5;
2000-01-01|pdf_generator|95.43
2000-01-01|report_importer|96.78
2000-01-01|report_exporter|98.62
2000-01-02|pdf_generator|97.25
2000-01-02|report_importer|98.25

sqlite> select distinct service from service_availabilities;
pdf_generator
report_importer
report_exporter

sqlite> select MIN(availability) as min_av, MAX(availability) as max_av from service_availabilities;
95.0|100.0

sqlite> select MIN(date) as start_date, MAX(date) as end_date from service_availabilities;
2000-01-01|2021-02-28

```

# Design

Für die DB-File, `COPY` oder bind mount?
* Daten sind klein (1,3M) und wir sind read-only, können einfach kopieren (dann ist DB auch versioniert & keine harten Path dependencies)
* Sollte DB drastisch größer werden oder PUT-Funktionalität kommen dann zu bind/volume mount wechseln (writes passieren aktuell im Image Layer und sind nicht persistent)

App-Aufbau:

* `models`: SQLAlchemy-Models
* `schemas`: PyDantic Models/Schemas
