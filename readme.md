# Необходимое ПО
- Java JDK >= 17 https://download.oracle.com/java/21/archive/jdk-21.0.3_windows-x64_bin.exe или https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html
- Python 2.7 https://www.python.org/ftp/python/2.7/python-2.7.amd64.msi
- Spigot server https://adfoc.us/serve/sitelinks/?id=765928&url=https://mohistmc.com/api/v2/projects/mohist/1.20.1/builds/871/mohist-1.20.1-871-server.jar
- PySpigot https://www.spigotmc.org/resources/pyspigot.111006/download?version=555271
- TLauncher и Minecraft версии 1.20.1

# Установка
1. Поместить файл `mohist-1.20.1-871-server.jar` в текущую папку
2. Запустить `start.bat`
3. Скрипт предложит согласиться с правилами использования, нужно напечатать `yes` в консоли
4. Дождаться окончания настройки сервера
5. Закрыть консоль скрипта
6. Перенести содержимое папки `Python27` в текущую папку
7. Перенести файл `pyspigot-0.7.0-SNAPSHOT.jar` в `plugins\PySpigot\scripts` (папка Plugins появится после завершения работы скрипта)
8. В файле `server.properties` заменить порт на `4642` и указать параметр `online-mode=false`
9. Снова запустить `start.bat`
10. Закрыть start.bat после завершения работы

# Первая программа
1. В папке `plugins\PySpigot\scripts` создать файл с расширением `.py` (например, `main.py`)
2. Написать в созданном файле представленный ниже код
```
import pyspigot as ps


def make_boom(sender, label, args):
    if isinstance(sender, Player):
        target_block = sender.getTargetBlock(None, 100)

        x = target_block.getX()
        y = target_block.getY()
        z = target_block.getZ()

        world = sender.getWorld()
        world.createExplosion(x, y, z, 50)
    return True


ps.command.registerCommand(make_boom, 'boom')
```
3. Запустить `start.bat`, если он еще не запущен
4. В консоли сервера выдать себе права администратора командой `op <Ваш ник>` (например, `op st1ch`)
5. В игре открыть `Сетевая игра` -> `По адресу` указать `localhost:4642`
6. По желанию можно выставить свободный режим игры для себя командой `/gamemode creative <Ваш ник>` (например, `/gamemode creative st1ch`)
7. Открыть чат в игре и вписать туда команду `/pyspigot reload main.py`

# Использование команд
Ранее в файле `main.py` мы зарегистрировали команду `boom`. Чтобы использовать ее внутри игры нужно открыть чат и написать `/boom`. Команда сделает небольшой взрыв в том месте, в которое будет направлен прицел игрока.

# Готовые примеры
В папке `examples` есть несколько скриптов, которые можно установить на свой сервер

## snake.py
- Перенести файл `snake.py` в папку `plugins\PySpigot\scripts`
- В игре вписать команду `/pyspigot reload snake.py`

## Команды
`/snake` - создает змейку в том месте, куда направлен прицел игрока
`/move` - включает в себя несколько команд:
- `/move MOVE` - запускает движение змейки вперед
- `/move STOP` - останавливает движение змейки
- `/move F` - задает направление движения вперед (F - Forward) F - параметр по умолчанию
- `/move R` - задает направление движения вправо (R - Right)
- `/move B` - задает направление движения назад (B - Back)
- `/move L` - задает направление движения влево (L - Left)

## builder.py
Скрипт для копирования построек
- Перенести файл `builder.py` в папку `plugins\PySpigot\scripts`
- В игре вписать команду `/pyspigot reload builder.py`

## Команды
- Чтобы начать копирование небходимо взять в руку `Деревянный меч`. Нажатие ЛКМ (левая кнопка мыши) задает блок от которого начать копирование, ПКМ (правая кнопка мыши) - блок до которого нужно скопировать.
- Далее необходимо в чате написать команду `/copy`. Это команда скопирует область блоков в `коллекцию построек`
- Для отображения `коллекции построек` необходимо написать команду `/get_builds`. Команда выведет `id` постройки и количество блоков, которое она содержит
- Для того, поставить скопированную постройку нужно воспользоваться командой `/build` и указать в ней `id` (номер постройки) и координаты ее расположения (например, `/build 0 10 65 20`)
