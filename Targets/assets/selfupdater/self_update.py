import requests
from time import sleep
import os

print('Running...')
rsp = requests.get('https://api.github.com/repos/MakerDepotAcademy/escaperoomgames/releases')

if rsp.ok:
  ID = rsp.json()[-1]['id']
  update = False

  if not os.path.exists('.last'):
    with open('.last', 'w+') as f:
      f.write(ID)
      update = True
  else:
    with open('.last', 'r+') as f:
      last = f.readline()
      if int(last) != ID:
        update = True
        f.seek(0)
        f.write(str(ID))

  if update:
    subprocess.call(['git', 'pull', '-X', 'theirs'])
    os.system('reboot')
