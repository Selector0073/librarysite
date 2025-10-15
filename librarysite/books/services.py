from django.http import HttpResponse
import openpyxl



def exportbooksexcel(books):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Books"

    headers = [
        "title", "img", "reviews", "content",
        "price", "availability", "reviews_count",
        "genre", "writed_at", "author"
    ]
    sheet.append(headers)

    for book in books:
        sheet.append([
            book.title,
            str(book.img),
            str(book.reviews),
            book.content,
            book.price,
            book.availability,
            book.reviews_count,
            str(book.genre),
            book.writed_at.isoformat() if book.writed_at else "",
            str(book.author)
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="books.xlsx"'

    workbook.save(response)
    return response



