# WIP

## [Dialogflow](https://dialogflow.com/)

Implemented in _class_ `Parser`. This class, however, doesn't use any features of Dialogflow but handles intents externally to declutter `app.py`.


### `Parser`.**`delete_data(uid, db)`**

Generates response for `delete data` intent.

|                                   Parameters                                         |                    Returns                   |
|--------------------------------------------------------------------------------------|----------------------------------------------|
| **`uid`:** the unique sender ID of the user<br>**`db`:** the database to delete from | **`str`:** if deletion was successful or not |


### `Parser`.**`read_timetable(uid, data)`**

Generates response for `read timetable` intent. This method features a dictionary to map `date-time` (since they may vary for different services) and entities parameters to arguments in order to avoid a `if-elif-...-else` ladder.

```python
    param_keys = {
                    "date_time": ["date_time"],
                    "startDateTime": ["startDateTime", "endDateTime"],
                    "startDate": ["startDate", "endDate"],
                    "startTime": ["startTime", "endTime"],
                }
```

|                                  Parameters                                         |                        Returns                        |
|-------------------------------------------------------------------------------------|-------------------------------------------------------|
| **`uid`:** the university ID of the user<br>**`data`:** the POST request dictionary | **`list`:** schedule for days according to parameters |


### `Parser`.**`parse(uid, data, db)`**

The main method to be called for parsing. It finds intents handled by the app, calls the function and returns the response.

```python
>>> parse({"keys-to-intent": "delete data"}, "1234567890", "123456Z")
Deleted! :)
```

|                                                               Parameters                                                          |                                Returns                                   |
|-----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **`request_data`:** the POST request dictionary<br>**`uid`:** the unique sender ID of the user<br>**`db`:** the database instance | **`str`:** the response<br>**`None`:** if response is not handled by app |