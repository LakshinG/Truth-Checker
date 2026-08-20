variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro" # Modern Free tier eligible
}

variable "key_name" {
  description = "Name of the existing SSH key pair in AWS to access the EC2 instance"
  type        = string
  default     = "my-aws-key" # Update this to your actual AWS key pair name
}
