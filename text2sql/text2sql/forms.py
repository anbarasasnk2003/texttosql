from django import forms

class ColumnForm(forms.Form):
    table_name = forms.CharField(label="Table Name", max_length=100)
    columns = forms.CharField(label="Columns (comma separated)", widget=forms.Textarea)

class QueryForm(forms.Form):
    natural_query = forms.CharField(label="Ask your question", widget=forms.Textarea)
