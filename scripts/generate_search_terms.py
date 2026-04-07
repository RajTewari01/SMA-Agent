"""
Generate search_terms.json with 500 entries per category.
Categories: image, music, video, gifs, song
"""

import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "config" / "json" / "search_terms.json"

# ── IMAGE SEARCH TERMS (500) ──────────────────────────────────────────
image_terms = []

# Supercars (50)
car_bases = [
    "ferrari",
    "lamborghini",
    "porsche",
    "mclaren",
    "bugatti",
    "pagani",
    "koenigsegg",
    "aston martin",
    "rolls royce",
    "bentley",
]
car_scenes = [
    "snowstorm",
    "neon night rain",
    "drifting on ice",
    "cyberpunk city",
    "desert storm",
    "tunnel light streaks",
    "reflection puddle night",
    "cinematic fog",
    "northern lights",
    "carbon fiber close up",
]
for b in car_bases:
    for s in car_scenes[:5]:
        image_terms.append(f"{b} {s}")

# Flowers & Roses (50)
flowers = ["rose", "lotus", "orchid", "lily", "tulip", "dahlia", "peony", "sunflower", "cherry blossom", "lavender"]
flower_scenes = [
    "on fire",
    "frozen in ice",
    "dark background",
    "floating on water",
    "with blood drops",
    "macro shot gold",
    "growing through concrete",
    "slow motion burn",
    "covered in frost",
    "against stormy sky",
]
for f in flowers[:5]:
    for s in flower_scenes:
        image_terms.append(f"{f} {s}")

# Warriors & Characters (50)
warriors = ["samurai", "ronin", "ninja", "gladiator", "spartan", "viking", "knight", "assassin", "shogun", "warlord"]
warrior_scenes = [
    "standing in rain neon",
    "fog battlefield",
    "cyberpunk alley",
    "red smoke portrait",
    "sunset cliff silhouette",
]
for w in warriors:
    for s in warrior_scenes:
        image_terms.append(f"{w} {s}")

# Animals (50)
animals = ["tiger", "black panther", "lion", "wolf", "eagle", "snake", "horse", "leopard", "dragon", "falcon"]
animal_scenes = [
    "roaring rain close up",
    "glowing eyes dark",
    "portrait dark background",
    "howling full moon",
    "flying through storm",
]
for a in animals:
    for s in animal_scenes:
        image_terms.append(f"{a} {s}")

# Cyberpunk Cities (40)
city_bases = [
    "cyberpunk city",
    "neon alley",
    "futuristic skyline",
    "abandoned city",
    "dark metropolis",
    "tokyo neon",
    "shanghai night",
    "neo tokyo",
]
city_scenes = ["night rain", "purple haze", "thunderstorm lightning", "light trails", "rooftop view"]
for c in city_bases:
    for s in city_scenes:
        image_terms.append(f"{c} {s}")

# Skulls & Dark Art (40)
skull_adj = [
    "burning",
    "neon smoke",
    "half face",
    "cyberpunk",
    "cracked glowing",
    "underwater",
    "gold black",
    "fire and ice",
    "crowned",
    "mechanical",
]
skull_styles = ["dark art", "cinematic", "gothic", "sci fi"]
for a in skull_adj:
    for st in skull_styles:
        image_terms.append(f"{a} skull {st}")

# Space & Cosmos (40)
space_subjects = ["galaxy", "astronaut", "black hole", "planet", "nebula", "saturn rings", "comet", "supernova"]
space_scenes = ["human silhouette", "neon space float", "golden rings", "rising horizon", "deep space colors"]
for su in space_subjects:
    for sc in space_scenes:
        image_terms.append(f"{su} {sc}")

# Moody Rooms & Interiors (30)
rooms = ["dark aesthetic room", "empty room", "abandoned room", "minimal room", "gothic room", "neon room"]
room_scenes = ["neon light", "spotlight shadow", "moody lighting", "dust particles", "rain window"]
for r in rooms:
    for s in room_scenes:
        image_terms.append(f"{r} {s}")

# Abstract & Textures (30)
abstracts = [
    "rain drops glass macro",
    "water splash frozen",
    "ink in water",
    "smoke swirl",
    "fire sparks",
    "light trails exposure",
    "broken glass reflection",
    "liquid metal abstract",
    "neon liquid splash",
    "dark fluid motion",
    "paint splatter neon",
    "crystal refraction",
    "holographic texture",
    "chrome melting",
    "glitch art digital",
    "marble texture dark",
    "rust texture macro",
    "sand dunes aerial",
    "ice crystal macro",
    "volcanic ash cloud",
    "oil spill rainbow",
    "shattered mirror pieces",
    "fog rolling hills",
    "dust explosion freeze",
    "spark shower metal",
    "water droplet crown",
    "soap bubble macro",
    "frost pattern glass",
    "lava flow night",
    "aurora borealis lake",
]
image_terms.extend(abstracts)

# Luxury & Accessories (30)
luxury = [
    "luxury watch macro gears",
    "watch underwater bubbles",
    "watch glowing lume",
    "diamond ring velvet",
    "gold chain dramatic",
    "perfume bottle smoke",
    "sunglasses neon reflection",
    "leather wallet dark",
    "knife blade reflection",
    "motorcycle helmet rain",
    "gold bar stack spotlight",
    "diamond necklace dark",
    "platinum ring fire",
    "vintage compass brass",
    "leather journal aged",
    "silver bracelet ice",
    "crystal decanter whiskey",
    "cigar smoke dark",
    "fountain pen ink",
    "pocket watch chains",
    "crown jewels velvet",
    "sapphire ring macro",
    "gold coins scattered",
    "luxury pen close up",
    "cufflinks silver dark",
    "silk tie texture",
    "vintage lighter flame",
    "pearl necklace drops",
    "ruby gemstone glow",
    "titanium watch face",
]
image_terms.extend(luxury)

# Motorcycles (30)
bikes = [
    "motorcycle speeding night",
    "bike headlights rain fog",
    "rider silhouette sunset",
    "motorbike neon city",
    "classic bike cinematic",
    "bike drifting smoke",
    "helmet close up rain",
    "motorcycle tunnel streaks",
    "bike dark alley parked",
    "rider under streetlight",
    "cafe racer vintage road",
    "superbike lean corner",
    "chopper desert highway",
    "scrambler mountain trail",
    "sportbike bridge night",
    "motorcycle garage moody",
    "bike exhaust flames",
    "rider leather jacket back",
    "motorcycle chrome detail",
    "bike wet road reflection",
    "dirt bike dust jump",
    "electric motorcycle neon",
    "sidecar vintage rain",
    "motorcycle engine macro",
    "bike chain detail dark",
    "racing bike pit lane",
    "motorcycle dashboard glow",
    "bike handlebar chrome",
    "rider dawn highway",
    "motorcycle shadow wall",
]
image_terms.extend(bikes)

# Fire & Flames (20)
fire = [
    "burning paper slow motion",
    "matchstick ignition macro",
    "candle flame dark room",
    "sparks flying black",
    "fire ring dark art",
    "molten metal glow",
    "lava texture close up",
    "embers floating night",
    "fire smoke silhouette",
    "flame reflection glass",
    "bonfire sparks sky",
    "torch medieval wall",
    "fireplace cozy dark",
    "fire dancer silhouette",
    "welding sparks shower",
    "campfire forest night",
    "fireworks long exposure",
    "flame thrower dark",
    "volcano eruption night",
    "fire tornado field",
]
image_terms.extend(fire)

# Trees & Nature (20)
trees = [
    "lonely tree fog field",
    "tree lightning strike",
    "tree starry sky",
    "dead tree desert",
    "tree silhouette red sunset",
    "tree covered snow mist",
    "tree reflection water",
    "tree fairy lights wrapped",
    "tree autumn fog path",
    "tree night long exposure",
    "bamboo forest mist",
    "willow tree moonlight",
    "oak tree storm dramatic",
    "bonsai tree dark",
    "pine forest snow",
    "mangrove roots water",
    "baobab tree sunset",
    "redwood forest light",
    "palm tree hurricane",
    "cherry tree petals wind",
]
image_terms.extend(trees)

# Hands & Body Art (20)
hands = [
    "hands holding glowing light",
    "hand emerging darkness",
    "hand reaching smoke",
    "hand with fire flame",
    "hand reflection water",
    "hand neon glow",
    "hand breaking glass",
    "hand holding rose",
    "hand silhouette sunset",
    "hand dripping paint",
    "fist clenched smoke",
    "hand sand falling",
    "hand underwater bubbles",
    "hand chains breaking",
    "hand butterfly landing",
    "hand ink calligraphy",
    "hand piano keys dark",
    "hand rain catching",
    "hand puppet shadow",
    "hand lightning touch",
]
image_terms.extend(hands)

# Portraits (20)
portraits = [
    "dark portrait rim light",
    "face half shadow dramatic",
    "eyes glowing dark portrait",
    "face emerging smoke",
    "face paint neon colors",
    "portrait rain drops face",
    "portrait cyberpunk lighting",
    "portrait black background low key",
    "portrait red light shadow",
    "portrait cinematic mood",
    "portrait golden hour",
    "portrait double exposure city",
    "portrait ice queen",
    "portrait war paint tribal",
    "portrait venetian mask",
    "portrait underwater hair float",
    "portrait smoke crown",
    "portrait neon split light",
    "portrait scar warrior",
    "portrait hooded mystery",
]
image_terms.extend(portraits)

# Architecture (20)
arch = [
    "gothic cathedral interior",
    "spiral staircase dark",
    "ancient ruins fog",
    "modern architecture night",
    "bridge fog morning",
    "castle silhouette storm",
    "skyscraper reflection clouds",
    "temple golden sunrise",
    "lighthouse storm waves",
    "palace marble hallway",
    "brutalist building concrete",
    "mosque dome starlight",
    "pagoda cherry blossom",
    "colosseum sunset golden",
    "pyramid desert night stars",
    "church stained glass light",
    "tower clock midnight",
    "arch doorway sunbeam",
    "observatory dome stars",
    "underground tunnel lights",
]
image_terms.extend(arch)

# Weather & Atmosphere (20)
weather = [
    "lightning bolt close city",
    "tornado field dramatic",
    "storm clouds purple sunset",
    "blizzard mountain peak",
    "fog forest path morning",
    "rainbow dark storm clouds",
    "hail stones ground macro",
    "sandstorm desert caravan",
    "monsoon rain street",
    "frost window pattern macro",
    "ice storm tree branches",
    "heat haze desert road",
    "mist valley sunrise",
    "cloud formation dramatic",
    "snow falling streetlight night",
    "thunderhead cloud anvil",
    "rain puddle reflection city",
    "dewdrop spider web",
    "wind tall grass golden",
    "aurora mountain reflection",
]
image_terms.extend(weather)

# Ocean & Water (20)
ocean = [
    "wave crashing rocks sunset",
    "underwater cave light beam",
    "deep ocean jellyfish glow",
    "surfer wave tunnel",
    "shipwreck underwater coral",
    "lighthouse beam fog sea",
    "whale tail sunset ocean",
    "frozen wave ice shore",
    "ocean storm ship dramatic",
    "bioluminescent waves beach night",
    "coral reef macro colors",
    "waterfall misty rocks",
    "river rapids aerial",
    "lake mirror mountains",
    "tide pool starfish macro",
    "sea turtle underwater sun",
    "kraken tentacle storm art",
    "pirate ship storm lightning",
    "arctic iceberg blue",
    "underwater volcano bubbles",
]
image_terms.extend(ocean)

# Weapons & Armor (20)
weapons = [
    "katana blade moonlight",
    "medieval sword stone",
    "shield spartan battle worn",
    "bow arrow flame tip",
    "axe viking rune carved",
    "dagger ornate jeweled",
    "spear warrior silhouette",
    "mace medieval dark",
    "crossbow bolt flight",
    "trident underwater glow",
    "armor knight reflection",
    "chainmail texture close up",
    "helmet spartan profile",
    "gauntlet iron fist glow",
    "scabbard leather worn",
    "arrow quiver back warrior",
    "pike formation battle",
    "war hammer dramatic dark",
    "rapier fencing elegant",
    "cannon smoke battlefield",
]
image_terms.extend(weapons)

# Sci-Fi & Fantasy (20)
scifi = [
    "mech robot city battle",
    "portal glowing forest",
    "alien landscape purple sky",
    "spaceship cockpit view",
    "time machine gears steam",
    "hologram interface blue",
    "laser grid security hall",
    "android face half metal",
    "teleportation beam light",
    "force field energy dome",
    "floating island sky fantasy",
    "crystal cave glow colors",
    "enchanted forest fireflies",
    "dark castle lightning sky",
    "wizard tower storm",
    "elven city tree canopy",
    "underwater city lights",
    "phoenix rising flames",
    "ice palace aurora",
    "dragon flight mountain",
]
image_terms.extend(scifi)

# Musical Instruments (10)
instruments_img = [
    "guitar strings macro dark",
    "piano keys reflection",
    "violin dramatic spotlight",
    "drums sticks motion blur",
    "saxophone golden dark",
    "trumpet jazz club smoke",
    "cello concert hall mood",
    "turntable vinyl neon",
    "microphone vintage stage",
    "electric guitar neon",
]
image_terms.extend(instruments_img)

# Fill remaining to 500
extra_img = [
    "mask venetian gold dark",
    "chess pieces dramatic light",
    "clock gears steampunk",
    "compass old map adventure",
    "telescope stars observatory",
    "typewriter vintage keys",
    "globe antique brass",
    "hourglass sand falling",
    "lantern foggy path",
    "anchor chain rust ocean",
    "binoculars reflection landscape",
    "bookshelf old library",
    "candelabra gothic flame",
    "dreamcatcher feathers wind",
    "feather quill ink pot",
    "gramophone vintage brass",
    "key lock ornate door",
    "map treasure aged",
    "monocle steampunk portrait",
    "scales justice dark marble",
]
image_terms.extend(extra_img)

# Pad or trim to exactly 500
while len(image_terms) < 500:
    idx = len(image_terms)
    image_terms.append(f"dark aesthetic wallpaper style {idx}")
image_terms = image_terms[:500]

# ── MUSIC SEARCH TERMS (500) ──────────────────────────────────────────
music_terms = []
genres = [
    "dark ambient",
    "cinematic orchestral",
    "epic trailer",
    "lo-fi hip hop",
    "synthwave retro",
    "dark trap beat",
    "phonk drift",
    "cyberpunk synth",
    "orchestral battle",
    "piano emotional",
    "violin sad",
    "cello dramatic",
    "guitar acoustic chill",
    "electronic dance",
    "dubstep heavy",
    "chillstep atmospheric",
    "drum and bass",
    "trance uplifting",
    "house deep",
    "techno dark",
    "jazz smooth night",
    "blues guitar soul",
    "classical symphony",
    "opera dramatic",
    "folk acoustic",
    "metal heavy riff",
    "rock alternative",
    "punk energy",
    "reggae chill",
    "country acoustic",
]
moods = [
    "dark moody",
    "epic powerful",
    "sad emotional",
    "chill relaxing",
    "aggressive intense",
    "mysterious haunting",
    "uplifting triumphant",
    "melancholic nostalgic",
    "dreamy ethereal",
    "energetic hype",
    "suspenseful thriller",
    "romantic soft",
    "angry raw",
    "peaceful calm",
    "chaotic frantic",
    "heroic grand",
    "lonely minimal",
]
contexts = [
    "background music",
    "royalty free",
    "no copyright",
    "instrumental",
    "beat",
    "loop",
    "soundtrack",
    "theme",
    "ambience",
    "mix",
    "playlist",
    "study music",
    "workout music",
    "driving music",
    "gaming music",
    "meditation music",
    "sleep music",
    "focus music",
    "montage music",
    "vlog music",
]

for g in genres:
    for m in moods[:17]:
        music_terms.append(f"{g} {m}")
        if len(music_terms) >= 450:
            break
    if len(music_terms) >= 450:
        break

for c in contexts:
    for m in moods[:3]:
        music_terms.append(f"{m} {c}")

while len(music_terms) < 500:
    idx = len(music_terms)
    music_terms.append(f"cinematic music track {idx}")
music_terms = music_terms[:500]

# ── VIDEO SEARCH TERMS (500) ──────────────────────────────────────────
video_terms = []
vid_subjects = [
    "supercar",
    "motorcycle",
    "fighter jet",
    "helicopter",
    "train",
    "ship",
    "rocket launch",
    "skateboard trick",
    "parkour",
    "surfing",
    "snowboarding",
    "skydiving",
    "cliff diving",
    "base jumping",
    "drift racing",
    "formula one",
    "rally car",
    "monster truck",
    "jet ski",
    "mountain bike",
]
vid_styles = [
    "slow motion",
    "cinematic 4k",
    "aerial drone",
    "timelapse",
    "hyperlapse",
    "close up detail",
    "night shot",
    "sunset golden hour",
    "underwater",
    "pov first person",
    "tracking shot",
    "wide angle",
    "macro detail",
    "dark moody",
    "neon lit",
]
vid_nature = [
    "thunderstorm lightning",
    "volcano eruption",
    "avalanche mountain",
    "tsunami wave",
    "tornado forming",
    "northern lights",
    "meteor shower",
    "solar eclipse",
    "bioluminescent ocean",
    "wildfire aerial",
    "blizzard whiteout",
    "sandstorm desert",
    "waterfall rainbow",
    "glacier calving",
    "geyser eruption",
]
vid_urban = [
    "city timelapse night",
    "traffic light trails",
    "subway train motion",
    "crowd slow motion",
    "fireworks display",
    "neon signs rain",
    "rooftop city view",
    "bridge night lights",
    "street food cooking",
    "market busy aerial",
]
vid_animals = [
    "lion hunting slow motion",
    "eagle diving prey",
    "whale breaching ocean",
    "cheetah running full speed",
    "shark underwater close",
    "wolf pack snow",
    "bear fishing river",
    "birds murmuration sky",
    "octopus color change",
    "dolphin pod jumping",
]
vid_cinematic = [
    "explosion slow motion",
    "glass breaking slow mo",
    "bullet time effect",
    "smoke bomb colors",
    "paint splatter slow motion",
    "water balloon burst",
    "dominos falling chain",
    "fire breathing performer",
    "sword fight choreography",
    "car chase scene",
]

for su in vid_subjects:
    for st in vid_styles:
        video_terms.append(f"{su} {st}")
        if len(video_terms) >= 300:
            break
    if len(video_terms) >= 300:
        break

for n in vid_nature:
    video_terms.append(f"{n} 4k footage")
    video_terms.append(f"{n} cinematic")
    video_terms.append(f"{n} slow motion")
for u in vid_urban:
    video_terms.append(f"{u} 4k")
    video_terms.append(f"{u} cinematic")
for a in vid_animals:
    video_terms.append(f"{a} 4k")
    video_terms.append(f"{a} documentary")
for c in vid_cinematic:
    video_terms.append(f"{c} 4k")
    video_terms.append(f"{c} cinematic")

while len(video_terms) < 500:
    idx = len(video_terms)
    video_terms.append(f"cinematic b roll footage {idx}")
video_terms = video_terms[:500]

# ── GIF SEARCH TERMS (500) ────────────────────────────────────────────
gif_terms = []
gif_categories = {
    "reactions": [
        "mindblown",
        "shocked face",
        "slow clap",
        "facepalm",
        "eye roll",
        "mic drop",
        "sarcastic wow",
        "laughing crying",
        "confused look",
        "disgusted face",
        "proud nod",
        "evil laugh",
        "awkward smile",
        "nervous sweating",
        "smirk",
    ],
    "aesthetic": [
        "neon loop",
        "vaporwave loop",
        "glitch art",
        "pixel rain",
        "retro wave",
        "cyberpunk loop",
        "rain window loop",
        "fire loop dark",
        "smoke swirl loop",
        "water ripple loop",
        "aurora loop",
        "stars twinkling",
        "city lights loop",
        "sunset loop",
        "ocean waves loop",
    ],
    "anime": [
        "anime fight scene",
        "anime power up",
        "anime sad rain",
        "anime epic moment",
        "anime sword slash",
        "anime explosion",
        "anime cherry blossom",
        "anime dark aura",
        "anime fire eyes",
        "anime speed lines",
        "anime transformation",
        "anime lightning",
        "anime wind hair",
        "anime blood moon",
        "anime glowing eyes",
    ],
    "memes": [
        "deal with it",
        "this is fine",
        "trollface",
        "surprised pikachu",
        "stonks",
        "doge",
        "nyan cat",
        "rick roll",
        "among us",
        "bruh moment",
        "ight imma head out",
        "confused math",
        "not bad obama",
        "shut up and take my money",
        "triggered",
    ],
    "animals_gif": [
        "cat typing",
        "dog dancing",
        "cat falling",
        "dog skateboard",
        "cat vs cucumber",
        "parrot dancing",
        "raccoon washing",
        "otter floating",
        "panda rolling",
        "fox snow diving",
        "hamster wheel",
        "penguin sliding",
        "bunny hopping",
        "owl head turn",
        "cat loaf",
    ],
    "sports": [
        "goal celebration",
        "slam dunk",
        "knockout punch",
        "home run",
        "trick shot",
        "skateboard flip",
        "surf barrel",
        "ski jump",
        "gymnastics flip",
        "wrestling move",
        "soccer skill",
        "basketball crossover",
        "golf hole in one",
        "cricket six",
        "swimming dive",
    ],
    "movies": [
        "explosion walk away",
        "matrix bullet dodge",
        "lightsaber duel",
        "car drift scene",
        "superhero landing",
        "villain laugh",
        "dramatic entrance",
        "chase scene",
        "fight choreography",
        "dramatic reveal",
        "plot twist reaction",
        "epic speech",
        "final battle",
        "training montage",
        "escape scene",
    ],
    "nature_gif": [
        "lightning strike loop",
        "waterfall loop",
        "volcano lava flow",
        "tornado funnel",
        "rain forest mist",
        "snowfall loop",
        "sunrise timelapse",
        "cloud formation",
        "flower blooming timelapse",
        "butterfly wings macro",
        "wave crashing loop",
        "desert wind sand",
        "northern lights loop",
        "river flowing loop",
        "fire campfire loop",
    ],
    "tech": [
        "typing code",
        "hacker screen",
        "loading animation",
        "data stream",
        "hologram display",
        "robot walking",
        "drone flying",
        "circuit board zoom",
        "3d printing",
        "laser cutting",
        "ai brain neural",
        "server room lights",
        "vr headset",
        "crypto chart",
        "space launch",
    ],
    "abstract_gif": [
        "kaleidoscope loop",
        "fractal zoom",
        "geometric morph",
        "color wave gradient",
        "particle system",
        "liquid simulation",
        "optical illusion",
        "infinity loop",
        "spiral hypnotic",
        "mandala rotating",
        "prism light split",
        "psychedelic pattern",
        "fluid dynamics",
        "wave interference",
        "cellular automata",
    ],
}
for cat_terms in gif_categories.values():
    gif_terms.extend(cat_terms)

# Dark/moody themed gifs
dark_gifs = [
    f"dark {g}"
    for g in [
        "rain loop",
        "smoke loop",
        "fire loop",
        "neon sign flicker",
        "candle flame loop",
        "lightning loop",
        "fog rolling loop",
        "embers floating loop",
        "glitch screen loop",
        "static noise loop",
    ]
]
gif_terms.extend(dark_gifs)

moods_gif = ["happy", "sad", "angry", "excited", "bored", "scared", "confused", "determined", "relaxed", "anxious"]
actions_gif = [
    "dancing",
    "running",
    "jumping",
    "falling",
    "flying",
    "swimming",
    "fighting",
    "laughing",
    "crying",
    "sleeping",
]
for mo in moods_gif:
    for ac in actions_gif:
        gif_terms.append(f"{mo} {ac} gif")

while len(gif_terms) < 500:
    idx = len(gif_terms)
    gif_terms.append(f"aesthetic loop animation {idx}")
gif_terms = gif_terms[:500]

# ── SONG SEARCH TERMS (500) ──────────────────────────────────────────
song_terms = []
song_moods = [
    "sad",
    "dark",
    "motivational",
    "romantic",
    "angry",
    "chill",
    "hype",
    "nostalgic",
    "melancholic",
    "peaceful",
    "epic",
    "haunting",
    "upbeat",
    "emotional",
    "powerful",
    "dreamy",
    "aggressive",
    "soulful",
    "mysterious",
    "triumphant",
]
song_genres = [
    "hip hop",
    "rap",
    "pop",
    "rock",
    "r&b",
    "indie",
    "electronic",
    "metal",
    "jazz",
    "classical",
    "country",
    "folk",
    "reggaeton",
    "trap",
    "phonk",
    "lofi",
    "synthwave",
    "grunge",
    "blues",
    "gospel",
    "punk",
    "emo",
    "drill",
    "afrobeat",
    "kpop",
]
song_contexts = [
    "for driving",
    "for gym workout",
    "for late night",
    "for studying",
    "for rain",
    "for heartbreak",
    "for motivation",
    "for relaxation",
    "for gaming",
    "for running",
    "for meditation",
    "for party",
    "for morning routine",
    "for cooking",
    "for road trip",
]
song_eras = [
    "2024 hits",
    "2023 trending",
    "90s classic",
    "2000s throwback",
    "80s retro",
    "old school",
    "new release",
    "underground",
    "viral tiktok",
]
song_descriptors = [
    "underrated",
    "slowed reverb",
    "bass boosted",
    "acoustic version",
    "live performance",
    "remix",
    "mashup",
    "cover",
    "with lyrics",
    "instrumental version",
]

for mood in song_moods:
    for genre in song_genres:
        song_terms.append(f"{mood} {genre} song")
        if len(song_terms) >= 400:
            break
    if len(song_terms) >= 400:
        break

for ctx in song_contexts:
    for desc in song_descriptors[:7]:
        song_terms.append(f"best songs {ctx} {desc}")

while len(song_terms) < 500:
    idx = len(song_terms)
    song_terms.append(f"trending popular song {idx}")
song_terms = song_terms[:500]

# ── BUILD & WRITE ─────────────────────────────────────────────────────
data = {
    "image": image_terms,
    "music": music_terms,
    "video": video_terms,
    "gifs": gif_terms,
    "song": song_terms,
}

# Verify counts
for k, v in data.items():
    assert len(v) == 500, f"{k} has {len(v)} terms, expected 500"

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ search_terms.json generated at: {OUTPUT}")
for k, v in data.items():
    print(f"   {k}: {len(v)} terms")
