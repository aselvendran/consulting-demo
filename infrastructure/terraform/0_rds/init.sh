current_dir='accounts/local'
export TF_DATA_DIR=${current_dir}/.terraform

terraform init -backend-config=${current_dir}/backend $@
