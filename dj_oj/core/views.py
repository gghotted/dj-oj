from django.shortcuts import redirect


def home_view(request):
    return redirect('problems:list')
