from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

# connect to airtable API
AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
# home_page is a function, takes in an argument 'request'
# def myview(request):
def home_page(request):
    #request.GET.get(‘query’, ‘’) returns the search word ‘five things'
#     print(str(request.GET.get('query', '')))
    user_query = str(request.GET.get('query', ''))
    # use the airtable python wrapper get_all and formula
    # FIND(1st arg user query, 2nd arg API search) {name} is name field in the dictionary?
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    # send result to front end, generally use a context dictionary, key-value pair
    # name the key as 'search_result'
    # context variable: store the search result in the value of the dictionary, name the key search_result
    stuff_for_frontend = {'search_result': search_result}
    # when return, render the 'request' in this html file. the context dictionary is: stuff_for_frontend
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    print('haha')
    if request.method == 'POST':
        data = {
            # from the modal's input
            'Name': request.POST.get('name'),
            #Pictures is a list
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        # when the insert function is actinoed, there will be an respnse to show us whatit's done
        # we can store the response in a variable
        try:
            response = AT.insert(data)
            # notify on create
            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to update a mvoie: {}'.format(e))
    #once this function runs, take me back to the root directory/ homepage/ yourapp.com
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.freeiconspng.com/uploads/no-image-icon-23.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id, data)
            # notify on update
            messages.success(request, 'Updated movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to update a mvoie: {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        #     print(movie_id)
        #retrieve the name first for the message tag, before deleting the item
        movie_name =AT.get(movie_id)['fields'].get('Name')
        # note before AT.delete, request doesn't have anything =>we used AT.get(movie_id) instead of reponse['fields']
        response = AT.delete(movie_id)
        # notify on delete, here we use the movie_name variable whic halready have the movie name
        messages.warning(request, 'Deleted movie: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Got an error when trying to delete a movie: {}'.format(e))
    return redirect('/')
