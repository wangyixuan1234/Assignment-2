import xmlrpc.client

# Heterogeneity: This client demonstrates the ability to interact with a server using XML-RPC,
# a protocol that allows for interoperability among heterogeneous systems with different hardware and operating systems.

# Connects to an XML-RPC server and allows the user to add topics or exit.
def main_menu():
    server_address = 'http://localhost:8000/'  # Openness: This can be modified to point to any server address,
    # showing the client's ability to interact with new or different systems.
    server = xmlrpc.client.ServerProxy(server_address)

    while True:
        # Display the main menu options to the user.
        print("\nRPC Notebook Client")
        print("1. Add Topic and Retrieve Wikipedia Info")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            # Prompt for a topic, request its Wikipedia link from the server, and display the result.
            topic = input("Enter topic to add and fetch Wikipedia link: ")
            try:
                result = server.add_topic_with_wiki_link(topic)
                print(result)
            except Exception as e:
                # Security: Error handling in place to ensure that exceptions do not compromise the client's integrity.
                print(f"An error occurred: {e}")
        elif choice == '2':
            # Security: The client provides a controlled exit path, preventing unauthorized termination.
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()
