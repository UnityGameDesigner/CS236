import os
import shutil

# Define the directory containing your audio files
audio_files_directory = '../../../Downloads/CREMA-D/AudioWAV'
folders_directory = 'trainingVideos'

# Get a list of all audio files
audio_files = [f for f in os.listdir(audio_files_directory) if f.endswith('.wav')]

for file in audio_files:
    # Extract the folder name from the file name (e.g., '1032_IEO' from '1032_IEO_NEU_XX.wav')
    folder_name = '_'.join(file.split('_')[:3])

    # Check if the corresponding folder exists
    target_folder_path = os.path.join(folders_directory, folder_name + '_XX')
    print(target_folder_path)
    if os.path.exists(target_folder_path):
        # Move the file into the corresponding folder only if the folder exists
        source_file_path = os.path.join(audio_files_directory, file)
        destination_file_path = os.path.join(target_folder_path, file)
        shutil.move(source_file_path, destination_file_path)
