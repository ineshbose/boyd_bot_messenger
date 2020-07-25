# Working

## Webhook

POST requests is what brings this app to life.


## App Flow

A POST request is sent by the platform to the webhook URL. This request data is spread across the app going from one function to another and being parsed.


## Calendar Cache

In `Timetable`, `calendar` acts as a cache dictionary keeping calendars for all users. This helps the app in being fast and also fetching constant changes.