#!/usr/bin/env python3
"""
Script d'optimisation des images pour la page voyages
- Compresse les JPG à 85% de qualité
- Crée des versions WebP (optionnel)
- Réduit la taille des fichiers de 40-70%
"""

import os
from PIL import Image
from pathlib import Path

# Configuration
QUALITY_JPG = 85  # Qualité JPG (80-90 recommandé)
QUALITY_WEBP = 80  # Qualité WebP
CREATE_WEBP = True  # Créer des versions WebP
MAX_SIZE = (2000, 2000)  # Taille maximale (largeur, hauteur)

# Dossiers à traiter
TRAVEL_FOLDERS = [
    'Finlande',
    'Norvège',
    'Estonie',
    'Lettonie',
    'France/Nice',
    'France/Monaco',
    'France/Cannes',
    'Espagne/Lloret de mar'
]

def optimize_image(image_path):
    """Optimise une image JPG"""
    try:
        # Ouvrir l'image
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Redimensionner si trop grande
            if img.size[0] > MAX_SIZE[0] or img.size[1] > MAX_SIZE[1]:
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                print(f"  ↓ Redimensionné: {image_path.name}")

            # Sauvegarder JPG optimisé
            original_size = os.path.getsize(image_path)
            img.save(image_path, 'JPEG', quality=QUALITY_JPG, optimize=True)
            new_size = os.path.getsize(image_path)
            saved = ((original_size - new_size) / original_size) * 100

            print(f"  ✓ {image_path.name}: {original_size//1024}KB → {new_size//1024}KB ({saved:.1f}% réduit)")

            # Créer version WebP
            if CREATE_WEBP:
                webp_path = image_path.with_suffix('.webp')
                img.save(webp_path, 'WEBP', quality=QUALITY_WEBP, method=6)
                webp_size = os.path.getsize(webp_path)
                print(f"    + WebP créé: {webp_size//1024}KB")

            return True

    except Exception as e:
        print(f"  ✗ Erreur avec {image_path.name}: {e}")
        return False

def main():
    """Optimise toutes les images"""
    print("🖼️  Optimisation des images de voyage\n")
    print(f"Configuration:")
    print(f"  - Qualité JPG: {QUALITY_JPG}%")
    print(f"  - Qualité WebP: {QUALITY_WEBP}%")
    print(f"  - Taille max: {MAX_SIZE}")
    print(f"  - Créer WebP: {'Oui' if CREATE_WEBP else 'Non'}\n")

    total_images = 0
    total_original = 0
    total_optimized = 0

    for folder in TRAVEL_FOLDERS:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"⚠️  Dossier introuvable: {folder}")
            continue

        print(f"\n📁 {folder}")

        # Trouver toutes les images JPG
        images = list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.JPG'))

        for img_path in images:
            original_size = os.path.getsize(img_path)
            if optimize_image(img_path):
                total_images += 1
                total_original += original_size
                total_optimized += os.path.getsize(img_path)

    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ")
    print("="*50)
    print(f"Images optimisées: {total_images}")
    print(f"Taille originale: {total_original/1024/1024:.1f} MB")
    print(f"Taille optimisée: {total_optimized/1024/1024:.1f} MB")
    saved_mb = (total_original - total_optimized) / 1024 / 1024
    saved_percent = ((total_original - total_optimized) / total_original) * 100
    print(f"Économisé: {saved_mb:.1f} MB ({saved_percent:.1f}%)")
    print("="*50)
    print("\n✅ Optimisation terminée!")

    if CREATE_WEBP:
        print("\n💡 N'oubliez pas de mettre à jour le HTML pour utiliser les images WebP")
        print("   Exemple: <picture>")
        print("              <source srcset='image.webp' type='image/webp'>")
        print("              <img src='image.jpg' alt='...'>")
        print("            </picture>")

if __name__ == '__main__':
    # Confirmation avant de commencer
    response = input("\n⚠️  Ce script va modifier vos images originales. Continuer? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        main()
    else:
        print("Annulé.")
