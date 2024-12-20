import os
import re

def zero_pad_episode_number(filename):
    """Ensure the episode number in the filename is zero-padded (e.g., E7 -> E07)."""
    match = re.search(r'(S\d+E)(\d+)', filename, re.IGNORECASE)
    if match:
        season_episode = match.group(1)
        episode_number = int(match.group(2))
        return re.sub(r'(S\d+E)(\d+)', f"{season_episode}{episode_number:02d}", filename)
    return filename

def match_and_rename(video_files, srt_files, current_dir):
    """Match .srt files to .mkv/.mp4 files based on episode numbers and rename .srt files and videos."""
    for video in video_files:
        padded_video = zero_pad_episode_number(video)
        print(f"Processing video file: {video} -> Padded: {padded_video}")

        video_episode = re.search(r'(S\d+E\d+)', padded_video, re.IGNORECASE)

        if video_episode:
            episode_pattern = video_episode.group(1)  # Extract SxxExx pattern
            print(f"Matching pattern for video: {episode_pattern}")
            matched = False

            # Rename the video file to match the padded format
            if video != padded_video:
                new_video_name = os.path.join(current_dir, padded_video)
                print(f"Renaming video '{video}' to '{new_video_name}'")
                os.rename(os.path.join(current_dir, video), new_video_name)

            for srt in srt_files:
                print(f"Checking SRT file: {srt}")
                if re.search(episode_pattern, srt, re.IGNORECASE):
                    new_srt_name = os.path.join(current_dir, os.path.splitext(padded_video)[0] + ".srt")
                    print(f"Renaming '{srt}' to '{new_srt_name}'")
                    os.rename(os.path.join(current_dir, srt), new_srt_name)
                    matched = True
                    break

            if not matched:
                print(f"No matching SRT found for video: {video}")
        else:
            print(f"Could not find episode pattern in video: {video}")

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located
    
    # Safety check: if the script is in a system directory like System32, prompt the user
    if "System32" in script_dir or os.path.abspath(script_dir) == "C:\\Windows\\System32":
        print(f"Warning: The script is running from {script_dir}. This is a system directory!")
        confirmation = input("Are you sure you want to proceed in this directory? (Y/N): ")
        if confirmation.lower() != 'y':
            print("Script aborted to prevent accidental file changes in system directories.")
            return

    print(f"Starting the script in directory: {script_dir}")

    # Get all files in the script's directory
    files = os.listdir(script_dir)
    print(f"Files in the directory: {files}")

    # Filter for .mkv, .mp4, and .srt files in the script's directory
    video_files = [f for f in files if f.lower().endswith(('.mkv', '.mp4'))]
    srt_files = [f for f in files if f.lower().endswith('.srt')]

    if not video_files:
        print("No video files (.mkv, .mp4) found.")
    if not srt_files:
        print("No .srt files found.")

    print(f"Found video files: {video_files}")
    print(f"Found SRT files: {srt_files}")

    # Match and rename .srt and video files
    match_and_rename(video_files, srt_files, script_dir)

    print("Script finished. Press Enter to exit.")
    input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input()
