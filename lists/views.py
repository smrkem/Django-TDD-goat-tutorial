from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect('/lists/{}/'.format(list_.id))
        except ValidationError:
            error = "List items can't be empty"

    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "List items can't be empty"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/{}/'.format(list_.id))
