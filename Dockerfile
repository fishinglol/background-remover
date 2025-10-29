FROM python:3.13.7

# Copy to /root/.u2net/ (not /home/.u2net/)
COPY u2net.onnx /root/.u2net/u2net.onnx

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]