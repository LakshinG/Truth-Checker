output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.truth_checker_repo.repository_url
}

output "public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

output "api_url" {
  description = "The URL to access the FastAPI endpoint"
  value       = "http://${aws_instance.web.public_ip}:8000"
}

output "private_key_pem" {
  value     = tls_private_key.deployer_key.private_key_pem
  sensitive = true
}
