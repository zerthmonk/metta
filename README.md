## METTA howto:
---
Все завернуто в докер, достаточно сказать `docker-compose build`

Сходу `docker-compose up` не заработает из-за необходимости залогиниться в телеграм (т.е. в контейнере `metta-back` сделан интерактивный шелл для удобства аутентификации, директива `up` его не поддерживает)

---
### Как залогиниться в телеграм:
---

- Залогиниться в [аккаунт Telegram](https://my.telegram.org/) с тем номером, который вы хотите использовать в приложении
- Кликнуть API Development
- Ввести новое имя и описание приложения (они могут быть любыми) и нажать кнопку "Create application"
- скопировать в корневой директории проекта файл `env.template` в `.env` 
- записать туда api_hash и api_id из предыдущего пункта

```
API_ID=<api_id>
API_HASH=<api_hash>
```

- запустить процедуру аутентификации в Telegram через  `docker-compose run metta-back` (или `pipenv run python back/auth.py`)

**ВАЖНО:** не нужно ни с кем делиться содержимым файлов `.env` и `.session` - обладая этой информацией можно залогиниться вами в Телеграм и делать там все что угодно.

-----

### Обоснование стека:

---
- Vue - все просто - в вашем стеке есть, я его не знаю, изучение привлекает больше чем React (и тем более Angular).
- Telethon - широкие возможности по собиранию статистики каналов (подписчиков, например)
- Quart - асинхронный брат Flask. Очень на него похож. Выбран потому, что я не настолько хорошо знаю Telethon, чтобы пользоваться его синхронным клиентом в связке с Flask.
- docker - потому что не хочу много node в системе :)
