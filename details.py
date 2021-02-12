from pathlib import Path
import datetime
from os import chdir

datetime_object = datetime.date.today()
date = 'zillow ' + str(datetime_object)
path = Path.cwd() / date
#chdir(path)
newpath = path / 'address'
newpath.mkdir()





datetime_object = datetime.date.today()
date = 'zillow ' + str(datetime_object)
path = Path.cwd() / date
path.mkdir()