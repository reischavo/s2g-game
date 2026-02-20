#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oyun logolarını indir ve kaydet
"""

import requests
import os

# Logo URL'leri (direkt indirilebilir)
logos = {
    'pubg.png': 'https://i.ibb.co/9ZQY8Kq/pubg-mobile.png',
    'valorant.png': 'https://i.ibb.co/7XqYxJK/valorant.png',
    'lol.png': 'https://i.ibb.co/9wKQY8K/lol.png',
    'cs2.png': 'https://i.ibb.co/7XqYxJK/cs2.png',
    'coc.png': 'https://i.ibb.co/9ZQY8Kq/coc.png',
    'discord.png': 'https://i.ibb.co/7XqYxJK/discord.png',
    'fortnite.png': 'https://i.ibb.co/9wKQY8K/fortnite.png',
    'minecraft.png': 'https://i.ibb.co/7XqYxJK/minecraft.png',
}

# Alternatif: Daha güvenilir kaynaklar
logos_alt = {
    'pubg.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/pubg_mobile_logo_icon_168524.png',
    'valorant.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/valorant_logo_icon_170802.png',
    'lol.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/league_of_legends_logo_icon_170823.png',
    'cs2.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/counter_strike_logo_icon_168594.png',
    'coc.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/clash_of_clans_logo_icon_168588.png',
    'discord.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/discord_logo_icon_168820.png',
    'fortnite.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/fortnite_logo_icon_168726.png',
    'minecraft.png': 'https://cdn.icon-icons.com/icons2/2699/PNG/512/minecraft_logo_icon_168974.png',
}

output_dir = 'static/images/game-logos'
os.makedirs(output_dir, exist_ok=True)

print('🎮 Oyun logoları indiriliyor...\n')

for filename, url in logos_alt.items():
    try:
        print(f'⬇️  {filename} indiriliyor...')
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f'✅ {filename} kaydedildi!')
    except Exception as e:
        print(f'❌ {filename} indirilemedi: {e}')

print('\n🎉 Tamamlandı!')
