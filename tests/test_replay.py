import glob
def test_replay_created():
    files = glob.glob("results\\trades_replay_*.json")
    assert len(files) > 0, "No replay trades file found. Run src\\engine.py first."
