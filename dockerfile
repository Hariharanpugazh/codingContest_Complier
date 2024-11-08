# Start with an Ubuntu image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for multiple languages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3 \
    python3-pip \
    openjdk-11-jdk \
    && apt-get clean

# Set up the working directory for code compilation
WORKDIR /code

# Copy the compilation script to the container
COPY compile.sh /code/compile.sh
RUN chmod +x /code/compile.sh

# Keep the container running
CMD ["tail", "-f", "/dev/null"]
