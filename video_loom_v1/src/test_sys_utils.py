from sys_utils import SysUtils


def test_is_running_in_pyinstaller_bundle():
    assert (SysUtils.is_running_in_pyinstaller_bundle() == False)
