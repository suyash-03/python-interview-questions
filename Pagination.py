from math import ceil


def paginate_response(items, page, page_size):
    """
    Paginates a list of items.

    Args:
        items (list): The list of items to paginate.
        page (int): The current page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        dict: A dictionary containing paginated items and metadata.
    """
    total_items = len(items)
    total_pages = ceil(total_items / page_size)

    if page < 1 or page > total_pages:
        return {
            "items": [],
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_items = items[start_index:end_index]

    return {
        "items": paginated_items,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages
    }

# Example usage:
if __name__ == "__main__":
    data = list(range(1, 101))  # Sample data: numbers from 1 to 100
    page = 2
    page_size = 10
    result = paginate_response(data, page, page_size)
    print(result)