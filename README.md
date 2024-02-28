# uwsgi and django harakiri behaviour

This experiment is to understand how uwsgi harakiri works with regards to multiple
processes and multiple threads.

We'd like the signal (SIGSYS/31) to be caught by the application so that we can
emit any cleanup logs/traces before the process is killed, to help us identify
attributes about slow requests.

Running the example:

```bash
# Create a python 3.10 virtualenv and activate it

$ pip install -r requirements.txt
$ cd app
$ uwsgi --ini uwsgi.ini

Then in a browser, launch http://127.0.0.1:8000/slow/
```

The sleep within the slow view is longer than the harakiri timeout, so we should
consistently see a harakiri on that view.

Is the signal caught within the application and the log messages from the signal
handler emitted?
