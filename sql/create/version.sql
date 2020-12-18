CREATE TABLE version (
	id TEXT PRIMARY KEY NOT NULL,
	parent_id TEXT,
	"timestamp" TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
	name TEXT,
	category TEXT NOT NULL,
	foreign key(parent_id) references version(id)
);
