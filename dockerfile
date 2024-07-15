FROM ubuntu:22.04
RUN apt update && apt upgrade && apt install python3.10 python3-pip