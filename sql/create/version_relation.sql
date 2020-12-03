CREATE TABLE version_relation (
	id TEXT NOT NULL,
	parent_id TEXT NOT NULL,
	"timestamp" TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY(id, parent_id),
	foreign key(id) references version(id),
	foreign key(parent_id) references version(id)
);