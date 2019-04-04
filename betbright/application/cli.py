import argparse
import asyncio

from injector import Injector

from betbright.application.config import BaseModule
from betbright.domain.entities import Sport, Event, Market, Selection
from betbright.domain.serializers import DataclassSerializer
from betbright.domain.unit_of_work import UnitOfWork


async def run(options):
    injector = Injector()
    module = BaseModule()
    await module.setup_aio_providers(injector)
    uow = injector.get(UnitOfWork)

    kwargs = {k: v for k, v in options._get_kwargs()}
    func = kwargs.pop('func')
    await func(uow, kwargs)


def get(model):
    async def get(uow, kwargs):
        print(f'> Getting {model.__name__}s')
        async for entity in uow.repo_map[model].get(**kwargs):
            print(entity)

    return get


def add(model):
    async def get(uow: UnitOfWork, kwargs):
        print(f'> Adding a {model.__name__}')
        kwargs['id'] = None
        serializer = DataclassSerializer(model)
        instance = serializer.from_kwargs(**kwargs)
        await uow.repo_map[model].add(instance)

    return get


def delete(model):
    async def get(uow: UnitOfWork, kwargs):
        print(f'> Deleting {model.__name__} {kwargs["id"]}')
        async for entity in uow.repo_map[model].get(**kwargs):
            await uow.repo_map[model].delete(entity)

    return get


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line utility for accessing the database')
    subparsers = parser.add_subparsers()

    add_group = subparsers.add_parser('add')
    add_subs = add_group.add_subparsers()
    for model in [Sport, Event, Market, Selection]:
        subparser = add_subs.add_parser(model.__name__.lower())
        for attr in model.__annotations__.keys():
            if attr == 'id':
                continue
            subparser.add_argument(f'--{attr}', type=str, nargs='?')
        subparser.set_defaults(func=add(model))

    get_group = subparsers.add_parser('get')
    get_subs = get_group.add_subparsers()
    for model in [Sport, Event, Market, Selection]:
        subparser = get_subs.add_parser(model.__name__.lower())
        for attr in model.__annotations__.keys():
            subparser.add_argument(f'--{attr}', type=str, nargs='?')
        subparser.set_defaults(func=get(model))

    get_group = subparsers.add_parser('delete')
    get_subs = get_group.add_subparsers()
    for model in [Sport, Event, Market, Selection]:
        subparser = get_subs.add_parser(model.__name__.lower())
        subparser.add_argument(f'id', type=str)
        subparser.set_defaults(func=delete(model))

    options = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(options))
