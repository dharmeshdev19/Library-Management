from models import BookEntry, Category, BookShelf
from app import db
import csv
from random import randint, choice


def populate_category_data():
    category_list = Category.query.all()
    shelf_list = BookShelf.query.all()

    # print("Category list:")
    # print(choice(category_list).name)
    # print("shelf list")
    # print(choice(shelf_list).name)
    # quit()
    
    # read csv file
    with open('excel_data/books.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                # random price generator
                price = randint(100, 1000)
                curr_random_category = choice(category_list)
                curr_random_shelf = choice(shelf_list)

                # print(row[1],row[2],row[11],price,int(curr_random_category.id),int(curr_random_shelf.id),)
                # quit()

                book_entry = BookEntry(name=row[1], book_language='English', author=row[2], publisher=row[11], price=price,
                    category=int(curr_random_category.id), book_shelf=int(curr_random_shelf.id), book_status=1)
                db.session.add(book_entry)
                db.session.commit()



if __name__ == "__main__":
    populate_category_data()