from django.shortcuts import render
def book_detail(request):
    book = {
        "title": "Капитанская дочка",
        "author": "Александр Пушкин",
        "year": 1836,
        "description": "История Петра Гринёва и Маши Мироновой.",
    }
    return render(request, "catalog/book_detail.html", {"book": book})

# Create your views here.
