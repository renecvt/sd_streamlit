#!/bin/sh

# Run streamlit application
touch /app/streamlitlog.txt
nohup python -m streamlit run /app/app.py > /app/streamlitlog.txt 2>&1 &

# Run ngrok
ngrok http --config /app/ngrok_config.yml 8501
