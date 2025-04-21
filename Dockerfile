FROM python:3.12.9-bookworm

WORKDIR /app

COPY . /app

# Install coreutils package
RUN apt-get install coreutils -y

# Install ngrok
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | tee /etc/apt/sources.list.d/ngrok.list \
  && apt update -y \
  && apt install ngrok -y

# Installing application dependencies
RUN pip install -r requirements.txt

EXPOSE 4040

# Run the entrypoint
RUN chmod +x ./bootstrap.sh
ENTRYPOINT [ "./bootstrap.sh" ]