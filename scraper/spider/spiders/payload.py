def generate_payload(page_size=50, page_from=0):
    return {
        "pagination": {
            "from": page_from,
            "size": page_size,
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
    }

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Business-User-Agent": "PCX-Web",
    "Content-Type": "application/json",
    "Host": "api.pcexpress.ca",
    "Origin": "https://www.realcanadiansuperstore.ca",
    "Referer": "https://www.realcanadiansuperstore.ca",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "Site-Banner": "superstore",
    "x-apikey": "1im1hL52q9xvta16GlSdYDsTsG0dmyhF",
}
