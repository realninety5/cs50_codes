import random
import re
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django import forms
from markdown2 import markdown
from . import util


# Form for creating a new wiki entry
class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title' , 'class': 'form-control'}))
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={'rows': '5',
                                        'placeholder': 'Content', 'class': 'form-control'}))

# Form to edit existing entry
class EditForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title' , 'class': 'form-control'}))
    content = forms.CharField(label='',
            widget=forms.Textarea(attrs={'rows': '5', 'placeholder': 'Content' , 'class': 'form-control'}))

# Form to allow users search within the wiki
class SearchForm(forms.Form):
    q = forms.CharField(label="",
            widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia' , 'class': 'form-control'}))

# View form editing wikis
@require_http_methods(['POST', "GET"])
def editform(request, title):
    # Get the title and its content
    post_title = title
    post_content = util.get_entry(title)
    pre_data = {'title': post_title, 'content': post_content}

    # if request is POST and valid, save the form, else prepopulate the form with old content and render it
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            util.save_entry(new_title, new_content)
            return redirect('entry', TITLE=new_title)
    form = EditForm(initial=pre_data)
    return render(request, 'encyclopedia/edit.html', {'form': form, 'title': post_title})


# Check for users search string and return the page
def formview(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data['q']
            all_ent = util.list_entries()
            if val.lower() in all_ent:
                ent = util.get_entry(all_ent[val.lower()])
                return redirect('entry', all_ent[val.lower()])
            #if ent:
                #return render(request, 'encyclopedia/entry.html', {'ent_val':ent, 'tit':val})

            # Else return pages with almost matching entries
            ls_entries = {}
            for item in all_ent:
                if re.search(f'{val}', all_ent[item], re.IGNORECASE):
                    ls_entries[item] = all_ent[item]
            return render(request, 'encyclopedia/index.html', {
                'entries': ls_entries})

        # If form is not valid, render the form
        return render(request, 'encyclopedia/layout.html', {'form': form})
    # If not POST, render an empty form
    return render(request, "encyclopedia/layout.html", {
        "entries": util.list_entries(), 'form': SearchForm()
    })

# Render all available enries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 'form': SearchForm()
    })

# Render a requested entry page
def entry(request, TITLE):
    all_ent = util.list_entries()
    try:
        ent_val = util.get_entry(all_ent[TITLE.lower()])
        return render(request,
            'encyclopedia/entry.html', {'ent_val':markdown(ent_val), 'tit':all_ent[TITLE.lower()]})
    except KeyError:
        return render(request, 'encyclopedia/entry.html')

# Creates a new entry from form input
def create(request):
    if request.method=='POST':
        c_form = CreateForm(request.POST)
        if c_form.is_valid():
            # If form is valid, obtain its values and check if same title already exists
            title = c_form.cleaned_data['title']
            content = c_form.cleaned_data['content']
            entries = [i.lower() for i in util.list_entries()]
            if title.lower() in entries:
                # If it exists, tell the user, else save the new entry
                return render(request,
                    'encyclopedia/create.html', {'p_exist': 'Page already exists'})
            util.save_entry(title, content)
            return redirect('entry', TITLE=title)
        return render(request, 'encyclopedia/create.html', {'c_form':c_form})
    return render(request, 'encyclopedia/create.html', {'c_form': CreateForm()})

# Render a random page from the list of available pages
def random_page(request):
    ran_val = random.randrange(0, len(util.list_entries()))
    title = list(util.list_entries())[ran_val]
    all_ent = util.list_entries()
    return redirect('entry', TITLE=all_ent[title])
