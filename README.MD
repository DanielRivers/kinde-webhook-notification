Play a MP3 sound when you get a new `user.created` webhook from Kinde

```bash
pip install Flask pyjwt requests cryptography
brew install mpg123

FLASK_APP=app.py flask run
```

This will start to accept webhooks on - http://127.0.0.1:5000/webhook

Will need to deploy somewhere public to test it out with live webhooks.