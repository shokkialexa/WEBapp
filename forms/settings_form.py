from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    theme = SelectField('Fon', validators=[DataRequired()], choices=['default', 'magic girl', 'Odyssey',
                                                                     'lonely mountain',
                                                                     'winter dreams', 'people routine',
                                                                     'house in the forest'])
    number_of_cards_in_hand = IntegerField('Number of cards in hand', validators=[DataRequired()], default=6)
    number_of_cards_in_deck = IntegerField('Number of cards in deck', validators=[DataRequired()], default=62)
    submit = SubmitField('Apply')
