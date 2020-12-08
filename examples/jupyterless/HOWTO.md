Assuming `py2gift` is installed, one can run
```
import importlib
import py2gift.core

my_module = importlib.import_module('my_module')
py2gift.core.build('my_settings.yaml', True, my_module, 'my_parameters.yaml', no_checks=True, embed_images=True)
```
to generate the final *gift* file.
