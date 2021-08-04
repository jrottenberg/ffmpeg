
Build 
```
docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --build-arg VCS_REF=$(git rev-parse --short HEAD)  -t custom/ffmpeg:latest -t custom/ffmpeg:4.4.0 --build-arg VERSION=4.4.0 .
```

build multiarch

```
docker buildx build --push --platform linux/arm64/v8,linux/amd64 --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --build-arg VCS_REF=$(git rev-parse --short HEAD) --tag custom/ffmpeg:latest --tag quay.io/custom/ffmpeg .
```
