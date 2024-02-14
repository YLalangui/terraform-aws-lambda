terraform {
  backend "s3" {
    bucket         = "server-explorer-lambda-terraform-state"
    key            = "terraform.tfstate"
    region         = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "server-explorer-function"
  handler       = "app.server_explorer"
  runtime       = "python3.10"
  role          = "arn:aws:iam::471112657088:role/lambda-ec2-role"
  timeout       = 30

  filename         = "../lambda_function.zip"
  source_code_hash = filebase64sha256("../lambda_function.zip")
}
