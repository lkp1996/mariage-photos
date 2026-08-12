import qrcode

# Remplace par l'URL finale une fois le service déployé sur Render
# (ex: "https://mariage-photos.onrender.com")
url = "https://REMPLACE-PAR-TON-URL.onrender.com"

img = qrcode.make(url)
img.save("qrcode.png")
print(f"QR code généré pour : {url}")
