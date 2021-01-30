- Поставить зависимости python через `pipenv sync`
- Залогиниться в [аккаунт Telegram](https://my.telegram.org/) с тем номером, который вы хотите использовать в приложении
- Кликнуть API Development
- Ввести новое имя и описание приложения (они могут быть любыми) и нажать кнопку "Create application"
- создать в корневой директории файл `.env` с api_hash и api_id из предыдущего пункта

```
API_ID='api_id'
API_HASH='api_hash'
```

- запустить процедуру авторизации приложения в Telegram через `pipenv run python back/auth.py`

**ВАЖНО:** не нужно ни с кем делиться содержимым файлов `.env` и `.session` - обладая этой информацией можно залогиниться вами в Телеграм и делать там все что угодно.

-----

**Источники вдохновения:**
- [Vue + Gulp project setup](https://github.com/dbybanez/vue-gulp-boilerplate/tree/master/test-app) by [@dbbybanez](https://github.com/dbybanez)
