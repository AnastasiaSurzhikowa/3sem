from django.shortcuts import render


def about(request):
    return render(request,'main/about.html')

def testpic(request):
    return render(request, 'main/testpic.html')

def calendar(request):
    return render(request, 'main/calendar.html')

def mainpage(request):
    return render(request, 'main/mainpage.html')

def contact(request):
    return render(request, 'main/contact.html')