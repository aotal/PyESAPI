# Architecture Documentation

## Overview

This project uses **FastAPI** to provide a RESTful interface over the Varian ESAPI (Eclipse Scripting API).
ESAPI is a .NET library that requires execution within a Single-Threaded Apartment (STA) thread.
FastAPI, being asynchronous, runs on an event loop that is separate from the STA thread required by ESAPI.

To bridge this gap, we use a **Worker Thread Pattern**.

## The Worker Thread Pattern

### Components

1.  **Main Application (FastAPI)**: Handles HTTP requests asynchronously.
2.  **ESAPI Worker Thread**: A dedicated background thread that initializes the ESAPI application and executes all ESAPI-related logic.
3.  **Request Queue**: A thread-safe queue (`queue.Queue`) used to pass tasks from the FastAPI thread to the Worker thread.

### Flow

1.  **Initialization**:
    - On startup, `app.main:lifespan` starts the `ESAPI-Worker` thread.
    - The worker thread initializes `pyesapi.CustomScriptExecutable.CreateApplication`.
    - Once initialized, it signals `esapi_ready`.

2.  **Request Handling**:
    - An HTTP request arrives at an endpoint (e.g., `/info`).
    - The endpoint function calls `run_in_esapi(func, **kwargs)`.
    - `run_in_esapi` places the function and arguments into the `esapi_request_queue`.
    - The endpoint waits (blocks) on a result queue.

3.  **Execution**:
    - The `ESAPI-Worker` picks the task from the queue.
    - It executes `func(app_esapi, **kwargs)`.
    - It places the result (or error) back into the specific result queue for that request.

4.  **Response**:
    - `run_in_esapi` retrieves the result.
    - If successful, it returns the data to the endpoint.
    - If failed, it raises an exception, which FastAPI translates to an HTTP error.

## Key Constraints

- **Single Thread**: All calls to `app_esapi` or ESAPI objects must happen inside the function passed to `run_in_esapi`.
- **Object Lifetime**: ESAPI objects (like `Patient`) should not be returned directly to the FastAPI layer because they are not thread-safe and may be disposed. Always convert data to Python dictionaries or Pydantic models inside the worker function.
- **Dispose**: Resources like `Patient` must be closed (`app_esapi.ClosePatient()`) within the same task execution block to avoid memory leaks.
