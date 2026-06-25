import logging
from slack_bolt import *
from slack_sdk.web import WebClient
import subprocess
import serial
import threading
import sys
import time
import re


# Initialize a Bolt for Python app
app = App()
epicserial = None

textBuffer = ""


def register(app: App):
  
    app.action("deny_delivery")(deny_delivery_callback) # Add this line



@app.action("ctrlc")
def ctrlc(ack, body, respond):
    epicserial.write("^[C".encode())
    ack()

@app.action("ctrld")
def crtld(ack, body, respond):
    epicserial.write("^[D".encode())
    ack()




@app.event("message")
def message(event, client):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    print("message received")

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and channel_id == "C0BCQCWM47N" and text[0] != "#":

        #     result = subprocess.run(text.split(), stdout=subprocess.PIPE)
        try:
            epicserial.write((text + "\r\n").encode())

        except:
            print("whomp")

    # Post the onboarding message in Slack


#  response = client.chat_postMessage(**message)


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
    """Print incoming data in real time."""
    while ser.is_open:
        try:
            data = ser.read(ser.in_waiting or 1)
            if data:
                print("womp2")
                sys.stdout.write(data.decode("utf-8", errors="replace"))

                message_text = ansi_escape.sub(
                    "", data.decode("ascii", errors="replace")
                )
                message = {
                    "channel": "C0BCQCWM47N",
                    "username": "supersecurebot",
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
    # ser.write(("whoami" + "\r\n").encode())


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    # app.start(3000)

    app_thread = threading.Thread(target=app.start, args=(3000,))
    app_thread.start()

    epicserial = terminal("/dev/pts/4", app.client)

    reader = threading.Thread(
        target=reader_thread,
        args=(
            epicserial,
            app.client,
        ),
    )
    reader.daemon = True
    reader.start()

    while True:
        pass
