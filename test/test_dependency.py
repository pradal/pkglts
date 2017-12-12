from pkglts.dependency import Dependency


def test_dependency_respect_strict_pkg_mng():
    # conda
    dep = Dependency("toto", pkg_mng="conda")
    assert dep.is_conda(strict=True)
    assert dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng=None)
    assert not dep.is_conda(strict=True)
    assert dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng="pip")
    assert not dep.is_conda(strict=True)
    assert not dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng="git+https://")
    assert not dep.is_conda(strict=True)
    assert not dep.is_conda(strict=False)
    
    # pip
    dep = Dependency("toto", pkg_mng="pip")
    assert dep.is_pip(strict=True)
    assert dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng=None)
    assert not dep.is_pip(strict=True)
    assert dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng="conda")
    assert not dep.is_pip(strict=True)
    assert not dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng="git+https://")
    assert not dep.is_pip(strict=True)
    assert not dep.is_pip(strict=False)


def test_dependency_write_correct_pip_requirements():
    dep = Dependency("toto", pkg_mng="pip", version="2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto==2.18  # pip install toto==2.18"
    
    dep = Dependency("toto", pkg_mng="pip", version="==2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto==2.18  # pip install toto==2.18"
    
    dep = Dependency("toto", pkg_mng="conda", version="2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "#toto=2.18  # conda install toto=2.18"
    
    dep = Dependency("toto", pkg_mng="conda", version="==2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "#toto=2.18  # conda install toto=2.18"
