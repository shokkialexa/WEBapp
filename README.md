![Dixit](./static/img/dixit_logo.png)
# Online Dixit
![](https://img.shields.io/github/repo-size/shokkialexa/WEBapp?color=orange&style=for-the-badge) ![](https://img.shields.io/github/stars/shokkialexa/WEBapp?style=for-the-badge&color=orange) 
#### Плюсы приложения
- [X] Бесплатно
- [X] Нет необходимости в регистрации
- [X] Есть обратная связь

 #### Демо-версия [тут](http://online-dixit-game.herokuapp.com/)
 
#### Что делать, чтобы установить приложение
- Скачать
- Запустить файл main.py
- Перейти по ссылке в консоли
- Наслаждаться приложением :)

##### Если не работает, откройте файл main.py, найдите строку 28
```python
    app.run(host='0.0.0.0', port=port)
```
##### И измените её на вот эту(либо другие host и port)
```python
    app.run(host='8080', port='127.0.0.1')
```