from getpass import getpass
from requests.auth import HTTPBasicAuth
import pyfiglet # type: ignore
from pyfiglet import FigletString  # type: ignore
from typing import Type, List, Any, Dict, Union, cast
import requests
import json

# global variable defining API server address
SERVER_URL = "http://127.0.0.1:8080"
# indicate if "next" menu is shown
next_menu = False
# number for exit in menus
exit_number = ["3","7"]
# number for get movies in user menu
get_movies = "1"
# number for create user menu or return
create_return = "2"
# number for get a random quote
random_quote = "3"
# number for search a quote
search_quote = "4"
# number for add a quote to user tops
add_quote = "5"
# number for get user's top quotes
get_tops = "6"

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


def show_options(state: str) -> Union[List[str], None]:
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
        "5 - Add a quote to your top by quote's id",
        "6 - Get user's top quotes",
        "7 - Exit the program"
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

def check_choice_validity(choice: Union[str, None], actions: Union[List[str], None])-> bool:
    """
    Function receive a int with a number of user's choice and perform one of the API calls accordingly
    :param choice: Integer parameter defining user's choice of action
    :return: Return True is choice is valide, False - in other case
    :rtype: Boolean
    """
    try:
        if choice is None or actions is None:
            return False
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
        if (next_menu and choice == exit_number[0]) or (not next_menu and choice == exit_number[1]):
            # user chose to exit
            show_exit()
            exit(0)
        elif not next_menu or (next_menu and choice == get_movies and choice != create_return):
            # if called from main menu or from next menu and user chosen option 1 == repeat the last action
            if next_menu and choice == get_movies:
                choice = previous_choice

            if choice == get_movies:
                # get movies list
                response = send_get(f"{SERVER_URL}/movies")
                if not response == None:
                    print(json.dumps(response, indent=1))
                    print("")
                else:
                    show_something_wrong()

            elif choice == create_return:
                # create a new user
                print("Enter new user's name and password")
                username, password = get_user_credentials()
                body = {"username": username, "password": password}
                response = send_post(f"{SERVER_URL}/users", body)
                if not response == None:
                    print(f"User was created with id: {response['id']}")
                    print("")
                else:
                    show_something_wrong()

            elif choice == random_quote:
                # get a random quote
                response = send_get(f"{SERVER_URL}/quotes/random")
                if not response == None:
                    print(json.dumps(response, indent=1))
                    print("")
                else:
                    show_something_wrong()

            elif choice == search_quote:
                # search for a quote
                search_text = input("Enter a phrase to search a quote for: ").strip()
                response = send_get(f"{SERVER_URL}/quotes/search?text={search_text}")
                if not response == None:
                    print(json.dumps(response, indent=1))
                    print("")
                else:
                    show_something_wrong()

            elif choice == add_quote:
                # add quote to user's top list
                while True:
                    try:
                        quote_number = int(input("Id of a quote to add to the top quotes: "))
                        break
                    except ValueError:
                        print("Only integers are allowed. Try again")
                        print("")
                        continue
                print("Enter user's name and password")
                # the program won't save user and password in session by design
                # as it will require also log-out functionality - could be a future development
                username, password = get_user_credentials()
                creds = [username, password]
                response = send_get(f"{SERVER_URL}/users/id", creds)
                if not response == None:
                    user_id = response
                else:
                    show_something_wrong()

                payload = {"id": quote_number}
                response = send_post(f"{SERVER_URL}/users/{user_id}/tops", payload, creds)
                if not response == None:
                    print(json.dumps(response, indent=1))
                    print("")
                else:
                    show_something_wrong()

            elif choice == get_tops:
                # get user's top quotes
                print("Enter user's name and password")
                # the program won't save user and password in session by design
                # as it will require also log-out functionality - could be a future development
                username, password = get_user_credentials()
                creds = [username, password]

                user_id = send_get(f"{SERVER_URL}/users/id", creds)
                if not user_id == None:
                    response = send_get(f"{SERVER_URL}/users/{user_id}/tops", creds)
                else:
                    response = None

                if not response == None:
                    print(json.dumps(response, indent=1))
                else:
                    show_something_wrong()
            else:
                # all non-implemented
                print("Will be implemented soon, try another one!")
                print("")
        elif next_menu and choice == create_return:
            # user chose to return to main menu
            next_menu = not next_menu
    except KeyboardInterrupt:
        print("")
    except Exception:
        next_menu = True
        show_something_wrong()

def send_get(url: str, credentials: List[str] = list())-> Any:
    """
    Function receives an url and return the result of a get request
    :param url: Url to perform get request
    :return: Return json of the result or None if status code was not == ok
    :rtype: Any
    """
    if len(credentials)>0:
        response = requests.get(url, auth=HTTPBasicAuth(*credentials))
    else:
        response = requests.get(url)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def send_post(url: str, payload: Union[Dict[str,int],Dict[str,str]] = cast(Union[Dict[str, int], Dict[str, str]], None), credentials: List[str] = list())-> Any:
    """
    Function receives an url and return the result of a post request
    :param url: Url to perform get request
    :param payload: A dictionary with payload==body for the post request
    :return: Return json of the result or None if status code was not == ok
    :rtype: Any
    """
    if payload is None:
        payload = {}

    if len(credentials)>0:
        response = requests.post(url, json=payload, auth=HTTPBasicAuth(*credentials))
    else:
        response = requests.post(url, json=payload)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

if __name__ == "__main__":
    main()
