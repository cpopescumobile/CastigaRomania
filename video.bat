rem The parameter is the https url from youtube
rem The ~ char in parameter expression means that the param was sent enclosed in "" because it contains an = char inside
yt-dlp.exe %~1

rem Wait 5 seconds before continuing
timeout 5

mkdir %2_selected
mkdir %2_selected\video

rem Wait 5 seconds before continuing
timeout 5

rem Renames and creates a txt file with the old file name as content
renameFile.py %2.mp4

rem Wait 2 seconds before continuing
timeout 2

extractFrames.py %2.mp4

rem Wait 5 seconds before continuing
timeout 5

move %2.mp4 %2_selected/video/%2.mp4

move %2.mp4.Title.txt %2_selected/video/%2_Title.txt

rem Wait 5 seconds before continuing
timeout 5

list_files.py %2

pause


