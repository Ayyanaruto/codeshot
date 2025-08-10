# Railway Deployment Guide for Codeshot MCP Server

This guide will help you deploy the Codeshot MCP server to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Railway CLI installed (optional but recommended)

## Deployment Steps

### Option 1: Deploy via GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create a new Railway project**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the Dockerfile

3. **Set Environment Variables**
   In your Railway project dashboard, go to Variables and add:
   ```
   AUTH_TOKEN=your_secure_auth_token_here
   MY_NUMBER=your_validation_number_here
   ```

### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and deploy**
   ```bash
   railway init
   railway up
   ```

4. **Set environment variables**
   ```bash
   railway variables set AUTH_TOKEN=your_secure_auth_token_here
   railway variables set MY_NUMBER=your_validation_number_here
   ```

## Environment Variables

The following environment variables are required:

- `AUTH_TOKEN`: Your secure authentication token for the MCP server
- `MY_NUMBER`: Your validation number for the Puch integration

Optional variables:
- `PORT`: Railway automatically sets this, defaults to 8086
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR), defaults to INFO

## Accessing Your Deployed Server

After deployment, Railway will provide you with a URL like:
`https://your-app-name.railway.app`

Your MCP server will be available at this URL.

## Health Check

The server includes a health check endpoint at `/health` that Railway can use to monitor your deployment.

## Fonts and Assets

All required fonts (Fira Code, JetBrains Mono, Source Code Pro) are included in the deployment and will be automatically available.

## Troubleshooting

1. **Build fails**: Check the Railway logs for detailed error messages
2. **Server not responding**: Verify your environment variables are set correctly
3. **Font issues**: Fonts are bundled in the Docker image, should work out of the box

## Local Testing

Before deploying, you can test the Docker build locally:

```bash
# Build the image
docker build -t codeshot-mcp .

# Run the container
docker run -p 8086:8086 -e AUTH_TOKEN=test -e MY_NUMBER=123 codeshot-mcp
```

## Support

For issues specific to Railway deployment, check:
- Railway documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
