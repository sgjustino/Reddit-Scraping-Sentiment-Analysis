import requests
import time

URL = 'http://sgjustino.pythonanywhere.com/'

INTERVAL = 300  

def check_server():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"Server is up at {URL}")
        else:
            print(f"Server returned status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error while checking server: {e}")

def main():
    while True:
        check_server()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
