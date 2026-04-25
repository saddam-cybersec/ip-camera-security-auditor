CAMERA_PORTS = [80, 443, 554, 8000, 8080, 8899]

DEFAULT_CREDENTIALS = [
    ("admin", "admin"), ("admin", "12345"), ("admin", "password"),
    ("admin", ""), ("root", "root"), ("root", "12345"),
    ("user", "user"), ("admin", "1234"), ("admin", "123456"), ("guest", "guest"),
]

VENDOR_RTSP_PATHS = {
    "hikvision": ["/Streaming/Channels/101", "/Streaming/Channels/1", "/h264/ch1/main/av_stream"],
    "dahua": ["/cam/realmonitor?channel=1&subtype=0", "/live"],
    "axis": ["/axis-media/media.amp", "/mjpg/video.mjpg"],
    "foscam": ["/videoMain", "/11"],
    "default": ["/", "/live", "/stream", "/video", "/live/ch00_0", "/cam/realmonitor", "/h264", "/mpeg4", "/mjpeg", "/live.sdp", "/video.mp4", "/stream1"],
}

HTTP_PATHS = [
    "/", "/index.html", "/login.html", "/login", "/admin", "/cgi-bin/",
    "/snapshot.jpg", "/snapshot", "/image.jpg", "/onvif/device_service", "/api/v1/"
]