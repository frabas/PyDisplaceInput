-- we don't know how to generate schema main (class Schema) :(

create table Scenarios
(
    biosce integer,
    name   text,
    notes  text
);

create table Config
(
    biosce integer not null
        constraint Config_Scenarios_biosce_fk
            references Scenarios (biosce)
            on update cascade on delete cascade,
    param  text,
    value  text,
    constraint Config_pk
        primary key (biosce, param)
);

create table Nodes
(
    id     integer not null,
    x      numeric not null,
    y      numeric not null,
    hidx   integer,
    biosce integer not null
        constraint Nodes_Scenarios_biosce_fk
            references Scenarios (biosce)
            on update cascade on delete cascade,
    constraint Nodes_pk
        primary key (id, biosce)
);

create table Edges
(
    id           integer not null,
    from_node_id integer not null,
    to_node_id   integer not null,
    w            integer not null,
    biosce       integer not null
        constraint Edges_Scenarios_biosce_fk
            references Scenarios (biosce)
            on update cascade on delete cascade,
    constraint Edges_pk
        primary key (id, biosce),
    foreign key (from_node_id, biosce) references Nodes
        on update cascade on delete cascade,
    foreign key (to_node_id, biosce) references Nodes
        on update cascade on delete cascade
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
