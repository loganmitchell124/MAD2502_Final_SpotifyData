import json

def import_json_from_user():
    """
    Author: Samantha Cuenot
    Summary: takes user spotify input and converts it to json
    """
    file_path = input("Please enter the path to the json file: ")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON")
        return None
    except Exception as e:
        print("Error: " + str(e))
        return None

