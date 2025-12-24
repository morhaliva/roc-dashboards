#!/bin/bash

echo "🚀 ROC Dashboards Deployment Script"
echo "===================================="
echo ""

# Check if running in deployment directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Please run this script from the deployment directory"
    exit 1
fi

# Configuration
IMAGE_NAME="roc-dashboards"
REGISTRY="your-registry.taboolasyndication.com"  # Update this
VERSION="latest"

echo "📋 Deployment Configuration:"
echo "   Image: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"
echo ""

# Menu
echo "Select deployment option:"
echo "1. Build Docker image only"
echo "2. Build and push to registry"
echo "3. Deploy to Kubernetes"
echo "4. Full deployment (build, push, deploy)"
echo "5. Local test (Docker)"
echo ""
read -p "Enter option (1-5): " option

case $option in
    1)
        echo ""
        echo "🐳 Building Docker image..."
        docker build -t ${IMAGE_NAME}:${VERSION} .
        echo "✅ Build complete!"
        ;;
    2)
        echo ""
        echo "🐳 Building Docker image..."
        docker build -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} .
        echo "📤 Pushing to registry..."
        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
        echo "✅ Push complete!"
        ;;
    3)
        echo ""
        echo "☸️  Deploying to Kubernetes..."
        kubectl apply -f kubernetes-deployment.yaml
        echo ""
        echo "📊 Checking deployment status..."
        kubectl get pods -l app=roc-dashboards
        echo ""
        echo "🌐 Checking ingress..."
        kubectl get ingress roc-dashboards-ingress
        echo "✅ Deployment complete!"
        ;;
    4)
        echo ""
        echo "🐳 Building Docker image..."
        docker build -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} .
        echo "📤 Pushing to registry..."
        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
        echo "☸️  Deploying to Kubernetes..."
        kubectl apply -f kubernetes-deployment.yaml
        echo ""
        echo "📊 Checking deployment status..."
        kubectl get pods -l app=roc-dashboards
        echo ""
        echo "🌐 Checking ingress..."
        kubectl get ingress roc-dashboards-ingress
        echo "✅ Full deployment complete!"
        ;;
    5)
        echo ""
        echo "🐳 Building Docker image..."
        docker build -t ${IMAGE_NAME}:${VERSION} .
        echo "🚀 Starting local container..."
        docker run -d -p 8080:80 --name roc-dashboards-test ${IMAGE_NAME}:${VERSION}
        echo ""
        echo "✅ Container started!"
        echo "🌐 Access your dashboard at: http://localhost:8080/roc_dashboards.html"
        echo ""
        echo "To stop: docker stop roc-dashboards-test && docker rm roc-dashboards-test"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "===================================="
echo "✨ Done!"

