# Use Python 3.10 for compatibility
FROM python3.10

# Set working directory
WORKDIR app

# Copy files
COPY . app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 7860

# Run the app
CMD [streamlit, run, app.py, --server.port, 7860, --server.address, 0.0.0.0]
