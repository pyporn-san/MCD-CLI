import concurrent.futures
import datetime
import os
from itertools import repeat

from colorama import Fore, init
from multporn import Multporn, Utils, Webpage
from termcolor import colored

init()


def main():
    # Choosing the links' input method
    try:
        print("Mode :")
        print(f"{colored('0', 'green')} To load from \"links.txt\" {colored('default', 'cyan')}")
        print(f"{colored('1', 'green')} For finding links in a webpage")
        print(f"{colored('2', 'green')} To search a query")
        Mode = int(cinput(f"{colored('3', 'green')} To input links manually "))
        if(Mode > 3 or Mode < 0):
            Mode = 0
    except ValueError:
        Mode = 0
    links = provideLinks(Mode)
    # Calling the Download function
    start = datetime.datetime.now()
    if links:
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            future_to_url = {executor.submit(Multporn, url, True): url for url in links}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as exc:
                    print(colored(f"{url} generated an exception: {exc}","red"))
    print(f"Done, took ", colored(datetime.datetime.now()-start, 'yellow'))
    _continue = cinput(f"Continue {colored('[Y/(N)]', 'cyan')}")
    if (_continue.lower().startswith("y")):
        return True
    else:
        return False


def provideLinks(arg):
    switcher = {
        0: fromFile,
        1: fromWebpage,
        2: search,
        3: manual}
    return switcher.get(arg)()


def fromFile():
    try:
        with open("links.txt", "r") as f:
            links = f.read().splitlines()
            if(not links):
                print(colored('\"links.txt\" is empty', 'red'))
            return links
    except:
        print(colored('\"links.exe\" doesn\'t exist', 'red'))
        with open("links.txt", "w") as _:
            pass
        links = []


def fromWebpage():
    page = Webpage(input("The webpage to load links from : "))
    return page.links


def search():
    query = input("Search query: ")
    try:
        page = int(
            cinput(f"What pages to load {colored('(Defaults to first page)', 'cyan')}: "))
    except:
        page = 1
    links = Utils.Search(query, page)
    for i in range(len(links)):
        print(f"{colored(f'{i+1}.', 'green')} {links[i]['name']}")
    try:
        page = int(
            cinput(f"Choose comic {colored('(Defaults to first)', 'cyan')}: "))-1
    except ValueError:
        page = 0
    return [links[page]["link"]]


def manual():
    try:
        num = int(cinput(f"Number of links {colored('1', 'cyan')}: "))
    except ValueError:
        num = 1
    links = [input(f"Link {str(i + 1)} : ") for i in range(num)]
    return links


def cinput(prompt):
    print(prompt, end="")
    return input()


if __name__ == "__main__":
    # Main loop
    while main():
        pass
