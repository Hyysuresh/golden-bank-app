FROM nginx:alpine

# Copy the static files into the Nginx public directory
COPY . /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

#expose port 80
EXPOSE 80
