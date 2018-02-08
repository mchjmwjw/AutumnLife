# AutumnLife
# for my dog
* start:
```
macos/linux: manage.py runserver --host 127.0.0.1 --port 8484
windows: python manage.py runserver --host 127.0.0.1 --port 8484
```

1. pip install flask-script

创建数据库迁移脚本
python manage.py db migrate -m "initial migration"
更新数据库
python manage.py db upgrade