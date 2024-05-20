import concurrent.futures
import requests
import time

# Define the API endpoint
api_url = "http://localhost:8000/v1/users/"

# Function to make a single API request
def call_api():
    response = requests.get(api_url)
    return response.status_code

# Function to execute the performance test
def performance_test(num_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(call_api) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                status_code = future.result()
                print(f"Request completed with status code: {status_code}")
            except Exception as e:
                print(f"Request generated an exception: {e}")

if __name__ == "__main__":
    num_requests = 400
    start_time = time.time()
    performance_test(num_requests)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")
