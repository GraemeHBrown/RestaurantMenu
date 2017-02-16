from wtforms import Form, StringField, SelectField, DecimalField, validators


class EditMenuItemForm(Form):
    name = StringField('Name', [validators.length(min=1, max=30),validators.InputRequired()])
    price = StringField('Price', [validators.InputRequired()])
    description = StringField('Description', [validators.length(min=4, max=100), validators.InputRequired()])
    course = SelectField('Course',[validators.InputRequired()], choices=[('', ''),('Starter', 'Starter'), ('Main', 'Main'), ('Dessert', 'Dessert'),('Side dish','Side dish'),('Beverage','Beverage')])


class NewRestaurantForm(Form):
    name = StringField('Name', [validators.length(min=1, max=30),validators.InputRequired()])


class EditRestaurantForm(Form):
    name = StringField('Name', [validators.length(min=1, max=30),validators.InputRequired()])


class NewMenuItemForm(Form):
    name = StringField('Name', [validators.length(min=1, max=30),validators.InputRequired()])
    price = StringField('Price', [validators.InputRequired()])
    description = StringField('Description', [validators.length(min=4, max=100), validators.InputRequired()])
    course = SelectField('Course',[validators.InputRequired()], choices=[('', ''),('Starter', 'Starter'), ('Main', 'Main'), ('Dessert', 'Dessert'),('Side dish','Side dish'),('Beverage','Beverage')])