from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine, func, sql
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from form_classes import EditMenuItemForm, NewRestaurantForm, EditRestaurantForm, NewMenuItemForm

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

###### This has the WTForms validation in it#################

### Start JSON API ###
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one_or_none()
    if not menuItem:
        return jsonify(MenuItem=['No menu item found for this ID...'])
    else:
        return jsonify(MenuItem=[menuItem.serialize])

### end JSON API###

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    form = NewRestaurantForm(request.form)
    if request.method == 'POST' and form.validate():
        newRestaurant = Restaurant(name=form.name.data)
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('new_restaurant.html', form=form)


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    form = EditRestaurantForm(request.form)
    restaurantToEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST' and form.validate():
            restaurantToEdit.name = form.name.data
            session.add(restaurantToEdit)
            session.commit()
            flash("Restaurant Successfully Edited!")
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('edit_restaurant.html', restaurant_id=restaurant_id, restaurant=restaurantToEdit, form=form)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant Successfully Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant_id=restaurant_id, restaurant_to_delete=restaurantToDelete)

#Note:  calling count for each query is quite expensive may need to refactor it to use EXISTS?
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    starterItems, mainItems, dessertItems, beverageItems, sideDishItems = (None,None,None,None,None)
    if session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Starter').count():
       starterItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Starter')
    if session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Main').count():
       mainItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Main')
    if session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Dessert').count():
       dessertItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Dessert')
    if session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Beverage').count():
       beverageItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Beverage')
    if session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Side dish').count():
       sideDishItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Side dish')
    return render_template('menu.html', restaurant=restaurant, starter_items=starterItems,
                           main_items=mainItems, dessert_items=dessertItems, beverage_items=beverageItems, side_dishes=sideDishItems)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    form = NewMenuItemForm(request.form)
    if request.method == 'POST' and form.validate():
        newItem = MenuItem(name=form.name.data, price=form.price.data, description=form.description.data, course=form.course.data, restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id=restaurant_id, form=form, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    form = EditMenuItemForm(request.form)
    itemToBeEdited = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST' and form.validate():
        if form.name.data:
            itemToBeEdited.name=form.name.data
        if form.price.data:
            itemToBeEdited.price=form.price.data
        if form.description.data:
            itemToBeEdited.description=form.description.data
        if form.course.data:
            itemToBeEdited.course=form.course.data
        session.add(itemToBeEdited)
        session.commit()
        flash("Menu Item Successfully Edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant_id=restaurant_id, form=form, item=itemToBeEdited)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menuItemToDelete)
        session.commit()
        flash("Menu Item Successfully Deleted!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item_to_delete=menuItemToDelete)


if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)