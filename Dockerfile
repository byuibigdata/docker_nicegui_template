FROM zauberzeug/nicegui:2.22.2

COPY . .

RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the NiceGUI port
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]
