# ![Logo](https://raw.githubusercontent.com/ineshbose/boyd_bot_messenger/master/docs/images/readme.png)

<p align="center">
<a href="https://github.com/ineshbose/boyd_bot_messenger/deployments" target="_blank"><img alt="GitHub deployments" src="https://img.shields.io/github/deployments/ineshbose/boyd_bot_messenger/boydbot?style=flat-square"></a>
<a href="https://app.codacy.com/manual/ineshbose/boyd_bot_messenger" target="_blank"><img alt="Codacy grade" src="https://img.shields.io/codacy/grade/a0e3d46567f54d5790b43445759eb749?style=flat-square"></a>
<a href="https://codeclimate.com/github/ineshbose/boyd_bot_messenger" target="_blank"><img alt="Code Climate maintainability" src="https://img.shields.io/codeclimate/maintainability/ineshbose/boyd_bot_messenger?style=flat-square"></a>
<a href="https://boyd-bot-messenger.readthedocs.io/en/latest/" target="_blank"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/boyd-bot-messenger?style=flat-square"></a>
<a href="https://libraries.io/github/ineshbose/boyd_bot_messenger" target="_blank"><img alt="Libraries.io dependency status for GitHub repo" src="https://img.shields.io/librariesio/github/ineshbose/boyd_bot_messenger?style=flat-square"></a>
<br>
<a href="https://github.com/ineshbose/boyd_bot_messenger/releases" target="_blank"><img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/ineshbose/boyd_bot_messenger?label=version&style=flat-square"></a>
<a href="https://github.com/PyCQA/bandit" target="_blank"><img alt="Security: bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg?style=flat-square"></a>
<a href="https://github.com/psf/black" target="_blank"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>
<a href="https://github.com/ineshbose/boyd_bot_messenger/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/ineshbose/boyd_bot_messenger?style=flat-square"></a>
<br>
<a href="https://gitter.im/ineshbose/boyd_bot_messenger" target="_blank"><img alt="Gitter" src="https://img.shields.io/gitter/room/ineshbose/boyd_bot_messenger?color=blueviolet&style=flat-square"></a>
<a href="https://www.firsttimersonly.com/" target="_blank"><img alt="first-timers-only" src="https://img.shields.io/badge/first--timers--only-friendly-blue.svg?style=flat-square"></a>
<a href="https://github.com/ineshbose/boyd_bot_messenger/pulse"><img alt="Made with love in Glasgow" src="https://madewithlove.now.sh/gb?heart=true&template=flat-square&text=Glasgow"></a>
<a href="https://opensource.org/"><img alt="Respect Open Source" src="https://img.shields.io/badge/respect-open%20source-critical?style=flat-square"></a>
<a href="https://github.com/ineshbose/boyd_bot_messenger"><img alt="Powered by Boyd Bot" src="https://img.shields.io/badge/powered%20by-Boyd%20Bot-5c6cff?style=flat-square"></a>
</p>
<p align="center">
<a href="https://www.facebook.com/uofgbot" target="_blank"><img alt="Facebook" src="https://img.shields.io/badge/-Facebook-22488C?style=flat-square&logo=facebook&logoColor=white&labelColor=22488C"></a>
<a href="https://m.me/uofgbot" target="_blank"><img alt="Messenger" src="https://img.shields.io/badge/-Messenger-3CB0FF?style=flat-square&logo=messenger&logoColor=white&labelColor=3CB0FF"></a>
<a href="https://www.behance.net/gallery/93421281/Glasgow-University-Timetable-Bot" target="_blank"><img alt="Behance" src="https://img.shields.io/badge/-Behance-195CFF?style=flat-square&logo=behance&logoColor=white&labelColor=195CFF"></a>
</p>


This repository is for the Flask version of the Boyd Bot - a chatbot helping university students with their timetable. <br />



## 🔧 Setup

### Cloning

The first step is to clone the repository in your preferred directory using

```sh
$ git clone https://github.com/ineshbose/boyd_bot_messenger
$ cd boyd_bot_messenger
```

This requires [Git](https://git-scm.com/) installed; you can also download a [ZIP](https://github.com/ineshbose/boyd_bot_messenger/archive/master.zip) instead.


### Packages

All requirements have been listed in `requirements.txt`, they can be installed in your preferred environment using

```sh
$ pip install -r requirements.txt
```


### Environment Variables

Access tokens, keys, etc. have been hidden from the repository for obvious reasons. These are used as environment variables.

```python
import os

xyz = os.environ.get("XYZ_KEY")
```

You **must** replace these with your own. You can either just replace `os.environ.get()` with the value (**this is discouraged**), or use

```sh
$ set XYZ_KEY="random_key_value"
```



## 🏛️ Want to use this for your university? [Fork it!](https://github.com/ineshbose/boyd_bot_messenger/fork)

It's lovely to know that you're considering to use this for your university. This project aims to act a base for many other chatbots. You can also [use this repository as a template](https://github.com/ineshbose/boyd_bot_messenger/generate). A good idea is to start development with the [terminal / CLI version](https://github.com/ineshbose/boyd_bot_terminal). The following are considerations / instructions that you should know about if you aren't aware:

### Services

This version uses some external services that should be easily replaceable.

* [Facebook Messenger](https://www.facebook.com/messenger): The idea for this project is to present the timetable without having to install another application. A large number of university students use Facebook and its messaging service - Messenger. Users are identified using their unique IDs generated by Facebook specific to the app.
* [Dialogflow](https://dialogflow.com/): also known as API AI. This enables webhook, integration with Facebook Messenger (and also other messaging services if needed), intents and small talk.
* [mongoDB](https://www.mongodb.com/): This is to store user details to acquire their timetable while being fast and convenient.

### Instructions

The code is documented using _docstrings_ on [Read the Docs](https://boyd-bot-messenger.readthedocs.io/en/latest/); make sure you go through it. Since this repository acts like a template, there is not much to change. Much of it is mentioned, for example

```python
tmzn = pytz.timezone("Europe/London")   # Timezone
cal_url = "link/to/timetable.ics"       # University ICS link
```


Templates should also be tailored to your need. Go through the files in [templates](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/templates) and [static](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/static).

### Deployment

Be sure to do your research on where and how to deploy your code! Make sure that access tokens, keys, etc. are changed, and, along with the code & database, are **secure**.


## 🙌 Contributions & Thanks

Contributions are more than welcome in any form, they are all allowed under the [MIT License](https://github.com/ineshbose/boyd_bot_messenger/blob/master/LICENSE)! 😄<br />

### Issues & Enhancements

There may be some planned updates or issues for this project. They're listed in the [issues section](https://github.com/ineshbose/boyd_bot_messenger/issues) with a helpful description (hopefully). Feel free to help out in order to solve these.

### Testers

* [Jakub Jelinek](https://github.com/kubajj)
* _Looking for Testers! **(for code security too)**_

### Special Thanks

* [Tom Wallis](https://github.com/probablytom)
* [Lakshay Kalbhor](https://github.com/kalbhor) and [Neel Vashisht](https://github.com/NeelVashisht),<br /> my high-school seniors, with their [similar project](https://github.com/kalbhor/MIT-Hodor)