from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange


class SettingsForm(FlaskForm):
    theme = SelectField('Fon', validators=[DataRequired()],
                        choices=['default', 'magic girl', 'Odyssey', 'lonely mountain', 'winter dreams',
                                 'people routine', 'house in the forest'])
    number_of_cards_in_hand = IntegerField('Number of cards in hand', validators=[DataRequired(), NumberRange(max=9,
                                           min=3)], default=6)
    number_of_cards_in_deck = IntegerField('Number of cards in deck', validators=[DataRequired(), NumberRange(max=72,
                                           min=31)], default=72)
    submit = SubmitField('Apply')
