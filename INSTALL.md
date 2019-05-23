[Docker]: https://www.docker.com/
[Lifting from the Deep]: https://github.com/DenisTome/Lifting-from-the-Deep-release

# Installation
## Requirements

To install and use this tool you need to have a working instance of [Docker] installed.


## Step 1
Clone the repository to a directory of your choice and jump to the **PoseEstimationTool** folder:

```bash 
git clone https://github.com/elindfo/PoseEstimationTool.git my-directory
cd my-directory/PoseEstimationTool
```

## Step 2
Create a Docker image with [Lifting from the Deep] installed named **"lifting"**: 

```bash
docker build -t lifting LiftingFromTheDeep
```

## Step 3
Create the PoseEstimationTool Docker image:

```bash
docker build -t pose-estimation-tool .
```

You're done!