Easy Notifyer
========

![image](https://img.shields.io/pypi/v/easy_notifyer?color=yellowgreen) 
![image](https://img.shields.io/github/languages/code-size/strpc/easy_notifyer) 
![image](https://img.shields.io/badge/Python-3.7%2B-success) 
![image](https://img.shields.io/github/license/strpc/easy_notifyer?color=informational)   


Easy bug reporter for small projects. Zero dependencies - download and run. Asyncio support.  

----

### Install  
`pip install easy-notifyer`

----

### Example usage:  
#### Telegram reporter
```python
from easy_notifyer import telegram_reporter


@telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",  
    chat_id=123456789,  # can be list from chat_id: [123456789, 876522345]
    exceptions=OSError,
)
def foo():
    ...
    raise OSError
```


`token` and `chad_id` can be used from environment variables:  
`export EASY_NOTIFYER_TELEGRAM_TOKEN="123456789:QweRtyuWErtyZxcdsG"`  
`export EASY_NOTIFYER_TELEGRAM_CHAT_ID="123456789, 876522345"`


```python
from easy_notifyer import telegram_reporter


@telegram_reporter(
    exceptions=OSError,        # can be tuple from exceptions
    as_attached=True,          # to send traceback as a file
    filename='bar_report.log'  # custom filename for attach
    header='Testing for bar',  # first line in message-report. default: "Your program has crashed ☠️"
)
async def bar():
    ...
    raise OSError
```


Can be using params `disable_web_page_preview` and `disable_notification`:
```python
from easy_notifyer import telegram_reporter


@telegram_reporter(
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

#### [More examples](/examples/)

----


#### Mail reporter
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


`host`, `port`, `login`, `password`, `from_addr`, `to_addrs` and `ssl`, can be used from environment variables:  
`export EASY_NOTIFYER_MAILER_HOST=smtp.example.org`  
`export EASY_NOTIFYER_MAILER_PORT=587`  
`export EASY_NOTIFYER_MAILER_LOGIN=login@example.com`  
`export EASY_NOTIFYER_MAILER_PASSWORD=qwerty12345`  
`export EASY_NOTIFYER_MAILER_FROM=login@example.com`  
`export EASY_NOTIFYER_MAILER_TO="myemail@gmail.com, mysecondmail@mail.com"`  
`export EASY_NOTIFYER_MAILER_SSL=False`  

```python
from easy_notifyer import mailer_reporter


@mailer_reporter(
    exceptions=OSError,             # can be tuple from exceptions
    as_attached=True,               # to send traceback as a file
    filename='bar_report.log',      # custom filename for attach
    header='Testing for bar',       # first line in message-report. default: "Your program has crashed ☠️"
    subject='hello from foobar',    # set custom subject for message
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

#### [More examples](./examples/)

----

### Environment
All optional. For comfortable using.  

*Features:*  
 * `EASY_NOTIFYER_SERVICE_NAME="my_first_project"` - for mark in report-message from second line.  
 * `EASY_NOTIFYER_DATE_FORMAT` - [datetime format](https://strftime.org/) in report-message. (`default=%Y-%m-%d %H:%M:%S`)  
 * `EASY_NOTIFYER_FILENAME_DT_FORMAT` - [datetime format](https://strftime.org/) for filename in as_attach report. (`default=%Y-%m-%d %H_%M_%S`)  


*Telegram settings:*  
 * `EASY_NOTIFYER_TELEGRAM_TOKEN="123456789:QweRtyuWErtyZ"` - Telegram bot token. [Get token](https://core.telegram.org/bots#6-botfather)  
 * `EASY_NOTIFYER_TELEGRAM_CHAT_ID="123456789, 876522345"` - int or int separated by commas.  
 * `EASY_NOTIFYER_TELEGRAM_API_URL="https://api.telegram.org"` - if need to use a proxy for api telegram.  


*Mail settings:*  
 * `EASY_NOTIFYER_MAILER_HOST=smtp.example.org` - set smtp server.  
 * `EASY_NOTIFYER_MAILER_PORT=587` - set port server.  
 * `EASY_NOTIFYER_MAILER_SSL=False` - set SSL mode for connection with server.  
 * `EASY_NOTIFYER_MAILER_LOGIN=login@example.com` - set login for authorization on server.  
 * `EASY_NOTIFYER_MAILER_PASSWORD=qwerty12345` - set password for authorization on server.  
 * `EASY_NOTIFYER_MAILER_FROM=login@example.com` - set *from* message.  
 * `EASY_NOTIFYER_MAILER_TO="myemail@gmail.com, mysecondmail@mail.com"` - set *to* message.    
