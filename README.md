# ROC Dashboards Deployment Guide

## Quick Deployment Options

### Option 1: Kubernetes Deployment (Recommended for Production)

**Prerequisites:**
- Access to Taboola's Kubernetes cluster
- Docker registry access
- kubectl configured

**Steps:**

1. **Build and Push Docker Image:**
```bash
cd /Users/mor.h/.cursor/deployment
cp ../roc_dashboards.html .
cp ../all_dashboards_data.json .

docker build -t your-registry.taboolasyndication.com/roc-dashboards:latest .
docker push your-registry.taboolasyndication.com/roc-dashboards:latest
```

2. **Deploy to Kubernetes:**
```bash
kubectl apply -f kubernetes-deployment.yaml
```

3. **Verify Deployment:**
```bash
kubectl get pods -l app=roc-dashboards
kubectl get ingress roc-dashboards-ingress
```

4. **Update DNS:**
Contact your DevOps team to point `roc-dashboards.taboolasyndication.com` to the ingress IP

---

### Option 2: Simple File Server (Quick & Easy)

**If you have access to an existing web server:**

1. Copy files to web server:
```bash
scp roc_dashboards.html user@webserver.taboolasyndication.com:/var/www/html/roc/
scp all_dashboards_data.json user@webserver.taboolasyndication.com:/var/www/html/roc/
```

2. Access via: `https://webserver.taboolasyndication.com/roc/roc_dashboards.html`

3. Ask IT to create alias: `roc-dashboards.taboolasyndication.com`

---

### Option 3: AWS S3 + CloudFront (If Taboola Uses AWS)

**Steps:**

1. **Create S3 Bucket:**
```bash
aws s3 mb s3://roc-dashboards-internal
aws s3 cp roc_dashboards.html s3://roc-dashboards-internal/
aws s3 cp all_dashboards_data.json s3://roc-dashboards-internal/
```

2. **Enable Static Website Hosting:**
```bash
aws s3 website s3://roc-dashboards-internal/ --index-document roc_dashboards.html
```

3. **Create CloudFront Distribution** pointing to the S3 bucket

4. **Configure DNS** via Route53 or internal DNS

---

### Option 4: GitHub Pages + Internal Proxy

**If you can use GitHub:**

1. Create a private GitHub repo
2. Push your files
3. Enable GitHub Pages
4. Have IT configure reverse proxy:
   - `roc-dashboards.taboolasyndication.com` → GitHub Pages URL

---

## What You Need from DevOps/IT:

1. **DNS Entry**: `roc-dashboards.taboolasyndication.com`
2. **SSL Certificate**: For HTTPS
3. **Deployment Access**: To Kubernetes/Web Server/AWS

## Files Included:

- `Dockerfile` - Container image definition
- `nginx.conf` - Web server configuration  
- `kubernetes-deployment.yaml` - K8s deployment manifests
- `README.md` - This file

## Contact:

For deployment help, contact:
- DevOps Team
- Platform Engineering
- IT Infrastructure

---

## Quick Start Command:

```bash
# Copy files to deployment folder
cp /Users/mor.h/.cursor/roc_dashboards.html /Users/mor.h/.cursor/deployment/
cp /Users/mor.h/.cursor/all_dashboards_data.json /Users/mor.h/.cursor/deployment/

# Build and deploy (adjust for your environment)
cd /Users/mor.h/.cursor/deployment
docker build -t roc-dashboards .
```

