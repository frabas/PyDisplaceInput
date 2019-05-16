PRAGMA foreign_keys = ON;

create table BioSce
(
	biosce int
		constraint BioSce_pk
			primary key
);

create table Config
(
	param text not null
		constraint Config_pk
			primary key,
	value text
);

create table GraphSce
(
	graphsce int
		constraint GraphSce_pk
			primary key
);

create table Nodes
(
	id integer not null,
	x numeric not null,
	y numeric not null,
	hidx integer,
	graphsce integer not null
		constraint Nodes_GraphSce_biosce_fk
			references GraphSce (biosce)
				on update cascade on delete cascade,
	constraint Nodes_pk
		primary key (id, graphsce)
);

create table Edges
(
	id integer not null
		constraint Edges_pk
			primary key,
	from_node_id integer not null,
	to_node_id integer not null,
	w integer not null,
	graphsce int,
	foreign key (from_node_id, graphsce) references Nodes
		on update cascade on delete cascade,
	foreign key (to_node_id, graphsce) references Nodes
		on update cascade on delete cascade
);

create table Populations
(
	id integer,
	name TEXT,
	biosce integer
		references BioSce
			on update cascade on delete cascade,
	constraint pk_Populations
		primary key (biosce, id)
);

create table PopulationParameters
(
	popId int,
	parameter TEXT not null,
	value numeric,
	biosce int,
	constraint pk_PopulationParameters
		primary key (popId, biosce, parameter),
	foreign key (biosce, popId) references Populations
		on update cascade on delete cascade
);

create index PopulationParameters_parameter_index
	on PopulationParameters (parameter);

create table Scenarios
(
	name text not null,
	notes text,
	biosce int not null
		references BioSce,
	fleetsce int not null,
	graphsce int not null
		references GraphSce
);

