cd ..
rm lambda_function.zip
mkdir -p package
poetry export -f requirements.txt --output package/requirements.txt --without-hashes
pip install -r package/requirements.txt --target package
cp -R src/* package/
cd package && zip -r ../lambda_function.zip . && cd ..
rm -rf package
cd terraform
terraform init
terraform destroy -auto-approve
