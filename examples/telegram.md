```python
from easy_notifyer import telegram_reporter


@telegram_reporter(token="123456789:QweRtyuWErtyZxcdsG", chat_id=123456789)
def foo():
    ...
    raise OSError
```

```python
import os

from easy_notifyer import Telegram, telegram_reporter

# set token and chat_id as environment variables.
os.environ.setdefault('EASY_NOTIFYER_TELEGRAM_TOKEN', "123456789:QweRtyuWErtyZxcdsG")
os.environ.setdefault('EASY_NOTIFYER_TELEGRAM_CHAT_ID', "123456789,876522345")


@telegram_reporter(
    exceptions=ZeroDivisionError,
    as_attached=True,
    disable_notification=True,
    filename='report bar func testing.txt',
    header='testing',
)
async def bar():
    ...
    a = 1 / 0
 

@telegram_reporter(exceptions=AttributeError)  # all errors except attributeerror will be received without notification
@telegram_reporter(
    header='www report',
    disable_notification=True,
    disable_web_page_preview=True,
)
def www():
    ...
    raise AttributeError

async def easy_bot():
    bot = Telegram()
    await bot.async_send_message('hello world')
```

```python
from easy_notifyer import Telegram

def main():
    bot = Telegram(token="123456789:QweRtyuWErtyZxcdsG", chat_id=123456789)
    try:
        raise ValueError
    except ValueError:
        bot.send_message('Something went wrong')
    
    file = open('image from main.jpg', 'rb')
    bot.send_attach(file)
    bot.send_attach(('picture.png', file))
    bot.send_attach(file, filename='pictute.png')
    bot.send_attach(b'hello world from main func')
    bot.send_attach(b'hello world from main func', filename='hello.txt')
    bot.send_attach(('hello.txt', b'hello world from main func'))
```
