import xmlrpc.client

# Establish a connection to the XML-RPC server.
# This client interface showcases transparency, as the RPC mechanisms are hidden from the user.
server = xmlrpc.client.ServerProxy('http://localhost:8000/')

# Function for the client to add a topic and request Wikipedia link from the server.
# It handles failure by catching exceptions and printing an error message.
def add_topic():
    try:
        topic = input("Enter topic to add and fetch Wikipedia link: ")
        result = server.add_topic_with_wiki_link(topic)
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")

# Client's user interface loop function.
# The loop represents a scalable client capable of making repeated requests.
def main_menu():
    while True:
        print("\nRPC Notebook Client")
        print("1. Add Topic and Retrieve Wikipedia Info")
        print("2. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_topic()
        elif choice == '2':
            break
        else:
            print("Invalid option, please try again.")

# The entry point of the client program.
if __name__ == "__main__":
    main_menu()