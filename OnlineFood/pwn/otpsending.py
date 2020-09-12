
import requests
import json

def sendASMS(contactno = "8919961080",message="Sorry Message not Available"):

    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+contactno


    headers = {
        'authorization': "hfCpNRqKqFH6H5Eue8r8Dma2Bg9GzDLmwRzbcgI2FXwZEdeuCJ8igkpzETBJ",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    return json.loads(response.text)


