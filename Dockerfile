FROM nginx:alpine

# Copy the dashboard HTML
COPY roc_dashboards.html /usr/share/nginx/html/
COPY all_dashboards_data.json /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

