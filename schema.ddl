-- we don't know how to generate schema main (class Schema) :(
create table Config
(
    biosce integer,
    param  text,
    value  text
);

create table Scenarios
(
    biosce integer,
    name   text,
    notes  text
);

create table Nodes
(
	id integer not null,
	x numeric not null,
	y numeric not null,
	hidx integer,
	biosce integer not null
		constraint Nodes_Scenarios_biosce_fk
			references Scenarios (biosce)
				on update cascade on delete cascade,
	constraint Nodes_pk
		primary key (id, biosce)
);

create table Populations
(
    id     integer,
    name   TEXT,
    biosce integer
        constraint fk_Populations
            references Scenarios (biosce)
            on update cascade on delete cascade,
    constraint pk_Populations
        primary key (biosce, id)
);

create table PopulationParameters
(
    popId     int,
    parameter TEXT not null,
    value     numeric,
    biosce    int,
    constraint pk_PopulationParameters
        primary key (popId, biosce, parameter),
    foreign key (biosce, popId) references Populations
        on update cascade on delete cascade
);

create index PopulationParameters_parameter_index
    on PopulationParameters (parameter);

