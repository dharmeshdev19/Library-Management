import yaml

def database_config(app):
	db = yaml.load(open('db.yaml'))
	database = db.get('database', None)
	mysql_host = db.get('mysql_host', None)
	mysql_user = db.get('mysql_user', None)
	mysql_password = db.get('mysql_password', None)
	mysql_db_name = db.get('mysql_db_name', None)
	port = db.get('port', None)
	app.config['SQLALCHEMY_DATABASE_URI'] = database+'://'+mysql_user+':'+mysql_password+'@'+mysql_host+':'+port+'/'+mysql_db_name
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	return app