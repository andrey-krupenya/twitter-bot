# Tweeter Bot

This application helps you automate work with the tweeter.
Search special words and generate efficient answers from templates.

## Getting Started

This application builds on the Django Framework.
To run it, please get code from the repository. 
Set the environment with requirements.

And run: 
```
python manage.py runserver
```

### Installing

Use file requirements.txt for installing all required package

```
pip install -r requirements.txt
```

## Running the tests

DB has being generated fixtures with a dictionary. 
It will be saved into **app_for_trafic/fixtures/fixture_for_testing.json** file.

```
python manage.py test --noinput --settings=bot_for_trafic.settings_test --verbosity=2
```

### Break down into end to end tests

Check all conditions.

### And coding style tests

Use PEP8 as a base style. 
Also, you can use google advanced for python code style

## Built With

* [DRF](https://www.django-rest-framework.org/) - The Django rest framework used
* [Tweepy](https://www.tweepy.org/) - Python library for accessing the Twitter API
* [Google style guide](https://google.github.io/styleguide/pyguide.html) - Google style guide


## Versioning

Version 1.0

## Authors

* **Andrey Krupenya** - *Initial work* - [TweeterBot](https://github.com/andrey-krupenya/twitter-bot)

## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
