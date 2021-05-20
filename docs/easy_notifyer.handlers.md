
### easy_notifyer.handlers.mailer.mailer_reporter(\*, host, port, login, password, from_addr, to_addrs, ssl=False, service_name=None)
Handler errors for sending report on email.


* **Parameters**


    * **host** (*str**, **optional*) – = post of smtp server.


    * **port** (*int**, **optional*) – = port of smtp server.


    * **login** (*str**, **optional*) – = login for auth in smtp server.


    * **password** (*str**, **optional*) – password for auth in smtp server.


    * **from_addr** (*str**, **optional*) – the address sending this mail.


    * **to_addrs** (*str**, **list**(**str**)**, **optional*) – addresses to send this mail to.


    * **ssl** (*bool**, **optional*) – use SSL connection for smtp.


    * **service_name** (*optional*) – Service name.



* **Return type**    `Callable`


## easy_notifyer.handlers.telegram module


### easy_notifyer.handlers.telegram.telegram_reporter(\*, token, chat_id, api_url=None, service_name=None)
Handler errors for sending report in telegram.


* **Parameters**


    * **token** (*str*) – Telegram bot token. Can be use from environment variable


    * **receive** (*To*) – [https://core.telegram.org/bots#6-botfather](https://core.telegram.org/bots#6-botfather).


    * **chat_id** (*int**, **str**, **list*) – Chat ids for send message.


    * **api_url** (*str*) – Url api for telegram.


    * **service_name** (*optional*) – Service name.



* **Return type**    `Callable`
