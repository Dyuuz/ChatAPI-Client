import requests

def chatapi_client(username, password):
    # Variable to maintain statetful info for a user
    protected_session = requests.Session()
    
    while True:
        print("Select an option:")
        print("1. Register")
        print("2. Login")
        print("3. Chat")
        print("4. Balance")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        try:
            if choice == '1':
                # Register Endpoint
                url = f"https://chatapi-1e6w.onrender.com/api/register"
                
                register_data = {
                    "username": username,
                    "password": password
                }
                
                # Register User with the register endpoint and the necessary json data
                register_response = protected_session.post(url, data=register_data)
                print(f"Register response: {register_response.json()}\n")

            elif choice == '2':
                # Login Endpoint
                url = f"https://chatapi-1e6w.onrender.com/api/login"
                
                login_data = {
                    "username": username,
                    "password": password
                }
                
                # Login User with the login endpoint and the necessary json data
                login_response = protected_session.post(url, json=login_data)
                print(f"Login successful: {login_response.json()}\n")
                
                if login_response.status_code == 200:
                    # Get csrf token linked to the user's session after signing in
                    csrf_token = protected_session.cookies.get('csrftoken')
                else:
                    print("Login failed")

            elif choice == '3':
                if login_response.status_code == 200 and protected_session.cookies.get('csrftoken') is not None:
                    user_message = input("Input a message: ")
                    msg_data = {
                        "message": user_message,
                        "token": login_response.json().get('Token')
                    }
                    
                    # Chat Endpoint
                    url = f"https://chatapi-1e6w.onrender.com/api/chat"
                    
                    # Custom header to provide metadata about the request or response
                    headers = {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json',
                        'Referer': 'https://chatapi-1e6w.onrender.com'
                    }
                    
                    # Make a chat request with the chat endpoint and the necessary json data
                    chat_response = protected_session.post(url, json=msg_data, headers=headers)
                    print(f"{chat_response.json()}\n")
                else:
                    print("Pls log in to make a chat request")

            elif choice == '4':
                if login_response.status_code == 200 and protected_session.cookies.get('csrftoken') is not None:
                    
                    # Balance Endpoint
                    url = f"https://chatapi-1e6w.onrender.com/api/balance"
                    
                    token_data = {
                        "token": login_response.json().get('Token'),
                    }
                    
                    # Custom header to provide metadata about the request or response
                    headers = {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json',
                        'Referer': 'https://chatapi-1e6w.onrender.com'
                    }
                    
                    # Make a chat request with the chat endpoint and the necessary json data
                    balance_response = protected_session.post(url, json=token_data, headers=headers)
                    print(f"{balance_response.json()}\n")
                    
                else:
                    print("You need to login first")

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please select a number between 1 and 5.\n")
            
        except Exception as e:
            print({"error": f"An unexpected error occurred: {str(e)}\n"})

if __name__ == "__main__":
    username = input("Input username: ")
    password = input("Input password: ")
    chatapi_client(username, password)