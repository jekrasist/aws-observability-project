# aws-observability-project

# 🚀 AWS Observability Service
**Building a Production-Ready Monitoring & Alerting Pipeline**

## 📖 Project Overview
This project demonstrates the implementation of a full-stack observability suite for a Python/Flask microservice. By integrating **Structured JSON Logging**, **Custom Boto3 Metrics**, and **AWS CloudWatch**, I created a system that doesn't just run, but "speaks" its health to an operations team.

---

## 🏗️ System Architecture
The architecture focuses on the **Three Pillars of Observability**:

1.  **Logs:** Flask produces JSON-formatted logs to `/tmp/app.log`. The **CloudWatch Agent** tails this file and streams it to **CloudWatch Log Groups**.
2.  **Metrics:** Business data (`SuccessfulOrders`) is sent directly from the application code to **CloudWatch Metrics** via the AWS SDK (**Boto3**).
3.  **Alerts:** An **SNS-backed Alarm** monitors order volume and notifies me via email if the service stops processing transactions.



---

## 🛠️ Technical Implementation

### 1. Structured Logging & Correlation IDs
Every incoming request is assigned a unique `uuid`. This **Correlation ID** is attached to every log entry, allowing for end-to-end tracing of a single order's journey.
* **Format:** JSON (Standard for ELK/CloudWatch parsing)
* **Goal:** 100% Traceability.

### 2. Infrastructure as Code (Manual Steps)
- **Host:** Amazon Linux 2023 (EC2 t3.micro).
- **Security:** Inbound Port 8080 open for API traffic.
- **IAM:** Instance Profile with `CloudWatchAgentServerPolicy` for secure data transmission.

---

## 📊 Monitoring Dashboard
The dashboard acts as our **"Single Pane of Glass."** It visualizes:
* **Business Health:** Total Successful Orders (Sum / 1m).
* **System Health:** CPU Utilization (Average / 1m).
* **Correlation:** Comparing traffic spikes with resource usage.

---

## 🚨 Incident Response (Alerting)
I configured a **Critical Alarm** on the `SuccessfulOrders` metric:
- **Condition:** If orders $\le$ 0 for 1 minute.
- **Action:** Triggers an SNS notification to my email.
- **Verification:** Successfully verified the "Confirm Subscription" handshake with AWS.

---

## 🚀 How to Run
1. **Start the App:** `python3 server.py &`
2. **Start the Agent:** `/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl ...`
3. **Generate Traffic:** ```bash
   for i in {1..20}; do curl http://[EC2_IP]:8080/order; sleep 1; done


## 🚨 Final Incident Report: Service Interruption Test

### Phase 1: Detection
- **Trigger:** Manual termination of the Flask service and CPU stress test.
- **Metric Observation:** `SuccessfulOrders` dropped to 0; `CPUUtilization` hit 100%.
- **Alarm State:** Transitioned to `ALARM` (Treating missing data as breaching).

### Phase 2: Notification
- **Channel:** AWS SNS (Simple Notification Service).
- **Result:** Received automated email alert within 2 minutes of the breach.

### Phase 3: Resolution & Recovery
- **Action:** Cleared CPU stress and restarted the Flask application.
- **Verification:** Sent 20 test requests via `curl` loop; metrics returned to baseline and Alarm returned to `OK`.
