"""
================================================================================
ASSIGNMENT 2: Installation and Configuration of Google App Engine
Subject: Cloud Computing (CC)
University: Savitribai Phule Pune University (SPPU)
Course: Third Year Computer Engineering (2019 Course)
================================================================================

PART 1 - THEORY
================================================================================

1. WHAT IS CLOUD COMPUTING?
----------------------------
Cloud computing is the delivery of computing services — including servers, storage,
databases, networking, software, analytics, and intelligence — over the Internet
("the cloud") to offer faster innovation, flexible resources, and economies of scale.
Instead of owning their own computing infrastructure or data centers, companies can
rent access to anything from applications to storage from a cloud service provider.

Types of Cloud Services:
  - IaaS (Infrastructure as a Service): Virtual machines, storage, networking (e.g., AWS EC2)
  - PaaS (Platform as a Service): Platform to build/deploy apps without managing infra (e.g., Google App Engine)
  - SaaS (Software as a Service): Ready-to-use software over internet (e.g., Gmail, Salesforce)

2. WHAT IS GOOGLE APP ENGINE (GAE)?
-------------------------------------
Google App Engine (GAE) is a fully managed Platform as a Service (PaaS) offered by
Google Cloud Platform (GCP). It allows developers to build and host web applications
in Google-managed data centers without managing the underlying infrastructure.

Key Features of Google App Engine:
  - Fully Managed: No need to manage servers or infrastructure
  - Auto Scaling: Automatically scales your app up/down based on traffic
  - Multi-language Support: Python, Java, Node.js, Go, PHP, Ruby, .NET
  - Built-in Services: Datastore, Memcache, Task Queue, etc.
  - Two Environments:
      * Standard Environment: Runs in a sandbox, fast scaling, free tier available
      * Flexible Environment: Runs in Docker containers, more control

3. GOOGLE APP ENGINE ARCHITECTURE
-----------------------------------
GAE follows a layered architecture:

  [User Browser]
       |
       v
  [Google Load Balancer]  <-- handles traffic distribution
       |
       v
  [App Engine Front End]  <-- routes requests
       |
       v
  [Application Instances] <-- your actual Python app runs here
       |
       v
  [Google Cloud Storage / Datastore]  <-- stores data

Components:
  - app.yaml       : Configuration file for the app (runtime, routing, env variables)
  - main.py        : Main application code (your Flask/webapp2 app)
  - requirements.txt: Python dependencies
  - static/        : Static files (HTML, CSS, JS)

4. HOW AUTO SCALING WORKS IN GAE
----------------------------------
- GAE monitors incoming requests
- If traffic increases, it automatically spins up more instances
- If traffic decreases, it scales down (even to 0 in Standard env)
- You can configure: min_instances, max_instances, target_cpu_utilization

5. INSTALLATION AND CONFIGURATION STEPS
-----------------------------------------
Step 1: Install Google Cloud SDK
  - Download from: https://cloud.google.com/sdk/docs/install
  - Run: gcloud init
  - Authenticate: gcloud auth login

Step 2: Create a GCP Project
  - Go to: https://console.cloud.google.com
  - Create a new project (e.g., "my-gae-app")
  - Enable billing (required for deployment)

Step 3: Enable App Engine API
  - Run: gcloud services enable appengine.googleapis.com
  - OR enable from GCP Console > APIs & Services

Step 4: Set up App Engine
  - Run: gcloud app create --region=asia-south1  (for India region)

Step 5: Create the Application Files
  - main.py        → Your Flask application
  - app.yaml       → Configuration
  - requirements.txt → Dependencies

Step 6: Deploy the Application
  - Run: gcloud app deploy
  - Access at: https://[PROJECT_ID].appspot.com

6. app.yaml CONFIGURATION FILE EXPLAINED
------------------------------------------
  runtime: python311          # Python version to use
  instance_class: F1          # Instance type (F1 = smallest, free tier)
  automatic_scaling:
    min_instances: 0          # Scale down to 0 when no traffic
    max_instances: 2          # Max 2 instances to control cost
    target_cpu_utilization: 0.65
  handlers:
    - url: /static            # Route for static files
      static_dir: static
    - url: /.*                # All other routes go to Flask app
      script: auto

7. ADVANTAGES OF GOOGLE APP ENGINE
------------------------------------
  - No server management required
  - Scales automatically (handles traffic spikes)
  - Integrated with other GCP services (BigQuery, Pub/Sub, etc.)
  - Built-in security and monitoring
  - Pay only for what you use

8. DISADVANTAGES OF GOOGLE APP ENGINE
---------------------------------------
  - Less control over underlying infrastructure compared to IaaS
  - Vendor lock-in (specific to Google Cloud)
  - Standard environment has sandbox restrictions
  - Can be expensive at high scale

9. USE CASES OF GOOGLE APP ENGINE
------------------------------------
  - Web applications and APIs
  - Mobile backends
  - IoT data processing
  - Real-time applications

================================================================================
PART 2 - IMPLEMENTATION CODE (Flask Web App on Google App Engine)
================================================================================
"""

# ─────────────────────────────────────────────────────────────────
# Import Flask framework — lightweight Python web framework
# Flask handles HTTP requests and returns responses
# ─────────────────────────────────────────────────────────────────
from flask import Flask, render_template_string, request, jsonify
import datetime  # To show current server time (proves app is live)
import os        # To read environment variables (like PORT)

# ─────────────────────────────────────────────────────────────────
# Create Flask app instance
# __name__ tells Flask where to find resources (templates, static files)
# ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────
# HTML Template — inline template so we don't need a separate file
# In a real project, this would go in templates/index.html
# ─────────────────────────────────────────────────────────────────
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GAE Demo App</title>
    <style>
        /* Simple clean styling */
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            background: #f0f4f8;
            color: #333;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1 { color: #1a73e8; }  /* Google Blue */
        .badge {
            background: #34a853;  /* Google Green */
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
        }
        input[type="text"] {
            padding: 10px;
            width: 70%;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #1557b0; }
        #response { margin-top: 15px; font-weight: bold; color: #34a853; }
    </style>
</head>
<body>
    <div class="card">
        <h1>☁️ Google App Engine Demo</h1>
        <span class="badge">● Live on GAE</span>
        <p>This is a simple web application deployed on Google App Engine (PaaS).</p>
        <p><strong>Server Time:</strong> {{ server_time }}</p>
        <p><strong>Environment:</strong> Google App Engine Standard (Python 3.11)</p>
    </div>

    <div class="card">
        <h2>Test the API</h2>
        <p>Enter your name and click Greet to test the backend API:</p>
        <input type="text" id="nameInput" placeholder="Enter your name..." />
        <button onclick="greetUser()">Greet Me</button>
        <div id="response"></div>
    </div>

    <div class="card">
        <h2>About This App</h2>
        <ul>
            <li>Built with <strong>Python + Flask</strong></li>
            <li>Deployed on <strong>Google App Engine (PaaS)</strong></li>
            <li>Auto-scales based on traffic</li>
            <li>No server management needed</li>
        </ul>
    </div>

    <script>
        // JavaScript to call our Flask API endpoint
        async function greetUser() {
            const name = document.getElementById('nameInput').value;
            if (!name) {
                alert('Please enter your name!');
                return;
            }
            // Call the /greet API endpoint
            const res = await fetch(`/greet?name=${encodeURIComponent(name)}`);
            const data = await res.json();
            document.getElementById('response').textContent = data.message;
        }
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# ROUTE 1: Home Page
# @app.route('/') means this function handles GET requests to '/'
# render_template_string renders HTML with dynamic values
# ─────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    # Get current server time — proves the app is running live
    server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HOME_PAGE, server_time=server_time)


# ─────────────────────────────────────────────────────────────────
# ROUTE 2: /greet API Endpoint
# Accepts a query parameter 'name' and returns a JSON response
# Example: /greet?name=Mangesh → {"message": "Hello, Mangesh! ..."}
# ─────────────────────────────────────────────────────────────────
@app.route('/greet')
def greet():
    # request.args.get() reads URL query parameters
    # Default is 'Guest' if no name is provided
    name = request.args.get('name', 'Guest')

    # Build the greeting message
    message = f"Hello, {name}! Welcome to Google App Engine. Your request was handled at {datetime.datetime.now().strftime('%H:%M:%S')}."

    # jsonify() converts Python dict to proper JSON response
    return jsonify({
        "message": message,
        "status": "success",
        "platform": "Google App Engine"
    })


# ─────────────────────────────────────────────────────────────────
# ROUTE 3: /info — Returns App Info as JSON
# Useful for health checks or API status monitoring
# ─────────────────────────────────────────────────────────────────
@app.route('/info')
def info():
    return jsonify({
        "app_name": "GAE Demo Application",
        "runtime": "Python 3.11",
        "platform": "Google App Engine Standard Environment",
        "framework": "Flask",
        "status": "Running",
        "timestamp": datetime.datetime.now().isoformat()
    })


# ─────────────────────────────────────────────────────────────────
# Entry point for running locally (for testing before deploying)
# On GAE, gunicorn handles this — so this block only runs locally
#
# To run locally:  python main.py
# To deploy:       gcloud app deploy
# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # os.environ.get('PORT', 8080) — GAE sets PORT env variable
    # On local machine it defaults to 8080
    port = int(os.environ.get('PORT', 8080))

    # debug=True → shows detailed errors during local development
    # Set debug=False before deploying to production!
    app.run(host='0.0.0.0', port=port, debug=True)