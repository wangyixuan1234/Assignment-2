from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests
import datetime

# Function to initialize an XML file for storing topics and their Wikipedia links.
# This tackles the challenge of heterogeneity by using XML, which is platform-agnostic.
def init_db_xml():
    root = ET.Element("data")  # Root element
    tree = ET.ElementTree(root)
    tree.write("db.xml")

# Function to query Wikipedia API for a given topic.
# This addresses the challenge of openness by allowing external data retrieval.
def query_wikipedia(topic):
    try:
        wikipedia_search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json"
        }
        response = requests.get(wikipedia_search_url, params=params)
        response.raise_for_status()  # Check for HTTP request errors
        search_results = response.json()
        
        # Check if search results are found and return the first result's link.
        if search_results["query"]["search"]:
            page_id = search_results["query"]["search"][0]["pageid"]
            return f"https://en.wikipedia.org/?curid={page_id}"
        return None
    except Exception as e:
        # Handle any exceptions by logging and returning None.
        # This addresses the failure handling challenge.
        print(f"An error occurred while querying Wikipedia: {e}")
        return None

# XML-RPC function that adds a new topic and its Wikipedia link to the XML database.
# It demonstrates the transparency design challenge by abstracting the details of the operation from the client.
def add_topic_with_wiki_link(topic):
    wiki_url = query_wikipedia(topic)
    if wiki_url is None:
        return f"No Wikipedia article found for topic '{topic}'."

    try:
        # Load and parse the existing XML database.
        tree = ET.parse('db.xml')
        root = tree.getroot()

        # Look for an existing topic in the XML structure.
        topic_element = next((t for t in root.findall('topic') if t.attrib.get('name') == topic), None)

        if topic_element is None:
            # Create a new topic element if it doesn't exist.
            topic_element = ET.SubElement(root, 'topic', {'name': topic})

        # Add Wikipedia URL to the topic element.
        # This also caters to the scalability challenge by managing entries in a structured way.
        if not topic_element.find('wikipedia'):
            ET.SubElement(topic_element, 'wikipedia').text = wiki_url
            tree.write('db.xml')
            return f"Wikipedia link added to topic '{topic}'."
        else:
            return f"Wikipedia link already present for topic '{topic}'."
    except Exception as e:
        # Handle exceptions by logging the error.
        # This again tackles the failure handling design challenge.
        return f"An error occurred while updating the XML database: {e}"

# Start XML-RPC server function.
# Security challenge can be addressed by implementing authentication mechanisms
# and using secure protocols such as HTTPS for XML-RPC server communication.
def start_server():
    server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    server.register_function(add_topic_with_wiki_link, "add_topic_with_wiki_link")

    init_db_xml()  # Ensure the XML database is initialized before starting the server.
    print("Server is listening on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    start_server()