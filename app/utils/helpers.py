import socket
import re

def probe_rtsp(ip, port, path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        req = f"OPTIONS rtsp://{ip}:{port}{path} RTSP/1.0\r\nCSeq: 1\r\n\r\n"
        s.send(req.encode())
        resp = s.recv(512).decode(errors="ignore")
        s.close()
        return "RTSP/1.0" in resp
    except:
        return False

def get_onvif_xml():
    return """<?xml version="1.0" encoding="utf-8"?>
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
      <s:Body><tds:GetDeviceInformation xmlns:tds="http://www.onvif.org/ver10/device/wsdl"/></s:Body>
    </s:Envelope>"""