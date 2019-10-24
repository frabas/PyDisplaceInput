PRAGMA foreign_keys = ON;

create table BioSce
(
	biosce int not null
		constraint BioSce_pk
			primary key
);

create table Config
(
	param text not null
		constraint Config_pk
			primary key,
	value text not null
);

create table FleetSce
(
	fleetsce int not null
		constraint FleetSce_pk
			primary key
);

create table GraphSce
(
	graphsce int not null
		constraint GraphSce_pk
			primary key
);

create table Nodes
(
	id integer not null,
	x numeric not null,
	y numeric not null,
	hidx integer not null,
	code_area integer,
	landscape integer,
	wind numeric,
	salinity numeric,
	sst numeric,
	nitrogen numeric,
	phosphorus numeric,
	oxygen numeric,
	carbon numeric,
	bathymetry numeric,
	shipping numeric,
	silt numeric,
	benthosbio numeric,
	benthosnum numeric,
	graphsce integer not null
		references GraphSce
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
	graphsce int not null,
	foreign key (from_node_id, graphsce) references Nodes
		on update cascade on delete cascade,
	foreign key (to_node_id, graphsce) references Nodes
		on update cascade on delete cascade
);

create unique index Edges_id_uindex
	on Edges (id);

create table Populations
(
	id integer not null,
	name text not null,
	biosce integer not null
		references BioSce
			on update cascade on delete cascade,
	constraint pk_Populations
		primary key (biosce, id)
);

create table PopulationParameters
(
	pop_id int not null,
	parameter text not null,
	value numeric not null,
	biosce int not null,
	period text,
	country text,
	constraint pk_PopulationParameters
		primary key (pop_id, biosce, parameter, period, country),
	foreign key (biosce, pop_id) references Populations
		on update cascade on delete cascade
);

create index PopulationParameters_parameter_index
	on PopulationParameters (parameter);

create table PopulationParametersWithSizeGroupAndAge
(
	pop_id int not null,
	parameter text not null,
	value numeric not null,
	biosce int not null,
	size_group int,
	age int,
	period text,
	node int,
	constraint pk_PopulationParameters
		primary key (pop_id, biosce, parameter, size_group, age),
	foreign key (biosce, pop_id) references Populations
		on update cascade on delete cascade
);

create index PopulationParametersWithSizeGroupAndAge_ByNode_index
	on PopulationParametersWithSizeGroupAndAge (pop_id, size_group, age, node);

create table Scenarios
(
	name text not null
		constraint Scenarios_pk
			primary key,
	notes text,
	biosce int not null
		references BioSce
			on update cascade on delete cascade,
	fleetsce int not null,
	graphsce int not null
		references GraphSce
			on update cascade on delete cascade
);

create table ScenarioConfig
(
	sce TEXT
		references Scenarios
			on update cascade on delete cascade,
	param TEXT not null,
	value TEXT
);

create table VesselsSpe
(
	fleetsce int not null
		references FleetSce
			on update cascade on delete cascade,
	VesselName TEXT
		constraint VesselsSpe_pk
			primary key
);

create table VesselsParameters
(
	VesselName TEXT not null
		references VesselsSpe
			on update cascade on delete cascade,
	Parameter text not null,
	Opt1 numeric,
	Opt2 numeric,
	Period numeric,
	Value numeric not null,
	constraint VesselsParameters_pk
		primary key (VesselName, Parameter, Opt1, Opt2)
);

