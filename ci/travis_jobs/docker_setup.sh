echo Get Docker image: ${DOCKERHUB_TAG}
echo 'doing docker build'
# Note: adding --build-arg <arg-name> without any value tells docker to
#  use value from local environment (export DO_GIT_CLONE)

#${TRAVIS_BUILD_DIR}/ci/travis_jobs/get_data_volumes.py

echo 'Timing Docker Load'
SECONDS=0
IMAGE=docker_images/images.tar
if [ -e "$IMAGE" ]; then
  tar -tvf $IMAGE;
else
  echo "$IMAGE does not exist";
fi;
docker load -i docker_images/images.tar || true
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
echo 

echo Timing docker build...
SECONDS=0

docker build -t ${DOCKERHUB_TAG} --build-arg SOURCE_BRANCH=${DOCKERHUB_DEFAULT_TAGNAME} --build-arg MET_BRANCH=${DOCKERHUB_MET_TAGNAME} --build-arg DO_GIT_CLONE ${TRAVIS_BUILD_DIR}/ci/docker

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
echo 'done'
