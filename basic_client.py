import requests
from config import HOST, PORT, ENDPOINT

def call_api(base_url, payload):
    """
    Calls the API to get a biased random number.

    Parameters:
        base_url (str): The base URL of the API.
        payload (dict): A dictionary containing the probability distribution.

    Returns:
        dict: The response from the API as a Python dictionary.
    """
    try:
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None

if __name__ == "__main__":
    url = f"http://{HOST}:{PORT}{ENDPOINT}"
    data = {
        "probabilities": [0.1, 0.2, 0.3, 0.1, 0.2, 0.1],
        "number_of_random": 10
    }

    print("Calling the API with payload:")
    print(data)

    result = call_api(url, data)
    print(type(result))
    print(result)