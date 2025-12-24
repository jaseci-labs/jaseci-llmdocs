# cloud


## From: contrib.md

* Version bump jac, jac-cloud, byllm
  * Remember to version bump requirement of jaclang in jac-cloud and byllm
* After success
  * Run `Release jac-cloud to PYPI` action manually


## From: introduction.md

Jac Cloud is a powerful cloud-native framework that transforms your Jac applications into production-ready API servers with minimal configuration. It bridges the gap between local Jac development and scalable cloud deployment, providing enterprise-grade features out of the box.
- Access a rich set of cloud-native features without writing additional code
- **Cloud Integration**
- Kubernetes deployment support
- Docker containerization
- ConfigMap-based configuration
- Horizontal scaling capabilities
- **Kubernetes Deployment](deployment.md)** - Deploy to the cloud


## From: deployment.md

# Cloud Deployment Guide

## Overview

Jac Cloud provides a Kubernetes-based deployment template to easily deploy your service into your cluster. This setup includes:

1. A Docker image with all necessary dependencies
2. Kubernetes configuration for essential resources (namespaces, service accounts, roles, etc.)
3. Dynamic configuration through environment variables and ConfigMaps

This guide will help you deploy your Jac applications to a Kubernetes cluster with minimal effort.

## Prerequisites

Before you begin, ensure you have:

1. **Kubernetes Cluster**: Access to a running Kubernetes cluster
2. **kubectl**: The Kubernetes command-line tool installed and configured
3. **Docker**: Docker installed for building and pushing images
4. **Namespace**: The target namespace should be created before deployment
5. **OpenAI API Key**: (Optional) An OpenAI API key if you're using OpenAI services

## Directory Structure

The deployment files are organized as follows:

```
jac-cloud/
├── scripts/
│   ├── Dockerfile
│   ├── init_jac_cloud.sh
│   ├── jac-cloud.yml
│   ├── module-config.yml
```

## Step-by-Step Deployment Guide

Follow these steps to deploy your Jac application to Kubernetes:

### 1. Build and Push the Docker Image

First, build the Jac Cloud Docker image using the provided Dockerfile:

```bash
docker build -t your-dockerhub-username/jac-cloud:latest -f jac-cloud/scripts/Dockerfile .
docker push your-dockerhub-username/jac-cloud:latest
```

After pushing the image, update the `image` field in `jac-cloud.yml` with your Docker image path.

### 2. Apply the ConfigMap

Apply the module configuration to set up module-specific settings:

```bash
kubectl apply -f jac-cloud/scripts/module-config.yml
```

This creates the `littlex` namespace and configures the module settings.

### 3. Apply Kubernetes Resources

Deploy the Jac Cloud application and all required resources:

```bash
kubectl apply -f jac-cloud/scripts/jac-cloud.yml
```

This sets up:

- RBAC roles and bindings
- The Jac Cloud deployment in the `littlex` namespace

### 4. Add OpenAI API Key (Optional)

If your application uses OpenAI services, add your API key as a Kubernetes secret:

```bash
# Encode your API key in base64
echo -n "your-openai-key" | base64
```

Then, update the base64 value in the `data.openai-key` field of the secret definition in `jac-cloud.yml` and apply it:

```bash
kubectl apply -f jac-cloud/scripts/jac-cloud.yml
```

### 5. Verify Your Deployment

Check that all resources are created successfully:

```bash
kubectl get all -n littlex
```

You should see the Jac Cloud pod running along with all associated resources.

## Configuration Details

### Environment Variables

The following environment variables can be configured for your deployment:

| Variable         | Description                         | Default Value   |
| ---------------- | ----------------------------------- | --------------- |
| `NAMESPACE`      | Target namespace for the deployment | `default`       |
| `CONFIGMAP_NAME` | Name of the ConfigMap to mount      | `module-config` |
| `FILE_NAME`      | JAC file to execute in the pod      | `example.jac`   |
| `OPENAI_API_KEY` | OpenAI API key (from secret)        | None            |

## Troubleshooting and Validation

### Verify Namespace

Check if the namespace exists:

```bash
kubectl get namespaces
```

### Verify ConfigMap

Ensure the ConfigMap is properly applied:

```bash
kubectl get configmap -n littlex
```

### Verify Deployment

Check if the Jac Cloud pod is running:

```bash
kubectl get pods -n littlex
```

## Advanced Usage

### Updating Configurations

To update the ConfigMap or deployment:

1. Modify the YAML files as needed
2. Apply the changes:

```bash
kubectl apply -f jac-cloud/scripts/module-config.yml
kubectl apply -f jac-cloud/scripts/jac-cloud.yml
```

### Monitoring Logs

View the logs of your Jac Cloud application:

```bash
kubectl logs -f deployment/jac-cloud -n littlex
```

### Scaling the Deployment

Increase the number of replicas to handle more traffic:

```bash
kubectl scale deployment jac-cloud --replicas=3 -n littlex
```

### Configuring Resource Limits

Adjust CPU and memory limits in the `jac-cloud.yml` file:

```yaml
resources:
  limits:
    cpu: "1"
    memory: "1Gi"
  requests:
    cpu: "500m"
    memory: "512Mi"
```

## Cleanup

To remove all deployed resources:

```bash
kubectl delete namespace littlex
```

This will delete all resources associated with your Jac Cloud deployment.


## From: sso_implementation.md

## Supported Platforms in Jac Cloud

Currently following SSO platforms are supported in Jac cloud for SSO

| **Platform name** | **Used for** |
|----------------------|-----------------|
| `APPLE` | Used for apple SSO integration for both websites and mobile apps|
| `GOOGLE` | Used for gmail SSO integration for websites|
| `GOOGLE_ANDROID` | Used for gmail SSO integration for android mobile apps|
| `GOOGLE_IOS` | Used for gmail SSO integration for ios mobile apps|

## Steps to implement SSO in Jac cloud Setting Your Environment variables

### Step 1: Obtain relevant client credentials from supported platforms
First choose the supported platform and register your application with the relevant platform to get credentials needed
to setup SSO in jac cloud.You can read following documentations and tutorials to register your application.

### Step 3: Call Register Callback Endpoint Provided by JAC Cloud

Once the `id_token` is obtained, call the callback endpoint provided by JAC Cloud

This will register your user with jac cloud and sso platform and returns you the required user informations like name,email etc


## From: llmdocs.md

### Mini (Recommended)
- Cloud APIs and endpoints
- Learn about [Jac Cloud](../jac-cloud/introduction.md) deployment


## From: streamlit.md

### Integration with Jac Cloud

You can build Streamlit frontends that interact with Jac Cloud APIs:

```jac
import streamlit as st;
import requests;

def make_api_call(token: str, endpoint: str, payload: dict) -> dict {
    response = requests.post(
        "http://localhost:8000/" + endpoint,
        json=payload,
        headers={"Authorization": "Bearer " + token}
    );
    return response.json() if response.status_code == 200 else {};
}

with entry {
    st.title("Jac Cloud Frontend");

    # Authentication
    if "token" not in st.session_state {
        st.session_state.token = None;
    }

    if not st.session_state.token {
        with st.form("login_form") {
            email = st.text_input("Email");
            password = st.text_input("Password", type="password");

            if st.form_submit_button("Login") {
                # Attempt login
                response = requests.post(
                    "http://localhost:8000/user/login",
                    json={"email": email, "password": password}
                );

                if response.status_code == 200 {
                    st.session_state.token = response.json()["token"];
                    st.rerun();
                } else {
                    st.error("Login failed!");
                }
            }
        }
    } else {
        st.success("Logged in successfully!");

        # Your app content here
        user_input = st.text_input("Enter your message:");

        if st.button("Send") and user_input {
            result = make_api_call(
                st.session_state.token,
                "walker/interact",
                {"message": user_input}
            );

            if result {
                st.write("Response:", result);
            }
        }
    }
}
```

- Check out the [Jac Cloud documentation](../jac-cloud/introduction.md) for backend integration
- Try building a complete application using Jac + Streamlit + Jac Cloud


## From: task-manager-lite.md

1. Install dependencies:
   ```bash
   pip install jac-streamlit requests jaclang jac-cloud byllm
   ```

1. Start the Jac Cloud server:
   ```bash
   jac serve task_manager.jac
   ```

1. **Install required dependencies:**
   ```bash
   pip install jac-streamlit jaclang datetime byllm jac-cloud
   ```

