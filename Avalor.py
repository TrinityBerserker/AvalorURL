import re
import requests
from urllib.parse import urlparse

class Avalor:
    def __init__(self):
        self.palabras_sospechosas = [
            'login', 'signin', 'account', 'secure', 'update', 'confirm',
            'bank', 'paypal', 'apple', 'microsoft', 'verify', 'credentials',
            'reset', 'password', 'wallet', 'billing'
        ]

    def analizar(self, url):
        puntaje = 0
        detalles = []
        recomendaciones = []

        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        try:
            parsed = urlparse(url)
            dominio = parsed.netloc
            ruta = parsed.path
        except Exception:
            return 100, ["❌ URL inválida"], ["Verifica que la URL esté bien escrita."]

        # 1. Longitud
        if len(url) > 54:
            puntaje += 15
            detalles.append("📏 URL muy larga (+15)")
            recomendaciones.append("Las URLs largas suelen ocultar el destino real. Verifica antes de hacer clic.")

        # 2. @
        if '@' in url:
            puntaje += 20
            detalles.append("🚫 Contiene '@' (+20)")
            recomendaciones.append("NUNCA accedas a URLs con '@'. El navegador ignora lo anterior y va a la IP.")  # ✅ CORREGIDO

        # 3. IP directa
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', dominio):
            puntaje += 30
            detalles.append("🌐 Usa dirección IP directa (+30)")
            recomendaciones.append("Los phishers usan IPs para evitar bloqueos. No confíes.")

        # 4. Subdominios
        if dominio.count('.') >= 3:
            puntaje += 15
            detalles.append(f"🔗 Demasiados subdominios ({dominio.count('.')} puntos) (+15)")
            recomendaciones.append("Muchos subdominios son tácticos para parecer legítimos.")

        # 5. Palabras clave
        texto_completo = (dominio + ruta).lower()
        for palabra in self.palabras_sospechosas:
            if palabra in texto_completo:
                puntaje += 5
                detalles.append(f"⚠️ Palabra clave '{palabra}' detectada (+5)")
                recomendaciones.append(f"La palabra '{palabra}' suele aparecer en páginas de phishing.")

        # 5b. Guiones
        if '-' in dominio:
            puntaje += 15
            detalles.append("➖ Contiene guiones en el dominio (+15)")
            recomendaciones.append("Los guiones son comunes en dominios falsos para imitar nombres reales.")

        # 6. HTTP
        if parsed.scheme == 'http':
            puntaje += 10
            detalles.append("🔓 Conexión HTTP (no cifrada) (+10)")
            recomendaciones.append("Sin HTTPS, cualquier persona en tu red puede leer tus datos.")

        # 7. Respuesta
        try:
            response = requests.get(url, timeout=3, allow_redirects=True)
            if response.history:
                puntaje += 10
                detalles.append("🔄 Redirige a otra URL (+10)")
                recomendaciones.append("Las redirecciones suelen llevar a sitios falsos.")
            if response.status_code != 200:
                puntaje += 5
                detalles.append(f"📡 Código inusual ({response.status_code}) (+5)")
                recomendaciones.append("Un código de respuesta extraño puede indicar un sitio mal configurado.")
        except requests.exceptions.RequestException:
            puntaje += 10
            detalles.append("⛔ La URL no responde o es inaccesible (+10)")
            recomendaciones.append("Si no responde, puede ser un dominio recién creado o ya bloqueado.")

        puntaje = min(puntaje, 100)
        return puntaje, detalles, recomendaciones


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🛡️  AVALOR - Phishing Defense System v3.0 (Con Contexto)")
    print("="*60)
    
    avalor = Avalor()
    url_objetivo = input("\n🔍 Ingresa la URL a analizar: ").strip()
    
    if not url_objetivo:
        print("❌ No ingresaste nada.")
    else:
        puntaje, detalles, recomendaciones = avalor.analizar(url_objetivo)
        
        print("\n📊 --- ANÁLISIS DETALLADO ---")
        for detalle in detalles:
            print(f"   {detalle}")
        
        print("\n💡 --- RECOMENDACIONES ---")
        for rec in recomendaciones:
            print(f"   • {rec}")
        
        print(f"\n🎯 PUNTAJE DE RIESGO: {puntaje}%")
        
        if puntaje >= 70:
            print("🔴 ALERTA MÁXIMA: Probabilidad muy alta de phishing.")
            print("   🔒 No ingreses datos personales ni contraseñas.")
        elif puntaje >= 40:
            print("🟡 RIESGO MEDIO: Verifica manualmente.")
            print("   👀 Revisa la URL en la barra de direcciones antes de continuar.")
        else:
            print("🟢 BAJO RIESGO: Parece legítima, pero mantén la precaución.")
        
        print("="*60 + "\n")
