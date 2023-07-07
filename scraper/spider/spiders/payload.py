from datetime import datetime


def generate_product_payload(code):
    # Get the current date
    now = datetime.now()

    # Format the date as day-month-year (e.g., 07062023)
    date_str = now.strftime('%d%m%Y')

    return f'/{code}?lang=en&date={date_str}&pickupType=STORE&storeId=1517&banner=superstore'


def generate_payload(page_size=50, page_from=0):
    return {
        "pagination": {
            "from": page_from,
            "size": page_size
        },
        "banner": "superstore",
        # generate this based on initial request later
        "cartId": "5d1f7722-6085-4f8e-b854-9bdd3e7d11ec",
        "lang": "en",
        "storeId": "1517",
        "pcId": None,
        "pickupType": "STORE",
        "offerType": "ALL",
        "categoryId": "27998",
    }


v4_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en",
    "Business-User-Agent": "PCXWEB",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "DNT": "1",
    "Origin": "https://www.realcanadiansuperstore.ca",
    "Referer": "https://www.realcanadiansuperstore.ca/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "Site-Banner": "superstore",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Brave\";v=\"114\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "x-apikey": "1im1hL52q9xvta16GlSdYDsTsG0dmyhF"
}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "DNT": "1",
    "Origin": "https://www.realcanadiansuperstore.ca",
    "Referer": "https://www.realcanadiansuperstore.ca/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "Site-Banner": "superstore",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Brave";v="111", " Not A;Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "Android",
    "x-apikey": "1im1hL52q9xvta16GlSdYDsTsG0dmyhF",
}


