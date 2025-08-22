import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio


class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        # 📌1.Ana sınıfa iki alan ekleyelim: hp (sağlık için) ve power (güç için), bu özellikler rastgele belirlenecek.
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"""Pokémon ismi: {self.name}
                Pokémon gücü: {self.power}
                Pokémon sağlığı: {self.hp}""" # Pokémon adını içeren dizeyi döndürür ## 📌 2.  hp ve power bilgisini de yazdır
        

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['front_default']
                    
                else:
                    return None
    

    # 📌 3. Pokemon sınıfına yeni attack metodunu ekleyin
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1,5)     
            if chance == 1:
                    return "Sihirbaz pokemon savaşta bir kalkan kullanıdı"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"



  # 📌 4.  Yeni çocuk sınıfları oluşturalım - Wizard ve Fighter
class Wizard(Pokemon):
    async def attack(self, enemy):
        magic_power = random.randint(5, 15)  
        self.power +=magic_power
        result = await super().attack(enemy)  
        self.power -= magic_power
        return result + f"\nSihirbaz Pokémon süper sihir kullandı. Eklenen güç: {magic_power}"


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)  
        self.power += super_power
        result = await super().attack(enemy)  
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"



#‼️TEST
async def main():
    wizard = Wizard("deniz")
    fighter= Fighter("dorukata")

    print(await wizard.info())
    print("#" * 10)
    print(await fighter.info())
    print("#" * 10)
    print(await wizard.attack(fighter))
    print(await fighter.attack(wizard))

# Asenkron main fonksiyonunu çalıştırıyoruz
asyncio.run(main())
