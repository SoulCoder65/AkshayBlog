from Flask_Projects import create_app
from Flask_Projects import db
app = create_app()
app.app_context().push()

if __name__ == '__main__':
	
	app.run(debug=True)