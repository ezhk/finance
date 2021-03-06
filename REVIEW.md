# Персональные финансы

Продукт, который помогает упорядочить расходы по соответствующим категориям  
и проанализировать наиболее затратные их них.  
  
Как конечная цель: _оптимизация расходов пользователя_.

## MVP

- web-interface для возможности учета расхода финансов;
- telegram-bot, предоставляющий альтернативу web-интерфейсу.

## UML-модель

Основные узлы модели:

- пользователь сайта, как основной объект, для которого сохраняются транзакции и категории;
- список категорий и транзакций между ними;
- связь между пользователем сайта и аккаунтом в telegram (вынесено в отдельную таблицу);
- история команд пользователя для дальнейшей аналитики.

![UML](pics/UML.png)

## Общая концепция проекта

В качестве базовой идеи — предоставление удобного интерфейса  
внесения доходов и расходов с подсчётом суммарного размера  
транзакций в течении календарного месяца (календарный месяц —  
базовый интервал агрегации сумм по категориям).

![Webinterface](pics/webinterface.png)  
  
Ещё одним каналом взаимодействия с данными транзакций — telegram bot,  
который поддерживает тот же набор доступных действий, что и web-interface.

![Telegraminterface](pics/telegraminterface.png)

## Технические детали

Верстка сайта реализована с использованием [vue.js](https://vuejs.org/) фреймворка, бекенд часть — [Django](https://www.djangoproject.com/) версии 3.  
Django, поскольку в 3 версии появилась асинхронность, запускается с помощью [daphne](https://github.com/django/daphne).  
  
Бот реализован на базе библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) и использованием polling-модели.  
Реализован как management-скрипт django и запускается с помощью django-admin.

## Альтернативы

| Название | Информация | Особенности |
|:--------:|:----:|:------------------:|
| CoinKeeper | about.coinkeeper.me | Очень удобное приложение контроля расходов. <br>Без использования бота. |
| Мобс     | mobsbot.ru | Неплохие возможности бота. <br>Без возможности внесения данных через сайт. |
| greenz   | greenzbot.ru | Реклама или абонентская плата при использовании сервиса. |
| budgetmoneybot | Рекламный пост на [habr](habr.com/ru/post/463969/) | Сканирование чеков. <br>Есть абонентская плата. |

На самом деле отличных и достойных альтернатив очень много,  
кто-то предоставляет приложения, которые просто невероятны по своей функциональности  
(как CoinKeeper), но при этом нет возможности взаимодействия через telegram.  
У кого-то есть сайты и боты, но большинство хороших ресурсов платные.  
  
Поэтому основная цель продукта, помимо классической цели любого менеджера финансов  
(оптимизации расходов) — создать __бесплатную открытую альтернативу__ существующим продуктам,  
с дальнейшей возможностью расширения до того уровня, который приемлем для вас.
