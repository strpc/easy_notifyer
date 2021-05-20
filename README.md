Easy Notifyer
========

![image](https://img.shields.io/pypi/v/easy_notifyer?color=yellowgreen)
![image](https://img.shields.io/github/languages/code-size/strpc/easy_notifyer)
![image](https://img.shields.io/badge/Python-3.7%2B-success)
![image](https://img.shields.io/github/license/strpc/easy_notifyer?color=informational)


Easy bug reporter for small projects. Zero dependencies - download and run. Asyncio support.

**[Documentation](./docs/)**

----

### Install
`pip install easy-notifyer`

----

### Example usage:
#### Telegram reporter
```python
from easy_notifyer import telegram_reporter

exception_telegram_reporter = telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",
    chat_id=123456789,  # can be list from chat_id: [123456789, 876522345], or @username
    service_name='qwe'
)

@exception_telegram_reporter(exceptions=OSError)
def foo():
    ...
    raise OSError
```


```python
from easy_notifyer import telegram_reporter


exception_telegram_reporter = telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",
    chat_id="@my_super_nickname",
    api_url='https://your_super_url_api.com/'
)

@exception_telegram_reporter(
    exceptions=OSError,               # can be tuple from exceptions
    as_attached=True,                 # to send traceback as a file
    filename='bar_report.log',        # custom filename for attach
    header='Testing for bar',         # first line in message-report. default: "Your program has crashed ☠️"
    datetime_format="%d - %H:%M:%S",  # format datetime for report
)
async def bar():
    ...
    raise OSError
```


Can be using params `disable_web_page_preview` and `disable_notification`:
```python
from easy_notifyer import telegram_reporter


exception_telegram_reporter = telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",
    chat_id=["@superadmin1", "@superadmin2"],
)

@exception_telegram_reporter(
    header='Test request to http://example.com',
    disable_web_page_preview=True,  # not worked if as_attach=True
    disable_notification=True,
)
def foo():
    ...
    raise ValueError
```

Can be using basic client:
```python
from easy_notifyer import Telegram


def main():
    ...
    telegram = Telegram()
    telegram.send_message('hello from easy notifyer')
    img = open('my_image.jpg', 'rb')
    telegram.send_attach(img, filename='my_image.jpg')


async def main_async():
    ...
    telegram = Telegram()
    await telegram.async_send_message('async hello from easy notifyer')
    img = open('my_image.jpg', 'rb')
    await telegram.async_send_attach(img, filename='my_image.jpg')

```

----


#### Mail reporter
```python
from easy_notifyer import mailer_reporter


exception_telegram_reporter = mailer_reporter(
    host='smtp.example.org',
    port=587,
    login='login@example.com',
    password='qwerty12345',
    from_addr='login@example.com',
    to_addrs='myemail@gmail.com, mysecondmail@mail.com',
    ssl=False,
    service_name='super app'
)

@exception_telegram_reporter(exceptions=ValueError)
def bar():
    ...
    raise ValueError
```


```python
from easy_notifyer import mailer_reporter

exception_telegram_reporter = mailer_reporter(
    host='smtp.example.org',
    port=587,
    login='login@example.com',
    password='qwerty12345',
    from_addr='login@example.com',
    to_addrs='myemail@gmail.com, mysecondmail@mail.com',
    ssl=False,
)

@exception_telegram_reporter(
    exceptions=OSError,               # can be tuple from exceptions
    as_attached=True,                 # to send traceback as a file
    filename='bar_report.log',        # custom filename for attach
    header='Testing for bar',         # first line in message-report. default: "Your program has crashed ☠️"
    subject='hello from foobar',      # set custom subject for message
    datetime_format="%d - %H:%M:%S",  # format datetime for report
)
async def foobar():
    ...
    raise OSError
```

Can be using basic client:
```python
from easy_notifyer import Mailer


def main():
    ...
    mailer = Mailer()
    img = open('my_image.jpg', 'rb')
    mailer.send_message(
        message='hello from main',
        subject='custom subject for message',
        attach=img,
        filename='my_image.jpg',
    )

```
