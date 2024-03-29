[elindfo]: https://github.com/elindfo
[alfonsinbox]: https://github.com/alfonsinbox
[Lifting from the Deep]: https://github.com/DenisTome/Lifting-from-the-Deep-release

# PoseEstimationTool
This tool has been developed by [elindfo] and [alfonsinbox] to simplify the process of estimating human poses in 3D using [Lifting from the Deep]. The tool currently handles either a set of JPEG images or a single MP4 video.

Before you begin, make sure to **install** the tool by following the instructions provided in the [installation guide](INSTALL.md).

## HOW-TO
Begin by creating directories with the following structure anywhere in your system:

```bash
my-directory/
    input/
```

Next, copy the JPEG images **or** a single MP4 video to `my-directory/input/`:

```bash
my-directory/
    input/
        example-image1.jpg
        example-image2.jpg
        ...
```
**or**

```bash
my-directory/
    input/
        example-video.mp4
```

Now run the pose estimation tool using the **absolute path** to `my-directory/` with one of the following two commands:

**Using images:**
```bash
docker run --rm -v /path/to/my-directory:/shared pose-estimation-tool
```

**Using video:**
```bash
docker run --rm -e VIDEO=true -v /path/to/my-directory:/shared pose-estimation-tool
```

This will create the following directory structure in `my-directory/` with the estimated results:
```bash
my-directory/
    angles/
        0.json
        ...
    estimations/
        example-image.json
        ...
    figures/
        0/
            above-0.png
            ...
        ...
    formatted/
        0.json
        ...
    input/
        example-image.jpg
        ...
    
```