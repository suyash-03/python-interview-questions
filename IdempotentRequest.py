request_ids = set()

def make_request(url, request_id):
    if request_id in request_ids:
        print(f"Request with ID {request_id} already processed.")
        return
    request_ids.add(request_id)
    print(f"Making request to {url}")


if __name__ == "__main__":
    make_request("http://example.com/api/data", "req-123")
    make_request("http://example.com/api/data", "req-123")  # This should be ignored
    make_request("http://example.com/api/other", "req-456")