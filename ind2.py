#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import click
import os


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option("-d", "--destination")
@click.option("-n", "--number")
@click.option("-t", "--time")
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
@click.option("-t", "--time")
def select(filename, time):
    routes = load_routes(filename)
    result = []

    for route in routes:
        time_route = tuple(route.get('time').split(':'))
        if time < time_route:
            result.append(route)

    # Возвратить список выбранных маршрутов.
    return result


def load_routes(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_routes(file_name, way):
    """
    Сохранить все пути в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as f:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(way, f, ensure_ascii=False, indent=4)


def main():
    cli()


if __name__ == '__main__':
    main()
