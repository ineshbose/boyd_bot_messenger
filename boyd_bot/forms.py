from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.widgets import html_params
from wtforms import StringField, PasswordField, SelectMultipleField
from wtforms import SubmitField, HiddenField, BooleanField


def select_multi_checkbox(field, ul_class='', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s /> ' % html_params(**options))
        html.append(u'<label for="%s">%s</label></li>' % (field_id, label))
    html.append(u'</ul>')
    return u''.join(html)


class RegisterForm(FlaskForm):

    reg_id = HiddenField("reg_id")
    uni_id = StringField("University ID", validators=[DataRequired()])
    uni_pw = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=True)

    subscribe = SelectMultipleField(
        "Notify Me About My Schedule",
        choices=[
            ('morning', 'Morning Alert'),
            ('before_class', 'Before Every Class'),
        ],
        widget=select_multi_checkbox,
    )

    submit = SubmitField("Login")
