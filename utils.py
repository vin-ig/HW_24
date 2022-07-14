from exception import RequestError
import os
from typing import Iterable, List, Union
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def filter(data: Iterable, value: str) -> Iterable:
	return (line.strip() for line in data if value in line)


def map(data: Iterable, value: str) -> Iterable:
	try:
		i = int(value)
		return (line.split()[i] for line in data if i < len(line.split()))
	except ValueError:
		raise RequestError('Check value')


def unique(data: Iterable) -> set:
	return set([row for row in data])


def sort(data: Iterable, value: str) -> List[str]:
	if value not in ('asc', 'desc'):
		raise RequestError('Check value')
	return sorted([i for i in data], reverse=False if value == 'asc' else True)


def limit(data: Iterable, value: str) -> Iterable:
	gen = iter(data)
	for i in range(int(value)):
		try:
			yield next(gen)
		except StopIteration:
			break


def regex(data: Iterable, value: str) -> Iterable:
	# value = 'images\/\w+\.png'
	value_t = 'images/\\w+\\.png'
	reg = re.compile(value)
	print(value)
	print(value_t)
	while True:
		try:
			gen = iter(data)
			line = next(gen)
			for i in re.findall(reg, line):
				yield line
		except StopIteration:
			break


def read(filename: str) -> Iterable:
	with open(f'{DATA_DIR}/{filename}', 'r') as file:
		while True:
			try:
				yield next(file).strip()
			except StopIteration:
				break


def get_query(data: Iterable, cmd: str, value: str) -> Union[Iterable, set, List[str]]:
	if cmd =='filter':
		return filter(data, value)
	elif cmd == 'map':
		return map(data, value)
	elif cmd == 'unique':
		return unique(data)
	elif cmd == 'sort':
		return sort(data, value)
	elif cmd == 'limit':
		return limit(data, value)
	elif cmd == 'regex':
		return regex(data, value)
	else:
		raise RequestError('Check command')
