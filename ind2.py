#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import click
import os
from datetime import datetime


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option("-d", "--destination", help='Введите пункт назначения')
@click.option("-n", "--number", help='Введите номер маршрута')
@click.option("-t", "--time", help='Введите время отправления')
def add(filename, destination, number, time):
    """
    Запросить данные о маршруте.
    """
    if os.path.exists(filename):
        routes = load_routes(filename)
    else:
        routes = []

    routes.append(
        {
            'destination': destination,
            'number': number,
            'time': time,
        }
    )

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Неправильный формат времени", file=sys.stderr)
        exit(1)

    with open(filename, "w", encoding="utf-8") as fl:
        json.dump(routes, fl, ensure_ascii=False, indent=4)
    click.secho("Маршрут добавлен")


@cli.command()
@click.argument('filename')
def display(filename):
    """
    Отобразить список маршрутов.
    """
    routes = load_routes(filename)
    if routes:
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

        for route in routes:
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


@cli.command()
@click.argument('filename')
@click.option("-t", "--time", help="Введите нужное время")
def select(filename, time):
    """
    Выбрать маршруты после заданного времени.
    """
    routes = load_routes(filename)
    result = []

    try:
        time = datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Неправильный формат времени", file=sys.stderr)
        exit(1)

    for route in routes:
        time_route = route.get('time')
        time_route = datetime.strptime(time_route, "%H:%M")
        if time < time_route:
            result.append(route)

    if result:
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

        for route in result:
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


def load_routes(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == '__main__':
    cli()
