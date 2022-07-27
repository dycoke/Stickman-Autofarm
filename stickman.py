from http.client import HTTPSConnection
import json
import time
import random
import threading
from notifypy import Notify
from pynput import keyboard

file = open("info1.txt")
text = file.read().splitlines()
keep_running = True

if len(text) != 7 or input("Configure bot? (y/n): ") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord server ID: "))
    text.append(input("Discord channel ID: "))
    print("Use Developer Tools to find the following data")
    text.append(input("Discord Application ID: "))
    text.append(input("Discord Session ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()


header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discord.com",
    "referrer": text[2]
}


def on_press(key):
    global keep_running
    if key == keyboard.Key.f9:
        print("Ok, time to stop.")
        keep_running = False
        return False


def connect():
    return HTTPSConnection("discord.com", 443)


def press_button(connection, channel_id, guild_id, message_id, button_id):
    button_data = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": text[5],
        "session_id": text[6],
        "data": {"component_type": 2, "custom_id": button_id}
    }

    try:
        connection.request("POST", "/api/v9/interactions", json.dumps(button_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:
            pass
        else:
            print(f"While pressing button, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to press button")


def send_message(connection, channel_id, message):
    message_data = {
        "content": message,
        "tts": False
    }

    try:
        connection.request("POST", f"/api/v9/channels/{channel_id}/messages", json.dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")


def get_response(connection, channel_id):
    channel = connection.request("GET", f"/api/v9/channels/{channel_id}/messages", headers=header_data)
    response = connection.getresponse()

    if 199 < response.status < 300:
        response_dict_str = response.read().decode('utf-8')
        response_dict = json.loads(response_dict_str)
        return response_dict
    else:
        print(f"While fetching message, received HTTP {response.status}: {response.reason}")


def search():
    try:
        send_message(connect(), text[4], ".search")
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        message_id = response_dict[0]["id"]
        search_options = response_dict[0]["components"][0]["components"]
        option_labels = []
        for i in range(len(search_options)):
            option_labels.append(search_options[i]["label"])
        if "Raid" in option_labels:
            choice = search_options[option_labels.index("Raid")]
        elif "Explore" in option_labels:
            choice = search_options[option_labels.index("Explore")]
        elif "Report to authorities" in option_labels:
            choice = search_options[random.randint(0,1)]
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"])
    except IndexError:
        print("bruh")


def mine():
    try:
        # if random.randint(1, 16) == 8:
        #     send_message(connect(), text[4], random.choice([".mnie", ".imne", ".mien"]))
        #     time.sleep(0.5)
        send_message(connect(), text[4], ".mine")
    except Exception as e:
        print("Encountered exception during mining:", e)


def chop():
    try:
        # if random.randint(1, 16) == 8:
        #     send_message(connect(), text[4], random.choice([".chpo", ".cohp"]))
        #     time.sleep(0.5)
        send_message(connect(), text[4], ".chop")
    except Exception as e:
        print("Encountered exception during mining:", e)


def fish():
    try:
        # if random.randint(1, 16) == 8:
        #     send_message(connect(), text[4], random.choice([".fsh", ".fsih", ".fihs"]))
        #     time.sleep(0.5)
        send_message(connect(), text[4], ".fish")
    except Exception as e:
        print("Encountered exception during mining:", e)


def watch_for_bob():
    global keep_running
    while True:
        if not keep_running:
            return
        response = get_response(connect(), text[4])
        if response[0]["author"]["id"] == "801298619533754399":
            notification = Notify()
            notification.audio = ""
            notification.send()
            keep_running = False
            return
        time.sleep(1)


def main():
    global keep_running
    # bal_now = True
    while True:
        if not keep_running:
            return
        search()
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(7.5)
        mine()
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(7)
        chop()
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(7)
        fish()
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(7)
        # if bal_now:
        #     bal()
        #     bal_now = False
        # else:
        #     bal_now = True
        # time.sleep(6)


def main2():
    global keep_running
    while True:
        mine()
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(14.5)
        chop()
        time.sleep(0.5)
        response_dict = get_response(connect(), text[4])
        if response_dict[0]["author"]["id"] == "561981424157196288":
            keep_running = False
        if not keep_running:
            return
        time.sleep(14.5)


listener = keyboard.Listener(on_press=on_press)
listener.start()
main_thread = threading.Thread(target=main)
main_thread.start()
bob = threading.Thread(target=watch_for_bob)
bob.start()
