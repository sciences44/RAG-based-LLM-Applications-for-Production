SHELL = /bin/bash

# Makefile for downloading data
EFS_DIR := data
RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER := 0

download_data:
	wget -e robots=off --recursive --no-clobber --page-requisites \
	--html-extension --convert-links \
	--domains docs.ray.io --no-parent --accept=html \
	-P "$(EFS_DIR)" https://docs.ray.io/en/master/

fix_ssl:
	echo $(cat ~/Documents/zscaler_cA.pem) >> 
	
load_data_in_pod:
	kubectl cp data "$$(kubectl get pods | grep raycluster-kuberay-head | awk '{print $$1}')":/dev/shm/data
	kubectl cp ~/Documents/zscaler_cA.pem "$$(kubectl get pods | grep raycluster-kuberay-head | awk '{print $$1}')":/home/ray/anaconda3/lib/python3.8/site-packages/certifi/zscaler_cA.pem 
	for pod_name in $$(kubectl get pods | grep raycluster-kuberay-worker-workergroup | awk '{print $$1}'); do \
		kubectl cp data "$$pod_name":/dev/shm/data; \
		kubectl cp ~/Documents/zscaler_cA.pem "$$pod_name":/home/ray/anaconda3/lib/python3.8/site-packages/certifi/zscaler_cA.pem \

	done

deploy_ray:
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/  
	helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0-rc.1

	helm install raycluster kuberay/ray-cluster --version 1.0.0-rc.1 --set image.tag=nightly-aarch64
	# (For x86_64 users)
	# helm install raycluster kuberay/ray-cluster --version 1.0.0-rc.1	

port_forward_ray:
	kubectl port-forward --address 0.0.0.0 svc/raycluster-kuberay-head-svc 8265:8265

style:
	black .
	flake8
	python3 -m isort .
	pyupgrade


# Cleaning
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
