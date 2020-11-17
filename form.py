from wtforms_alchemy import ModelForm, ModelFormField
from models import *

class BookEntryForm(ModelForm):
    class Meta:
        model = BookEntry