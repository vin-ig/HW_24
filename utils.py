from exception import RequestError
import os
from typing import Iterable

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def filter(data: Iterable, value: str) -> Iterable:
	return (line.strip() for line in data if value in line)
	# Выглядит красивее, но уходит в рекурсию
	# return filter(lambda row: value in row, data)


def map(data, value):
	try:
		i = int(value)
		return (line.split()[i] for line in data if i < len(line.split()))
	except ValueError:
		raise RequestError('Check value')


def unique(data, value):
	return set([row for row in data])


def sort(data, value):
	if value not in ('asc', 'desc'):
		raise RequestError('Check value')
	return sorted([i for i in data], reverse=False if value == 'asc' else True)


def limit(data, value):
	gen = iter(data)
	for i in range(int(value)):
		try:
			yield next(gen)
		except StopIteration:
			break


def read(filename):
	with open(f'{DATA_DIR}/{filename}', 'r') as file:
		while True:
			try:
				yield next(file).strip()
			except StopIteration:
				break


def get_query(data, cmd, value):
	if cmd =='filter':
		return filter(data, value)
	elif cmd == 'map':
		return map(data, value)
	elif cmd == 'unique':
		return unique(data, value)
	elif cmd == 'sort':
		return sort(data, value)
	elif cmd == 'limit':
		return limit(data, value)
	else:
		raise RequestError('Check command')
