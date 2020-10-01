PRAGMA foreign_keys = ON;

create table BioSce
(
	biosce int not null
		constraint BioSce_pk
			primary key
);

create table ClosuresSpe
(
    ClosureSce NUMERIC not null,
    ClosureId  NUMERIC not null,
    NodeId     NUMERIC not null,
    Type       TEXT,
    Period     NUMERIC not null,
    Opt        NUMERIC,
    Closures   TEXT
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
	icesrectanglecode numeric,
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
	landscape int,
	constraint pk_PopulationParameters
		primary key (pop_id, biosce, parameter, period, country, landscape),
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


create table HarboursParameters
(
   HarbourName TEXT    not null,
   NodeId integer not null,
    Parameter  text    not null,
    graphsce integer,
	  Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint HarboursParameters_pk
        primary key (HarbourName, NodeId, Parameter, Opt1, Opt2, Period)
 );

create table HarbourParametersWithSpeciesAndMarketCat
(
	node_id int not null,
	parameter text not null,
	value numeric not null,
	marketcat int,
	period text,
	species int
);

create index HarbourParametersWithSpeciesAndMarketCat_ByPop_index
	on HarbourParametersWithSpeciesAndMarketCat(node_id, marketcat, species);

create table HarbourParametersWithVesselSize
(
	node_id int not null,
	parameter text not null,
	value numeric not null,
	period text,
	vesselsize int,
	constraint pk_Harbours
		primary key (node_id, parameter, period, vesselsize)
);

create table BenthosParameters
(
	landscape_id int not null,
	parameter text not null,
	value numeric not null,
	period text,
	funcgroup int,
	constraint pk_Harbours
		primary key (landscape_id, parameter, period, funcgroup)
);


create table MetiersParametersWithLandscape
(
	MetierName int not null,
	Parameter text not null,
	Value numeric not null,
	funcgroup int,
	Period int,
	landscape int,
	constraint pk_Metiers
		primary key (MetierName, Parameter, funcgroup, Period, landscape)
);

create table MetiersParametersWithSpeciesAndSzGroup
(
	MetierName int not null,
	Parameter text not null,
	Value numeric not null,
	fleetsce int not null,
	species int,
	szgroup int,
	Period int
);


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

create table FishfarmsParameters
(
    FishfarmName TEXT    not null,
    Parameter  text    not null,
    Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint FishfarmsParameters_pk
        primary key (FishfarmName, Parameter, Opt1, Opt2, Period)
);

create table FishfarmsSpe
(
    FishfarmName TEXT
        constraint FishfarmsSpe_pk
            primary key
);

create table ShipsParameters
(
    ShipName TEXT    not null,
    Parameter  text    not null,
    Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint ShipsParameters_pk
        primary key (ShipName, Parameter, Opt1, Opt2, Period)
);

create table ShipsSpe
(
    ShipName TEXT
        constraint ShipsSpe_pk
            primary key
);

create table FirmsParameters
(
    FirmName TEXT    not null,
    Parameter  text    not null,
    Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint FirmsParameters_pk
        primary key (FirmName, Parameter, Opt1, Opt2, Period)
);

create table FirmsSpe
(
    FirmName TEXT
        constraint FirmsSpe_pk
            primary key
);

create table VesselsParameters
(
    VesselName TEXT    not null,
    Parameter  text    not null,
    Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint VesselsParameters_pk
        primary key (VesselName, Parameter, Opt1, Opt2, Period)
);

create index VesselsParameters_NameParameterPeriod_index
    on VesselsParameters (VesselName, Parameter, Period);

create index VesselsParameters_NameParameter_index
    on VesselsParameters (VesselName, Parameter);

create table VesselsSpe
(
    fleetsce   int not null
        references FleetSce
            on update cascade on delete cascade,
    VesselName TEXT
        constraint VesselsSpe_pk
            primary key
);

create table MetiersParameters
(
    MetierName int    not null,
    Parameter  text    not null,
    Opt1       numeric,
    Opt2       numeric,
    Period     numeric,
    Value      numeric not null,
    constraint MetiersParameters_pk
        primary key (MetierName, Parameter, Opt1, Opt2, Period)
);

create index MetiersParameters_NameParameterPeriod_index
    on MetiersParameters (MetierName, Parameter, Period);

create index MetiersParameters_NameParameter_index
    on MetiersParameters (MetierName, Parameter);


create table MetiersSpe
(
    fleetsce   int not null
        references FleetSce
            on update cascade on delete cascade,
    metier_name TEXT
        constraint MetiersSpe_pk
            primary key,
		MetierName int
);


create table HarboursSpe
(
  node_id int not null,

	HarbourName TEXT,


	graphsce int not null
        references GraphSce
            on update cascade on delete cascade


);
