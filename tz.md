# httpcurrencyexchange

Описание первой задачи:
Написать HTTP сервис конвертации валют. Это подразумевает, что все запросы и ответы приходят в виде HTTP запросов. Конвертация должна пройти как можно быстрее.


Функционал:
Загрузка данных:
Данные в сервис попадают в виде http запросов
Не нужно сохранять данные в постоянное хранилище, мы допускаем что наш сервис стабильный и никогда не падает. Все данные храним в памяти

Конвертация:
Запросы и ответы реализуем через концепцию REST
Из любой валюты в любую если в системе есть необходимые данные
Курс вещь не стабильная и постоянно меняется во времени. Должна поддерживаться конвертация в конкретный момент времени и по текущему курсу

Ограничения по использованию сторонних библиотек: Разрешается использовать только легковесный http сервер (по желанию). 
Хранение и работа с данными должна быть написана только с использованием стандартных возможностей языка.
Необходимо покрыть сервис тестами. В дальнейшем мы будем сохранять данные, что бы они персистились между стартами сервиса


   
   
