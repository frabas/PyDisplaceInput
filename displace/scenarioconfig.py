from displace.importer import HashFileImporter


class ScenarioConfig(HashFileImporter):
    params = (
        "dyn_alloc_sce", "dyn_pop_sce", "biolsce", "fleetsce", "freq_do_growth",
        "freq_redispatch_the_pop",
        "a_graph", "nrow_coord", "nrow_graph", "a_port", "graph_res",
        "is_individual_vessel_quotas", "check_all_stocks_before_going_fishing", "dt_go_fishing",
        "dt_choose_ground", "dt_start_fishing", "dt_change_ground", "dt_stop_fishing",
        "dt_change_port", "use_dtrees",
        "tariff_pop", "freq_update_tariff_code",
        "arbitary_breaks_for_tariff", "total_amount_credited", "tariff_annual_hcr_percent_change",
        "update_tariffs_based_on_lpue_or_dpue_code",
        "metier_closures"
    )

    def __init__(self):
        super(ScenarioConfig, self).__init__("simusspe_{name}/{scenario}.dat", self.__load)

    @property
    def nbpops(self):
        return self.__nbpops

    def __load(self, db, lines):
        for param, line in zip(self.params, lines):
            db.insert_scenario_config_entry(param, line)
