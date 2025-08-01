# MCP Server with NSE India Data

This project provides a MCP (Model Context Protocol) server that uses data from the NSE India API.

## Prerequisites

- Docker
- Docker Compose

## How to run locally

1.  **Build and run the services:**

    ```bash
    docker-compose up --build
    ```

This will start both the `nseindia` and `mcp` services. The `mcp` service will be available on port `8000`.