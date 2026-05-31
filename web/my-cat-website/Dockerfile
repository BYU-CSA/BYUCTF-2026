# Use a base Python image
FROM python:3.11

# create unpriv user
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

# Copy application files
COPY app.py .
COPY templates/ templates/

# Install dependencies
RUN pip install flask

# set perms
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

# Run the database setup script first, then start main.py
USER ctf
CMD ["python3", "app.py"]
EXPOSE 1337