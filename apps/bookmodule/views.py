from django.shortcuts import render
from django.db.models import (
    Sum, Avg, Min, Max, Count, F,
    FloatField, ExpressionWrapper, Q
)
from .models import Book, Publisher, Address, Student
from django.shortcuts import redirect
from django.utils import timezone
from .forms import BookForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "bookmodule/index.html")


@login_required(login_url='login')
def viewbook(request, bookId):
    book = get_object_or_404(Book, id=bookId)
    return render(request, 'bookmodule/one_book.html', {'book': book})

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


def links_page(request):
    return render(request, 'bookmodule/links.html')


def text_formatting_page(request):
    return render(request, 'bookmodule/text_formatting.html')


def listing_page(request):
    return render(request, 'bookmodule/listing.html')


def tables_page(request):
    return render(request, 'bookmodule/tables.html')


def search_books(request):

    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def simple_query(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/bookList.html', {'books': books})


def complex_query(request):
    mybooks = Book.objects \
        .filter(author__isnull=False) \
        .filter(title__icontains='and') \
        .filter(edition__gte=2) \
        .exclude(price__lte=100)[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) &
        ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': books})


def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})



def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/stats.html', stats)


def lab8_task7(request):
    data = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/cities.html', {'data': data})



def lab9_task1(request):
    total_books = Book.objects.count()

    books = Book.objects.annotate(
        availability_percentage=ExpressionWrapper(
            (F('quantity') * 100.0) / total_books,
            output_field=FloatField()
        )
    )
    return render(request, 'lab9/task1.html', {'books': books})


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Sum('book__quantity')
    )
    return render(request, 'lab9/task2.html', {'publishers': publishers})



def lab9_task3(request):
    publishers = Publisher.objects.annotate(
        oldest_book=Min('book__pubdate')
    )
    return render(request, 'lab9/task3.html', {'publishers': publishers})



def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'lab9/task4.html', {'publishers': publishers})



def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        high_rated_books=Count(
            'book',
            filter=Q(book__rating__gte=4)
        )
    )
    return render(request, 'lab9/task5.html', {'publishers': publishers})


def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_books=Count(
            'book',
            filter=Q(
                book__price__gt=50,
                book__quantity__lt=5,
                book__quantity__gte=1
            )
        )
    )
    return render(request, 'lab9/task6.html', {'publishers': publishers})


@login_required(login_url='login')
def list_books(request):
    books = Book.objects.all()
    return render(
        request,
        'bookmodule/list_books.html',
        {'books': books}
    )


@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            rating=request.POST['rating'],
            pubdate=timezone.now()
        )
        return redirect('/books/lab9_part1/listbooks')

    return render(request, 'addbook.html')

@login_required(login_url='login')
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)


    if request.method == 'POST':
        book.title = request.POST['title']
        book.price = request.POST['price']
        book.quantity = request.POST['quantity']
        book.rating = request.POST['rating']
        book.save()
        return redirect('/books/lab9_part1/listbooks')

    return render(
        request,
        'bookmodule/edit_book.html',
        {'book': book}
    )

@login_required(login_url='login')
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/books/lab9_part1/listbooks')

@login_required(login_url='login')
def list_books_form(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books_form.html', {'books': books})

@login_required(login_url='login')
def add_book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():  
            form.save()
            return redirect('/books/lab9_part2/listbooks')
    else:
        form = BookForm()

    return render(request, 'add_book_form.html', {'form': form})


@login_required(login_url='login')
def edit_book_form(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('/books/lab9_part2/listbooks')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book_form.html', {'form': form})

@login_required(login_url='login')
def delete_book_form(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/books/lab9_part2/listbooks')