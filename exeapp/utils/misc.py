

def pages_from_range(range_str):
    '''
    parses a range and returns pages
    :param range_str:
    :return:pages
    '''
    pages = set()
    for part in range_str.split(','):
        x = part.split('-')
        pages.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(pages)