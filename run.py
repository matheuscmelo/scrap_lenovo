import requests
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep
class RequestThread(Thread):

    def __init__(self, msgs, code, codes):
        self.msgs = msgs
        self.code = code
        self.codes = codes
        Thread.__init__(self)
    
    def run(self):
        page = requests.get("http://systemx.lenovofiles.com/help/topic/com.lenovo.conv.8695.doc/{}.html".format(self.code))
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('title').contents[0]
        if "server" in title:
            page_topic = soup.find('h1', class_="title topictitle1").contents[0].lower()
            prefix_and_id = soup.find_all('strong', class_="ph b")
            prefix_and_id = list(prefix_and_id[0].parent.parent)
            prefix = prefix_and_id[1].contents[1]
            id = prefix_and_id[3].contents[2]
            print(prefix + id)
            if (prefix+id) not in self.codes:
                severity = soup.find_all('div', class_="section")[1].contents[1].contents[0].strip()
                topic = ""
                if len(addition_set.intersection(set(page_topic.split()))) > 0:
                    topic = "addition"
                elif len(deletion_set.intersection(set(page_topic.split()))) > 0:
                    topic = "deletion"
                elif len(status_set.intersection(set(page_topic.split()))) > 0:
                    topic = "status"
                elif len(login_set.intersection(set(page_topic.split()))) > 0:
                    topic = "login"
                elif len(network_set.intersection(set(page_topic.split()))) > 0:
                    topic = "network"
                elif len(power_set.intersection(set(page_topic.split()))) > 0:
                    topic = "power"
                elif len(security_set.intersection(set(page_topic.split()))) > 0:
                    topic = "security"
                elif len(firmware_set.intersection(set(page_topic.split()))) > 0:
                    topic = "firmware"
                elif len(device_set.intersection(set(page_topic.split()))) > 0:
                    topic = "device"
                elif len(storage_set.intersection(set(page_topic.split()))) > 0:
                    topic = "storage"
                elif len(system_set.intersection(set(page_topic.split()))) > 0:
                    topic = "system"
                else:
                    topic = "other"
                if topic != "other":
                    self.codes.add(prefix + id)
                self.msgs[topic].add("{} {}".format(prefix + id, severity))

page = requests.get('http://systemx.lenovofiles.com/help/topic/com.lenovo.conv.8695.doc/r_imm_error_messages.html')

soup = BeautifulSoup(page.content, 'html.parser')
msgs = {name:set() for name in ["network", "login", "power", "security", "firmware", "device", "other", "status", "storage", "system", "addition", "deletion"]}
# "other" is meant to hold all error messages that were not classified

# all sets containing adequate words for classification
deletion_set = set(['deleted', 'deleted.'])
addition_set = set(['added', 'add', 'created', 'created.', ])
network_set = set(["network", "ethernet", "ip", "hostname", "lan", "dchp","ssh", "connection", "lan:", "enet[[arg1]]"])
login_set = set(["SNMPv3","login", "password"])
power_set = set(["power-cycled","power", "boot", "powered", "reset", "power:", "restart", "restarted", "reset."])
security_set = set(["detected","security", "certificate", "ssl", "security:"])
status_set = set(["failed.","failed","set","made","terminated.","terminated","succeeded.","succeeded","problems", "problem","status", "enable", "enabled", "disable", "disabled", "scheduled", "started", "completed", "cleared", "enabled.", "disabled.", "started.", "removed", "removed.", "remove", "changed", "changed.", "generated", "generated.", "error", "errors", "alert", "alerts", "by"])
firmware_set = set(["firmware"])
device_set = set(["(fan","sensor", "computersystemelementname", "fan", "device"])
storage_set = set(["storagevolumeelementname", "storage", "enclosure", "enclosure."])
system_set = set(["drive","[computersystemelementname]", "[computersystemelementname].", "computersystemelementname", "cpu", "bios", "supply", "[powersupplyelementname]", "[powersupplyelementname].", "powersupplyelementname", "uefi", "uefi.", "uefi:", "subsystem", "subsystem:"])

raw_links = list(soup.find_all('li', class_="link ulchildlink"))
raw_links = [link.contents for link in raw_links]
threads = [] #using threads to improve performance
codes = set()
for i in range(1, len(raw_links)):
    code = raw_links[i][0].contents[0].contents[0][:17].split("-")
    code = code[0] + code[1]
    thread = RequestThread(msgs, code, codes)
    thread.start()
    threads.append(thread)
    sleep(0.05)

all_stopped = False
while not all_stopped:
    for thread in threads:
        all_stopped = all_stopped or not thread.is_alive()
    sleep(0.2)

sleep(2)

# remove repeated codes from "other"
keys = set(msgs.keys())
keys.remove("other")
contains = []
for category in keys:
    for msg in msgs[category]:
        id1 = msg.split()[0]
        for msg_other in msgs["other"]:
            id2 = msg_other.split()[0]
            if id1 == id2:
                contains.append(msg_other)

for msg in contains:
    msgs["other"].remove(msg)

for category in msgs.keys():
    with open(category + ".txt", 'a+') as file:
        for msg in msgs[category]:
            file.write(msg + "\n")

    
