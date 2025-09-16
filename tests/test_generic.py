import os
from .context import generic

script_dir = os.path.dirname(__file__)
test_dir = os.path.join(script_dir, "testdir")
os.makedirs(test_dir, exist_ok=True)

name = "TestObject"
path = os.path.join(test_dir, name + ".yaml")
gnric = None

def test_init():
    global gnric
    gnric = generic.Generic(
        path=test_dir,
        name="TestObject"
    )
    assert gnric.name == name
    assert gnric.path == path

def test_to_file():
    global gnric
    gnric.to_file()
    assert os.path.isfile(path)
    gnric = None

def test_from_file():
    global gnric
    gnric = generic.Generic.from_file(file=path)
    assert gnric.name == name

def test_template_yaml():
    os.chdir(test_dir)
    tmp_path = os.path.join(test_dir, "template.yaml")
    generic.Generic.template_yaml()
    assert os.path.isfile(tmp_path)
    tmp_path = os.path.join(test_dir, "template2.yaml")
    generic.Generic.template_yaml(path=tmp_path)
    assert os.path.isfile(tmp_path)

def test_cleanup():
    import shutil
    shutil.rmtree(test_dir)
    assert not os.path.isdir(test_dir)
