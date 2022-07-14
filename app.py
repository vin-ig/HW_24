from flask import Flask, request
from utils import get_query, read
from exception import RequestError

app = Flask(__name__)


@app.route('/perform_query/')
def query():
	data = request.args
	try:
		from_file = read(data.get('file_name'))
		query = get_query(from_file, data.get('cmd1'), data.get('value1'))
		if data.get('cmd2'):
			query = get_query(query, data.get('cmd2'), data.get('value2'))

		return app.response_class('\n'.join(query), content_type="text/plain")

	except (FileNotFoundError, RequestError) as e:
		return f'{e}', 400


if __name__ == '__main__':
	app.run(debug=True)
