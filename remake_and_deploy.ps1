# Stop and remove containers with the specific name and Dockerfile label

# needs to be fixed, this block doesnt work
$containersToStop = docker ps -q -a  --filter ancestor=gridgame:Dockerfile
foreach ($containerId in $containersToStop) {
    docker stop $containerId
    docker rm $containerId
}

# Causes the script to exit on failure of next commands
$ErrorActionPreference = "Stop"

# Rebuild the Dockerfile
docker build -t "gridgame:Dockerfile" .

# Run the container detached on host port 8001
docker run -d -p 8001:8001 gridgame:Dockerfile > $null

Write-Host "`n`nSuccessfully rebuilt and launched container`n"