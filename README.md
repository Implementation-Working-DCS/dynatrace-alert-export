<h1 align="center">
  <br>
  <a href="http://www.dcs.ar"><img src="https://i.imgur.com/GgjNXNl.png" alt="DCSolutions" width="200"></a>
  <br>
Dyntrace Alert Export to CSV and Send it by email.
  <br>
</h1>

<h4 align="center"> Exporta las alertas de la semana de dynatrace y las envia via mail.

<p align="center">
  <a href="#Funciones">Funciones</a> •
  <a href="#Como se usa">Como se usa</a> •
  <a href="#Creditos">Creditos</a> •
</p>


## Funciones

* Exporta las alertas de la semana de dynatrace a un archivo CSV.
* Se inicia todos los viernes a las 9 am
* Se envia via mail al usuario que se complete.

## Como se usa

Para clonar esta repositorio, vas a necesitar [Git](https://git-scm.com) y [Python](https://www.python.org/downloads/) (que viene con [pip](https://pypi.org/project/pip/)) instalados en tu PC

```bash
# Clone el repositorio.
$ git clone https://github.com/Implementation-Working-DCS/dynatrace-alert-export.git

# Ir al repo
$ cd dynatrace-alert-export

# Iniciar la app (testing)
$ python3 -m dyna_export.py

# Iniciar la app (crontab)
$ crontab -e
TZ = "America/Argentina/Buenos_Aires"
0 9 * * 5 /usr/bin/python3 /ruta/a/tu/script/dyna_export.py

# Restart el service
$ sudo service cron restart
```

## Creditos

- [Matias Dante](https://github.com/matiasdante)

