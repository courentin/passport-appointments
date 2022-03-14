from collections import defaultdict
from turtle import delay
from typing import Dict, Iterable
from parso import parse
import requests
from bs4 import BeautifulSoup
import datetime
import time
import subprocess
from argparse import ArgumentParser

CMD = """
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
"""


def notify(title, text):
    subprocess.call(["osascript", "-e", CMD, title, text])


def request_website():
    url = "https://teleservices.paris.fr/rdvtitres/jsp/site/Portal.jsp?page=appointmentsearch&view=search&category=titres"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    return soup


def extract_next_next_available_appointments(soup: BeautifulSoup):
    next_available_appointments = soup.select(".nextAvailableAppointments > div")
    next_available_appointments_dict = defaultdict(list)
    for next_appointment in next_available_appointments:
        location = next_appointment.select_one("h4").text.strip()
        address = next_appointment.select_one(":nth-child(2) > div > p").text.strip()
        slots = next_appointment.select("ul > li > a")
        for slot in slots:
            text_slot = slot.text.strip()
            #                                      20 October 2021 10:30
            date_slot = datetime.datetime.strptime(text_slot, "%d %B %Y %H:%M")
            next_available_appointments_dict[f"{location} ({address})"].append(
                date_slot
            )

    return next_available_appointments_dict


def filter_next_x_days(
    next_available_appointments: Dict[str, Iterable[datetime.datetime]], x: int
):
    in_x_days = datetime.datetime.now() + datetime.timedelta(days=x)
    filtered_slots = {
        location: [slot for slot in slots if slot <= in_x_days]
        for location, slots in next_available_appointments.items()
    }

    return {
        location: slots for location, slots in filtered_slots.items() if len(slots) > 0
    }

if __name__ == "__main__":
    parser = ArgumentParser(
        description="A script that searches appointments for passport in Paris",
    )
    parser.add_argument("--disable-notification", action="store_true")

    args = parser.parse_args()

    should_continue = True
    while should_continue:
        time.sleep(10)
        soup = request_website()
        next_available_appointments = extract_next_next_available_appointments(soup)
        filtered_appointments = filter_next_x_days(next_available_appointments, 14)

        if filtered_appointments:
            for location, slots in filtered_appointments.items():
                pass
            print(filtered_appointments)
            print(
                "https://teleservices.paris.fr/rdvtitres/jsp/site/Portal.jsp?page=appointmentsearch&view=search&category=titres"
            )
            if not args.disable_notification:
                notify("Found slots !!", "See the console")
            should_continue = False
