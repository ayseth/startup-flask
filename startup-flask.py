from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from startup_setup import Startup, Base, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route("/startups")
def showstartups():
	startups = session.query(Startup).all()
	return render_template('startup.html', startups = startups)
	# return "This will show startups"

@app.route("/startups/<int:startup_id>/founders", methods=['GET', 'POST'])
def showfounder(startup_id):
	startup_1 = session.query(Startup).filter_by(id=startup_id).one()
	details = session.query(Founder).filter_by(startup_id=startup_id).all()
	if request.method == 'POST':
		newsfounder = Founder(name=request.form['name'], bio=request.form['bio'], startup_id=startup_id)
		session.add(newsfounder)
		session.commit()
		flash("Founder Added successfully")
		return redirect(url_for('showfounder', startup_id=startup_id))
	else:
		return render_template('founders.html', startup_1=startup_1, details=details)
	
		
	# return "This page will show founders"
@app.route("/startups/<int:founder_id>/edit/founder", methods=['GET', 'POST'])
def editfounder(founder_id):
	editfounder = session.query(Founder).filter_by(id=founder_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editfounder.name = request.form['name']
		if request.form['bio']:
			editfounder.bio = request.form['bio']
		session.add(editfounder)
		session.commit()
		flash("Founder Edited successfully")
		return redirect(url_for('showfounder', startup_id=editfounder.startup_id))
	else:
		return render_template('editfounder.html', edit=editfounder)

@app.route("/startups/<int:founder_id>/delete/founder", methods=['GET', 'POST'])
def deletefounder(founder_id):
	deletefounder = session.query(Founder).filter_by(id=founder_id).one()
	if request.method == 'POST':
		session.delete(deletefounder)
		session.commit()
		flash("Founder Deleted successfully")
		return redirect(url_for('showfounder', startup_id=deletefounder.startup_id))
	else:
		return render_template('deletefounder.html', delete=deletefounder)


@app.route("/startups/new", methods=['GET', 'POST'])
def newstartup():
	if request.method == 'POST':
		newstartup = Startup(name=request.form['name'])
		session.add(newstartup)
		session.commit()
		flash("Startup Added successfully")
		return redirect(url_for('showstartups'))
	else:
		return render_template('newstartup.html')
	# return "This page will cretae a new startup"

@app.route("/startups/<int:startupid>/edit", methods=['GET', 'POST'])
def editstartup(startupid):
	editedstartup = session.query(Startup).filter_by(id=startupid).one()
	if request.method == 'POST':
		if request.form['name']:
			editedstartup.name = request.form['name']
		session.add(editedstartup)
		session.commit()
		flash("Startup Edited successfully")
		return redirect(url_for('showfounder', startup_id=startupid))
	else:
		return render_template('editstartup.html', edit=editedstartup)

	# return "This page is used to edit startup id"

@app.route("/startups/<int:startup_id>/delete", methods=['GET', 'POST'])
def deletestartup(startup_id):
	delstartup = session.query(Startup).filter_by(id=startup_id).one()
	if request.method == 'POST':
		session.delete(delstartup)
		session.commit()
		flash("Startup Deleted successfully")
		return redirect(url_for('showstartups'))
	else:
		return render_template('deletestartup.html', delstartup=delstartup)
	# return "This page is used to delete startup id"

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

