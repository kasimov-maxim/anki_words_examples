from typing import Any

import requests

__all__ = [
    "send_anki_request",
]


class InvalidResponseError(Exception):
    """Exception raised for errors in the response format."""


class ServerError(Exception):
    """Exception raised for errors returned by the server."""


def send_anki_request(action: str, **params: Any) -> Any:
    """
    Sends a request to the local Anki server and
        returns the result of the action.
        See info about AnkiConnect plugin:
            https://ankiweb.net/shared/info/2055492159
            https://foosoft.net/projects/anki-connect/

    This function constructs a JSON request
        with the specified action and parameters,
        sends it to the Anki server
        at http://127.0.0.1:8765,
        and processes the response.

    :param action: The name of the action to execute on the Anki server.
    :param params: Additional parameters to include in the request.
    :return: The result of the action from the server.
    :raises InvalidResponseError: If the response is missing required fields.
    :raises ServerError: If the server returns an error.
    """
    # Server URL and API version
    url = "http://127.0.0.1:8765"
    version = 6

    # Create the request payload
    request_payload: dict[str, Any] = {
        "action": action,
        "params": params,
        "version": version,
    }

    # Send the request to the Anki server
    response = requests.post(url, json=request_payload, timeout=15)
    response.raise_for_status()  # Check for HTTP errors

    # Decode the JSON response
    response_json: dict[str, Any] = response.json()

    # Validate the response structure
    if "error" not in response_json or "result" not in response_json:
        raise InvalidResponseError("Response is missing required fields")

    # Check if the server returned an error
    if response_json.get("error") is not None:
        print(response_json)
        raise ServerError(response_json["error"])

    # Return the result of the action
    return response_json["result"]


def get_field_value(note: dict[str, Any], field_name: str) -> str | None:
    """
    Retrieves the value of a specified field in a note.

    :param note: A dictionary representing the Anki note.
    :param field_name: The name of the field whose value to retrieve.
    :return: The field value as a string if it exists, otherwise None.
    """
    return note["fields"].get(field_name, {}).get("value", None)


def clean_word(word: str) -> str:
    """
    Cleans the word by taking the last part if it contains a slash
    and trimming any extra whitespace.

    :param word: The word to clean.
    :return: The cleaned word.
    """
    return word.split("/")[-1].strip() if "/" in word else word.strip()


if __name__ == "__main__":
    # send_anki_request("createDeck", deck="test1")
    # result = send_anki_request("deckNames")
    # print(f"got list of decks: {result}")
    #
    # card_list = send_anki_request("findNotes", query="deck:459")
    # print(f"got list of {len(card_list)} cards: {card_list}")
    #
    # update_result = send_anki_request("updateNote", note={
    #         "id": 1729260796966,
    #         "fields": {
    #             "examples": """..."""
    #         }
    #     }
    # )
    # note = send_anki_request("notesInfo", notes=(1729260796966,))
    # print(json.dumps(note[-1]))

    notes = send_anki_request("notesInfo", notes=(1729260796966,))
    print(notes[-1])
