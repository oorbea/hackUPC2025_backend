FROM python:3.12.6-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia y instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto que tu app usa
EXPOSE 5000

# Arranca la aplicación
CMD ["python", "app.py"]
