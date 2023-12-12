import os
import shutil

# Define the original directory of your audio files (where you want them moved back to)
original_audio_files_directory = '../../../Downloads/CREMA-D/AudioWAV'

# Define the directory containing the folders with audio files
folders_directory = 'trainingVideos'

# Get a list of all folders
folders = [f for f in os.listdir(folders_directory) if os.path.isdir(os.path.join(folders_directory, f))]

for folder in folders:
    folder_path = os.path.join(folders_directory, folder)
    # Get all audio files in the folder
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    for file in audio_files:
        source_file_path = os.path.join(folder_path, file)
        destination_file_path = os.path.join(original_audio_files_directory, file)

        # Move the file back to the original directory
        shutil.move(source_file_path, destination_file_path)

print("All files have been moved back to the original directory.")