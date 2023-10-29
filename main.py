from website.app import create_app

app = create_app()
# the below line only allows us to run the server directly via this file
if __name__ == "__main__":
    app.run(
        debug=True
        
    )  # this runs the Flask app and creates a web server. Reruns when changes are made
