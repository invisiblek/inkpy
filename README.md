inkpy
=====

a python app for gathering, storing, and presenting temperature data from an inkbird IBT-series temperature thermometer

this application is targeted for python 3.x

the uuids and byte strings in this project have been shamelessly stolen from other projects on github

files
- `requirements.txt` - `pip3 install -r requirements.txt --user` to get the required pip modules
- `app.cfg` - (copy `app.cfg.example` to this and modify to your needs) main config file
- `finddevices.py` - used to scan for nearby `iBBQ` devices and get a mac address to put in your `app.cfg`
- `gather.py` - the main gathering script. this will create and connect to your database and begin scalping data
- `cleanup.py` - a script that can be cron'd in order to prevent the database from getting too large

TODO:
- web interface
- mobile app
- tons and tons of other stuff i assume

**WORK IN PROGRESS. WILL PROBABLY EAT YOUR CAT. PROCEED AT YOU OWN RISK**
