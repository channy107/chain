from hashlib import sha256
from uuid import uuid4

print(str(uuid4()))
# x = 5
# y = 0
# while sha256(str(x*y).encode()).hexdigest()[-1] != "0":
#     y += 1
# print(y)

# while sha256(str(x*y).encode()).hexdigest()[:4] != "0000":
#     # print(sha256(str(x*y).encode()).hexdigest())
#     y += 1
# # print(sha256(str(x*y).encode()).hexdigest())
# print(y)


# while True:
#     y = y + 1
#     if sha256(str(x*y).encode()).hexdigest()[-1] == "0":
#         print(y)
#         break

# while True:
#     y = y + 1
#     if sha256(str(x*y).encode()).hexdigest()[:2] == "00":
#         print(y)
#         break



