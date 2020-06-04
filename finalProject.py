from flask import Flask, render_template, url_for, request, flash, redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def restaurantsPage():
	restaurantsAll = session.query(Restaurant).all()
	return render_template("restaurants.html",restaurants=restaurantsAll)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return render_template("restaurantMenu.html",restaurant=restaurant,items=items)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created !")
		return redirect(url_for('restaurantsPage'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		flash("Restaurant Deleted !")
		return redirect(url_for('restaurantsPage'))
	else:
		return render_template('deleteRestaurant.html',restaurant=restaurantToDelete)

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		restaurantToEdit.name = request.form['editName']
		session.add(restaurantToEdit)
		session.commit()
		flash("Restaurant Edited !")
		return redirect(url_for('restaurantsPage'))
	else:
		return render_template('editRestaurant.html',restaurant=restaurantToEdit)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],
						description = request.form['description'],
						price  = "$"+request.form['price'],
						course = request.form['course'],
						restaurant_id=restaurant_id
						)
		session.add(newItem)
		session.commit()
		flash("New item added in the menu !")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("An item has been deleted !")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=itemToDelete)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	itemToEdit = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		itemToEdit.name = request.form['name']
		if request.form['description']!="":
			itemToEdit.description = request.form['description']
		itemToEdit.price = "$" + request.form['price']
		itemToEdit.course = request.form['course']
		session.add(itemToEdit)
		session.commit()
		flash("An item has been edited !")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=itemToEdit)


if __name__ == '__main__':
	app.secret_key = "not_really_secret_key"
	app.debug = True
	app.run(host="0.0.0.0",port=5000)
