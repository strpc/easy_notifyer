# Easy Notifyer
----
Easy bug reporter for small projects or sentry on minimums.  


### Install  
`pip install easy-notifyer`


### Example usage:  
```python
from easy_notifyer import telegram_reporter


@telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",  
    chat_id=123456789  # can be list from chat_id: [123456789, 876522345]
)
def foo():
    ...
    raise OSError
```


`token` and `chad_id` can be used from environment variables:  
`export EASY_NOTIFYER_TELEGRAM_TOKEN="123456789:QweRtyuWErtyZxcdsG"`  
`export EASY_NOTIFYER_TELEGRAM_CHAT_ID="123456789,876522345"`
```python
from easy_notifyer import async_telegram_reporter


@async_telegram_reporter(
    exceptions=OSError,        # can be tuple from exceptions
    as_attached=True,          # to send traceback as a file
    filename='bar_report.log'  # filename for attach
    header='Testing for bar',  # first line in message-report
)
async def bar():
    ...
    raise OSError
```


Can be using params `disable_web_page_preview` and `disable_notification`:
```python
from easy_notifyer import telegram_reporter

@telegram_reporter(
    header='*Test request to http://example.com*', 
    disable_web_page_preview=True,  # not worked if as_attach=True
    disable_notification=True,
)
def foo():
    ...
    raise ValueError
```

**[More examples](/examples/telegram.md)**


### Environment variables
All optional. For comfortable using.  
`EASY_NOTIFYER_PROJECT_NAME="my_first_project"` - for mark in report-message from second line.  
`EASY_NOTIFYER_DATE_FORMAT="%Y-%m-%d %H:%M:%S"` - datetime format in report-message.  
`EASY_NOTIFYER_FILENAME_DT_FORMAT="%Y-%m-%d %H_%M_%S"` - datetime format for filename in as_attach report.  
`EASY_NOTIFYER_TELEGRAM_TOKEN="123456789:QweRtyuWErtyZ"` - Telegram bot token. [Get token](https://core.telegram.org/bots#6-botfather)  
`EASY_NOTIFYER_TELEGRAM_CHAT_ID="123456789, 876522345"` - int or int separated by commas.  
`EASY_NOTIFYER_TELEGRAM_API_URL="https://api.telegram.org"` - if need to use a proxy for api telegram.  
