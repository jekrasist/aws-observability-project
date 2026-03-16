# System Architecture

The application is built to demonstrate the **Push** and **Pull** models of observability.

### 1. The Direct Push (Metrics)
The application uses the **AWS SDK (Boto3)** to actively "push" business data (SuccessfulOrders) directly to the CloudWatch API. This is ideal for real-time business KPIs.

### 2. The Log Stream (Agent-based)
The application writes structured JSON logs to a local file. The **CloudWatch Unified Agent** runs as a sidecar-style process, watching the file and "streaming" it to CloudWatch Logs. This decouples the application from the logging infrastructure, ensuring that even if the network is slow, the app doesn't hang.



### 3. Traceability
By implementing **UUID-based Correlation IDs**, we ensure that every single request can be traced from the initial user `curl` command through the application logic and finally into the persistent log storage.
