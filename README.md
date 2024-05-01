# Introduction
The Game of Thrones Dashboard is an educational web application designed for Game of Thrones enthusiasts and Python developers. It provides an interactive and user-friendly interface to explore and analyze a comprehensive dataset containing information about characters, houses, books, and seasons.

Built with Python and Streamlit, this application demonstrates how to create data-driven web applications for educational purposes.

# Build

Build for a single architecture:
```sh
docker build --rm -t alisio/got_app .
```

Building for amd64 and arm64:
```sh
docker buildx --use --name mybuilder
docker buildx create --use --name mybuilder\n
docker buildx inspect --bootstrap\n
docker buildx build --platform linux/amd64,linux/arm64 --output "type=image,push=true"  --tag alisio/got_app:latest --builder mybuilder .
```