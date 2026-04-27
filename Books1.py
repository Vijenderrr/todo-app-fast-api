from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Path, Query #Path is used to define path parameters in the API endpoints, and Body is used to define the request body for POST and PUT requests
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    # id: Optional[int] = None  # id is optional in the request, it will be assigned automatically
    id: Optional[int] = Field(default=None, description="The ID of the book, assigned automatically if not provided")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "VijenderSingh",
                "description": "This is a description of the new book.",
                "rating": 4,
                "published_date": 2020
            }
        }
    }

BOOKS = [Book(id=1, title='Title One', author='Author One', description='Description One', rating=5, published_date=2020),
         Book(id=2, title='Title Two', author='Author Two', description='Description Two', rating=4, published_date=2021),
         Book(id=3, title='Title Three', author='Author Three', description='Description Three', rating=3, published_date=2022),
         Book(id=4, title='Title Four', author='Author Four', description='Description Four', rating=2, published_date=2023),
         Book(id=5, title='Title Five', author='Author Five', description='Description Five', rating=1, published_date=2024),
         Book(id=6, title='Title Six', author='Author Six', description='Description Six', rating=0, published_date=2025)]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):  # Path is used to define the validation of book_id as a path parameter, and gt=0 ensures that the book_id must be greater than 0
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")  # If the book with the given id is not found, a 404 error is raised with the message "Book not found"

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request :BookRequest):
    new_book = Book(**book_request.model_dump())  # Unpacking the BookRequest model to create a new Book instance
    print(type(new_book))
    BOOKS.append(new_book)


def find_book_id(book: Book):
    if len(BOOKS) > 0:
       book.id = BOOKS[-1].id + 1  #id is assigned as the last book's id + 1
    else:
        book.id = 1
    
    return book


@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if(BOOKS[i].id == book.id):
            BOOKS[i] = book
            book_changed = True
        return {"message": "Book updated successfully"}
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")  # If the book with the given id is not found, a 404 error is raised with the message "Book not found"
    

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book (book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
        
        
@app.get("/books/published", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=1900, lt=2100)):  #Query is used to define the validation of published_date as a query parameter, and gt=1900 and lt=2100 ensure that the published_date must be between 1900 and 2100
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return