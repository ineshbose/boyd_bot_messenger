# Boyd Bot (Messenger)
[![GitHub deployments](https://img.shields.io/github/deployments/ineshbose/boyd_bot_messenger/boydbot?style=flat-square)](https://github.com/ineshbose/boyd_bot_messenger/deployments)
[![GitHub](https://img.shields.io/github/license/ineshbose/boyd_bot_messenger?style=flat-square)](LICENSE)
<a href="https://www.facebook.com/uofgbot"><img src="https://img.shields.io/badge/Facebook--informational?style=flat-square&logo=facebook" />
<a href="https://m.me/uofgbot"><img src="https://img.shields.io/badge/Messenger--9cf?style=flat-square&logo=messenger" />
<a href="https://www.behance.net/gallery/93421281/Glasgow-University-Timetable-Bot"><img src="https://img.shields.io/badge/Behance--lightgrey?style=flat-square&logo=behance" /></a>

This repository is for the Flask version of the Boyd Bot - a chatbot helping university students with their timetable. <br />
This version is specific to [University of Glasgow](https://www.gla.ac.uk/), and uses [Facebook Messenger](https://www.facebook.com/messenger) and [Dialogflow](https://dialogflow.com/).

## Set-Up
### Packages
All requirements have been listed in `requirements.txt`, they can be installed using
```
$ pip install -r requirements.txt
```

### Environment Variables
Access tokens, keys, etc have been hidden from this repository for obvious reasons. Wherever you see `os.environ.get()`, a key is being used. You may replace these with your own.

## To-Do
- [x] Read Next Class
- [ ] Locations
- [ ] Book Rooms (might have to ditch considering `selenium` is removed)
- [x] Small talk(?) (Switch to Dialogflow)
- [ ] Background Scheduler (opt-in feature)

## Note
This repository was created fresh as the previous (private) repository had some keys in the commit history. If any sensitive data is pushed accidentally, a new repository will be created.

## Contributions & Thanks
Contributions are more than welcome in any form! <br />

### Testers
* [Jakub Jelinek](https://github.com/kubajj)
* Jules Petrella
* [Luke Holland](https://github.com/AmazonPriime)
* [Marc Auf Der Heyde](https://github.com/marcaufderheyde)

### Special Thanks
* [Mr. Tom Wallis](https://github.com/probablytom)
* [Lakshay Kalbhor](https://github.com/kalbhor) and [Neel Vashisht](https://github.com/NeelVashisht),<br /> my high-school seniors, with their [similar project](https://github.com/kalbhor/MIT-Hodor)

<br /><hr><br />
More on [Behance](https://www.behance.net/gallery/93421281/Glasgow-University-Timetable-Bot).