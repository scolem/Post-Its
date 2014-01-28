import os

os.system('crontab -l > oldcrontab')
os.system('cp oldcrontab newcrontab')
os.system('echo "*/5 * * * * python /home/pi/Scott/Post-Its/pi/runThis.py >> /tmp/out.txt 2>&1" >> newcrontab')
os.system('crontab < newcrontab')
os.system('rm newcrontab')
