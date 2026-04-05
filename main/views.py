from django.shortcuts import render

def mainpage(request):
    context = {
        'isSummary': 1,
        'generation': 14,
        'welcome': "Django Basic",
    }
    return render(request, 'main/mainpage.html', context)

def secondpage(request):
    context = {
        'isSummary': 0,
        'welcome': "Let Me Introduce Myself",
    }
    return render(request, 'main/secondpage.html', context)