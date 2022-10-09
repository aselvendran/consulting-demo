current_dir='accounts/local'
export TF_DATA_DIR=${current_dir}/.terraform

terraform apply -var-file=${current_dir}/variables.tfvars $@
