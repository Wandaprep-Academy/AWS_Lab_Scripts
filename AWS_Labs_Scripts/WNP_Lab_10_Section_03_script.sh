#!/bin/bash
exec > >(tee /var/log/userdata.log|logger -t userdata -s 2>/dev/console) 2>&1

# 1. Update system
dnf update -y

# 2. Install Apache, Stress tool, CloudWatch Agent
dnf install -y httpd stress amazon-cloudwatch-agent
systemctl start httpd
systemctl enable httpd

# 3. Create simple webpage with instance details
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

cat <<EOF > /var/www/html/index.html
<h1>WandaPrep Auto Scaling Demo</h1>
<p>Instance ID: $INSTANCE_ID</p>
<p>Availability Zone: $AZ</p>
EOF

# 4. Configure CloudWatch Logs
cat <<EOF >/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/httpd/access_log",
            "log_group_name": "wp-asg-access-log",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/var/log/messages",
            "log_group_name": "wp-asg-system-log",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

systemctl start amazon-cloudwatch-agent
systemctl enable amazon-cloudwatch-agent
