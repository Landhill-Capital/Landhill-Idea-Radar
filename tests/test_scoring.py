from idea_radar.scoring import Idea


def test_ship_threshold():
    i = Idea(name="X", source="s", summary="",
             scores={"pain_intensity": 3, "willingness_to_pay": 3,
                     "founder_market_fit": 3, "unfair_local_advantage": 2,
                     "distribution_path": 2, "defensibility_24mo": 1})
    assert i.total == 14
    assert i.verdict == "SHIP"


def test_kill_threshold():
    i = Idea(name="Y", source="s", summary="", scores={"pain_intensity": 1})
    assert i.verdict == "KILL"
