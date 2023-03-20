from django.shortcuts import render


def home(request):
    return render(request, template_name='shop_main/index.html')
