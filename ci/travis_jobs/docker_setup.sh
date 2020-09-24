echo Get Docker image: ${DOCKERHUB_TAG}
echo 'doing docker build'
# Note: adding --build-arg <arg-name> without any value tells docker to
#  use value from local environment (export DO_GIT_CLONE)

#${TRAVIS_BUILD_DIR}/ci/travis_jobs/get_data_volumes.py

### Loading Docker Image from cache
echo 'Timing Docker Load'
SECONDS=0
IMAGE=docker_images/images.tar
#if [ -e "$IMAGE" ]; then
#  tar -tvf $IMAGE;
#else
#  echo "$IMAGE does not exist";
#fi;
docker load -i docker_images/images.tar || true
docker images
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
echo 

### Building new docker image hopefully with help from cache
echo 'Timing docker Build'
SECONDS=0

docker build -t ${DOCKERHUB_TAG} --build-arg SOURCE_BRANCH=${DOCKERHUB_DEFAULT_TAGNAME} --build-arg MET_BRANCH=${DOCKERHUB_MET_TAGNAME} --build-arg DO_GIT_CLONE ${TRAVIS_BUILD_DIR}/ci/docker
docker images
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

### Save newly built image dtcenter/METplus:develop
echo 'Timing Docker Save'
SECONDS=0
echo "Saving Docker Images"
docker images
# docker save -o docker_images/images.tar $(docker images -a -q)
echo docker save -o docker_images/images.tar ${DOCKERHUB_TAG} ${DOCKERHUB_MET_TAGNAME}
docker save -o docker_images/images.tar ${DOCKERHUB_TAG} ${DOCKERHUB_MET_TAGNAME}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

echo 'done'
