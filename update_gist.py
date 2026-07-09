import requests
import subprocess
import base64
import hashlib
import json
import gzip
import io
import os

# --- КОНФИГУРАЦИЯ ---
GIST_ID = "a66814180363b8e34a03eb7e1b532b59" # Замените на ваш ID
GITHUB_TOKEN = os.environ.get("GIST_TOKEN")

TARGETS = [
    {
        "url": "https://raw.githubusercontent.com/s741dev/8cf923f83818315e7b47bc635fe87b93/main/1d1619b2c966003e235aad70010c113e",
        "key": "3082058930820371a003020102021500d20b9c75258f602834e61d869ebfea1aee1b1dc2300d06092a864886f70d01010b05003074310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e205669657731143012060355040a130b476f6f676c6520496e632e3110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643020170d3233303533313038310110375a180f32303533303533313038313030375a3074310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e205669657731143012060355040a130b476f6f676c6520496e632e3110302e060355040b1307416e64726f69643110300e06035504031307416e64726f696430820222300d06092a864886f70d01010105000382020f003082020a0282020100d01019905306412b990caeeafe9d201ec67753e3f5feb544609d6ac844e83790d1fbc1bdfa3e5d898288feaa168ae128a650fed416ff16afb45958bd112e2fd82323bc1371a2c6e8304b641e0a76f5e4b73c043a450f576e28258a7cca51281fa2bff5c250324c35aca35c2c32acaa854cb3aa5636c301035e6e34579e185eaece3154a1f26e86da8f58de01211455ff67db6d9c8ec0a48bc20888df0e043e7c5e8481a174b8c1872a774932d9ea2bc123f435b8369875bfcc4d8367c49535ff6577ee72383b3433c46252c849826b9d7d3272c39b6b069fcbf6d214392d377688e5303e2e9bfcc8dc87a2a7b464ec48acd4921ef9c81bbcadfcf2f61e3a8c42b116adcd73957ff921e886c2863397eabd6134ef4fb24c98049af40b047c1be7dabd7963cc5631db4e7805c170bd42937f632be9a91901c138a7d26053af40321fda614344dcb4adf967db69b388073cc04069be69102e904c4e5e6caffb2efad6b1c203d4313f1b219d6d9b268cdf335d58695062edb85748ff20c15528f9657a9c838a1c1d0095b8b4eead3dfd871b4b12dc67fe96148183fafb3b995f955dad8c80cd1dc4232d70e09b061167742051155244e2c524dad93cc621e2a575c4fe5912dc9273a5b8e6cb49349e56a3ffad1999ff26d839be242618447e2d2ec8c1f4ee7326ad047326aaf0468e8b12b942598e9cb2d5a596e0bd1c4fe93681830203010001a310300e300c0603551d13040530030101ff300d06092a864886f70d01010b05000382020100bbc624212d22469db46320a507dc4c2592fcb30b95b53912c9d092f2a800d38efbc391a20f25c452f7b994b824bc159a3dd6873edba1f8e0bbfc26d490ca70ead8a8b7cf9a1279c541069eb0fdfa928aa95f2884f999bdf2f3d33fef5a1c8deff4f0b4ce2bd7cda47bf2c123f6e439feef510d63bb066536e30640e0c1185d62324f2e29e95dee1c7ec612af7d78f3aa4c2496189be214c2af6fbc0f7083241ec5239fc2175a38d842673965e96fb013a7c218afa9541cfa4478059a08e3b6cbadce7d47da06bafca1f2d81611acd3dac4d95664e72c6751204c3bb97cb2145c700c6a7c69aaa9618610d1272fd45b4ed7f7bbafb2ec26e29a4513de3e6df9cb7caed339a90bf0bf39b31b9282d7144fac57a40761cbd173efec21e74a149ea48f7c34d9f79d67abefeed215945fe34d6763e41c319bddd3ce35987bbcc0a2dc939a95d221d20a56c7960b5bc844761a53f5520d52a71c80c2a4fe9948c2358492c6a2416cda7a5f9bf6a9e4932880e5f4bd8549c880ff0f63964203d4865959b6ce6307e068b73fc4e6583e095ec6d05aa92a8c55b3e5c5141a34deeadd76945d39da039350d0b95c6cf13927dfc0ea10aab8cdd4544d3166ebd3b9e13c381d70137a1c0b01ce343f6e3daeede046ac0166e9a0df3c9416d10979ad42a2e4eb90a927967feca660bffd0bb5614de37696aac21407f35b7aa2155315daa42e63com.gitivpn.secureg", 
        "prefix": "guti"
    },
    {
        "url": "https://raw.githubusercontent.com/s741dev/761480176b4895f7eece0f2bffcadb76/refs/heads/main/66005353de5a730d61ad168ccf2a228d",
        "key": "3082058930820371a0030201abcajhu6b6jjjhhhgggt0ecb3985adb8af59a67300d06092a864886df70d0155555500311431lkj00906035d5040613025553311330110603d557708130a43616c69666da004a69613266301406458540407130d4d6f756e74845h5g5f5d5s696577311d43012060605040a130b476f6f676c652077777632e3110300e060355040b1395416e64726fd69643110300e06035504031307416e64727f6d8783020170d3233304565513037353833303533303533313037353833335sd231reweda3074310b10090603550406137761733113306206bvhfgydhfgdgftegftry666f726e6961311637763603550407130d4d6f756e7469896e205669657731143012060355040a130b491f6f676c6520496e632e3110300e060355040b1307416e30726f69643110300e060355040313074jhu87uyu6796430844222300d06092a864886f70d01010105000382020f003082020a028202010097a3ce07ce7f0dcce2b0335d1580c09fdf63ab6c4ab641d54f33337f30394cd7320a8e69643e65b5f69ded69f7ec4831e719b4bc4d6475f4fe933f05b9f23afc14266211ac8187cdce4b807c395ca550e25cf2914b20a42502407db9ea008ecfdf2990443lllllllllo4f4ae5a3e2ce7b071930948a057a8288052725d2060aca5b9690ba0e79bea6e3da724cdd67dc01052311c4b7e300c40f3254ba8458e297cd83f28a9ee6fd74bacbf4eb467e3e34e687ea318ee9f7212ece50914570c0f685c953280e5a133288fa81baf1a18269b8a664d2b9b46c0824df4ce2fe9111111111173c829f709f4f65ae1f9cf3d15eb6259ac4da55e414e56cbdcb9c5fb2ebd21427dfb35ef5cb41f759bfdb200eb5baca10fd2057b16e1a4f62871096e02385t5r5y8u88f8e8fe8ffec2791dd826b994191d25df8269f8e839eb12243834e5714a6eeaed5323d452a3be9084faa9947b10df9b4bda92fae1978abf4adb05c55e191aa985291c63fc19c9f998be2f35829cdc1d9a2c5aa6e299c73d8b8c2d35b5ef02fab2c8520bc12afeda1247454860d9e388fc6a6b00d56bcebe08d86cc4b4e08882d30c87db66bfb4a22d7b9abd962cbfccd4c21ab7b54e203aa4f2a9fd2f0073fbba208e312d9c1687e1fd2877d15d8e4a959696345a5d88dc09713a9719e1451f56c0c5a7fd72d52c9d04ac097b40f6f11e87b9806a9bc61a7b0f627f70df50203010074a310710e720c0603551d13073522030101ff374d06092a805875f70d01010b0576038209817774c99383f5a497800c19b4d3c79b097a761f18847efd05b1778d6b4ceff16bcb0ee2ff2fec4acf383a868a8154871e347b399a245b284707a58a027acad14f7f6695679f06d519fca580b4e14c7c6fJJJJJGGGGG7beaa5f19fd6f16dc14b58076460fbc2daa6158e71fcf658ea6c8da2842b37afc0301041bb7f5ba4488aec9ee860c2ec4b6ce1416be13220a2cc8120f356aecefc0345abeaac6199e111c80f5cb9d4d4b0e010cc9b3aa40d9778157855cf82f05e17bef834b2b4f93472d6ba5af1b48437ea3332fea85e07bc24aa59686c0fbc1d32c6d198c4df87a14e1a1b6738d948d8b53c06d8af0ab25fe3acbf824a39224c6557d040d441578670afdd1d8a07a7b3072609bb0ac947f723425542f73fe75341e2d61d864761a5d879c4aac3b23a42af9c9bd5703b61488cfaa0894bca5bb09f0e6de68b900e9c2f42bc78e5e9673c9194e3c28f03bae62e79929282208d0aaf42493e99a4f38b0ae0cc378994f3ab07cb91098f73e88971d4a20e65ff6e8fb343295c27c6823d4e6c71b55f1d0ed619a29bffdc09234ce122dd6b4e249acaciuo897yt6y1b5c44071eea32bc8002ddc994682e8c4a095314106f3b5f06chgh1f8115eb9d1609450a2dfe4e3ec3fa96eafea6a255555993d733f1a97717e69418e003b6ac1c878f1112d6e1c98967f1b7e02b0b35c0225abb86970f01be773c9f5f621996cc79a117880com.netrino.v2rayapp", 
        "prefix": "netr"
    },
    {
        "url": "https://raw.githubusercontent.com/s741dev/b9c58db918dcbf8700547090eca614ba/refs/heads/main/b0081ea40bdefb175133ed288181e9c4",
        "key": "3082058931920332d003020102040300d5c881026b6b14587185adb18af159a1673100d1060192a186418861f70d01010blkjhg114310b300906011104061302555331133011060355040813045858hc69666f726e6961311630140603550407130d4d6f756e1212l96e205669657731143012060355040a130b476f6f676c6520496e632e3110300e060355040b1395416e64726f69643110300e06035504031744416e64726f69643020170d3233306633313037353833335a180f32303533306578713037353833335a3074310b1009060355040613025073311330110603550485130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e205669657731143012060355040a130b476f6f676c1020496e632e3990300e060355040b1307416e30726f69643110335e06035504031307416e64726f696430844222300d06092a864886f70d01010105000382020f003082020a028202010097a3ce07ce7f0dcce2b0585d1580c09fdf63ab6c4ab811d54f38937f30394cd7770a8e69643e47b5f69ded69f7ec4831e719b4bc4d6475f4fe933f05a7f23afc14288211ac8187cdce4b807c395ca550e25cf2914b20a42502407db9ea008ecfdf20604648875be1fd88f4ae5a3e2ce7b071930948a057a5587552725d2060aca5b9290ba0e79bea6e3da724bad67dc01052441c4b7e990c40f4754ba8458e637cd83f64a9ee6fd74bacbf4eb408e3e34e687ea318ee9f7732ece50914570c0f355c953280e5c533288fa81baf1a18218b8a664d2b9b46c0824df4ea2fe9eedf414defb73c829f709f4f65ae1f9cf3d15eb6259ac4da55e414e56cbdcb9c9fb2ebd21427dfb35ef5cb33b759bfdb224eb5baca22fd2057b16e1a4f62871096e0238e193e27dd3fec6991dd839b994191d16df8269f8e839eb12193834e5714a6eeaed5345d452a3be9084faa9947b10df9b4bda92fae1978abf4adb05c55e191aa985291c63fc19c9f998be2f35829cdb5d9a2c5ab4e299c73d8b8c2d35b5ef02fab2c8587ea12afede5247454860d9e388fc6a6b21d56bcebe08d86cc4b4e08882d30c87db66bfb4a45d7b9abd962cbfccd4c96ab7b54e333aa4f2a9fd2f0073fbba208e312d9c1687e1fd2877d15d8e4a959696345a5d88dc09713a9719e1451f56c0c5a7fd72d36c9d04ac097b40f6f11e87b0006a9ce61a9c0f627f63df50203019991a310300e300c0603551d13040001030101ff300d06092a864886f70d01010b0500038202010074c99383f5a491100c00b4d3c15b097a761f50847efd05b3478d6b4ceff00bcb0ee2ff2fec4acf383a868a8994871e347b399c045b284707a58a027acad53f7f6695679f09b519fdb582a4e99c7c6ff2e56060337beaa5f19fd6f16dc14b58081460fbc2ddb6158e71fcf658ea6c8da2842b37afc2601041bb7f5bf1488aec0ee860c2ec4b6ce5716be72220a1ac8330f356aecefc0345abeaac6199e791c31f5cb9d4d4b0e561bc9b3aa40d9773957855cf77f05e17bef924b2b4f93472d6ba5af1b43137ea3332fea48e07bc24aa59613c0fbc1d32c6d198c4df32a14e1a1b6738d948d8b53c06d8af0ab96fe3bbbf824a39224c6307d040d441578670afdd1d8a07a7b3072609bb0ac947f723425542f73fe75341e2d61d864761a5d879c4aac3b23b12af9c9bd5703b61492cfaa0134bcc6bb09f0e6de68b810e9c2f42bc78e5e8062c4994e3c28f03bae62e79049282208d0aaf42406e99a4f38b0ae0cc366402f3ab07cb91098f73e88971d4a20e65ff6e8fb343295c27c6823d4e6c71b27f1d0ed619b89bffdc51234ce122dd6b4e249acacf89943f11d4e0a44991eea32bc8002ddc994682e8c4c495314133f3b5f06c8bf1f5282oiu89609450a2dfe4e3ec3fa15eafea6a345d13993d733f8b22404e69418e012b6ac1c254lkj22d6e1c75507f1b7e66b0b35c5306ebb86970f30be773c7f7a621348ac75d4lkjlkcom.alan.alanvpn", 
        "prefix": "alan"
    }
]

def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"files": {"vless_links.txt": {"content": content}}}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Gist успешно обновлен!")
    else:
        print(f"Ошибка при обновлении: {response.status_code} - {response.text}")

def get_vless_links(target):
    url = target["url"]
    magic_key_str = target["key"]
    prefix = target["prefix"]
    
    try:
        response = requests.get(url, timeout=30).json()
        raw_bytes = base64.b64decode(response["data"])
        iv, ciphertext = raw_bytes[:16], raw_bytes[16:]
        key = hashlib.sha256(magic_key_str.encode('utf-8')).digest()
        
        process = subprocess.Popen(
            ['openssl', 'enc', '-d', '-aes-256-ctr', '-K', key.hex(), '-iv', iv.hex()],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        decrypted_bytes, err = process.communicate(input=ciphertext)
        
        if process.returncode != 0: return []

        with gzip.GzipFile(fileobj=io.BytesIO(decrypted_bytes)) as f:
            data = json.loads(f.read().decode('utf-8'))
            
                links = []
        configs = data.get("configs", {}).get("normal", [])

        for item in configs:
            config = item.get("config")

            # Новый формат — config уже содержит готовую ссылку
            if isinstance(config, str) and config.startswith((
                "vless://",
                "vmess://",
                "trojan://",
                "ss://",
                "hy2://",
                "hysteria://",
                "tuic://"
            )):
                links.append(config)
                continue

            # Старый формат — config содержит JSON, собираем ссылку
            if isinstance(config, str):
                conf = json.loads(config)
            else:
                conf = config

            proxy = next((o for o in conf.get("outbounds", [])
                          if o.get("tag") == "proxy"), None)
            if not proxy:
                continue

            vnext = proxy["settings"]["vnext"][0]
            vnext["address"] = "8.6.112.0"

            user = vnext["users"][0]
            stream = proxy["streamSettings"]
            tls = stream.get("tlsSettings", {})
            net = stream.get("network", "ws")

            path = "/"
            host = ""

            if net == "xhttp":
                xh = stream.get("xhttpSettings", {})
                path = xh.get("path", "/")
                host = xh.get("headers", {}).get("Host", tls.get("serverName", ""))
            elif net == "ws":
                ws = stream.get("wsSettings", {})
                path = ws.get("path", "/")
                host = ws.get("headers", {}).get("Host", "")

            params = [
                "allowInsecure=1",
                "encryption=none",
                f"fp={tls.get('fingerprint', 'chrome')}",
                f"host={host}",
                "mode=stream-one" if net == "xhttp" else None,
                f"path={path}",
                f"security={stream.get('security', 'none')}",
                f"sni={tls.get('serverName', '')}",
                f"type={net}"
            ]

            params = [p for p in params if p is not None]

            remarks = conf.get("remarks", "server")

            links.append(
                f"vless://{user['id']}@{vnext['address']}:{vnext['port']}?"
                f"{'&'.join(params)}#{prefix}-{remarks}"
            )

        return links
    except Exception as e:
        print(f"Ошибка обработки: {e}")
        return []

if __name__ == "__main__":
    all_links = ""
    for target in TARGETS:
        for link in get_vless_links(target):
            all_links += link + "\n\n"
    
    if all_links and GITHUB_TOKEN:
        update_gist(all_links)
    else:
        print("Ссылки не найдены или отсутствует токен.")
        
