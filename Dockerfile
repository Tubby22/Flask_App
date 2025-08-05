#Using an official Python runtime as a parentimage
FROM python

#Set Working directory in the container
WORKDIR /Auth

#copy the files to the dockerimage directory
COPY .. /Auth


# installing all the dependencies
RUN pip install -r requirements.txt



#making port 5000 available for application running
EXPOSE 8000

#run the python file
CMD [ "python","Authentication.py" ]
