pyinstaller.exe --clean         `
    --onedir                    `
    --noconsole                 `
    -i ".\imgs\arctic-fox.ico"  `
    --name "FoxTubeDownloader"  `
    --add-data="config.yaml:."  `
    --add-binary=".\bin\ffmpeg\bin\ffmpeg.exe:bin\ffmpeg\bin"   `
    --add-binary=".\bin\yt-dlp.exe:bin"                         `
    --upx-dir=".\bin\upx"                                       `
    --splash ".\imgs\splash_upscale.png"                        `
    .\start.py