import re

# utils


def extract_price(snip):
    txt = re.sub("[^0-9]", "", snip)
    return txt


def extract_currency(snip):
    if snip != "Price[Price disclosed on request]":
        start = re.search(r"Price", snip).end()
        end = re.search(r"[0-9]", snip).start()

        txt = snip[start:end]
    else:
        txt = "na"
    return txt


def extract_period(snip):
    txt = snip.split(" ")[-1].strip()
    return txt


def extract_date(snip):
    start = re.search(r"Updated on ", snip).end()
    end = re.search(r" by:", snip).start()

    txt = snip[start:end]

    return txt


def extract_vals(table_dict, str1):
    if str1 in table_dict:
        txt = table_dict[str1][0]
    else:
        txt = "na"
    return txt


def get_table_rows_todict(lnk):
    table = lnk.find_all("table")[0]
    rows = table.find_all("tr")
    row_list = []
    for tr in rows:
        td = tr.find_all("td")
        row = [i.text.rstrip() for i in td]
        row_list.append(row)

    row_list.pop(0)
    row_list.pop(0)
    row_list.pop(0)
    return {d[0]: d[1:] for d in row_list}
