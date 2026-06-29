import logging
from slack_bolt import App
from slack_sdk.web import WebClient
import subprocess
import serial
import threading
import sys
import time
import re
import os
from dotenv import load_dotenv, dotenv_values 
from slack_bolt.adapter.socket_mode import SocketModeHandler
from vm_stuff import VirtualMachine

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

load_dotenv() 

serialTerminal = None
botChannel = os.getenv("CHANNEL")

@app.action("ctrlc")
def ctrlc(ack, body, respond):
    serialTerminal.write("^[C".encode())
    ack()

@app.action("ctrld")
def crtld(ack, body, respond):
    serialTerminal.write("^[D".encode())
    ack()

@app.event("message")
def message(event, client):
    text = event.get("text")
    event.get("user")
    if text and event.get("channel") == botChannel and text[0] != "#":
        try:
            serialTerminal.write((text + "\r\n").encode())

        except:
            print("womp womp")


# "borrowed" from stackoverflow 
ansi_escape = re.compile(
    r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""",
    re.VERBOSE,
)


def reader_thread(ser, client):
    while ser.is_open:
        try:
            data = ser.read(ser.in_waiting or 1)
            if data:
                print("womp2")

                message_text = ansi_escape.sub(
                    "", data.decode("ascii", errors="replace")
                )
                message = {
                    "channel": botChannel,
                    "icon_emoji": ":waga:",
                    "blocks": [
                        {
                            "type": "rich_text",
                            "elements": [
                                {
                                    "type": "rich_text_preformatted",
                                    "language": "sh",
                                    "elements": [
                                        {"type": "text", "text": message_text}
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "CTRL+C",
                                        "emoji": False,
                                    },
                                    "value": "ctrlc",
                                    "action_id": "ctrlc",
                                },
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "CTRL+D",
                                        "emoji": False,
                                    },
                                    "value": "ctrld",
                                    "action_id": "ctrld",
                                },
                            ],
                        },
                    ],
                }
                client.chat_postMessage(**message)
                sys.stdout.flush()
        except serial.SerialException:
            break



def terminal(port, client):
    baudrate = 9600
    ser = serial.Serial(port, baudrate, timeout=0.1)
    print("serial conected")
    return ser



def wait_until(delegate, timeout: int):
    end = time.time() + timeout
    while time.time() < end:
        if delegate():
            return True
        else:
            time.sleep(0.1)
    return False

if __name__ == "__main__":
    myEpicVM = VirtualMachine()
    vmThread = threading.Thread(
    target=myEpicVM.runVM
    )
    vmThread.daemon = True
    vmThread.start()
    

    wait_until(lambda: (myEpicVM.serial != ""), 5)
    serialLocation = myEpicVM.serial

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    smh = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])

    app_thread = threading.Thread(target=smh.start, args=())
    app_thread.start()

    serialTerminal = terminal(serialLocation, app.client)

    reader = threading.Thread(
        target=reader_thread,
        args=(
            serialTerminal,
            app.client,
        ),
    )
    reader.daemon = True
    reader.start()

    while True:
        pass
