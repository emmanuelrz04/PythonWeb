# ANALOGY

Client sits and orders → User types a URL

Kitchen (backend) prepares → Flask server processes

Waiter takes the order → Route directs the request

Chef prepares the food → Python function executes

Waiter delivers the dish → HTML is rendered

# In other words:

USER types:
http://127.0.0.1:5000/
↓

BROWSER sends a REQUEST to the server
↓

Flask SERVER receives the request
↓

ROUTING: Flask looks for the correct function (@app.route)
↓

Python FUNCTION executes (fetches data, processes logic)
↓

TEMPLATE receives the data and builds the HTML
↓

RESPONSE is sent back to the browser
↓

USER sees the beautiful page
