from bs4 import BeautifulSoup
import json

with open('bakers.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all divs with class "icon-circle", and try to find the transaction from here, give that the whole transaction
# is part the div that is great-grandparent of this ones
icon_circle_divs = soup.find_all('div', class_='icon-circle')


def get_great_grandparent(tag):
    if tag and tag.parent and tag.parent.parent and tag.parent.parent.parent:
        return tag.parent.parent.parent
    return None


# Collect all unique great-grandparent divs
great_grandparent_divs = set()

for div in icon_circle_divs:
    great_grandparent = get_great_grandparent(div)
    if great_grandparent:
        great_grandparent_divs.add(great_grandparent)

print(len(great_grandparent_divs))
transactions = list(great_grandparent_divs)

transactions_list = list()

if transactions:
    for div in transactions:
        category_span = div.find('div', class_='_8i-eheZb5L24RqIZiPgP8')
        if category_span:
            category = category_span.text.strip()
        else:
            category = None

        source_span = div.find('span', class_='_3xS5kDGaZwCwAvWCWCxswm')
        if source_span:
            source = source_span.find_next('span').text.strip()
        else:
            source = None

        description_span = div.find('div', class_='_2lJjm7w8pNpdChmKFMrtos')
        if description_span:
            description = description_span.text.strip()
        else:
            description = None

        price_span = div.find('span', class_='_3fg4YMdrgBxwppTd3zZxUP') or div.find('span',
                                                                                    class_='M57fAgGLu2oOBJaysreP2') or div.find(
            'span', class_='_3k7QtxKdo0DCpq_IFUNCOK')
        if price_span:
            price = price_span.text.strip()
            price = price.replace('€', '')
            price = price.replace(',', '')


        else:
            price = None

        transaction = {
            'category': category,
            'source': source,
            'description': description,
            'price': price
        }

        print(transaction)
        transactions_list.append(transaction)

sorted_transactions = sorted(transactions_list, key=lambda obj: float(obj.get('price', 0)) > 0, reverse=True)

with open('dump.json', 'w') as file:
    json.dump(sorted_transactions, file, indent=4)

if sorted_transactions:
    with open("output.txt", "a") as file:
        for transaction in sorted_transactions:
            toAdd = ''
            if transaction.get('category') == 'Transfer, withdraw':
                continue
            if float(transaction.get('price', 0)) > 0 and transaction.get('source', 'default') not in ['ActivoCredit',
                                                                                                       'AforroNet']:
                if transaction.get('category') == 'Wage, invoices':
                    toAdd = f'Wages [{transaction.get('price')}] Income'
                    print(f'Wages [{transaction.get('price')}] Income')
                    file.write(toAdd + "\n")
                else:
                    toAdd = f'Other [{transaction.get('price')}] Income'
                    print(f'Other [{transaction.get('price')}] Income')
                    file.write(toAdd + "\n")
            if float(transaction.get('price', 0)) < 0:
                price = abs(float(transaction.get('price')))
                toAdd = f'Income [{price}] {transaction.get('category')}'
                print(f'Income [{price}] {transaction.get('category')}')
                file.write(toAdd + "\n")
