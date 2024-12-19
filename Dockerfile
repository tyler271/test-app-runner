# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
FROM public.ecr.aws/amazonlinux/amazonlinux:2
RUN yum install python3.7 -y && curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && yum update -y
RUN yum install -y amazon-linux-extras && amazon-linux-extras enable python3.8 && yum install python3.8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD python3 app.py
EXPOSE 8080
