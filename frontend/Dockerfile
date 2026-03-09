FROM node:20-alpine
RUN apk add --no-cache bash git

COPY frontend/docker-entrypoint.sh /opt/docker-entrypoint.sh
RUN chown node:node /opt/docker-entrypoint.sh && chmod +x /opt/docker-entrypoint.sh


USER node
WORKDIR /app
COPY frontend/package* .
ENV NODE_PATH=/home/node/.node_modules
RUN npm install 
#--prefix /home/node/.node_modules


EXPOSE 5173

ENTRYPOINT ["/opt/docker-entrypoint.sh"]