variable "aws_region" {
  description = "The AWS region to deploy the resources"
  type        = string
  default     = "us-west-2"
}

variable "aws_access_key" {
  description = "AWS access key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
}
