from five_ws_one_h_api import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=False, threaded=False)
