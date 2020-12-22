# Api endpoint - Divisist Asistance

Proyecto simple que haciendo uso de webscrapping, consulta las notas de las materias de un estudiante.
-Endpoints:
```
[POST]
api/v1.0/login
{
    "usuario":"",
    "password":"",
    "documento":""
}

[GET]
api/v1.0/get-notas-materias

[POST]
/api/v1.0/get-nota-by-voice
{
    "data":"",
    "value":"",
}

[POST]
api/v1.0/logout

```