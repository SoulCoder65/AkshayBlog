from Flask_Projects import create_app
from Flask_Projects import db
app = create_app()
app.app_context().push()

if __name__ == '__main__':
	
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)