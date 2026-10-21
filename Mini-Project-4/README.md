# Mini Project 4: AWS Infrastructure Automation

## Overview
Deployment of a Student Record and Academic Management Flask application using Docker, Terraform, Ansible, AWS EC2, and Nginx.

## Architecture
Developer / Local Source
        |
        v
Docker Container (Flask + Gunicorn)
        |
        v
Nginx Reverse Proxy (Port 80)
        |
        v
AWS EC2 in a Terraform-managed VPC

Terraform provisions the VPC, public subnet, internet gateway, route table, security group, EC2 instance, SSH key pair, and private encrypted S3 bucket.

Ansible automates server setup, Docker installation, Nginx configuration, and application deployment.

## API Validation
- GET /api/health
- GET /api/students
- POST /api/students
- POST /api/enrollments
- POST /api/marks
- GET /api/students/<student_id>/gpa/<semester>

## Validation Results
The application was deployed on AWS EC2 and the health and student APIs returned successful responses. Student creation, enrollment, marks submission, and GPA calculation were tested successfully.

## Project Structure
- application/ — Flask application and Dockerfile
- terraform/ — AWS infrastructure configuration
- ansible/ — Deployment playbooks, inventory, and roles
- logs/ — Project logs
- screenshots/ — Implementation and validation evidence

## Cleanup
The Mini Project 4 EC2 instance was stopped after testing. Terraform-managed AWS resources should be destroyed after preserving the required submission evidence.
