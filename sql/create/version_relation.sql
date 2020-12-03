CREATE TABLE version_relation (
	id STRING NOT NULL,
	parent_id STRING,
	"timestamp" TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY(id, parent_id)
);
