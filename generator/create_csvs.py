"""Generate CSVs of random data for Warbler.

Students won't need to run this for the exercise; they will just use the CSV
files that this generates. You should only need to run this if you wanted to
tweak the CSV formats or generate fewer/more rows.
"""

import csv
from random import choice, randint, sample
from itertools import permutations
import requests
from faker import Faker
from helpers import get_random_datetime

MAX_WARBLER_LENGTH = 140

USERS_CSV_HEADERS = [
    "email",
    "username",
    "image_url",
    "password",
    "bio",
    "header_image_url",
    "location",
]
MESSAGES_CSV_HEADERS = ["text", "timestamp", "user_id"]
FOLLOWS_CSV_HEADERS = ["user_being_followed_id", "user_following_id"]

NUM_USERS = 300
NUM_MESSAGES = 1000
NUM_FOLLWERS = 5000

fake = Faker()

# Generate random profile image URLs to use for users

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("men", 100), ("women", 100)]
    for i in range(count)
]

# Generate random header image URLs to use for users

header_image_urls = [
    "https://img.freepik.com/free-photo/glowing-spaceship-orbits-planet-starry-galaxy-generated-by-ai_188544-9655.jpg?w=2000&t=st=1701096984~exp=1701097584~hmac=7d8420c88b2ace8fd4a296a6fce12a577ad8bf9276a123107845d47cf51f6b1a",
    "https://img.freepik.com/free-photo/ultra-detailed-nebula-abstract-wallpaper-9_1562-754.jpg?w=2000&t=st=1701097020~exp=1701097620~hmac=93e46bbb2e45294cec02b28671e7fe45a75bcb9e94630669ddc13ffe574b062c",
    "https://img.freepik.com/free-photo/galactic-night-sky-astronomy-science-combined-generative-ai_188544-9656.jpg?w=2000&t=st=1701097035~exp=1701097635~hmac=a3cd93aa4ee68b6564b603cfb82c98357edd4b6620a603f6c4f88e4f427a6868",
    "https://img.freepik.com/free-photo/mountain-landscape-illuminated-by-moonlight-milky-way-generated-by-ai_188544-11622.jpg?w=2000&t=st=1701097048~exp=1701097648~hmac=8b572fcb8536123365fcb0021ae05cd28f98153fca74051e4f5fe9c08d39ca7f",
    "https://img.freepik.com/free-vector/gradient-galaxy-background_23-2148983655.jpg?w=2000&t=st=1701097083~exp=1701097683~hmac=e5a5f5395d3a84ef65e0c336070e1a5d0410eb83480612473379f9095563bda1",
    "https://img.freepik.com/free-photo/night-sky-glows-with-iridescent-deep-space-generative-ai_188544-11285.jpg?w=2000&t=st=1701097100~exp=1701097700~hmac=498c0229d04df1d4ebef5812104f352b7a686ae5a8ebc549f8c29913a1e9e0e6",
    "https://img.freepik.com/free-photo/space-planet-science-night-generated-by-ai_188544-15619.jpg?w=2000&t=st=1701097195~exp=1701097795~hmac=77653c75278f0a925750ba5858d7793f35fd6583ec4bbf4db1a0e6fb6bdaf1a2",
    "https://img.freepik.com/free-photo/space-background-realistic-starry-night-cosmos-shining-stars-milky-way-stardust-color-galaxy_1258-154750.jpg?w=2000&t=st=1701097209~exp=1701097809~hmac=85593e7ed420f8789fce05b5d8673630656be0183aeac316cd31773852c8afa2",
    "https://img.freepik.com/free-photo/spaceship-orbits-dark-galaxy-glowing-blue-comet-generated-by-ai_188544-9662.jpg?w=2000&t=st=1701097240~exp=1701097840~hmac=e70779f24de730bdeeaddecfe004e8003bd69a62d5099d789d5320d84d8f4dd8",
    "https://img.freepik.com/free-photo/ultra-detailed-nebula-abstract-wallpaper-10_1562-745.jpg?w=2000&t=st=1701097265~exp=1701097865~hmac=25d80a6a661670751ab523333da09bc07bc8d6b9035305f26fc9fa984d2939d7",
    "https://img.freepik.com/free-vector/gradient-universe-background_23-2149635763.jpg?w=2000&t=st=1701097284~exp=1701097884~hmac=52638f26e551214fc289c8e4a8517f1eb97fa1632835a65435273c97c8b31d8f",
    "https://img.freepik.com/free-photo/night-sky-with-planets-galaxies-scene-generative-ai_188544-7873.jpg?w=2000&t=st=1701097308~exp=1701097908~hmac=b944c0d34f06d561d5fdb7380388f4641c07efec9976e71a99bcd140a83102d1",
    "https://img.freepik.com/free-photo/night-sky-glows-with-galaxy-mystical-silhouette-generative-ai_188544-11287.jpg?w=2000&t=st=1701097331~exp=1701097931~hmac=f5cda8d06586ec0fa34333d4d1b96ca4d57914dbed5a9483ef18e620f44484b0",
]

with open("generator/users.csv", "w") as users_csv:
    users_writer = csv.DictWriter(users_csv, fieldnames=USERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(NUM_USERS):
        users_writer.writerow(
            dict(
                email=fake.email(),
                username=fake.user_name(),
                image_url=choice(image_urls),
                password="$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe",
                bio=fake.sentence(),
                header_image_url=choice(header_image_urls),
                location=fake.city(),
            )
        )

with open("generator/messages.csv", "w") as messages_csv:
    messages_writer = csv.DictWriter(messages_csv, fieldnames=MESSAGES_CSV_HEADERS)
    messages_writer.writeheader()

    for i in range(NUM_MESSAGES):
        messages_writer.writerow(
            dict(
                text=fake.paragraph()[:MAX_WARBLER_LENGTH],
                timestamp=get_random_datetime(),
                user_id=randint(1, NUM_USERS),
            )
        )

# Generate follows.csv from random pairings of users

with open("generator/follows.csv", "w") as follows_csv:
    all_pairs = list(permutations(range(1, NUM_USERS + 1), 2))

    users_writer = csv.DictWriter(follows_csv, fieldnames=FOLLOWS_CSV_HEADERS)
    users_writer.writeheader()

    for followed_user, follower in sample(all_pairs, NUM_FOLLWERS):
        users_writer.writerow(
            dict(user_being_followed_id=followed_user, user_following_id=follower)
        )
