import os

# Наличие необходимых файлов
def test_fileExist():
    assert os.path.exists('../config.py')
    assert os.path.exists('../BaseController.py')
    assert os.path.exists('../Model.py')
    assert os.path.exists('../Router.py')
    assert os.path.exists('../start.py')
    assert os.path.exists('../TenderController.py')