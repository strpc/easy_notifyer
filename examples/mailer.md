```python
from easy_notifyer import mailer_reporter


@mailer_reporter(
    host='smtp.example.org',
    port=587,
    login='login@example.com',
    password='qwerty12345',
    from_addr='login@example.com',
    to_addrs='myemail@gmail.com, mysecondmail@mail.com',
    ssl=False,
    exceptions=ValueError,
)
def bar():
    ...
    raise ValueError
```

```python
import os

from easy_notifyer import mailer_reporter


# set params as environment variables.
os.environ.setdefault('EASY_NOTIFYER_MAILER_HOST', "smtp.example.org")
os.environ.setdefault('EASY_NOTIFYER_MAILER_PORT', "587")
os.environ.setdefault('EASY_NOTIFYER_MAILER_LOGIN', "login@example.com")
os.environ.setdefault('EASY_NOTIFYER_MAILER_PASSWORD', "qwerty12345")
os.environ.setdefault('EASY_NOTIFYER_MAILER_FROM', "login@example.com")
os.environ.setdefault('EASY_NOTIFYER_MAILER_TO', "myemail@gmail.com, mysecondmail@mail.com")
os.environ.setdefault('EASY_NOTIFYER_MAILER_SSL', "False")


@mailer_reporter(
    exceptions=ZeroDivisionError,
    as_attached=True,
    filename='bar_report.log',
    header='Testing for bar',
    subject='hello from foobar',
)
async def bar():
    ...
    a = 1 / 0
 

@mailer_reporter(
    exceptions=AttributeError, 
    subject='AttributeError sended as a attach', 
    as_attached=True
)
@mailer_reporter(subject='All errors, sended as body msg')
def foo():
    ...
    raise AttributeError

```

```python
from easy_notifyer import Mailer

def main():
    with Mailer() as mailer:
        try:
            raise ValueError
        except ValueError:
            mailer.send_message(message='Something went wrong')
        
        file = open('image from main.jpg', 'rb')
        mailer.send_message(attach=file, filename='my_image.jpg')
        mailer.send_message(attach=b'hello world from main func')
        mailer.send_message(attach=b'hello world from main func', filename='hello.txt')
```
