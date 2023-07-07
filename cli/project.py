from getpass import getpass
from urllib.request import HTTPBasicAuthHandler
import pyfiglet # type: ignore
from pyfiglet import FigletString  # type: ignore
from typing import Type, List, Any, Dict
import requests
import sys

# global variable defining API server address
SERVER_URL = "http://127.0.0.1:8080"
# indicate if "next" menu is shown
next_menu = False

def main() -> None:
    """
    Main function which triggers intial logic and shows the main menu and subsequent actions
    :return: No return value
    :rtype: None
    """
    show_greeting()
    actions = show_options("main")
    prev_choice = ""
    choice = ""
    while True:
        try:
            prev_choice = choice
            choice = input("Type an option number: ")
            print("")
            if not check_choice_validity(choice, actions):
                continue
            perform_action(choice, prev_choice)
            actions = show_options("next" if next_menu else "main")
        except KeyboardInterrupt:
            show_exit()
            break
        except Exception:
            # if user not entered a numerical or did other error choosing menu or something else happend
            show_something_wrong()
            continue

def get_figlet(text: str) -> Type[FigletString]:
    """
    Function return text in figlet font == digital
    :return: Return a string transformed from text using pyfiglet library
    :rtype: str
    """
    return pyfiglet.figlet_format(text, font = "digital" )


def get_user_credentials()-> List[str]:
    """
    Function requests for a user name and password
    :return: No return value
    :rtype: A list with username at pos 0 and password at post 1 in it
    """
    username = input("Username: ").strip()
    password = getpass().strip()
    return [username, password]

def show_greeting()->None:
    """
    Function prints greeting
    :return: No return value
    :rtype: None
    """
    print(get_figlet("""
    MONTY PYTHON BEST QUOTES API!
        CLI to interact with it
    """))
    print("         For more info - check project's README.md")
    print("")

def show_exit()->None:
    """
    Function prints exit information and exits programm
    :return: No return value
    :rtype: None
    """
    print("")
    print("===================================")
    print("Program closed by user")
    print("===================================")
    print("")


def show_options(state: str)->List[str]:
    """
    Function prints available option from the current point of program's flow
    :param state: String parameter defining the logic - which options to show
    :return: No return value
    :rtype: List with available options as strings
    """
    actions = []
    if state=="main":
        actions = [
        "1 - Get a list of all movies from which quotes are available",
        "2 - Create a new user to store top quotes list",
        "3 - Get a random quote",
        "4 - Search for a quote/quotes",
        "5 - Get a random scene (all quotes from a scene will be printed)",
        "6 - Search for a scene by a movie name and scene name/number",
        "7 - Add a quote to your top by quote's id",
        "8 - Exit the program"
        ]
    elif state=="next":
        actions = [
        "1 - Repeat the last action",
        "2 - Return to the main menu",
        "3 - Exit the program"
        ]
    if len(actions)>0:
        print("===================================")
        print("Choose an action:")
        for element in actions:
            print(element)
        print("===================================")
        return actions
    else:
        return None

def check_choice_validity(choice: str, actions: List[str])-> bool:
    """
    Function receive a int with a number of user's choice and perform one of the API calls accordingly
    :param choice: Integer parameter defining user's choice of action
    :return: Return True is choice is valide, False - in other case
    :rtype: Boolean
    """
    try:
        choice_as_number = int(choice)
        if actions[choice_as_number-1].find(str(choice_as_number)) != -1:
            return True
        else:
            # action with a given number is not in actions list
            return False
    except:
        # not a number was given
        show_something_wrong()
        return False

def show_something_wrong()->None:
    """
    Function prints a warning about unexpected end of the request
    :return: No return value
    :rtype: None
    """
    print("===================================")
    print("Ooops, something went wrong")
    print("")


def perform_action(choice: str, previous_choice: str)-> None:
    """
    Function receive a int with a number of user's choice and perform one of the API calls accordingly
    :param choice: String parameter defining user's choice of action
    :param previous_choice: String parameter user's previous action
    :return: No return value
    :rtype: None
    """
    global next_menu
    try:
        if (next_menu and choice == "3") or (not next_menu and choice == "8"):
            # user chose to exit
            show_exit()
            exit(0)
        elif not next_menu or (next_menu and previous_choice == "1" and choice != "2"):
            # if called from main menu or from next menu and user chosen option 1 == repeat the last action
            if choice == "1":
                # get movies list
                response = send_get(f"{SERVER_URL}/movies")
                if not response == None:
                    for movie in response:
                        print(movie["name"][0])
                    print("")
                else:
                    show_something_wrong()
                    print(response)
            elif choice == "2":
                # create a new user
                print("Enter new user's name and password")
                username, password = get_user_credentials()
                body = {"username": username, "password": password}
                response = send_post(f"{SERVER_URL}/users", body)
                if not response == None:
                    print(f"User was created with id: {response['id']}")
                    print("")
                else:
                    print(response)
        elif next_menu and choice == "2":
            # user chose to return to main menu
            next_menu = not next_menu
    except KeyboardInterrupt:
        print("")
    except Exception:
        next_menu = True
        show_something_wrong()


def send_get(url: str)-> Any:
    """
    Function receives an url and return the result of a get request
    :param url: Url to perform get request
    :return: Return json of the result or None if status code was not == ok
    :rtype: Any
    """
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def send_post(url: str, payload: Dict[str,str] = {}, credentials: List[str] = list())-> Any:
    """
    Function receives an url and return the result of a post request
    :param url: Url to perform get request
    :param payload: A dictionary with payload==body for the post request
    :return: Return json of the result or None if status code was not == ok
    :rtype: Any
    """
    response = requests.post(url, json=payload if len(payload)>0 else "", auth=HTTPBasicAuthHandler(credentials) if len(credentials)>0 else "")

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

if __name__ == "__main__":
    main()