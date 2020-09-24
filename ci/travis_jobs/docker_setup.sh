echo Get Docker image: ${DOCKERHUB_TAG}
echo 'doing docker build'
# Note: adding --build-arg <arg-name> without any value tells docker to
#  use value from local environment (export DO_GIT_CLONE)

#${TRAVIS_BUILD_DIR}/ci/travis_jobs/get_data_volumes.py

echo Timing docker build...
SECONDS=0

echo Pull docker image from DockerHub
docker pull ${DOCKERHUB_TAG}

echo Build docker image using pulled image as cached from rebuild anything that has updated since the last docker push
docker build --cache-from ${DOCKERHUB_TAG} -t ${DOCKERHUB_TAG} --build-arg SOURCE_BRANCH=${DOCKERHUB_DEFAULT_TAGNAME} --build-arg MET_BRANCH=${DOCKERHUB_MET_TAGNAME} --build-arg DO_GIT_CLONE ${TRAVIS_BUILD_DIR}/ci/docker

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
echo 'done'
