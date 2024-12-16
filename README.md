## Tags
- kserve
- text-generation
- meta-llama/Llama-3.2-1B-Instruct


### Sample request

```
curl --location 'http://localhost:8019/v1/models/Meta-Llama-3.2-1B-Instruct:predict' \
--header 'Content-Type: application/json' \
--data '{
    "messages" : [
        {"role": "user", "content": "Hi there!"},
        {"role": "assistant", "content": "Nice to meet you!"},
        {"role": "user", "content": "Can I ask a question?"}
    ],
    "max_tokens": 256
}'
```


## Deploy
docker build  -t meta-llama-3.2-1b-instruct .
docker run -ePORT=8080 -p8080:8080 docker.io/library/meta-llama-3.2-1b-instruct

kubectl apply -f kserve_inference_service.yaml


https://kserve.github.io/website/master/modelserving/v1beta1/custom/custom_model/