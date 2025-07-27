layout = {
    "position": "right-top",
    "offset": [5, 5],  # x, y
    "size": [785, 60]  # width, height
}

statusTable = {
    "top": 5,
    "labelX": 10,
    "labelWidth": 85,
    "valueX": 95,
    "valueWidth": 120,
    "rowHeight": 16,
    "rowSpacing": 1,
    "rows": [
        {"label": "SteamCMD:", "value": "Not Installed", "objectName": "label-status-steamcmd"},
        {"label": "ATLAS:", "value": "Not Installed", "objectName": "label-status-atlas"},
        {"label": "REDIS:", "value": "Not Running", "objectName": "label-status-redis"}
    ]
}

metricsTable = {
    "top": 5,
    "labelX": 300,
    "labelWidth": 50,
    "valueX": 355,
    "valueWidth": 40,
    "rowHeight": 16,
    "rowSpacing": 1,
    "rows": [
        {"label": "CPU:", "value": "", "objectName": "label-cpu"},
        {"label": "Memory:", "value": "", "objectName": "label-mem"}
    ]
}

buttons = {
    "btn-exit-leave": {
        "objectName": "btn-exit-leave",
        "text": "EXIT (NO STOP)",
        "width": 200,
        "height": 24,
        "top": 32,
        "offsetRight": 5
    },
    "btn-exit-stop": {
        "objectName": "btn-exit-stop",
        "text": "EXIT (STOP)",
        "width": 200,
        "height": 24,
        "top": 5,
        "offsetRight": 5
    },
    "btn-redis-stop": {
        "objectName": "btn-redis-stop",
        "text": "STOP REDIS",
        "width": 120,
        "height": 24,
        "top": 32,
        "offsetRight": 210
    },
    "btn-redis-start": {
        "objectName": "btn-redis-start",
        "text": "START REDIS",
        "width": 120,
        "height": 24,
        "top": 5,
        "offsetRight": 210
    }
}
