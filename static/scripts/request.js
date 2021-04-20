function CreateRequest()
{
    var Request = false;

    if (window.XMLHttpRequest)
    {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        //Internet explorer
        try
        {
             Request = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (CatchException)
        {
             Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }

    if (!Request)
    {
        alert("Невозможно создать XMLHttpRequest");
    }

    return Request;
}
/*
Функция посылки запроса к файлу на сервере
r_method  - тип запроса: GET или POST
r_path    - путь к файлу
r_args    - аргументы вида a=1&b=2&c=3...
r_handler - функция-обработчик ответа от сервера
*/
function SendRequest(r_method, r_path, r_args, r_handler)
{
    //Создаём запрос
    var Request = CreateRequest();

    //Проверяем существование запроса еще раз
    if (!Request)
    {
        return;
    }
    Request.onreadystatechange = function()
    {
        //Если обмен данными завершен
        if (Request.readyState == 4)
        {
            if (Request.status == 200)
            {
                //Передаем управление обработчику пользователя
                r_handler(Request);
            }
        }

    }
    //Проверяем, если требуется сделать GET-запрос
    if (r_method.toLowerCase() == "get" && r_args.length > 0)
    {
        r_path += "?" + r_args;
    }


    //Инициализируем соединение
    Request.open(r_method, r_path, true);

    if (r_method.toLowerCase() == "post")
    {
        //Если это POST-запрос

        //Устанавливаем заголовок
        Request.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=utf-8");
        //Посылаем запрос
        Request.send(r_args);
    }
    else
    {
        //Если это GET-запрос

        //Посылаем нуль-запрос
        Request.send(null);
    }
}
function Update(filename)
{
    //Создаем функцию обработчик
    var Handler = function(Request)
    {
        var htmlcode = new DOMParser().parseFromString(Request.responseText, 'text/html');
        if (document.getElementById("staticBackdrop") == null)
        {
            if (document.getElementById("form") != null && htmlcode.getElementById("form") != null)
            {
                if (document.getElementById("form").innerHTML != htmlcode.getElementById("form").innerHTML);
                {
                    document.getElementById("form").innerHTML = htmlcode.getElementById("form").innerHTML;
                }
                if (document.getElementById("header").innerHTML != htmlcode.getElementById("header").innerHTML)
                {
                    document.getElementById("header").innerHTML = htmlcode.getElementById("header").innerHTML;
                }
            }
            if (document.getElementById("pole") != null && htmlcode.getElementById("pole") != null)
            {
                if (document.getElementById("pole").innerHTML != htmlcode.getElementById("pole").innerHTML)
                {
                    document.getElementById("pole").innerHTML = htmlcode.getElementById("pole").innerHTML;
                }
            }
        }
        if (document.location.href != Request.responseURL)
        {
            document.location.href = Request.responseURL;
            Update(document.location.href);
        }

    }


    //Отправляем запрос
    SendRequest("GET",filename,"",Handler);

}
let timerId = setInterval(Update, 10000, document.location.href);
addEventListener("keydown", function(event)
{
if (typeof timerId != 'undefined')
{
    clearInterval(timerId);
}
let timerIdTimeout = setTimeout(function delay() {
let timerId = setInterval(Update, 10000, document.location.href);
}, 40000)
});

