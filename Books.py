from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title' : 'Title One', 'author' : 'Author One', 'category': 'Science'},
    {'title' : 'Title Two', 'author' : 'Author Two', 'category': 'Fiction'},
    {'title' : 'Title Three', 'author' : 'Author Three', 'category': 'Non-Fiction'},
    {'title' : 'Title Four', 'author' : 'Author Four', 'category': 'Science'},
    {'title' : 'Title Five', 'author' : 'Author Five', 'category': 'Fiction'},
    {'title' : 'Title Six', 'author' : 'Author Six', 'category': 'Non-Fiction'},
]

@app.get("/")
async def first_api():
    return {"message": "This is the first API"}

@app.get('/books/get_all_books_from_author/')
async def get_all_books_from_author(author_name: str):
    author_list = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            author_list.append(book)

    return author_list

# how to use both path and query parameters together
@app.get("/books/{book_title}/")
async def read_book_by_title_and_category(book_title: str, book_category: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold() and \
        book.get('category').casefold() == book_category.casefold():
            return book

@app.get("/books")
async def read_all_books():
    return BOOKS

# to use parameters from the path
@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        

# for QUERY parameters
# it will automatically add the query parameter in the url as ?book_category=Science
@app.get("/books/")
async def read_books_by_category(book_category: str):
    catrgory_by_books = []
    for books in BOOKS:
        if books.get('category').casefold() == book_category.casefold():
            catrgory_by_books.append(books)
    return catrgory_by_books


@app.post("/books/create_book")
async def create_book(new_book=Body() ):
    BOOKS.append(new_book)
    return BOOKS


@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if(BOOKS[i].get('title').casefold() == updated_book.get('title').casefold()):
            BOOKS[i] = updated_book
            return BOOKS
        


