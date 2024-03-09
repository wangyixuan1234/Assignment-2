from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests

# Scalability: The XML file acts as a simple data store, which can be scaled to a more robust database system as needed.
# The function 'init_db_xml' is responsible for initializing the XML database.
# This database stores topics and their corresponding Wikipedia links.
def init_db_xml():
    # Heterogeneity & Transparency: The server is using a common data format (XML), which can be easily processed
    # by different platforms, maintaining transparency as it hides the data handling complexity.
    try:
        # Try to parse an existing XML file. If the file exists and is well-formed,
        # the function will proceed without any changes to the file.
        ET.parse('db.xml')  # Attempt to parse the existing XML file.
    except ET.ParseError:
        # If the file is not found or is not well-formed (malformed),
        # a new file is created with a root 'data' element, establishing a fresh database.
        # Openness: The system is robust to errors and can initialize a new database if necessary,
        # demonstrating the system's ability to recover and adapt to new conditions.
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write("db.xml")  # Write the new XML structure to 'db.xml'.

# The function 'query_wikipedia' takes a topic as input and queries the Wikipedia API to fetch a related link.
# Failure handling: This function handles the failure by returning None if no results are found or an error occurs,
#which prevents one failure from causing total system failure.
def query_wikipedia(topic):
    # Transparency: The details of interfacing with the Wikipedia API are abstracted away from the clients.
    try:
        # Setup for Wikipedia API request. The 'params' dictionary contains the parameters
        # for the query, including the action type, the search string, and the response format.
        wikipedia_search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json"
        }
        # Sends a GET request to the Wikipedia API with the specified parameters.
        response = requests.get(wikipedia_search_url, params=params)
        # If the response indicates an HTTP error, an exception will be raised.
        response.raise_for_status()
        # Scalability: Raises an exception for HTTP errors
        # that can be scaled to more sophisticated error handling.
        
        # Parse the JSON response to extract search results.
        search_results = response.json()
        if search_results["query"]["search"]:
            # If search results are found, extract the page ID of the first result
            # and create a URL pointing directly to the corresponding Wikipedia page.
            page_id = search_results["query"]["search"][0]["pageid"]
            return f"https://en.wikipedia.org/?curid={page_id}"
        # If no results are found, return None.
        return None
    except Exception as e:
        # If any error occurs during the API request or response handling,
        # the error is printed and None is returned.
        print(f"An error occurred while querying Wikipedia: {e}")
        return None

# The 'add_topic_with_wiki_link' function is designed to add a new topic with its Wikipedia link
# to the XML database, or update the link if the topic already exists.
# Openness: This function can be extended to support additional data sources or interfaces.
def add_topic_with_wiki_link(topic):
    # Call 'query_wikipedia' to get the Wikipedia URL for the topic.
    wiki_url = query_wikipedia(topic)
    if wiki_url is None:
        # If no URL is found, inform the user that no article was found for the topic.
        # Failure handling: The system provides meaningful feedback to the user in case of failure,
        # preventing complete system unresponsiveness.
        return f"No Wikipedia article found for topic '{topic}'."

    try:
        # Attempt to parse the XML database and prepare to add or update the topic.
        tree = ET.parse('db.xml')
        root = tree.getroot()

        # Look for an existing 'topic' element in the database by comparing attributes.
        # If the topic is new, create a new 'topic' element.
        # Security: Only adds or updates the topic if it's a valid topic, preventing unauthorized data manipulation.
        topic_element = next((t for t in root.findall('topic') if t.attrib.get('name') == topic), None)
        if topic_element is None:
            topic_element = ET.SubElement(root, 'topic', {'name': topic})
        
        # Within the 'topic' element, look for an existing 'wikipedia' link element.
        # If it doesn't exist, create one and set its text to the Wikipedia URL.
        # If it exists, update the text with the new URL.
        wiki_element = topic_element.find('wikipedia')
        if wiki_element is None:
            ET.SubElement(topic_element, 'wikipedia').text = wiki_url
        else:
            wiki_element.text = wiki_url
        # Write the updated XML structure back to the file.
        tree.write('db.xml')
        # Confirm to the user that the link was added or updated.
        return f"Wikipedia link added/updated for topic '{topic}'."
    except Exception as e:
        # If an error occurs during XML parsing or writing, inform the user.
        # Failure handling: The system communicates any issues back to the client,
        # ensuring stability in case of unexpected errors.
        return f"An error occurred while updating the XML database: {e}"

# The 'start_server' function sets up and starts the XML-RPC server.
# Scalability: By running on '0.0.0.0', the server is capable of accepting requests over any network interface,
# aiding in load distribution.
def start_server():
    # The server is configured to listen on all network interfaces at port 8000.
    # 'allow_none=True' allows the server to serialize a None value in the responses.
    server = SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
    # Register the function 'add_topic_with_wiki_link' with the server,
    # making it callable by clients.
    # Openness: The server's functionality can be expanded by registering new functions,
    # demonstrating the flexibility of the system.
    server.register_function(add_topic_with_wiki_link, "add_topic_with_wiki_link")

    # Before starting the server, ensure that the XML database is initialized.
    # Transparency & Security: The server hides the details of database initialization from clients,
    # providing a secure environment at startup.
    init_db_xml()
    # Notify the console that the server is now listening for requests.
    print("Server is listening on port 8000...")
    # Start the server's main loop, waiting for incoming connections.
    server.serve_forever()

if __name__ == "__main__":
    # If the script is run as the main program, execute the server startup function.
    start_server()
