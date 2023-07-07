# logic to scrap data for the database from website or html file
from bs4 import Tag, BeautifulSoup, NavigableString
from typing import Dict
import argparse
import collections, io
import csv, requests
import re, sys
from time import sleep
import roman # type: ignore


def main() -> None:
    """
    Main function calls check on CLI arguments, parse html function and write parsed into
    csv file. Support two modes:
    -m in command line is given - doesn't require -p parameter and works in multi-links mode - links are pre-defined in
    get_links()
    -p in command line is given - program parses only from given file
    :return: No return value
    :rtype: None
    """
    args = check_cli_arguments()

    if args.m:
    # Option for parsing of a links array
        links = get_links()
        for link in links:
            arr = parse(link, 1)
            write_to_csv(args.f,arr)
    elif args.p:
    # Option for one input file parsing
        arr = parse(args.p, args.h)
        write_to_csv(args.f,arr)


def check_cli_arguments() -> argparse.Namespace:
    """
    Check correctnes of the CLI arguments. Usage: datascrapper.py -h|--help|-m|-t <0/1>|-p <file-to-parse.html>|-f <csv-to-write.csv>
    :return: Args parsed of type argparse.Namespace
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog="datascrapper.py", description="Parse html file into csv")
    parser.add_argument("-m", action='store_true', help="Multi-link mode - links for scrapping are in the code, -p, -h are not needed")
    parser.add_argument("-p", help="File name of html file to parse")
    parser.add_argument("-t", nargs="?", default = 0, help="1 - parse html file by the given in -p link,\
                         0 - parse html file by given in -p path")
    parser.add_argument("-f", nargs="?", default = "results.csv", help="File name of csv file to write parsed results to")
    args = parser.parse_args()

    if (args.m and args.p) or (not args.m and not args.p):
        parser.print_usage()
        parser.exit(1)
    if args.t and args.t.find(".htm") == -1:
        print("Wrong -p parameter - should be htm or html file")
        parser.exit(1)
    if args.f and args.f.find(".csv") == -1:
        print("Wrong -f parameter - should be csv file")
        parser.exit(1)

    return args

def get_links() -> collections.abc.MutableSequence:
    # one time operation - all data scrapped into parsed_results.csv
    links = []

    # list of html pages for Life of Brian scripts
    # http://montypython.50webs.com/Life_of_Brian.htm
    for i in range(35):
        links.append(f"http://montypython.50webs.com/scripts/Life_of_Brian/{i+1}.htm")

    # list of html pages for Holy Grail scripts
    # http://montypython.50webs.com/Holy_Grail_Scripts.htm
    for i in range(23):
        links.append(f"http://montypython.50webs.com/scripts/Holy_Grail/Scene{i+1}.htm")

    # list of html pages for Life of Brian scripts
    # http://montypython.50webs.com/Meaning_of_Life.htm
    links.append("http://montypython.50webs.com/scripts/Meaning_of_Life/intro.htm")
    for i in range(13):
        links.append(f"http://montypython.50webs.com/scripts/Meaning_of_Life/{i+1}.htm")

    return links

def write_to_csv(fname: str, arr: collections.abc.MutableSequence) -> None:
    """
    Creates/updates a csv file out of an array with dicts. Dictionaries within array are identical
    :param arr: An array with dictionaries, all dictionaries are identical with keys:
    movie, scene_number, scene_name, character, type, text
    :param fname: a name for the csv which will be created/updated as a result of parsing
    :return: No return value, csv file <fname>.csv is created
    :rtype: None
    """

    fieldnames = ["movie", "scene_number", "scene_name", "type", "character", "text"]

    try:
        # try to open file
        with open(fname, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)  # Read all rows into memory as dictionaries

        # add data from array to the file and write it with existing data
        for row in arr:
            data.append(row)

        if reader.fieldnames is not None:
            fieldnames = list(reader.fieldnames)
        else:
            sys.exit("No fieldnames found in the scv file")

        with open(fname, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    except FileNotFoundError:
        # if file not exists - create it and write
        with open(fname, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arr)
    return None

def is_dialogue(tag: Tag) -> bool:
    """
    Filter only <p> tags with children <span> having class='name' -
    those are dialogues
    :param tag: BeautifulSoup object tag - bs4.element.Tag
    :return: True if tag satisfies the logic, False - if not
    :rtype: bool
    """
    if tag.name == "p":
        for ch in tag.children:
            if isinstance(ch, NavigableString):
                continue
            if isinstance(ch, Tag):
                return ch.name == "span" and ch.has_attr("class") and ch["class"]==["name"]
    return False

def is_directions(tag: Tag) -> bool:
    """
    Filter only <p> tags with children <i> tag -
    those are durections
    :param tag: BeautifulSoup object tag - bs4.element.Tag
    :return: True if tag satisfies the logic, False - if not
    :rtype: bool
    """
    if tag.name == "p":
        for ch in tag.children:
            if isinstance(ch, NavigableString):
                continue
            if isinstance(ch, Tag):
                return ch.name == "i"
    return False

def parse_scene(text: str) -> Dict[str, str]:
    """
    Parse text with scene number and name into dictionary with keys number, name
    :param text: String to parse, expected format: "Scene <Number>: " or "Part <Roman Number>: "
    :return: Dictionary {"Number": "1", "Name": "Name"}
    :rtype: Dict[str, str]
    """
    text = text.strip()
    # Scene can be formatted "Scene <Number>: " or "Part <Roman Number>: "
    matches = re.search(r"^(?P<Scene_number>(Scene ([1-9]|[12][0-9]|3[0-5])|Part ([MDCLXVI]+))): (?P<Scene_name>[a-z0-9 _\-\W]+)$", text, re.IGNORECASE)
    scene_number = "NULL"
    scene_name = "NULL"

    if matches:
        scene_number = matches.group("Scene_number")
        if scene_number.find("Part") != -1:
            scene_number = roman.fromRoman(scene_number.replace("Part","").strip())
        elif scene_number.find("Scene") != -1:
            scene_number = scene_number.replace("Scene","").strip()
        scene_name = matches.group("Scene_name")

    return {"scene_number": scene_number, "scene_name": scene_name}

def parse(html: str, url: int = 1) -> collections.abc.MutableSequence:
    """
    Parse given html. Parser is expecting <p> tags with <span> tags inside with class == 'name' - dialogues and
    <p> tags with <i> tags inside - directions. Source - http://montypython.50webs.com/scripts/Holy_Grail/Scene3.htm
    :param html: An html file to parse
    :param url: 0 - parse as a file, 1 - parse as html link
    :return: array of dictionaries with keys: movie, scene_number, scene, character, type (enum: direction, dialogue), phrase
    :rtype: array
    """
    if url:
    # parse from url
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
        }
        sleep(1)
        r = requests.get(html, headers=headers, verify=False)
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
    # parse from file
        try:
            with open(html,'r', encoding='iso-8859-1') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
        except FileNotFoundError:
            sys.exit(f"{html} file not found")

    # resulting array of dicts
    result = []

    # all h2 tags are movie name
    movie = "NULL"
    for h2 in soup.find_all("h2"):
        movie = h2.text
        # Clean data from Script text
        movie = movie.replace("Script", "").strip()
        break

    # all h1 tags are scene name in format Scene N: Scene name - parse with regex
    scene_number, scene_name = "NULL", "NULL"
    for h1 in soup.find_all("h1"):
        scene = h1.text.strip()
        scene_number, scene_name = parse_scene(scene).values()
        break

    for tg in soup.find_all("p"):
        # we totally rely here on the pre-defined html structure
        try:
            add_entry = False
            if is_dialogue(tg):
                character = tg.next.text.replace(":","").strip()
                phrase = tg.text.replace(tg.next.text,"").replace("\n","").strip()
                phtype = "dialogue"
                add_entry = True
            elif is_directions(tg):
                character = "NULL"
                phrase = tg.text.replace("\n","").strip()
                phtype = "direction"
                add_entry = True

            if add_entry:
                # dictionary with keys:
                # movie, scene_number, scene, character, type (enum: direction, dialogue), phrase
                entry = {}
                entry["movie"] = movie
                entry["character"] = character
                entry["scene_number"] = scene_number
                entry["scene_name"] = scene_name
                entry["type"] = phtype
                entry["text"] = phrase

                result.append(entry)
        except:
            sys.exit(f"{fp} format is not parsable")

    return result

if __name__ == "__main__":
    main()