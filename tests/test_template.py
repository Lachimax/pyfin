import os

script_dir = os.path.dirname(__file__)

def test_mkdir():
    test_dir = os.path.join(script_dir, "testdir")
    os.makedirs(test_dir)
    assert os.path.exists(test_dir)