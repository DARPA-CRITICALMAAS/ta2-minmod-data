FROM ubuntu:latest

RUN apt-get update && apt-get install -y wget net-tools default-jdk psmisc

WORKDIR /app

COPY fusekiDeploy.sh .

ENV TTL=final_temp.ttl

COPY $TTL .

# Set the script as executable
RUN chmod +x fusekiDeploy.sh

CMD ["sh", "fusekiDeploy.sh"]
