# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app.models import Terrorist, Org


class TerroristForm(FlaskForm):
    lname = StringField(
            label='lname',
            validators=[DataRequired(), Length(min=1, max=512)]
        )
    fname = StringField(
            label='fname',
            validators=[DataRequired(), Length(min=1, max=512)]
        )
    mname = StringField(
            label='mname',
            validators=[Length(min=-1, max=512), Optional()]
        )
    iin = StringField(
            label='iin',
            validators=[Length(min=-1, max=512), Optional()]
        )
    birthdate = DateField(
            label='birthdate',
            validators=[Optional()]
        )
    note = StringField(
            label='note',
            validators=[Length(min=-1, max=512), Optional()]
        )
    included = DateField(
            label='included',
            validators=[Optional()]
        )
    excluded = DateField(
            label='excluded',
            validators=[Optional()])
    submit = SubmitField('Save')


class OrgForm(FlaskForm):
    name = StringField(
            label='name',
            validators=[DataRequired(), Length(min=1, max=512)]
        )
    name_eng = StringField(
            label='name eng',
            validators=[DataRequired(), Length(min=-1, max=512)]
        )
    note = StringField(
            label='note',
            validators=[Optional(),
            Length(max=512)]
        )
    included = DateField(
            label='included',
            validators=[Optional()]
        )
    excluded = DateField(
            label='excluded',
            validators=[Optional()]
        )
    submit = SubmitField(label='Save')
