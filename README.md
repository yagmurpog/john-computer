# john computer
connect your qemu vm to slack!!!

## how it works?
this simple python script takes a terminal serial port (whether its a real or a virtual one) and lets you mirror it to a channel on slack.

if you're using qemu you can easily create a virtual serial port by adding `-serial pty` to your launch options

## running
- create a python venv (or not i'm not here to judge lol)
```
python -m venv env/
```
- install the dependencies
```
pip install -r requirements.txt
```
- create a vm folder
```
mkdir vm
```
- create a base image for your vm
```
qemu-img create -f qcow2 john_base.img 4G
```
- install and configure your vm
- create set env variables, `SLACK_BOT_TOKEN SLACK_SIGNING_SECRET SLACK_APP_TOKEN`
- create a channel on slack add the bot there, copy the channel id and set `CHANNEL` enviroment variable to it
- start the vm with `vm-start.sh`, set the `SERIAL` enviroment variable to the serial port
- finally start the bot with `python app.py`


## todo (maybe??? no promises)
- merge everything to a script
- fix ctrl+c ctrl+d
- allow restoring the vm from slack 
- only allow commands from users

## requirements
qemu
python