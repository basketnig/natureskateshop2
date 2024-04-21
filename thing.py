from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField


class ThingsForm(FlaskForm):
    type = StringField('type')
    name = StringField("name")
    price = IntegerField("price")
    imgurl = StringField("imgurl")
    color = StringField("color")
    size = StringField("size")
    availbility = BooleanField("availbility")
    submit = SubmitField('Применить')