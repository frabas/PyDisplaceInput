create table Scenarios
(
    biosce integer,
    name   text,
    notes  text
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

create unique index PopulationParameters_parameter_uindex
    on PopulationParameters (parameter);

