#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path


def get_route(way, destination, number, time):
    """
    Запросить данные о маршруте.
    """
    way.append(
        {
            'destination': destination,
            'number': number,
            'time': time,
        }
    )

    return way


def display_routes(way):
    """
    Отобразить список маршрутов.
    """
    if way:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 4,
            '-' * 20
        )
        print(line)
        print(
            '| {:^30} | {:^4} | {:^20} |'.format(
                "Пункт назначения",
                "№",
                "Время"
            )
        )
        print(line)

        for route in way:
            print(
                '| {:<30} | {:>4} | {:<20} |'.format(
                    route.get('destination', ''),
                    route.get('number', ''),
                    route.get('time', '')
                )
            )
        print(line)

    else:
        print("Маршруты не найдены")


def select_routes(way, period):
    """
    Выбрать маршруты после заданного времени.
    """
    result = []

    for route in way:
        time_route = tuple(route.get('time').split(':'))
        if period < time_route:
            result.append(route)

    # Возвратить список выбранных маршрутов.
    return result


def save_routes(file_name, way):
    """
    Сохранить все пути в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as f:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(way, f, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все пути из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fl:
        return json.load(fl)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("routes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления маршрута.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new way"
    )
    add.add_argument(
        "-d",
        "--destination",
        action="store",
        required=True,
        help="The way's name"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        help="The way's number"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="Start time(hh:mm)"
    )

    # Создать субпарсер для отображения всех путей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all ways"
    )

    # Создать субпарсер для выбора маршрута.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the way"
    )
    select.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="The required period"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все пути из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        routes = load_routes(args.filename)
    else:
        routes = []

    # Добавить путь.
    if args.command == "add":
        routes = get_route(
            routes,
            args.destination,
            args.number,
            args.time
        )
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        display_routes(routes)

    # Выбрать требуемых рааботников.
    elif args.command == "select":
        time_select = args.time.split(":")
        time_select = tuple(time_select)
        selected = select_routes(routes, time_select)
        display_routes(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_routes(args.filename, routes)


if __name__ == '__main__':
    main()
