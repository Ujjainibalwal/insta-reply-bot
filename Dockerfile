# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Copy requirements file first to leverage cache
COPY ./requirements.txt /code/requirements.txt

# Install dependencies (CPU versions to save space)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create static folder directory
RUN mkdir -p /code/static

# Copy application files
COPY ./app.py /code/app.py
COPY ./static/index.html /code/static/index.html

# Copy dataset files
COPY ./data /code/data

# Copy model folder weights
COPY ./model /code/model

# Set environment variables for hugging face
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Run uvicorn server on port 7860 (Hugging Face expects port 7860)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
