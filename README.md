# QR Code API

This is the API for setting the redirect for my QR code tattoo. Also see [the associated repo](https://github.com/samanthavbarron/qr-code/tree/main) for generating QR codes that make for good tattoos as well as [my blog post](https://samantha.wiki/projects/qr-code-tattoo/).

## Repo Structure

This repository contains a python Flask app, which implements an api, intended
to be hosted at `api.example.com`. The repository is structured as follows.

- `app`: This is the primary module for the Python package, and contains
  `main.py` where the Flask app is implemented.
- `test`: This is the testing module, which tests the `app` module.
- `.env`: This is where the environment variables live.
- `Dockerfile`: The Dockerfile used to create a container for the flask app.

## Environment Variables

The following environment variables are required for the app to function:

- `API_KEY`: The API key used for certain functionalities.
- `API_HOST`: The host to use for the flask app.
- `API_PORT`: The port to use for the flask app.
- `API_QR_DEFAULT`: The default URL for the redirect on start.
