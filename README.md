
# Что делает скрипт.
`tg_bot.py` и `vk_bot.py`  это два бота-помощника которые обучены нейросетью [DialogFlow](https://dialogflow.cloud.google.com/) и отвечают на часто задаваемые вопросы пользователей.


# Как настроить скрипт.
Cкачайте репозиторий себе на компьютер .
Переименуйте файл `.env.dist` в `.env`

Настройка `Google Cloud` и `DialogFlow`
1. Создайте аккаунт в [Google Cloud]('https://console.cloud.google.com/welcome?project=regal-fortress-361907).
2. Далее создайте проект в [Google Cloud](https://console.cloud.google.com/projectcreate?previousPage=%2Fwelcome%3Fproject%3Dregal-fortress-361907&organizationId=0)
3. Запомните `Project ID` вашего проекта! он нужен будет  для связки с агентом в `DialogFlow`
4. Перейдите в [DialogFlow](https://dialogflow.cloud.google.com/#/newAgent) на верху слева от логотипа нужно выбрать где будет размещен ваш `Agent` выбирайте только `Global`   далее нажмите на кнопку `Create Agent`
5. Дайте ему имя и нажмите на кнопку `Google Project` там выберите `Project ID` приложения  которого вы создали в `Google Cloud` далее нажимайте на кнопку `Create`.
6. Теперь нужно создать `json-ключ` перейдите в пункт [`Service accounts`](https://console.cloud.google.com/iam-admin/serviceaccounts?project=regal-fortress-361907) на верху нажмите на кнопку `Create service account` дайте имя ключу и жмите `Create and continue`.
	Нажмите на кнопку `select role` перейдите в  `Currently used` выберите  `owner` и нажмите `Done`.
7. После выполнения 6 пункта у вас должна появиться запись.Справа от от нее нажмите на три точки и выберите пункт `Manage Keys` далее `Add Keys` нажимайте на `Create new keys` далее выбираете  тип файла `json` после нажатия на кнопку `Create` к вам на компьютер должен скачаться файл `json` его нужно добавить в папку проекта.
8. откройте файл `.env` найдите поле `GOOGLE_APPLICATION_CREDENTIALS` и присвойте ему имя `json` файла который вы скачали. 
Пример: `GOOGLE_APPLICATION_CREDENTIALS=watchful-idea-361908-e220cj46g100a.json` 

Создание группы в VK и получения токена Группы.
1. Создайте группу [VK](https://vk.com/) она должна появиться на вкладке управления.
2. Перейдите в группу нажмите управление перейдите в пункт `Работа с Api`. 
3. Нажмите `Создать Ключ` поставьте галочки возле пункта `Разрешить приложению доступ к управлению сообществом` и `Разрешить приложению доступ к сообщениям сообщества`.
4. Перейдите  во вкладку `Long Poll API` и напротив `Long Poll API` выберите включить.
5. Токен полученный на третьем шаге нужно сохранить в файл `.env` найдите поле `VK_GROUP_TOKEN` и присвойте ему токен группы. 
6. 
 
Создание Телеграмм бота.
1. [Ссылка](https://lifehacker.ru/kak-sozdat-bota-v-telegram/) на инструкцию как создать телеграмм бота.
2. Полученный токен бота сохраните в файл `.env` найдите поле `TG_TOKEN` и присвойте ему свой токен.
3. Напишите в телеграмме боту [userinfobot](https://t.me/userinfobot) он отправит вам `id` его нужно сохранить в файл `.env` найдите поле `TG_CHAT_ID` и присвойте ему свой id.
	
Скачайте нужные библиотеки следующей командой.
```python
pip install -r requirements.txt
```
Запустите скрипт `create_intent.py` он создаст новый `Intents` в `DialogFlow` с вопросами на ответы из списка `questions.json`.
Запуск скрипта.
```python 
python create_intent.py
```
Запуск Телеграмм бота.
```python
python tg_bot.py
```
Запуск бота Вконтакте.
```python
python vk_bot.py
```
Результат работы ботов.

`Telegramm bot`

![Telegramm bot](/gif/tg.gif "работа бота")


`VK bot`
![VK bot](/gif/vk.gif "работа бота")
 






