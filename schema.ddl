create table Populations
(
	id integer
		constraint Populations_pk
			primary key,
	name TEXT
);

create table PopulationParameters
(
	popId int
		constraint PopulationParameters_pk
			primary key
		references Populations
			on update cascade on delete cascade,
	parameter TEXT not null,
	value numeric
);

create unique index PopulationParameters_parameter_uindex
	on PopulationParameters (parameter);

