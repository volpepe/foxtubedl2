pyinstaller.exe --clean         `
    --noconsole                 `
    -i ".\imgs\arctic-fox.ico"  `
    --name "FoxTubeDownloader-Portable"  `
    --add-data="config.yaml:."  `
    --add-binary=".\bin\ffmpeg\bin\ffmpeg.exe:bin\ffmpeg\bin"   `
    --add-binary=".\bin\ffmpeg\bin\ffplay.exe:bin\ffmpeg\bin"   `
    --add-binary=".\bin\ffmpeg\bin\ffprobe.exe:bin\ffmpeg\bin"  `
    --add-binary=".\bin\yt-dlp.exe:bin"                         `
    --upx-dir=".\bin\upx"                                       `
    --onefile                                                   `
    --splash ".\imgs\splash_upscale.png"                        `
    .\start.py