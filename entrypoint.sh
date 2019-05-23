mkdir -p estimations formatted figures angles

cd input
if [ $VIDEO = true ];
then
    echo 'Converting video to images'
    for file in *.mp4
    do
        ffmpeg -i $file %04d.jpg
    done
    echo 'Done!'
    echo ''
fi

echo 'Performing pose estimations'
python /Lifting-from-the-Deep-release/applications/demo.py /shared/input jpg
echo 'Done!'
echo ''

echo 'Formatting pose estimation data'
cd /scripts
for estimation_file in /shared/estimations/*.json
do
    python3 input_formatter_3d.py $estimation_file /shared/formatted
done
echo 'Done!'
echo ''

echo 'Generating 3D figures'
for formatted_file in /shared/formatted/*.json
do
    echo "Generating figure for file ${formatted_file}"
    OUTPUT_DIR=/shared/figures/$(basename $formatted_file .json)
    mkdir -p $OUTPUT_DIR
    python3 figure_creator.py $formatted_file $OUTPUT_DIR
done
echo 'Done!'
echo ''

echo 'Calculating angle data'
for formatted_file in /shared/formatted/*.json
do
    echo "Calculating angles for file ${formatted_file}"
    python3 joint_angle_calculator.py $formatted_file /shared/angles
done
echo 'Done!'
echo ''
