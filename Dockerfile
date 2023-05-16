FROM python:3.11.3-bullseye
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]