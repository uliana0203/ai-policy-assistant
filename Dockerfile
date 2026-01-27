# ============================
# Stage 1: Base environment
# ============================
FROM python:3.11-slim

# Disable Python buffering and create working directory
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Command to start the app
CMD ["python", "-m", "ui.app"]
