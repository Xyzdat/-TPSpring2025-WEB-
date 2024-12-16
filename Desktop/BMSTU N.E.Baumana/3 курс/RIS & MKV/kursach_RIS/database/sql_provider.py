import os
from string import Template

class SQLprovider:
    def __init__(self, path):
        self._scripts = {}
        for file in os.listdir(path):
            if file.endswith('.sql'):
                self._scripts[file] = Template(open(f'{path}/{file}', 'r').read())

    def get(self, file, **kwargs):
        _sql = self._scripts[file].substitute(**kwargs)
        return _sql